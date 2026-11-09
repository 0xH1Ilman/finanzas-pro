# biotech-catalyst-vol — catalizadores binarios y volatilidad

## Cuándo
Biotech/farma con evento: PDUFA, AdComm, readout de fase 1/2/3, presentación en congreso (ASCO, ASH, ESMO, AACR), CRL, aprobación EMA/CHMP, earnings con ventas de lanzamiento.

## Flujo

1. **Calendario del evento** (buscado y fechado): fuente primaria (nota de prensa de la compañía, FDA, ClinicalTrials.gov, programa del congreso). Marca si la fecha es exacta, «Q-año» o «1H/2H». PDUFA puede llegar antes. Readouts «topline» suelen anunciarse pre-market.
2. **Estructura de vol**: IV por vencimiento (term structure). El vencimiento que cruza el evento tendrá IV inflada («kink»). Calcula:
   - **Expected move implícito** ≈ precio del straddle ATM del primer vencimiento post-evento / S (≈0,8 × σ√T en BS; el straddle es mejor proxy).
   - **IV de evento aislada** (forward vol): con dos vencimientos T1 (pre) y T2 (post):  σ_evento² ≈ σ2²·T2 − σ1²·T1  (en varianza total; T en años). Calcúlala con código.
3. **Comparación histórica**: movimientos de la propia acción y de comparables en eventos similares (misma fase, misma indicación, mismo tamaño de compañía). `options_tools.py event-move --straddle X --hist ...` da ratio implícito/histórico.
4. **Distribución binaria**: los resultados no son lognormales: escenario éxito (+x %) / fracaso (−y %, a menudo −50/−80 % en small caps de un solo activo) / ambiguo. Pide o estima probabilidades (tasas históricas de éxito por fase y área: p. ej. estudios BIO/Informa) y marca la estimación como tal.
5. **Implicaciones para covered calls**:
   - Vender el vencimiento que cruza el evento = cobrar la IV de evento, pero cede el upside del escenario éxito.
   - Vender solo vencimientos previos al evento = prima menor, mantiene el upside.
   - La call no cubre el gap bajista: si el riesgo es existencial, collar/put spread.
6. **Factores específicos**: cash runway (trimestres de caja / quema), riesgo de ampliación de capital post-dato (ATM, follow-on), short interest y days to cover, opcionalidad de M&A, propiedad institucional, partners.

## Salida
Tabla: evento, fecha (exacta/estimada, fuente), S, straddle, expected move, IV pre/post, IV de evento, movimiento histórico medio/mediano en eventos comparables, ratio implícito/histórico, opción de estrategia con trade-offs.

## Skills de terceros
`catalyst-calendar` y `earnings-preview` (Anthropic, `references/02-*`), `option-vol-analysis`, `options-strategy-advisor` (`01-*`), `news-sentiment`, `insider-trading` (staskh).
