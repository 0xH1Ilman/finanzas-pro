# earnings-check — veredicto beat/miss que aguanta Reddit

## Cuándo
«¿X batió?», «resumen de resultados de X», «X reportó, ¿qué tal?», o antes de publicar sobre resultados.

## Flujo

1. **Identifica el periodo**: trimestre fiscal exacto (p. ej. Q3 FY2027) y fecha de publicación.
2. **Fuente primaria**: nota de prensa (IR de la compañía, Business Wire/PR Newswire/GlobeNewswire) o 8-K (Ex. 99.1). Extrae:
   - Ingresos totales.
   - EPS GAAP diluido.
   - EPS ajustado / non-GAAP diluido (y la tabla de reconciliación: qué excluyen: SBC, amortización de intangibles, one-offs, impuestos).
   - Métricas clave del sector (p. ej. biotech: ventas por producto, cash runway; SaaS: ARR, NRR; bancos: NII, NIM).
   - Guidance (rango, periodo, si sube/baja/mantiene).
3. **Consenso**: busca el consenso **de cada base** con proveedor y fecha. Lo habitual en titulares (LSEG/Zacks/FactSet) es **ajustado**. Si no encuentras consenso GAAP, **no** emitas veredicto GAAP: di «sin consenso GAAP disponible».
4. **Calcula** con `scripts/earnings_check.py` (rechaza bases mezcladas):
   ```bash
   python3 scripts/earnings_check.py --json datos.json
   ```
   Formato de `datos.json`:
   ```json
   {"ticker":"XYZ","period":"Q3 FY2026","metrics":[
     {"name":"EPS","basis":"adjusted","actual":1.23,"consensus":1.10,"consensus_source":"LSEG, 2026-11-04"},
     {"name":"EPS","basis":"gaap","actual":0.85,"consensus":null},
     {"name":"Revenue","basis":"reported","actual":2450,"consensus":2400,"unit":"USD M","consensus_source":"LSEG"}
   ]}
   ```
   Umbral por defecto «in line»: ±1 % para ingresos, ±$0.01 o ±2 % para EPS (lo mayor). Ajustable con `--inline-pct`.
5. **Reacción**: precio pre/after-market con hora. No atribuyas causa al movimiento sin evidencia (call, guidance, comentario de la directiva).
6. **Entrega** (tabla):

| Métrica | Base | Real | Consenso (fuente, fecha) | Dif. | Veredicto |
|---|---|---|---|---|---|

Seguido de: guidance vs consenso, 2–4 puntos clave del call (si ya ocurrió), reacción de precio con hora, riesgos/dudas de calidad (one-offs que inflan el ajustado, cambios de definición).

## Trampas típicas
- Titulares que comparan GAAP con consenso ajustado → «miss» falso (o «beat» falso).
- Beneficio por operaciones continuadas vs total.
- Splits recientes (EPS no comparable con estimaciones antiguas).
- Divisa (ADR que reportan en EUR/JPY/CNY).
- Biotech pre-revenue: el EPS importa poco; mira cash, quema y catalizadores.
- Cambios en la definición del non-GAAP entre trimestres: señálalo.

## Plantilla para Reddit
```
**$XYZ Q3 FY26** (reportado 2026-11-04 AMC)
- Revenue: $2.45B vs $2.40B est. (LSEG) → beat +2.1%
- Adj. EPS: $1.23 vs $1.10 est. (LSEG) → beat
- GAAP EPS: $0.85 (no GAAP consensus available, not comparable to adj. est.)
- Guide Q4 rev: $2.5–2.6B vs $2.52B est. → midpoint above
- AH: +6.8% at 17:42 ET
Source: company PR / 8-K. Not financial advice.
```
