#!/usr/bin/env python3
"""Backtest de carteras con ETFs apalancados sintéticos de reajuste diario (HFEA y variantes).

Cada activo se simula a partir de la rentabilidad diaria del SUBYACENTE:
  r_LETF = L * r_sub - (L - 1) * rf_diario - comision_diaria
Rebalanceo: daily | monthly | quarterly | annual | none | band:X (desviación absoluta X).

Ejemplos:
  python3 leveraged_backtest.py --demo
  python3 leveraged_backtest.py --csv datos.csv --assets SPX:3:0.0091,TLT20:3:0.0106 \
      --weights 0.55,0.45 --rebalance quarterly --rf-col tbill
CSV: columna `date` (YYYY-MM-DD) + columnas de precios (o rentabilidades con --returns)
     + opcional columna de tipo corto anual en decimal (--rf-col) o --rf fijo.
"""
import argparse, csv, json, math, os, random, sys
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from perf_metrics import metrics

def load(path, cols, returns, rf_col, start, end):
    dates, data, rfs = [], {c: [] for c in cols}, []
    with open(path) as fh:
        for row in csv.DictReader(fh):
            d = date.fromisoformat(row["date"][:10])
            if (start and d < start) or (end and d > end):
                continue
            if any(not row.get(c) for c in cols):
                continue
            dates.append(d)
            for c in cols:
                data[c].append(float(row[c]))
            rfs.append(float(row[rf_col]) if rf_col and row.get(rf_col) else None)
    if not returns:
        for c in cols:
            p = data[c]
            data[c] = [0.0] + [p[i] / p[i - 1] - 1 for i in range(1, len(p))]
    return dates, data, rfs

def demo_data(n=252 * 30, seed=7):
    rnd = random.Random(seed)
    dates, eq, bd, rf = [], [], [], []
    d = date(1995, 1, 3)
    for i in range(n):
        while d.weekday() >= 5:
            d += timedelta(days=1)
        dates.append(d); d += timedelta(days=1)
        z1, z2 = rnd.gauss(0, 1), rnd.gauss(0, 1)
        rho = -0.3
        eq.append(0.0003 + 0.011 * z1)
        bd.append(0.00015 + 0.009 * (rho * z1 + math.sqrt(1 - rho * rho) * z2))
        rf.append(0.03)
    return dates, {"EQ": eq, "BOND": bd}, rf

def should_rebalance(mode, prev, cur, weights_now, target):
    if mode == "daily":
        return True
    if mode == "none":
        return False
    if mode == "monthly":
        return cur.month != prev.month
    if mode == "quarterly":
        return (cur.month - 1) // 3 != (prev.month - 1) // 3
    if mode == "annual":
        return cur.year != prev.year
    if mode.startswith("band:"):
        x = float(mode.split(":")[1])
        return any(abs(w - t) > x for w, t in zip(weights_now, target))
    raise ValueError(mode)

def run(dates, rets, assets, weights, rebalance, rfs, rf_fixed):
    names = [a[0] for a in assets]
    hold = [w for w in weights]  # valor por activo, cartera inicia en 1
    eq_curve = [1.0]
    letf_curves = {n: [1.0] for n in names}
    for i in range(1, len(dates)):
        rf = rfs[i] if rfs and rfs[i] is not None else rf_fixed
        rf_d = rf / 252
        for k, (n, L, fee) in enumerate(assets):
            r = L * rets[n][i] - (L - 1) * rf_d - fee / 252
            r = max(r, -1.0)
            hold[k] *= (1 + r)
            letf_curves[n].append(letf_curves[n][-1] * (1 + r))
        tot = sum(hold)
        eq_curve.append(tot)
        if tot <= 0:
            break
        if i + 1 < len(dates):
            wn = [h / tot for h in hold]
            if should_rebalance(rebalance, dates[i], dates[i + 1], wn, weights):
                hold = [tot * w for w in weights]
    return eq_curve, letf_curves

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv"); ap.add_argument("--demo", action="store_true")
    ap.add_argument("--assets", default="EQ:3:0.0091,BOND:3:0.0106", help="COL:apalancamiento:comision_anual,...")
    ap.add_argument("--weights", default="0.55,0.45")
    ap.add_argument("--rebalance", default="quarterly")
    ap.add_argument("--returns", action="store_true", help="las columnas ya son rentabilidades diarias")
    ap.add_argument("--rf-col"); ap.add_argument("--rf", type=float, default=0.03)
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out-csv", help="guardar curva de equity")
    a = ap.parse_args()
    assets = []
    for spec in a.assets.split(","):
        n, L, fee = spec.split(":"); assets.append((n, float(L), float(fee)))
    weights = [float(x) for x in a.weights.split(",")]
    assert abs(sum(weights) - 1) < 1e-6, "los pesos deben sumar 1"
    assert len(weights) == len(assets)
    if a.demo:
        dates, rets, rfs = demo_data()
        print("AVISO: datos SINTÉTICOS de demostración, no históricos.", file=sys.stderr)
    else:
        if not a.csv:
            ap.error("--csv o --demo")
        dates, rets, rfs = load(a.csv, [x[0] for x in assets], a.returns, a.rf_col,
                                date.fromisoformat(a.start) if a.start else None, date.fromisoformat(a.end) if a.end else None)
    eq, letfs = run(dates, rets, assets, weights, a.rebalance, rfs, a.rf)
    unlev = [(n, 1.0, 0.0) for n, _, _ in assets]
    eq_u, _ = run(dates, rets, unlev, weights, a.rebalance, rfs, a.rf)
    rf_mean = (sum(x for x in rfs if x is not None) / max(1, sum(1 for x in rfs if x is not None))) if rfs and any(x is not None for x in rfs) else a.rf
    res = {"periodo": [dates[0].isoformat(), dates[len(eq) - 1].isoformat()],
           "config": {"assets": assets, "weights": weights, "rebalance": a.rebalance},
           "cartera_apalancada": metrics(eq, dates[:len(eq)], rf_mean),
           "misma_cartera_sin_apalancar": metrics(eq_u, dates[:len(eq_u)], rf_mean)}
    for n, curve in letfs.items():
        res[f"LETF_{n}_solo"] = metrics(curve, dates[:len(curve)], rf_mean)
    # decay teórico aproximado por activo
    for n, L, _ in assets:
        r = rets[n][1:]
        m = sum(r) / len(r); var = sum((x - m) ** 2 for x in r) / len(r)
        res.setdefault("volatility_decay_aprox_anual", {})[n] = -(L * L - L) / 2 * var * 252
    print(json.dumps(res, indent=2, ensure_ascii=False, default=lambda x: round(x, 5) if isinstance(x, float) else str(x)))
    if a.out_csv:
        with open(a.out_csv, "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["date", "levered", "unlevered"])
            for d, v, u in zip(dates, eq, eq_u):
                w.writerow([d.isoformat(), v, u])

if __name__ == "__main__":
    main()
