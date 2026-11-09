"""Monitorización de estrategias en vivo: estado de la señal, movimiento que la activaría mañana, registro de posiciones y operaciones,
comparación entre rendimiento real y esperado, deterioro de la señal y alertas. El estado se guarda en FPQ_HOME/monitor/<nombre>.json."""
import json, datetime as dt, numpy as np, pandas as pd
from . import config, signals, metrics as M, validate as V
def _path(name): return config.home() / "monitor" / f"{name}.json"
def load(name):
    p = _path(name); return json.loads(p.read_text()) if p.exists() else dict(name=name, created=str(dt.date.today()), state=None, log=[], positions=[], changes=[])
def save(st): _path(st["name"]).write_text(json.dumps(st, indent=1, default=str, ensure_ascii=False))
def signal_status(returns, spec, state_now=None):
    """Lectura de una señal con histéresis al último cierre. returns: rentabilidades diarias del activo de la señal (cierres ajustados).
    Devuelve valor, estado, distancia a los umbrales, últimas lecturas y el movimiento de mañana que cambiaría el estado."""
    t = spec.get("type", "vol"); w = spec.get("window", 20); r = np.asarray(returns.dropna(), float); f = signals.MEASURES[t]
    v = f(r, **({"halflife": w} if t == "ewma" else {"window": w})); st = signals.hysteresis(v, spec["exit"], spec["enter"]); state = int(st[-1]) if state_now is None else int(state_now)
    target = spec["exit"] if state == 0 else spec["enter"]; move = None
    if t in ("vol", "downside"):
        grid = np.linspace(0, 0.25, 2501)
        def val(x): return f(np.r_[r[-(w - 1):], x], window=w)[-1]
        if state == 0:
            for sgn in (-1, 1):
                ok = [x for x in grid if val(sgn * x) > target]
                if ok: move = dict(down=-ok[0]) if sgn == -1 else {**(move or {}), "up": ok[0]}
        else:
            z = val(0.0); move = dict(flat_day_enough=bool(z < target))
            if z >= target:
                n = 1; rr = r.copy()
                while n < w and f(np.r_[rr[-(w - n):], np.zeros(n)], window=w)[-1] >= target: n += 1
                move["flat_days_needed"] = n
    lvl = "rojo" if (state == 0 and v[-1] > spec["exit"]) or (state == 1 and v[-1] < spec["enter"]) else ("amarillo" if state == 0 and v[-1] > spec["exit"] - 0.05 else "verde")
    return dict(date=str(returns.dropna().index[-1])[:10], value=float(v[-1]), state="risk-off" if state else "risk-on", computed_state=int(st[-1]), threshold=target, distance=float(target - v[-1]),
                last5=[round(float(x), 4) for x in v[-5:]], trigger_move=move, level=lvl, action=("CAMBIAR en la siguiente sesión" if lvl == "rojo" else "sin cambios"))
def record(name, date, value, positions=None, note=""):
    """Registra el valor de la cartera (y opcionalmente las posiciones) en una fecha."""
    st = load(name); st["log"] = [x for x in st["log"] if x["date"] != str(date)[:10]] + [dict(date=str(date)[:10], value=float(value), note=note)]; st["log"].sort(key=lambda x: x["date"])
    if positions: st["positions"].append(dict(date=str(date)[:10], positions=positions))
    save(st); return st
def record_change(name, date, what, why):
    st = load(name); st["changes"].append(dict(date=str(date)[:10], what=what, why=why)); save(st)
def live_returns(name):
    st = load(name); s = pd.Series({pd.Timestamp(x["date"]): x["value"] for x in st["log"]}).sort_index(); return s.pct_change().dropna()
def expectation_cone(backtest_returns, days, n=5000, block=21, seed=1, q=(0.05, 0.25, 0.5, 0.75, 0.95)):
    """Banda esperada del rendimiento acumulado a `days` días según el backtest (bootstrap por bloques)."""
    r = np.log1p(np.asarray(backtest_returns, float)); rng = np.random.default_rng(seed); out = np.array([r[V.stationary_indices(len(r), block, rng, days)].sum() for _ in range(n)])
    return {f"p{int(x*100)}": float(np.expm1(np.quantile(out, x))) for x in q}
def live_vs_expected(name, backtest_returns):
    """Compara lo real con lo esperable: percentil del resultado real dentro de la distribución del backtest para el mismo nº de días."""
    lr = live_returns(name)
    if len(lr) < 1: return dict(status="sin datos suficientes")
    st = load(name); d0 = pd.Timestamp(st["log"][0]["date"]); d1 = pd.Timestamp(st["log"][-1]["date"]); days = max(int(np.busday_count(d0.date(), d1.date())), 1)
    real = float((1 + lr).prod() - 1); cone = expectation_cone(backtest_returns, days); r = np.log1p(np.asarray(backtest_returns, float)); rng = np.random.default_rng(2)
    sims = np.array([r[V.stationary_indices(len(r), 21, rng, days)].sum() for _ in range(5000)]); pct = float((sims < np.log1p(real)).mean())
    return dict(days=days, real=real, cone=cone, percentile=pct, alert=pct < 0.05, message=("por debajo del 5% esperado: revisar ejecución, costes o deterioro" if pct < 0.05 else "dentro de lo esperado"))
def decay_check(returns, rf=0.0, window=756):
    """Deterioro: Sharpe de la ventana reciente frente a la distribución de ventanas pasadas del mismo tamaño."""
    r = pd.Series(returns); ex = r - rf; roll = ex.rolling(window).mean() / r.rolling(window).std() * np.sqrt(252); roll = roll.dropna()
    if len(roll) < 2: return dict(status="historial insuficiente")
    last = float(roll.iloc[-1]); return dict(recent_sharpe=last, hist_median=float(roll.median()), percentile=float((roll < last).mean()), alert=bool((roll < last).mean() < 0.10))
def exposure_check(weights_now, spec):
    """Compara pesos actuales con objetivos y bandas de la estrategia; devuelve qué regla saltaría."""
    rb = spec.get("rebalance", {}); out = []
    for a, w in spec["weights"].items():
        cur = weights_now.get(a, 0.0); up = rb.get("upper", {}).get(a, w + rb["dev"] if rb.get("dev") and a not in rb.get("dev_exempt", []) else None); lo = rb.get("lower", {}).get(a, (w - rb["dev"]) if rb.get("dev") and a not in rb.get("dev_exempt", []) and a not in rb.get("upper", {}) else None)
        fl = "REBALANCEO COMPLETO" if (up is not None and cur >= up) or (lo is not None and cur <= lo) else ""
        for tr in spec.get("trim", []):
            if tr["asset"] == a and cur >= tr["at"]: fl = f"RECORTAR a {tr['to']:.1%}"
        out.append(dict(asset=a, target=w, current=cur, drift=cur - w, upper=up, lower=lo, action=fl))
    return pd.DataFrame(out)
def alerts(name, signal=None, exposure=None, live=None, decay=None):
    a = []
    if signal and signal["level"] != "verde": a.append(f"SEÑAL {signal['level'].upper()}: {signal['value']:.1%} frente a umbral {signal['threshold']:.0%} → {signal['action']}")
    if exposure is not None:
        for x in exposure[exposure.action != ""].itertuples(): a.append(f"PESO {x.asset} {x.current:.1%}: {x.action}")
    if live and live.get("alert"): a.append("RENDIMIENTO REAL por debajo del 5% esperado")
    if decay and decay.get("alert"): a.append("DETERIORO: Sharpe reciente en el 10% inferior de su historia")
    st = load(name); st["last_alerts"] = dict(date=str(dt.date.today()), alerts=a); save(st); return a
