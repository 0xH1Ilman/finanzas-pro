# macro-fed — política monetaria y datos macro

## Fuentes primarias (por orden)
- Fed: comunicados FOMC, SEP/dot plot (marzo, junio, septiembre, diciembre), actas (3 semanas después), discursos, H.4.1 (balance), H.15 (tipos).
- Datos: BLS (CPI, PPI, empleo/NFP, JOLTS), BEA (PIB, PCE), Census (ventas minoristas), ISM (PMIs), Univ. de Michigan (expectativas de inflación), Conference Board.
- Mercado: CME FedWatch (probabilidades implícitas de futuros de fondos federales), curva del Tesoro, breakevens TIPS (FRED: T5YIE, T10YIE), SOFR futures.

## Flujo para «¿qué hará la Fed?»
1. Rango actual de fed funds (buscado, con fecha de la última reunión).
2. Próxima reunión y probabilidades FedWatch (hora del dato).
3. Últimos datos de inflación (CPI/PCE core, mensual y anual) y empleo vs consenso.
4. Lo que dijeron el presidente y los votantes recientemente (citas cortas con fecha).
5. Dot plot vigente vs precio del mercado (¿mercado más dovish o hawkish que la Fed?).
6. Lectura (opinión marcada) con escenarios y qué dato los cambiaría.

## Conceptos útiles
- Datos «vs consenso» con la misma base (SA vs NSA, MoM vs YoY, headline vs core).
- Curva: 2s10s, 3m10y; desinversión por bull/bear steepening; term premium (ACM, Kim-Wright).
- Condiciones financieras: índices NFCI (Chicago Fed), GS FCI; spreads de crédito (HY OAS).
- Regla de Taylor como referencia, no como predicción.

## Skills de terceros
`macro-regime-detector`, `economic-calendar-fetcher`, `fxmacrodata-calendar`, `market-environment-analysis` (tradermonty), `macro-rates-monitor`, `swap-curve-strategy` (LSEG/Anthropic) en `references/04-*` y `08-*`.
