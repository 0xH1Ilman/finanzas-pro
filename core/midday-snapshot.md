# midday-snapshot — foto de mercado a media sesión

## Cuándo
«¿Cómo va el mercado?», «snapshot», «midday», «resumen del día».

## Regla de oro
Todo buscado en el momento. Cada bloque con **hora ET** de los datos. Si una fuente devuelve el cierre de ayer, se descarta o se marca. Comprueba que la fecha de la página es la de hoy.

## Bloques (en este orden)

1. **Titular de 1 línea**: qué mueve hoy (dato macro, Fed, earnings mega-cap, geopolítica).
2. **Índices**: S&P 500, Nasdaq 100/Composite, Dow, Russell 2000 — nivel y % vs cierre anterior. Opcional: Stoxx 600, Nikkei, Hang Seng (cierres).
3. **Volatilidad**: VIX (y VVIX/MOVE si relevante), skew si hay evento.
4. **Tipos y dólar**: UST 2Y, 10Y, 30Y (nivel y pb), curva 2s10s; DXY; EUR/USD; USD/JPY; USD/COP si interesa.
5. **Commodities**: WTI/Brent, oro, cobre; BTC/ETH.
6. **Sectores**: los 11 sectores S&P (o ETFs SPDR) ordenados por %; mejores/peores; amplitud (A/D, % sobre MA50 si disponible).
7. **Movers**: top subidas/bajadas con causa documentada (earnings, guidance, M&A, FDA, rating).
8. **Calendario restante**: datos macro de la tarde, subastas del Tesoro, Fed speakers, earnings after-close.
9. **Lectura** (opinión marcada): 2–3 frases de régimen (risk-on/off, rotación, qué vigilar).

## Fuentes sugeridas
Índices/futuros: CNBC, Reuters, Bloomberg, WSJ markets, Yahoo Finance. Tipos: Tesoro de EE. UU., CNBC bonds. Macro calendario: Investing.com, MarketWatch, Fed. Sectores: SPDR / Finviz. FedWatch: CME.

## Formato
Tabla compacta por bloque; % con signo; pb para tipos; hora ET en cabecera del bloque. Cierra con **Fuentes**.

## Skills de terceros relacionadas
`market-environment-analysis`, `market-breadth-analyzer`, `sector-analyst`, `economic-calendar-fetcher`, `market-news-analyst`, `morning-note` (en `references/04-*` y `02-*`).
