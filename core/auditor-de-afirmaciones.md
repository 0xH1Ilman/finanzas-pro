# Auditor de afirmaciones financieras

Revisa un texto (propio o ajeno: post, tesis, hilo, nota) antes de publicarlo o de creérselo. Devuelve una tabla `Afirmación | Problema | Gravedad (alta/media/baja) | Corrección/qué verificar`.

## Checklist

**Datos**
- [ ] ¿Cada cifra tiene fuente y fecha? ¿Es primaria?
- [ ] ¿Datos actuales o desactualizados (precio, consenso, tipos)?
- [ ] ¿Unidades, divisa, periodo fiscal correctos?

**Comparaciones**
- [ ] GAAP vs non-GAAP mezclados.
- [ ] Básico vs diluido; continuadas vs totales.
- [ ] YoY vs QoQ; orgánico vs reportado.
- [ ] Price return vs total return; nominal vs real.
- [ ] Múltiplos con denominadores distintos (forward vs trailing, EV vs market cap).

**Estadística**
- [ ] Cherry-picking de fechas (¿qué pasa si mueves el inicio/fin?).
- [ ] Sesgo de supervivencia (índices, fondos, ganadores).
- [ ] Correlación presentada como causalidad.
- [ ] Muestra pequeña / overfitting en backtests; sin out-of-sample; sin costes ni slippage.
- [ ] Anualización incorrecta; vol no anualizada; Sharpe sin tipo libre de riesgo.
- [ ] Probabilidades riesgo-neutrales (delta, N(d2)) presentadas como reales.

**Opciones y apalancamiento**
- [ ] Ignora volatility decay / daily reset en LETFs.
- [ ] Ignora coste de financiación, spreads bid-ask, asignación anticipada, dividendos.
- [ ] «Ingresos» por prima presentados sin el riesgo a la baja ni el upside cedido.

**Lenguaje y cumplimiento**
- [ ] Promesas («seguro», «no puede perder»).
- [ ] Recomendación personalizada presentada como asesoría.
- [ ] Falta divulgación de posición.
- [ ] Posibles problemas de manipulación (bombo de small caps, rumores sin fuente).

## Salida
Veredicto general (publicable / publicable con cambios / no publicable), tabla de hallazgos ordenada por gravedad, versión corregida si se pide.
