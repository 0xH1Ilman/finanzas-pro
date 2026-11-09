# Carteras apalancadas a largo plazo (HFEA, HiEA y variantes)

## Conceptos
- **HFEA** (Hedgefundie's Excellent Adventure): 55 % UPRO (3× S&P 500 diario) / 45 % TMF (3× Treasuries 20+ años diario), rebalanceo trimestral. Variantes: 60/40, 40/60, con TQQQ, con oro (UGL), con managed futures, con ETFs 2× (SSO/UBT).
- **HiEA** y otras variantes de comunidad: confirma la definición exacta que use el usuario antes de modelarla (los nombres circulan con composiciones distintas).
- **Daily reset**: el ETF apalancado replica L× la rentabilidad **diaria**, no la del periodo. Volatility decay ≈ −(L²−L)/2 · σ² por unidad de tiempo (aprox. continua). Con σ alta el decay domina.
- **Coste de financiación implícito**: el ETF paga ≈ (L−1) × tipo corto (vía swaps/futuros) + comisión (UPRO ~0,9 %). Con tipos al 4–5 %, son ~9–10 % anuales de arrastre en un 3×. Esto mató a HFEA en 2022 junto con la correlación positiva acciones-bonos.
- **Correlación acciones-bonos**: la tesis depende de que sea negativa. En regímenes de inflación (1970s, 2022) es positiva.

## Herramienta
`scripts/leveraged_backtest.py` trabaja con un CSV de rentabilidades diarias o precios del índice subyacente (no del ETF), y simula el ETF apalancado con costes:

```bash
python3 scripts/leveraged_backtest.py --csv datos.csv \
   --assets SPX:3:0.0091,TLT20:3:0.0106 --weights 0.55,0.45 \
   --rebalance quarterly --rf-col tbill --start 1990-01-01
# --rebalance: daily|monthly|quarterly|annual|band:0.10|none
# formato de assets: COLUMNA:apalancamiento:comisión_anual
# rf-col: columna con el tipo corto anual (decimal) para el coste de financiación; o --rf 0.04
python3 scripts/leveraged_backtest.py --demo   # datos sintéticos para probar
```

Columnas del CSV: `date` + una columna por activo con **precios** (o `--returns` si son rentabilidades diarias) + opcional tipo corto anual.

Salida: CAGR, vol, Sharpe, Sortino, max drawdown (fecha pico/valle, duración), Ulcer index, Calmar, peor año, % de meses positivos, y comparación con la cartera sin apalancar y con buy-and-hold del índice.

## Datos
Sin red abierta no hay descarga directa: pide al usuario un CSV o búscalo (Shiller S&P, FRED para tipos (DGS20, DTB3), Kenneth French). Para TMF largo plazo se usan simulaciones de bonos a 20 años a partir de yields (duración ~17): r_bono ≈ y_{t−1}/252 − D·Δy + ½·C·Δy². Explica el método.

## Lectura honesta de resultados
- Muestra sensibilidad: periodos 1982–2021 (tipos bajando = viento de cola) vs 1970s y 2022.
- Muestra el drawdown y su duración en tiempo: >80 % y años bajo agua son el escenario real.
- Sesgo de retrospectiva: la cartera se popularizó tras un periodo excepcional.
- Fiscalidad del rebalanceo (ventas con plusvalía) — ver `core/fiscal-multipais.md`.

## Skills de terceros
`backtest-expert`, `drawdown-circuit-breaker`, `macro-regime-detector` (tradermonty), `asset-allocation`, `rebalancing`, `diversification`, `historical-risk` (JoelLewis).
