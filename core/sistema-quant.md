# Sistema cuantitativo `fpq` — guía de uso

Paquete propio en `scripts/quant/fpq/` (Python + numpy/pandas/scipy; núcleo del motor en C que se compila solo). Sustituye a los backtests escritos a mano. Todo lo que hay aquí se ha ejecutado y tiene pruebas (`fpq_cli.py test`).

```python
import sys; sys.path.insert(0, "<ruta-skill>/scripts/quant")
from fpq import panel, engine, validate, research, metrics
p = panel.load()                                   # panel diario 1986→ (almacén del usuario o copia incluida)
```

## 1. Flujo de una investigación (siempre en este orden)

| Paso | Qué | Con qué |
|---|---|---|
| 1 | Formular la hipótesis y el parámetro a priori **antes** de mirar resultados | texto; se guarda en el registro |
| 2 | Comprobar qué datos son reales y cuáles proxy en el periodo | `panel.provenance(cols, ini, fin)`, `panel.synthetic_share(...)` |
| 3 | Validar el motor contra una referencia del usuario (export de Testfolio, tabla anual de su whitepaper) | `engine.Backtest(...).run()`; error medio por año < 4 puntos |
| 4 | Estudio completo | `research.study(p, spec, start=, split=, end=, compare=, hypothesis=)` |
| 5 | Leer la auditoría y resolver lo de gravedad alta | `out["audit"]` |
| 6 | Informar: veredicto primero, luego tablas | `out["dir"]/report.md` (también PDF y Excel) |
| 7 | Dejar constancia | el estudio se registra solo; `experiments.promote(id, "validated"/"rejected", ...)` |

`research.study` hace de una vez: métricas por periodo con mediana de calendarios; misma cartera sin la regla; rejilla y meseta; placebo en cada periodo; sensibilidad de ejecución (retraso y coste) y de proxies (−2 y −4 puntos); matriz de configuraciones → PBO, walk-forward, Reality Check y Sharpe deflactado; intervalo de confianza del Sharpe; Monte Carlo a 10 años; peores 1, 2, 5 y 21 días con el estado de la regla; atribución; auditoría; procedencia. Tarda ~20 s para 40 años.

**Descubrimiento y validación van separados.** Un experimento nace en fase `discovery`/`validation`; solo pasa a `validated` con las pruebas adjuntas. Las variantes probadas se cuentan (`trials`, `trials_before`) porque deflactan el Sharpe.

## 2. Definir una estrategia

```python
spec = dict(name="Mi cartera",
  weights={"TQQQ": .25, "AVUV": .1875, "AVDV": .1875, "KMLM": .1875, "GOLD": .1875},
  rebalance=dict(every_months=24, phase=11,            # fase 11 con 24 meses = diciembre de años pares
                 upper={"TQQQ": .50}, dev=.20,          # rebalanceo completo si TQQQ ≥ 50% o cualquier otro se desvía ±20 puntos
                 dev_exempt=[], reset_calendar=False),
  regime=dict(signal=dict(type="vol", asset="QQQ", window=20, exit=.35, enter=.25),   # también downside | ewma | sma | drawdown
              assets=["TQQQ"], refuge={"KMLM": .5, "GOLD": .5}, delay=1, cost=.001),
  trim=[dict(asset="BITU", at=.125, to=.05, recipients=["AVUV", "AVDV", "KMLM", "GOLD"])],   # recorte de satélite; no reinicia calendario
  costs=dict(turnover=.0005), tax=dict(rate=.19), flows=dict(amount=.01, every_months=1, mode="current"))
```

- La señal se calcula con el cierre de t y se opera al cierre de t+`delay`. Bandas y calendario se evalúan al cierre.
- Un activo con tope `upper` explícito no tiene banda inferior (nunca se recompra a la baja); si se quiere, se indica en `lower`. Recomprar TQQQ al caer al 5% lleva la caída máxima de la cartera sin filtro de −49% a −64%.
- En risk-off, las patas apalancadas se venden a una sub-cartera refugio; al volver, se recompran en la proporción que tenían. Nunca se recompra a la baja.
- Aportaciones `mode="current"` = según pesos actuales (no adelantan rebalanceos); `"target"` = según objetivos.
- Impuestos: tipo único sobre plusvalías realizadas, coste medio, compensación de pérdidas, pagados al momento desde la cartera (aproximación).
- Otra medida de señal: pasa `state=` (array 0/1 de la longitud del panel) a `Backtest.run`.

Para estrategias que no son «pesos fijos + reglas» (momentum, tendencia, reversión, long-short, volatilidad objetivo): `wengine.backtest(returns, weights, rf, lag=1, rebalance="M", commission=, spread=, slippage=, borrow_spread=, short_fee=)` con los constructores `w_momentum`, `w_trend`, `w_meanrev`, `w_voltarget`, `w_inverse_vol`. `lag ≥ 1` siempre.

## 3. Datos

**Qué responde.** En la nube solo GitHub (clonado, raw y releases) y PyPI. `fpq_cli.py doctor` lo comprueba de una vez. En un equipo con red abierta funcionan además Yahoo, Stooq, FRED, Ken French, EDGAR, Tesoro, BCE, Banco Mundial y CBOE (`providers.*`); sus analizadores están probados sin red, pero las descargas no se han podido probar desde la nube.

| Fuente (GitHub) | Contenido | Hasta |
|---|---|---|
| `ravelab/l-etf` | Nasdaq-100 y S&P 500 diarios con dividendos (NDX desde 31-ene-1985), TQQQ/UPRO/QLD/SSO reales, tipo de financiación | se actualiza cada semana |
| `Johnbrick123/sp500-data` (release `prices.parquet`, 240 MB) | acciones del S&P 500 y ~150 ETFs con precio ajustado: SPY, QQQ, IJS, IWN, EFA, EWJ, TLT, IEF, GLD, AGG… | cada noche |
| `robcarver17/pysystemtrade` | ~250 futuros diarios desde los 70–80 | mar-2024 |
| `bautheac/FFresearch` | factores Fama-French diarios EE. UU. (1971–abr 2021) y regionales (jul 1990–2019/21) | 2021 |
| `coinmetrics/data` | bitcoin diario desde 2010 | con unos meses de retraso |
| `cran/qrmdata` | Nikkei, FTSE, DAX… diarios 1984–2015 | 2015 |

`fpq_cli.py data fetch` las descarga a `~/.fpq/raw`; `data build` reconstruye el panel y lo guarda versionado en `~/.fpq/store` (cada versión con hash, fuente, tipo y avisos de calidad). La skill incluye una copia del panel (`data/panel.csv.gz`) para trabajar sin red.

**Columnas del panel y cómo se construyen** (rentabilidades diarias; `BORROW` es un tipo anual, no una rentabilidad):

| Columna | Real desde | Antes |
|---|---|---|
| `QQQ`, `SPY`, `CASH` | todo el periodo (índices con dividendos, letras) | `SPY` antes de abr-1988: mercado EE. UU. de Ken French |
| `TQQQ`, `UPRO`, `QLD`, `SSO` | 2010 / 2009 / 2006 / 2006 | `L·r − (L−1)·(tipo+diferencial)/252 − comisión/252`, diferencial calibrado al ETF real (TQQQ: correlación 0,999) |
| `GOLD` | nov-2004 (GLD) | futuro de oro + letras |
| `TLT`, `IEF` | jul-2002 | futuro de bonos × beta ajustada + letras. `TMF` = 3× sintético sin calibrar |
| `AVUV` | nunca (es proxy) | factores Fama-French ajustados a carteras small value (R² 0,98) −0,6%/año hasta abr-2021; después combinación de IJS e IWN |
| `AVDV` | nunca (es proxy) | hasta jun-1990 gran capitalización Japón/Reino Unido/Hong Kong (**débil**); factores ex-EE. UU. hasta 2019–21; después EFA y ETFs de país |
| `KMLM` | nunca (es proxy) | réplica propia de tendencia: 24 futuros sin renta variable, media de 250 sesiones, riesgo igual, 12% de volatilidad, −1,2%/año. **Acaba el 28-mar-2024** |
| `BTC`, `BITU` | BTC desde 2010 | `BITU` = 2× BTC − financiación − 0,95% − 10,8% (coste calibrado en el whitepaper del usuario) |

Validación del conjunto contra el whitepaper de Golden Papilio Antimachus (1995–2023): CAGR 20,6% frente a 20,2% (GPA) y 18,4% frente a 18,8% (HMEA); error medio por año 2,8 y 3,7 puntos.

**Series del usuario.** `fpq_cli.py data splice --csv export.csv --map KMLMSIM=KMLM DFSVX=AVUV` sustituye columnas donde haya dato y muestra el solape (correlación, error de seguimiento, diferencia anual). Hazlo siempre que el usuario aporte CSV: elimina el supuesto más fuerte (la réplica de tendencia) y permite llegar hasta hoy.

**Punto en el tiempo.** Fundamentales: `providers.edgar_facts` devuelve cada dato con su fecha de presentación y `store.as_of(df, fecha)` da lo conocido ese día. Macro: `providers.fred_vintages` (necesita clave gratuita de FRED). Sin fecha de publicación, usa `store.lag_publication(serie, días)` con un retraso conservador y dilo.

## 4. Validación (`fpq.validate`)

| Pregunta | Función | Lectura |
|---|---|---|
| ¿Depende del parámetro exacto? | `grid` + `plateau` | celdas que mejoran a la base; puesto del elegido; rango de vecinos |
| ¿Es mejor que salir al azar con la misma frecuencia? | `placebo_test` | p < 0,05 en Sharpe y caída = reductora de riesgo real |
| ¿Aguanta retrasos y costes? | `execution_sensitivity` | — |
| ¿Depende del nivel de los proxies? | `proxy_sensitivity` | la conclusión no debe cambiar con −2 / −4 puntos |
| ¿Qué intervalo tiene el Sharpe? | `bootstrap_ci`, `psr`, `min_track_record` | — |
| ¿Sobrevive a haber probado N variantes? | `deflated_sharpe`, `reality_check`, `adjust_pvalues` | DSR < 0,95 = no es evidencia |
| ¿Elegir el mejor del pasado sirve? | `config_matrix` → `pbo`, `walk_forward` | PBO > 0,5 = no optimices; usa el valor a priori |
| ¿Qué cabe esperar a 10–20 años? | `monte_carlo` (bloques mensuales emparejados) | subestima caídas intra-mes |
| Validación cruzada para modelos | `purged_kfold`, `cpcv`, `expanding_cv` | purga = horizonte de la etiqueta |

Lo aprendido con V2 (para calibrar expectativas): mejora la caída en 42 de 42 celdas y el Sharpe en 34–41, pero el CAGR solo en ~20; el Reality Check en rentabilidad da p ≈ 0,7 y el walk-forward queda por debajo de la variante mediana. Conclusión tipo: «robusta como reductora de riesgo; el CAGR extra es en parte suerte».

## 5. Carteras, atribución y factores

- `portfolio`: `risk_contribution`, `risk_budget` (paridad o presupuesto), `hrp`, `min_variance`, `max_sharpe`, `mean_variance_costs`, `allocate_strategies`, `band_policy_cost`, `diversification` (ratio y retorno de diversificación ≈ cosecha de volatilidad).
- `attribution`: `contribution_to_return` / `contribution_to_risk` (con `Result.weights`), `brinson` y `brinson_multi` (asignación, selección, interacción), `factor_attribution`, `by_period`, `rule_value`, `cost_drag`.
- `factors`: `rolling_exposures`, `sort_portfolios` (construir un factor propio), `build_price_factors` (momentum, baja volatilidad, reversión, tendencia), `carry_factor`, `factor_momentum`, `factor_timing_test`, `crowding`, `stability`.

## 6. Regímenes, derivados y ML

- `regimes`: `vol_trend_regimes` (sin ajuste), `hmm_fit` / `hmm_filter` / `hmm_walkforward`, `garch11`, `kmeans`, `pca`, `absorption_ratio`, `cusum_breaks`, `conditional_performance`. Un HMM ajustado con todo el historial mira al futuro: para decidir usa `hmm_walkforward`.
- `derivs`: BSM y griegas vectorizadas, volatilidad implícita, volatilidad realizada (cierre, Parkinson, Garman-Klass, Yang-Zhang), `svi_fit`, `sabr_vol`/`sabr_fit`, `heston_call`, `local_vol_dupire`, `skew_metrics`, `term_structure`, `legs_value` (griegas agregadas), `payoff_table`, `delta_hedge_sim`; futuros: `continuous_series`, `roll_yield`, `curve_state`. **No hay cadenas históricas de opciones en las fuentes gratuitas**: estas funciones se alimentan de cotizaciones que aporte el usuario; no se reconstruyen superficies sin datos.
- `ml`: `features`, `labels`, `walk_forward_probabilities`, `oos_probabilities` (purged K-fold), `score`, `calibration`, `compare`, `permutation_importance`, `psi`/`drift_report`. Resultado de referencia: sobre el Nasdaq-100 1990–2024 ningún modelo mejora a lo sencillo (AUC 0,50–0,53); no vendas ML sin pasar `ml.compare`.

## 7. Ejecución y monitorización

- `execsim.simulate(bars, orders)`: órdenes a cierre, a apertura y limitadas sobre barras OHLCV, ejecución parcial por participación en volumen, horquilla, deslizamiento e impacto raíz cuadrada; devuelve el coste frente al cierre de la señal. Sin bróker.
- `monitor.signal_status(serie, spec_señal, estado)`: valor al último cierre, distancia al umbral, últimas 5 lecturas y **movimiento de mañana que cambiaría el estado**. `exposure_check` compara pesos con bandas. `record` / `live_vs_expected` sitúan el resultado real en la distribución esperada del backtest; `decay_check` vigila el deterioro; `alerts` lo resume.

## 8. Auditoría (`fpq.audit`)

Controles: sesgo de anticipación, costes e impuestos omitidos, peso de datos reconstruidos, dependencia de la réplica de tendencia, muestra corta, pocos episodios, minería de datos sin corregir, Sharpe deflactado insuficiente, PBO alto, sin fuera de muestra, sin placebo, un solo calendario, sesgo de selección del activo, producto apalancado simulado, benchmark, colas, anualización y datos desactualizados. Cada hallazgo trae gravedad y la prueba que lo resuelve.

## 9. Scripts anteriores (revisados)

| Script | Estado | Limitación |
|---|---|---|
| `options_tools.py` | fórmulas verificadas (BSM contra valor de referencia 10,4506, paridad, griegas, binomial, covered call) | theta por día natural; sin dividendos discretos |
| `perf_metrics.py` | coincide con `fpq.metrics` | usa desviación poblacional; Ulcer en fracción, no en % |
| `leveraged_backtest.py` | correcto para rebalanceos simples | sin diferencial de financiación, sin costes, sin filtro de régimen → usa `fpq` |
| `earnings_check.py` | lógica de bases GAAP/no-GAAP correcta | — |

## 10. Lo que el sistema no hace (dilo si se pide)

- Datos intradía, libro de órdenes o conexión a bróker.
- Cadenas históricas de opciones ni superficies reconstruidas.
- Descargas web desde la nube (solo GitHub/PyPI); en esas sesiones el panel de managed futures acaba en mar-2024 salvo que el usuario aporte la serie.
- MLflow, DVC, Optuna, vectorbt, QuantLib o CVXPY: no se incluyen porque el registro en SQLite, las rejillas y scipy cubren lo necesario sin dependencias; añádelos solo si un caso concreto lo exige.
- El directorio `~/.fpq` (almacén, experimentos, monitorización) no persiste entre sesiones en la nube: entrega siempre el informe y el zip; en un equipo propio sí persiste.
