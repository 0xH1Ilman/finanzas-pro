# Opciones y covered calls — motor de decisión

Pensado para venta sistemática de calls cubiertas contra posiciones de IV alta (p. ej. biotech).

## Herramienta
`scripts/options_tools.py` (sin dependencias externas):

```bash
# Precio y griegas europeas (BS con dividendo continuo q)
python3 scripts/options_tools.py bs --S 42.5 --K 45 --T-days 30 --r 0.043 --q 0 --iv 0.85 --type call
# IV implícita desde una prima de mercado
python3 scripts/options_tools.py iv --S 42.5 --K 45 --T-days 30 --r 0.043 --price 3.10 --type call
# Americana (binomial CRR), útil con dividendos discretos o puts
python3 scripts/options_tools.py binomial --S 42.5 --K 40 --T-days 30 --r 0.043 --iv 0.85 --type put --steps 500
# Covered call: rendimientos, breakeven, prob. de asignación
python3 scripts/options_tools.py covered-call --S 42.5 --K 45 --T-days 30 --premium 3.10 --r 0.043 --iv 0.85 --basis 38
# Comparar una cadena de strikes (CSV: strike,bid,ask[,iv])
python3 scripts/options_tools.py cc-chain --S 42.5 --T-days 30 --r 0.043 --csv chain.csv --target-delta 0.25
# Expected move implícito de un evento (straddle ATM) vs movimientos históricos
python3 scripts/options_tools.py event-move --S 42.5 --straddle 9.8 --hist 0.32,-0.55,0.12,0.41,-0.08
```

## Marco de decisión (covered call)

| Variable | Qué mirar | Regla práctica (ajustable) |
|---|---|---|
| Delta del strike | Prob. aproximada de asignación | 0,15–0,30 para quien quiere conservar la acción; 0,35–0,50 para maximizar prima |
| DTE | Theta vs. gamma | 21–45 días; evitar cruzar un catalizador binario salvo que se busque cobrar esa IV |
| IV rank / percentil | ¿Prima cara o barata? | Vender más agresivo con IVR alto; con IVR bajo, plantearse no vender |
| Rendimiento estático | prima / precio | Anualizado con `(1+r)^(365/DTE)−1` |
| Rendimiento si asignada | (prima + (K−S)) / S | Comparar con el upside que se cede |
| Catalizadores | PDUFA, readouts, earnings | Ver `core/biotech-catalyst-vol.md` |
| Liquidez | spread bid/ask, OI, volumen | Spread > 10 % de la mid = coste oculto grande |
| Dividendo / ex-date | Riesgo de ejercicio anticipado | Call ITM con extrínseco < dividendo → riesgo alto |

## Gestión
- **Roll**: cuando delta > ~0,6–0,7 o a 7–10 DTE con extrínseco bajo: roll up-and-out por crédito neto si es posible. Documenta crédito/débito y nuevo breakeven.
- **Cierre anticipado**: recomprar al 50–80 % de beneficio si queda mucho tiempo (libera el subyacente para otra venta).
- **Riesgo de cola**: la covered call **no protege a la baja** más allá de la prima. En biotech con readout, valorar collar (`ib-collar` en referencias) o put spread.
- **Registro**: lleva un log (fecha, strike, DTE, prima, IV, delta, resultado) y compara P&L vs. solo acciones (buy-and-hold) — el benchmark honesto.

## Errores comunes
- Anualizar linealmente primas de 1 semana (infla el rendimiento).
- Tratar delta como probabilidad real (es riesgo-neutral; con IV de evento sobreestima el movimiento «normal»).
- Ignorar el coste de oportunidad del upside cedido en biotech (un buen readout puede ser +80 %).
- Usar la IV del strike ATM para todos los strikes (hay skew).

## Skills de terceros útiles (`references/01-opciones-volatilidad-*`)
`options-strategy-advisor` (tradermonty), `greeks`, `option-chain`, `spread-analysis`, `ib-find-short-roll`, `ib-collar`, `ib-pmcc-advisor`, `scanner-pmcc` (staskh), skills de opciones de AlphaGBM, `option-vol-analysis` (LSEG), `volatility-modeling` (JoelLewis), `options-pricing` (agiprolabs).
