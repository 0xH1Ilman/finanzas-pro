"""Auditoría metodológica independiente de un backtest. Devuelve hallazgos con gravedad (alta / media / baja / info), el motivo y la prueba que lo resuelve.
Se ejecuta siempre antes de dar por bueno un resultado; un hallazgo de gravedad alta sin resolver impide pasar el experimento a 'validated'."""
import numpy as np, pandas as pd
from . import panel as PN, signals, metrics as M
SEV = {"alta": 0, "media": 1, "baja": 2, "info": 3}
def audit(result=None, spec=None, context=None, returns=None, periods=252):
    """result: Result del motor de reglas (o None si se audita una serie `returns`). context (lo que declara el investigador), claves opcionales:
    trials (nº de variantes probadas), dsr, oos (dict de métricas fuera de muestra), placebo_p (dict), calendars_reported (bool), benchmark (str),
    universe_ex_post (bool), lag (para motores de pesos), costs_included (bool), proxy_sensitivity_done (bool), data_end (fecha), tail_checked (bool)."""
    c = context or {}; F = []; add = lambda sev, check, detail, fix: F.append(dict(gravedad=sev, control=check, detalle=detail, prueba=fix))
    r = result.returns if result is not None else returns; spec = spec or (result.spec if result is not None else {}); yrs = len(r) / periods
    reg = spec.get("regime")
    # sesgo de anticipación
    lag = c.get("lag", reg.get("delay", 1) if reg else None)
    if lag is not None and lag < 1: add("alta", "Sesgo de anticipación", f"La señal se ejecuta con retraso {lag}: usa el cierre con el que se calcula.", "Repetir con retraso ≥ 1 y con 2, 3 y 5 días (validate.execution_sensitivity).")
    if reg and reg.get("delay", 1) >= 1: add("info", "Alineación temporal", "Señal al cierre de t, ejecución al cierre de t+1 o posterior.", "—")
    # costes
    tc = spec.get("costs", {}).get("turnover", 0); swc = (reg or {}).get("cost", 0)
    if not c.get("costs_included", tc > 0 or swc > 0): add("media", "Costes omitidos", "No hay comisiones, horquilla ni deslizamiento.", "Añadir costes de rotación (≥ 5 pb) y de cambio de régimen (≥ 10 pb); probar 0,5% y 1%.")
    if spec.get("tax", {}).get("rate", 0) == 0: add("baja", "Impuestos", "Resultados antes de impuestos; cada rebalanceo y cada cambio de régimen realiza plusvalías.", "Repetir con el tipo efectivo del vehículo (spec['tax']['rate']).")
    # datos sintéticos
    if result is not None:
        try:
            sh = PN.synthetic_share(result.weights.columns if result.weights is not None else list(spec["weights"]), r.index[0], r.index[-1]); bad = {k: v for k, v in sh.items() if v > 0.3}
            if bad: add("media", "Datos reconstruidos o sintéticos", f"Parte no observada del periodo: {bad}.", "Declararlo en el informe, validar contra una referencia con datos reales en el solape y repetir restando 2 y 4 puntos anuales a esas patas (validate.proxy_sensitivity).")
            if "KMLM" in sh and sh["KMLM"] > 0 and not c.get("proxy_sensitivity_done"): add("media", "Dependencia de la réplica de tendencia", "La pata de managed futures es una réplica propia, no el índice del fondo.", "validate.proxy_sensitivity con −2 y −4 puntos en KMLM; pedir al usuario la serie KMLMSIM.")
        except Exception: pass
    # tamaño de muestra
    if yrs < 10: add("media", "Muestra corta", f"{yrs:.1f} años: no cubre un ciclo completo de mercado.", "Extender con proxies (panel) o declarar que no hay evidencia estadística; calcular validate.min_track_record.")
    if reg and result is not None:
        ep = len(signals.episodes(result.signal.values, result.signal.index))
        if ep < 10: add("media", "Pocos episodios de la regla", f"Solo {ep} episodios de régimen: el placebo tendrá poca potencia.", "Ampliar el periodo o tratar la regla como hipótesis, no como resultado.")
    # búsqueda de parámetros
    tr = c.get("trials", 1)
    if tr > 1 and c.get("dsr") is None: add("alta", "Minería de datos sin corregir", f"Se probaron {tr} variantes y no se ha deflactado el Sharpe.", "validate.deflated_sharpe con el nº total de pruebas; validate.pbo sobre la matriz de configuraciones; validate.reality_check.")
    if c.get("dsr") is not None and c["dsr"] < 0.95: add("alta", "Sharpe deflactado insuficiente", f"DSR = {c['dsr']:.2f} < 0,95 tras {tr} pruebas.", "No presentar el Sharpe como evidencia de habilidad.")
    if c.get("pbo") is not None and c["pbo"] > 0.5: add("media", "Probabilidad de sobreajuste alta", f"PBO = {c['pbo']:.2f}: elegir la mejor configuración dentro de muestra no ayuda fuera de muestra.", "No optimizar el parámetro; usar el valor a priori o el centro de la meseta.")
    if not c.get("oos"): add("alta" if tr > 1 else "media", "Sin tramo fuera de muestra", "No se ha separado un periodo que no se usara para elegir parámetros.", "Reservar un tramo (p. ej. 1986–1994) e informar completo / fuera de muestra / dentro de muestra.")
    if reg and c.get("placebo_p") is None: add("media", "Sin prueba placebo", "No se ha comparado la regla con señales aleatorias de igual frecuencia.", "validate.placebo_test (≥ 300 placebos) en periodo completo y fuera de muestra.")
    if spec.get("rebalance", {}).get("every_months", 0) > 1 and not c.get("calendars_reported", False): add("media", "Un solo calendario", "Con rebalanceo de calendario, el mes de inicio cambia el resultado en varios puntos.", "Informar la mediana de todas las fases (Backtest.median_calendars) con mínimo, máximo y peor caída.")
    # selección ex post y supervivencia
    held = set(spec.get("weights", {}))
    if c.get("universe_ex_post", bool(held & {"TQQQ", "QQQ", "QLD", "BITU", "BTC"})): add("media", "Sesgo de selección del activo", "El universo incluye activos elegidos sabiendo que fueron los ganadores del periodo (Nasdaq-100, bitcoin).", "Repetir con el índice amplio (UPRO/SPY) y declarar el sesgo; no extrapolar la rentabilidad pasada del activo.")
    if held & {"TQQQ", "UPRO", "TMF", "BITU", "QLD", "SSO"}: add("baja", "Producto apalancado simulado", "Antes de su lanzamiento el ETF apalancado es una simulación: no recoge cierres, suspensiones ni errores de seguimiento en crisis.", "Declararlo; revisar el peor día (una caída del índice ≥ 33% en un día dejaría a cero un 3×).")
    # benchmark
    if not c.get("benchmark"): add("baja", "Benchmark", "No se ha declarado benchmark.", "Comparar con S&P 500, con 60/40 y con la misma cartera sin la regla.")
    # colas
    w1 = float(r.min()); e = (1 + r).cumprod(); w2 = float(e.pct_change(2).min())
    if not c.get("tail_checked"): add("media" if w1 < -0.10 else "baja", "Eventos de cola", f"Peor día {w1:.1%} ({r.idxmin().date()}); peores 2 días {w2:.1%}.", "Revisar qué hizo la regla esos días; una señal a cierre con ejecución al día siguiente no protege de un crash de un día.")
    # anualización
    if isinstance(r.index, pd.DatetimeIndex):
        per_year = len(r) / max((r.index[-1] - r.index[0]).days / 365.25, 1e-9)
        if abs(per_year - periods) / periods > 0.1: add("alta", "Anualización", f"La serie tiene {per_year:.0f} observaciones por año pero se anualiza con {periods}.", "Usar el nº real de periodos por año.")
    if c.get("data_end") and (pd.Timestamp.now() - pd.Timestamp(c["data_end"])).days > 120: add("baja", "Datos desactualizados", f"El último dato es de {str(c['data_end'])[:10]}.", "Actualizar el panel (fpq_cli.py data build) o pedir las series recientes.")
    d = pd.DataFrame(F); d = d.sort_values("gravedad", key=lambda s: s.map(SEV)).reset_index(drop=True) if len(d) else d
    return d
def verdict(findings):
    n = findings["gravedad"].value_counts().to_dict() if len(findings) else {}
    return dict(alta=n.get("alta", 0), media=n.get("media", 0), baja=n.get("baja", 0), apto_para_validar=n.get("alta", 0) == 0)
