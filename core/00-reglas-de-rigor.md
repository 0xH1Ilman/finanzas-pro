# Reglas de rigor (aplican a todo lo financiero)

Objetivo: que cualquier cifra que salga de aquí aguante el escrutinio de un subreddit de finanzas, un PM o un compliance officer.

## A. Datos

| Regla | Detalle |
|---|---|
| Frescura | Precios, IV, spreads, consenso, tipos, calendarios: **siempre buscados**, nunca de memoria. Indica hora (con zona: ET para EE. UU.) y fuente por cifra. |
| Horario | Pre-market (04:00–09:30 ET), regular (09:30–16:00 ET), after-hours (16:00–20:00 ET). Di en qué sesión está el dato. Midday ≈ 12:00–13:30 ET. |
| Fuente primaria | Resultados: nota de prensa / 8-K / 10-Q / 10-K / transcript. Macro: BLS, BEA, Fed, Tesoro. Opciones: cadena del broker o proveedor (CBOE, OCC). Agregadores (Yahoo, MarketWatch, Investing) solo como apoyo y diciéndolo. |
| Conflicto de fuentes | Si dos fuentes difieren, enseña ambas y explica la causa probable (GAAP vs ajustado, diluido vs básico, operaciones continuadas vs totales, fecha distinta, divisa). |
| Revisiones | Consenso: anota la fecha y el proveedor (LSEG/IBES, FactSet, S&P CapIQ, Zacks, Visible Alpha). Distintos proveedores dan distintos números. |
| Unidades | Divisa, escala (M, B), periodo (trimestre fiscal vs natural), por acción básica o diluida. |

## B. Comparaciones válidas

- EPS GAAP ↔ consenso GAAP. EPS ajustado (non-GAAP) ↔ consenso ajustado. **Nunca cruzar.**
- Ingresos totales ↔ consenso de ingresos totales (no ingresos por producto vs total).
- Mismo periodo fiscal. Ojo con años fiscales desplazados (p. ej. NVDA, AAPL, MSFT).
- Guidance: compara el punto medio con el consenso del periodo siguiente; di si es rango.
- Crecimientos: interanual (YoY) vs secuencial (QoQ); orgánico vs reportado (FX, M&A).
- Rentabilidades: con o sin dividendos (total return vs price return); nominal vs real; anualizado con capitalización correcta.

## C. Cálculo

- Todo número derivado (rendimientos, griegas, CAGR, drawdown, breakevens, tamaños de posición) → **ejecuta código** (`scripts/`). Muestra la fórmula o el comando.
- Anualizar: `(1+r)^(365/días) − 1` para rentabilidades de opciones; no multiplicar linealmente salvo que se diga «simple».
- Volatilidad: anualizar con √252 (días hábiles). Distingue IV (implícita), HV/RV (histórica/realizada).
- Probabilidades de opciones: N(d2) ≈ probabilidad (riesgo-neutral) de acabar ITM; delta ≈ proxy rápido. Son medidas riesgo-neutrales, no probabilidades reales.

## D. Lenguaje

- Hecho («la compañía reportó…»), cálculo («implica…»), opinión («a mi juicio…») separados.
- Nada de «garantizado», «seguro», «no puede bajar».
- Recomendaciones: presenta opciones con trade-offs; la decisión es del usuario. Añade «no es asesoramiento financiero» cuando el contenido vaya a publicarse o trate de una operación concreta.
- Si falta un dato, dilo y no lo rellenes.

## E. Checklist exprés antes de enviar

1. ¿Cada cifra tiene fuente y hora?
2. ¿Comparé bases iguales?
3. ¿Los derivados se calcularon con código?
4. ¿Distinguí hecho/cálculo/opinión?
5. ¿Fuentes al final?
