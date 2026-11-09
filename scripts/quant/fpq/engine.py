"""Motor diario de carteras con reglas: pesos objetivo, calendario fijo, bandas absolutas, filtro de régimen con sub-cartera refugio,
recorte de satélites, aportaciones, costes e impuestos. Núcleo en C (se compila solo) con implementación de referencia en Python (`run_py`)
que da el mismo resultado; si no hay compilador se usa la de Python.
Convención temporal: la señal se calcula con el cierre de t y se opera al cierre de t+delay (delay=1 por defecto). Las bandas y el calendario se evalúan y ejecutan al cierre."""
import ctypes, json, subprocess, pathlib, copy, numpy as np, pandas as pd
from . import signals, metrics as M
_here = pathlib.Path(__file__).parent; _lib = None
def _load():
    """Compila el núcleo en C la primera vez (en FPQ_HOME, porque la carpeta de la skill puede ser de solo lectura). Si no hay compilador, devuelve False."""
    global _lib
    if _lib is not None: return _lib
    src = _here / "_engine.c"
    try:
        import hashlib
        from . import config
        so = config.home() / f"_engine_{hashlib.sha256(src.read_bytes()).hexdigest()[:10]}.so"
        if not so.exists(): subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", str(so), str(src), "-lm"], check=True, capture_output=True)
        _lib = ctypes.CDLL(str(so))
    except Exception: _lib = False
    return _lib
def engine_info(): return "C (compilado)" if _load() else "Python (sin compilador: ~15 veces más lento, mismos resultados)"
def run_py(R, w, up, dn, lev, refw, sig, mlast, mon, every, phase, reset, trim_at, trim_to, rec, tc, swc, flow, flow_mode, tax, want_w=False):
    """Implementación de referencia (lenta, legible). Misma lógica que _engine.c."""
    T, N = R.shape; h = w.astype(float).copy(); s = np.zeros(N); f = np.zeros(N); bas = w.astype(float).copy(); sb = 0.0; carry = 0.0; V0 = 1.0; E = 1.0
    levw = w[lev].sum(); mode = int(sig[0]); anchor = phase; st = np.zeros(7); eq = np.empty(T); val = np.empty(T); W = np.empty((T, N)) if want_w else None
    if mode == 1:
        Pp = h[lev].sum(); f[lev] = w[lev] / levw if levw > 0 else 0; h[lev] = 0; bas[lev] = 0; s = Pp * refw; sb = Pp
    for t in range(T):
        cost = 0.0; txb = 0.0; trd = 0.0; g = 1 + R[t]; h *= g; s *= g; S = s.sum()
        if sig[t] != mode:
            if sig[t] == 1:
                Pp = h[lev].sum(); B = bas[lev].sum(); f[lev] = h[lev] / Pp if Pp > 0 else 0; h[lev] = 0; bas[lev] = 0
                txb += Pp - B; cost += swc * Pp; s = s + Pp * refw; sb = Pp; S += Pp; trd += Pp
            else:
                txb += S - sb; cost += swc * S; h[lev] = f[lev] * S; bas[lev] = h[lev]; s = np.zeros(N); trd += S; S = 0.0; sb = 0.0
            mode = int(sig[t]); st[1] += 1
        tot = h.sum() + S
        for j in range(N):
            if trim_at[j] > 0 and not (mode == 1 and lev[j]) and h[j] / tot >= trim_at[j]:
                ex = h[j] - trim_to[j] * tot; txb += ex * (1 - bas[j] / h[j]); bas[j] *= (h[j] - ex) / h[j]; h[j] -= ex; cost += tc * 2 * ex; trd += ex
                k = rec[j].astype(bool); den = h[k].sum()
                if den > 0: a = ex * h[k] / den; h[k] += a; bas[k] += a
                st[2] += 1
        doit = every > 0 and bool(mlast[t]) and ((mon[t] - anchor) % every) == 0; band = False
        for j in range(N):
            nw = f[j] * S / tot if (mode == 1 and lev[j]) else h[j] / tot
            if (w[j] > 0 or nw > 0) and (nw >= up[j] or nw <= dn[j]): doit = True; band = True
        if doit:
            traded = 0.0
            for j in range(N):
                if mode == 1 and lev[j]: continue
                tg = tot * w[j]; d = tg - h[j]
                if d < 0 and h[j] > 0: txb += (-d) * (1 - bas[j] / h[j]); bas[j] *= tg / h[j]
                else: bas[j] += d
                traded += abs(d); h[j] = tg
            if mode == 1:
                St = tot * levw; d = St - S
                if d < 0 and S > 0: txb += (-d) * (1 - sb / S); sb *= St / S
                else: sb += d
                traded += abs(d); s = St * refw; f[lev] = w[lev] / levw if levw > 0 else 0; h[lev] = 0; S = St
            cost += tc * traded; trd += traded / 2; st[0] += 1
            if band:
                st[6] += 1
                if reset: anchor = mon[t]
        due = 0.0
        if tax > 0:
            net = txb + carry
            if net > 0: due = tax * net; carry = 0.0
            else: carry = net
        st[3] += trd / tot; st[4] += cost / tot; st[5] += due / tot
        if cost + due > 0:
            k = 1 - (cost + due) / tot; h *= k; s *= k; bas *= k; sb *= k; S *= k; tot *= k
        E *= tot / V0; eq[t] = E; val[t] = tot
        if want_w: W[t] = (h + s) / tot
        a = flow[t] if flow is not None else 0.0
        if a != 0:
            a = max(a, -0.999 * tot)
            if flow_mode == 0: k = 1 + a / tot; h *= k; s *= k; bas *= k; sb *= k
            else:
                for j in range(N):
                    if mode == 1 and lev[j]: s = s + a * w[j] * refw; sb += a * w[j]
                    else: h[j] += a * w[j]; bas[j] += a * w[j]
            tot += a
        V0 = tot
    return eq, val, W, st
def run_c(R, w, up, dn, lev, refw, sig, mlast, mon, every, phase, reset, trim_at, trim_to, rec, tc, swc, flow, flow_mode, tax, want_w=False):
    lib = _load()
    if not lib or R.shape[1] > 64: return run_py(R, w, up, dn, lev, refw, sig, mlast, mon, every, phase, reset, trim_at, trim_to, rec, tc, swc, flow, flow_mode, tax, want_w)
    T, N = R.shape; c = lambda a, t: np.ascontiguousarray(a, dtype=t); p = lambda a: a.ctypes.data_as(ctypes.c_void_p) if a is not None else None
    R = c(R, np.float64); w = c(w, np.float64); up = c(up, np.float64); dn = c(dn, np.float64); lev = c(lev, np.uint8); refw = c(refw, np.float64); sig = c(sig, np.int8)
    mlast = c(mlast, np.uint8); mon = c(mon, np.int32); trim_at = c(trim_at, np.float64); trim_to = c(trim_to, np.float64); rec = c(rec, np.uint8)
    flow_ = c(flow, np.float64) if flow is not None else None; eq = np.empty(T); val = np.empty(T); W = np.empty((T, N)) if want_w else None; st = np.zeros(7)
    D = ctypes.c_double; I = ctypes.c_int
    lib.fpq_run(I(T), I(N), p(R), p(w), p(up), p(dn), p(lev), p(refw), p(sig), p(mlast), p(mon), I(every), I(phase), I(int(reset)), p(trim_at), p(trim_to), p(rec),
                D(tc), D(swc), p(flow_), I(flow_mode), D(tax), p(eq), p(val), p(W), p(st))
    return eq, val, W, st
PRESETS = {
 "gpa": dict(name="Golden Papilio Antimachus sin cripto", weights={"TQQQ": .25, "AVUV": .1875, "AVDV": .1875, "KMLM": .1875, "GOLD": .1875},
             rebalance=dict(every_months=24, phase=11, upper={"TQQQ": .50}, dev=.20),
             regime=dict(signal=dict(type="vol", asset="QQQ", window=20, exit=.35, enter=.25), assets=["TQQQ"], refuge={"KMLM": .5, "GOLD": .5}, delay=1, cost=.001)),
 "gpa_full": dict(name="Golden Papilio Antimachus completo", weights={"TQQQ": .20, "BITU": .05, "AVUV": .1875, "AVDV": .1875, "KMLM": .1875, "GOLD": .1875},
             rebalance=dict(every_months=24, phase=11, upper={"TQQQ": .40}, dev=.20, dev_exempt=["BITU"]),
             regime=dict(signal=dict(type="vol", asset="QQQ", window=20, exit=.35, enter=.25), assets=["TQQQ", "BITU"], refuge={"KMLM": .5, "GOLD": .5}, delay=1, cost=.001),
             trim=[dict(asset="BITU", at=.125, to=.05, recipients=["AVUV", "AVDV", "KMLM", "GOLD"])]),
 "hmea": dict(name="HMEA original 20×5", weights={"TQQQ": .2, "AVUV": .2, "AVDV": .2, "KMLM": .2, "GOLD": .2}, rebalance=dict(every_months=24, phase=11, upper={"TQQQ": .40}, dev=.20)),
 "hfea": dict(name="HFEA 55/45", weights={"UPRO": .55, "TMF": .45}, rebalance=dict(every_months=3, phase=0)),
 "6040": dict(name="60/40", weights={"SPY": .6, "IEF": .4}, rebalance=dict(every_months=12, phase=11)),
 "spy": dict(name="S&P 500", weights={"SPY": 1.0}, rebalance=dict(every_months=0)),
 "qqq": dict(name="Nasdaq-100", weights={"QQQ": 1.0}, rebalance=dict(every_months=0)),
}
def preset(name, **over):
    s = copy.deepcopy(PRESETS[name])
    for k, v in over.items(): _set(s, k, v)
    return s
def _set(spec, path, value):
    """Cambia un parámetro por ruta con puntos: 'regime.signal.exit', 'weights.TQQQ', 'rebalance.phase'."""
    ks = path.split("."); d = spec
    for k in ks[:-1]: d = d.setdefault(k, {})
    d[ks[-1]] = value
def with_params(spec, params):
    s = copy.deepcopy(spec)
    for k, v in params.items():
        if k == "leveraged_weight":      # reparte el resto a partes iguales entre los no apalancados
            lev = s["regime"]["assets"] if "regime" in s else [next(iter(s["weights"]))]; oth = [a for a in s["weights"] if a not in lev]
            tot_lev = sum(s["weights"][a] for a in lev)
            for a in lev: s["weights"][a] *= v / tot_lev
            for a in oth: s["weights"][a] = (1 - v) / len(oth)
            if "upper" in s.get("rebalance", {}):
                for a in s["rebalance"]["upper"]: s["rebalance"]["upper"][a] = 2 * s["weights"][a]
        else: _set(s, k, v)
    return s
class Result:
    def __init__(s, eq, val, W, st, idx, cols, rf, spec, sig):
        s.equity = pd.Series(eq, index=idx); s.value = pd.Series(val, index=idx); s.returns = s.equity.pct_change(); s.returns.iloc[0] = eq[0] - 1
        s.weights = pd.DataFrame(W, index=idx, columns=cols) if W is not None else None; s.rf = pd.Series(rf, index=idx); s.spec = spec; s.signal = pd.Series(sig, index=idx)
        s.stats = dict(rebalances=int(st[0]), switches=int(st[1]), trims=int(st[2]), turnover=float(st[3]), costs=float(st[4]), taxes=float(st[5]), band_rebalances=int(st[6]))
    def metrics(s, bench=None):
        m = M.summary(s.returns.values, s.rf.values, None if bench is None else bench.reindex(s.returns.index).values); m.update(s.stats)
        m["switches_per_year"] = s.stats["switches"] / (len(s.returns) / 252); m["time_out"] = float(s.signal.mean()); return m
class Backtest:
    """bt = Backtest(panel, spec, start, end); res = bt.run(); bt.median_calendars() para la mediana de todas las fases del calendario."""
    def __init__(s, panel, spec, start=None, end=None):
        s.spec = copy.deepcopy(spec); s.full = panel; w = s.spec["weights"]; reg = s.spec.get("regime"); cols = list(w)
        if reg: cols += [a for a in reg["refuge"] if a not in cols]
        s.cols = cols; sub = panel[cols + ["CASH"]]; ok = sub.dropna().index
        a = max(pd.Timestamp(start), ok[0]) if start else ok[0]; b = min(pd.Timestamp(end), ok[-1]) if end else ok[-1]
        s.i0 = panel.index.searchsorted(a); s.i1 = panel.index.searchsorted(b, side="right"); s.idx = panel.index[s.i0:s.i1]
        s.R = panel[cols].values[s.i0:s.i1]
        if np.isnan(s.R).any(): raise ValueError(f"faltan datos en {[c for c in cols if panel[c].iloc[s.i0:s.i1].isna().any()]} entre {a.date()} y {b.date()}")
        s.rf = panel["CASH"].values[s.i0:s.i1]; N = len(cols); s.w = np.array([w.get(c, 0.0) for c in cols])
        if abs(s.w.sum() - 1) > 1e-9: raise ValueError(f"los pesos suman {s.w.sum():.4f}, no 1")
        rb = s.spec.get("rebalance", {}); dev = rb.get("dev"); ex = set(rb.get("dev_exempt", []))
        s.up = np.array([rb.get("upper", {}).get(c, (s.w[i] + dev) if (dev and s.w[i] > 0 and c not in ex) else 9.0) for i, c in enumerate(cols)])
        # un activo con tope `upper` explícito NO tiene banda inferior salvo que se indique en `lower`: nunca se recompra a la baja
        s.dn = np.array([rb.get("lower", {}).get(c, (s.w[i] - dev) if (dev and s.w[i] > 0 and c not in ex and c not in rb.get("upper", {})) else -9.0) for i, c in enumerate(cols)])
        s.lev = np.array([bool(reg) and c in reg["assets"] for c in cols]); s.refw = np.array([reg["refuge"].get(c, 0.0) if reg else 0.0 for c in cols])
        s.every = int(rb.get("every_months", 0)); s.phase = int(rb.get("phase", 0)); s.reset = bool(rb.get("reset_calendar", False))
        m = np.asarray(s.idx.year * 12 + s.idx.month - 1); s.mon = m; s.mlast = np.r_[m[1:] != m[:-1], False]
        s.trim_at = np.zeros(N); s.trim_to = np.zeros(N); s.rec = np.zeros((N, N), np.uint8)
        for tr in s.spec.get("trim", []):
            j = cols.index(tr["asset"]); s.trim_at[j] = tr["at"]; s.trim_to[j] = tr["to"]
            for c in tr["recipients"]: s.rec[j, cols.index(c)] = 1
        s.tc = float(s.spec.get("costs", {}).get("turnover", 0.0)); s.tax = float(s.spec.get("tax", {}).get("rate", 0.0))
        fl = s.spec.get("flows"); s.flow = None; s.flow_mode = 0
        if fl and fl.get("amount"):
            s.flow = np.zeros(len(s.idx)); per = fl.get("every_months", 1); s.flow[s.mlast & ((m - m[0]) % per == 0)] = fl["amount"]; s.flow_mode = 0 if fl.get("mode", "current") == "current" else 1
        s._sigcache = {}
    def state(s, spec=None):
        reg = spec if spec is not None else (s.spec.get("regime") or {}).get("signal")
        if not reg: return np.zeros(len(s.full), np.int8)
        k = json.dumps(reg, sort_keys=True)
        if k not in s._sigcache: s._sigcache[k] = signals.make(s.full, reg)
        return s._sigcache[k]
    def _shift(s, st, delay):
        if s.i0 >= delay: return st[s.i0 - delay:s.i1 - delay]
        return np.r_[np.zeros(delay - s.i0, np.int8), st[:s.i1 - delay]]
    def run(s, phase=None, state=None, weights=False, engine="c", **over):
        """over: delay, switch_cost, every, tc, tax. state: señal completa (longitud del panel) para placebos o señales externas."""
        reg = s.spec.get("regime") or {}; delay = over.get("delay", reg.get("delay", 1)); swc = over.get("switch_cost", reg.get("cost", 0.0))
        st = s.state() if state is None else state; sig = s._shift(np.asarray(st, np.int8), delay) if reg else np.zeros(len(s.idx), np.int8)
        fn = run_c if engine == "c" else run_py
        eq, val, W, stt = fn(s.R, s.w, s.up, s.dn, s.lev, s.refw, sig, s.mlast, s.mon, over.get("every", s.every), s.phase if phase is None else phase, s.reset,
                             s.trim_at, s.trim_to, s.rec, over.get("tc", s.tc), swc, s.flow, s.flow_mode, over.get("tax", s.tax), weights)
        return Result(eq, val, W, stt, s.idx, s.cols, s.rf, s.spec, sig)
    def phases(s): return range(max(s.every, 1))
    def median_calendars(s, **kw):
        """Mediana de las métricas entre todas las fases posibles del calendario, con mínimo, máximo y peor caída."""
        d = pd.DataFrame([s.run(phase=k, **kw).metrics() for k in s.phases()]); o = d.median(numeric_only=True).to_dict()
        o.update(CAGR_min=d.CAGR.min(), CAGR_max=d.CAGR.max(), MDD_worst=d.MDD.min(), Sharpe_min=d.Sharpe.min(), n_calendars=len(d)); return o
def run(panel, spec, start=None, end=None, **kw): return Backtest(panel, spec, start, end).run(**kw)
