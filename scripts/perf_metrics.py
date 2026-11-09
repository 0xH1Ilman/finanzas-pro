#!/usr/bin/env python3
"""Métricas de rendimiento a partir de una serie de valores (equity) o rentabilidades diarias.
Uso como módulo: from perf_metrics import metrics; o CLI:
  python3 perf_metrics.py --csv serie.csv --col equity [--returns] [--rf 0.04] [--date-col date]
"""
import argparse, csv, math, statistics
from datetime import date

def metrics(values, dates=None, rf=0.0, periods=252):
    """values: lista de valores de cartera (>0). dates: lista de datetime.date opcional."""
    rets = [values[i] / values[i - 1] - 1 for i in range(1, len(values))]
    n = len(rets)
    if n < 2:
        raise ValueError("Serie demasiado corta")
    years = ((dates[-1] - dates[0]).days / 365.25) if dates else n / periods
    cagr = (values[-1] / values[0]) ** (1 / years) - 1 if years > 0 else float("nan")
    vol = statistics.pstdev(rets) * math.sqrt(periods)
    rf_p = (1 + rf) ** (1 / periods) - 1
    ex = [r - rf_p for r in rets]
    sharpe = statistics.mean(ex) / statistics.pstdev(rets) * math.sqrt(periods) if statistics.pstdev(rets) > 0 else float("nan")
    down = [min(0.0, e) for e in ex]
    dd_dev = math.sqrt(sum(d * d for d in down) / n) * math.sqrt(periods)
    sortino = statistics.mean(ex) * periods / dd_dev if dd_dev > 0 else float("nan")
    peak, peak_i, mdd, mdd_peak_i, mdd_trough_i = values[0], 0, 0.0, 0, 0
    sq = 0.0; longest = cur = 0
    for i, v in enumerate(values):
        if v >= peak:
            peak, peak_i = v, i; cur = 0
        else:
            cur += 1; longest = max(longest, cur)
        dd = v / peak - 1
        sq += dd * dd
        if dd < mdd:
            mdd, mdd_peak_i, mdd_trough_i = dd, peak_i, i
    ulcer = math.sqrt(sq / len(values))
    out = dict(cagr=cagr, vol_anual=vol, sharpe=sharpe, sortino=sortino, max_drawdown=mdd,
               calmar=(cagr / abs(mdd)) if mdd < 0 else float("nan"), ulcer_index=ulcer,
               dias_max_bajo_agua=longest, anos=years, valor_final_x=values[-1] / values[0])
    if dates:
        out["mdd_pico"] = dates[mdd_peak_i].isoformat(); out["mdd_valle"] = dates[mdd_trough_i].isoformat()
        by_year = {}
        for i in range(1, len(values)):
            y = dates[i].year
            by_year.setdefault(y, [values[i - 1], values[i]])[1] = values[i]
        yr = {y: v[1] / v[0] - 1 for y, v in by_year.items()}
        out["peor_ano"] = min(yr.items(), key=lambda kv: kv[1]); out["mejor_ano"] = max(yr.items(), key=lambda kv: kv[1])
        by_m = {}
        for i in range(1, len(values)):
            k = (dates[i].year, dates[i].month)
            by_m.setdefault(k, [values[i - 1], values[i]])[1] = values[i]
        out["pct_meses_positivos"] = sum(1 for v in by_m.values() if v[1] > v[0]) / len(by_m)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True); ap.add_argument("--col", required=True)
    ap.add_argument("--date-col", default="date"); ap.add_argument("--returns", action="store_true")
    ap.add_argument("--rf", type=float, default=0.0)
    a = ap.parse_args()
    dates, vals = [], []
    with open(a.csv) as fh:
        for row in csv.DictReader(fh):
            if not row.get(a.col):
                continue
            dates.append(date.fromisoformat(row[a.date_col][:10])); vals.append(float(row[a.col]))
    if a.returns:
        eq = [1.0]
        for r in vals:
            eq.append(eq[-1] * (1 + r))
        vals = eq; dates = [dates[0]] + dates
    import json
    print(json.dumps(metrics(vals, dates, a.rf), indent=2, default=lambda x: round(x, 6) if isinstance(x, float) else str(x)))

if __name__ == "__main__":
    main()
