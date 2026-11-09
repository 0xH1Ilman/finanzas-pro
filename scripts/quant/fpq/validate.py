"""Validación estadística: fuera de muestra, rejillas y mesetas, placebo, sensibilidad de ejecución y de proxies, bootstrap por bloques,
Monte Carlo emparejado, Sharpe probabilístico y deflactado, Reality Check de White, corrección por pruebas múltiples, PBO (CSCV),
validación cruzada purgada y combinatoria, y walk-forward."""
import itertools, math, numpy as np, pandas as pd
from scipy import stats as sps
from . import engine as E, metrics as M, signals
# ---------------------------------------------------------------- rejillas
def grid(panel, spec, params, periods, base=None, phase="median"):
    """params: {'regime.signal.window':[10,20,...], 'regime.signal.exit':[...]} (rutas con puntos; 'leveraged_weight' también vale).
    Si una clave es tupla de rutas, sus valores son tuplas (parámetros ligados). periods: {'nombre': (inicio, fin)}.
    Devuelve DataFrame con una fila por (periodo, combinación) y las métricas (mediana de calendarios si phase='median')."""
    keys = list(params); rows = []
    for combo in itertools.product(*[params[k] for k in keys]):
        pr = {}
        for k, v in zip(keys, combo):
            if isinstance(k, tuple): pr.update(dict(zip(k, v)))
            else: pr[k] = v
        sp = E.with_params(spec, pr)
        for pn, (a, b) in periods.items():
            bt = E.Backtest(panel, sp, a, b); m = bt.median_calendars() if phase == "median" else bt.run(phase=phase).metrics()
            rows.append({"period": pn, **{(k if isinstance(k, str) else "+".join(k)): v for k, v in zip(keys, combo)}, **{x: m[x] for x in ("CAGR", "Sharpe", "MDD", "Sortino", "UPI", "Vol", "switches_per_year", "time_out")}})
    return pd.DataFrame(rows)
def plateau(g, chosen, base_metrics=None, metrics=("Sharpe", "CAGR", "MDD")):
    """Lee una rejilla: cuántas celdas mejoran a la base, puesto de la combinación elegida y dispersión de sus vecinos.
    chosen: dict {columna_parámetro: valor}. base_metrics: {periodo: {métrica: valor}} de la cartera sin la regla."""
    pc = [c for c in g.columns if c not in ("period", "CAGR", "Sharpe", "MDD", "Sortino", "UPI", "Vol", "switches_per_year", "time_out")]; out = {}
    for pn, d in g.groupby("period", sort=False):
        sel = d[np.logical_and.reduce([np.isclose(d[c].astype(float), float(v)) if not isinstance(v, tuple) else d[c] == v for c, v in chosen.items()])]
        o = {"cells": len(d)}
        for m in metrics:
            if base_metrics: o[f"{m}_beats_base"] = int((d[m] > base_metrics[pn][m]).sum())
            if len(sel): o[f"{m}_chosen"] = float(sel[m].iloc[0]); o[f"{m}_rank"] = int((d[m] > sel[m].iloc[0]).sum()) + 1
            o[f"{m}_median"] = float(d[m].median()); o[f"{m}_iqr"] = (float(d[m].quantile(.25)), float(d[m].quantile(.75)))
        if len(sel):                                                    # vecinos: un paso en cada parámetro (orden de la rejilla)
            nb = d.copy()
            for c, v in chosen.items():
                vals = list(dict.fromkeys(d[c])); i = next((k for k, x in enumerate(vals) if x == v or (not isinstance(v, tuple) and abs(float(x) - float(v)) < 1e-12)), None)
                if i is not None: nb = nb[nb[c].isin(vals[max(i - 1, 0):i + 2])]
            for m in metrics: o[f"{m}_neighbors"] = (float(nb[m].min()), float(nb[m].mean()), float(nb[m].max()))
        out[pn] = o
    return out
# ---------------------------------------------------------------- placebo y sensibilidades
def placebo_test(bt, n=400, seed=7, phase=None):
    """Compara la regla con n señales aleatorias de igual número de episodios y duraciones. Valor p = fracción de placebos ≥ regla."""
    rng = np.random.default_rng(seed); st = bt.state(); real = bt.run(phase=phase).metrics()
    pl = pd.DataFrame([bt.run(phase=phase, state=signals.placebo(st, rng, bt.i0, bt.i1)).metrics() for _ in range(n)])
    return dict(real={k: real[k] for k in ("CAGR", "Sharpe", "MDD")}, placebo_median={k: float(pl[k].median()) for k in ("CAGR", "Sharpe", "MDD")},
                p={k: float((pl[k] >= real[k]).mean()) for k in ("CAGR", "Sharpe", "MDD")}, n=n, episodes=len(signals.episodes(st[bt.i0:bt.i1], bt.idx)))
def execution_sensitivity(bt, delays=(0, 1, 2, 3, 5), costs=(0.001, 0.005, 0.01)):
    rows = [dict(delay=d, cost=0.001, **{k: v for k, v in bt.median_calendars(delay=d, switch_cost=0.001).items() if k in ("CAGR", "Sharpe", "MDD")}) for d in delays]
    rows += [dict(delay=1, cost=c, **{k: v for k, v in bt.median_calendars(delay=1, switch_cost=c).items() if k in ("CAGR", "Sharpe", "MDD")}) for c in costs if c != 0.001]
    return pd.DataFrame(rows)
def proxy_sensitivity(panel, specs, haircuts, start=None, end=None):
    """haircuts: lista de dicts {columna: puntos anuales a restar}. specs: {'nombre': spec}. Comprueba que la conclusión no depende del nivel de los proxies."""
    rows = []
    for hc in [{}] + list(haircuts):
        p2 = panel.copy()
        for c, a in hc.items(): p2[c] = p2[c] - a / 252
        for nm, sp in specs.items():
            m = E.Backtest(p2, sp, start, end).median_calendars(); rows.append(dict(haircut=str(hc) if hc else "ninguno", strategy=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MDD=m["MDD"]))
    return pd.DataFrame(rows)
def subperiods(panel, specs, periods):
    rows = []
    for pn, (a, b) in periods.items():
        for nm, sp in specs.items():
            m = E.Backtest(panel, sp, a, b).median_calendars(); rows.append(dict(period=pn, strategy=nm, **{k: m[k] for k in ("CAGR", "Vol", "Sharpe", "Sortino", "MDD", "UPI", "CAGR_min", "CAGR_max", "MDD_worst")}))
    return pd.DataFrame(rows)
def head_to_head(panel, spec_a, spec_b, start=None, end=None):
    """En cuántos calendarios A supera a B en CAGR, Sharpe y caída máxima."""
    A = E.Backtest(panel, spec_a, start, end); B = E.Backtest(panel, spec_b, start, end); n = max(len(A.phases()), len(B.phases()))
    a = pd.DataFrame([A.run(phase=k % max(A.every, 1)).metrics() for k in range(n)]); b = pd.DataFrame([B.run(phase=k % max(B.every, 1)).metrics() for k in range(n)])
    return {m: f"{int((a[m] > b[m]).sum())}/{n}" for m in ("CAGR", "Sharpe", "MDD")}
# ---------------------------------------------------------------- bootstrap y Monte Carlo
def stationary_indices(n, block, rng, size=None):
    """Bootstrap estacionario (Politis-Romano): bloques de longitud geométrica con media `block`."""
    size = size or n; idx = np.empty(size, dtype=np.int64); i = rng.integers(n)
    for t in range(size):
        idx[t] = i; i = rng.integers(n) if rng.random() < 1.0 / block else (i + 1) % n
    return idx
def bootstrap_ci(r, stat=M.sharpe, n=2000, block=21, alpha=0.05, seed=1, **kw):
    """Intervalo de confianza de cualquier estadístico por bootstrap estacionario. r: rentabilidades (array) o matriz T×K (se remuestrean las filas juntas)."""
    r = np.asarray(r, float); rng = np.random.default_rng(seed); vals = np.array([stat(r[stationary_indices(len(r), block, rng)], **kw) for _ in range(n)])
    return dict(point=float(stat(r, **kw)), lo=float(np.quantile(vals, alpha / 2)), hi=float(np.quantile(vals, 1 - alpha / 2)), se=float(vals.std()))
def monte_carlo(returns, years=10, n=10000, block_months=12, seed=3, bench=None):
    """Monte Carlo emparejado sobre rentabilidades MENSUALES: remuestrea bloques de meses consecutivos, los mismos para todas las columnas.
    returns: DataFrame (una columna por cartera). Devuelve percentiles de CAGR, caída máxima, prob. de pérdida y de batir a `bench`.
    Limitaciones: subestima caídas intra-mes y solo recombina lo ocurrido en la muestra."""
    X = np.log1p(returns.dropna().values); T, K = X.shape; H = years * 12; rng = np.random.default_rng(seed); nb = math.ceil(H / block_months)
    starts = rng.integers(0, T - block_months + 1, size=(n, nb)); ix = (starts[:, :, None] + np.arange(block_months)[None, None, :]).reshape(n, -1)[:, :H]
    P = X[ix].cumsum(axis=1); cg = np.expm1(P[:, -1, :] / years); pk = np.maximum.accumulate(np.concatenate([np.zeros((n, 1, K)), P], axis=1), axis=1)[:, 1:, :]; mdd = np.expm1((P - pk).min(axis=1))
    out = {}
    for j, c in enumerate(returns.columns):
        o = {f"CAGR_p{q}": float(np.percentile(cg[:, j], q)) for q in (5, 25, 50, 75, 95)}
        o.update(P_loss=float((cg[:, j] < 0).mean()), MDD_median=float(np.median(mdd[:, j])), MDD_p95=float(np.percentile(mdd[:, j], 5)), P_MDD_worse_40=float((mdd[:, j] < -0.40).mean()))
        if bench is not None and c != bench: o[f"P_beat_{bench}"] = float((cg[:, j] > cg[:, list(returns.columns).index(bench)]).mean())
        out[c] = o
    return pd.DataFrame(out).T
# ---------------------------------------------------------------- Sharpe: significación y deflactado
def sharpe_se(sr, n, skew=0.0, kurt=3.0): return math.sqrt(max((1 - skew * sr + (kurt - 1) / 4 * sr * sr) / (n - 1), 1e-18))
def psr(r, sr_benchmark=0.0, periods=252):
    """Probabilistic Sharpe Ratio (Bailey y López de Prado): P(Sharpe verdadero > sr_benchmark). sr_benchmark anualizado."""
    r = np.asarray(r, float); sr = r.mean() / r.std(ddof=1); return float(sps.norm.cdf((sr - sr_benchmark / math.sqrt(periods)) / sharpe_se(sr, len(r), sps.skew(r), sps.kurtosis(r, fisher=False))))
def expected_max_sharpe(n_trials, var_sr):
    """Sharpe máximo esperado por puro azar entre n_trials estrategias sin habilidad (por periodo)."""
    if n_trials < 2: return 0.0
    g = 0.5772156649; return math.sqrt(var_sr) * ((1 - g) * sps.norm.ppf(1 - 1 / n_trials) + g * sps.norm.ppf(1 - 1 / (n_trials * math.e)))
def deflated_sharpe(r, n_trials, trial_sharpes=None, periods=252):
    """Deflated Sharpe Ratio: PSR contra el Sharpe máximo esperable tras probar n_trials variantes.
    trial_sharpes: Sharpes ANUALIZADOS de las variantes probadas (para estimar su varianza); si falta, se usa la varianza teórica 1/n."""
    r = np.asarray(r, float); n = len(r); v = (np.var(np.asarray(trial_sharpes) / math.sqrt(periods), ddof=1) if trial_sharpes is not None and len(trial_sharpes) > 1 else 1.0 / (n - 1))
    sr0 = expected_max_sharpe(n_trials, v); sr = r.mean() / r.std(ddof=1)
    return dict(sharpe=float(sr * math.sqrt(periods)), sr0_annual=float(sr0 * math.sqrt(periods)), dsr=float(sps.norm.cdf((sr - sr0) / sharpe_se(sr, n, sps.skew(r), sps.kurtosis(r, fisher=False)))), n_trials=n_trials)
def min_track_record(r, sr_benchmark=0.0, alpha=0.05, periods=252):
    """Años de historial necesarios para que el Sharpe observado supere sr_benchmark con confianza 1−alpha."""
    r = np.asarray(r, float); sr = r.mean() / r.std(ddof=1); b = sr_benchmark / math.sqrt(periods)
    if sr <= b: return float("inf")
    return float((1 + (1 - sps.skew(r) * sr + (sps.kurtosis(r, fisher=False) - 1) / 4 * sr * sr) * (sps.norm.ppf(1 - alpha) / (sr - b)) ** 2) / periods)
def reality_check(excess, n=2000, block=21, seed=5):
    """Reality Check de White: ¿la mejor de K estrategias bate al benchmark más de lo esperable por haber buscado entre K?
    excess: matriz T×K de rentabilidades de cada estrategia MENOS el benchmark. Devuelve valor p del máximo."""
    X = np.asarray(excess, float); T, K = X.shape; mu = X.mean(0); V = math.sqrt(T) * mu.max(); rng = np.random.default_rng(seed); c = 0
    for _ in range(n):
        ix = stationary_indices(T, block, rng); c += (math.sqrt(T) * (X[ix].mean(0) - mu).max()) >= V
    return dict(best=int(mu.argmax()), best_excess_annual=float(mu.max() * 252), p_value=float(c / n), K=K)
def adjust_pvalues(p, method="holm"):
    """Corrección por pruebas múltiples: 'bonferroni', 'holm' o 'bh' (tasa de falsos descubrimientos)."""
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); out = np.empty(m)
    if method == "bonferroni": return np.minimum(p * m, 1)
    if method == "holm": out[o] = np.minimum(np.maximum.accumulate(p[o] * (m - np.arange(m))), 1); return out
    if method == "bh": out[o] = np.minimum(np.minimum.accumulate((p[o] * m / (np.arange(m) + 1))[::-1])[::-1], 1); return out
    raise ValueError(method)
# ---------------------------------------------------------------- PBO, validación cruzada, walk-forward
def pbo(returns_matrix, blocks=16, metric=M.sharpe):
    """Probability of Backtest Overfitting por CSCV (Bailey, Borwein, López de Prado, Zhu). returns_matrix: T×K (una columna por configuración).
    PBO = fracción de particiones en las que la mejor configuración dentro de muestra queda por debajo de la mediana fuera de muestra."""
    X = np.asarray(returns_matrix, float); T, K = X.shape; sz = T // blocks; B = [X[i * sz:(i + 1) * sz] for i in range(blocks)]; lam = []; deg = []
    for comb in itertools.combinations(range(blocks), blocks // 2):
        tr = np.concatenate([B[i] for i in comb]); te = np.concatenate([B[i] for i in range(blocks) if i not in comb])
        si = np.array([metric(tr[:, k]) for k in range(K)]); so = np.array([metric(te[:, k]) for k in range(K)]); b = si.argmax()
        w = (sps.rankdata(so)[b]) / (K + 1); lam.append(math.log(w / (1 - w))); deg.append((si[b], so[b]))
    lam = np.array(lam); deg = np.array(deg)
    return dict(pbo=float((lam <= 0).mean()), n_splits=len(lam), median_logit=float(np.median(lam)), is_best_mean=float(deg[:, 0].mean()), oos_of_best_mean=float(deg[:, 1].mean()),
                slope=float(np.polyfit(deg[:, 0], deg[:, 1], 1)[0]))
def purged_kfold(n, k=5, embargo=0, purge=0):
    """Particiones K-fold para series temporales: del entrenamiento se quitan `purge` observaciones a cada lado del bloque de prueba y `embargo` después."""
    edges = np.linspace(0, n, k + 1).astype(int)
    for i in range(k):
        a, b = edges[i], edges[i + 1]; tr = np.r_[np.arange(0, max(a - purge, 0)), np.arange(min(b + purge + embargo, n), n)]; yield tr, np.arange(a, b)
def cpcv(n, groups=6, test_groups=2, embargo=0, purge=0):
    """Validación cruzada combinatoria purgada: todas las combinaciones de `test_groups` bloques de prueba entre `groups`."""
    edges = np.linspace(0, n, groups + 1).astype(int)
    for comb in itertools.combinations(range(groups), test_groups):
        mask = np.ones(n, bool); te = []
        for g in comb:
            a, b = edges[g], edges[g + 1]; te.append(np.arange(a, b)); mask[max(a - purge, 0):min(b + purge + embargo, n)] = False
        yield np.flatnonzero(mask), np.concatenate(te)
def expanding_cv(n, min_train, step):
    for a in range(min_train, n, step): yield np.arange(0, a), np.arange(a, min(a + step, n))
def config_matrix(panel, spec, params, start=None, end=None, ensemble=True):
    """Rentabilidades diarias de cada combinación de parámetros (columnas). ensemble=True promedia todas las fases del calendario."""
    keys = list(params); cols = {}
    for combo in itertools.product(*[params[k] for k in keys]):
        pr = {}
        for k, v in zip(keys, combo):
            if isinstance(k, tuple): pr.update(dict(zip(k, v)))
            else: pr[k] = v
        bt = E.Backtest(panel, E.with_params(spec, pr), start, end)
        cols[str(combo)] = pd.concat([bt.run(phase=ph).returns for ph in bt.phases()], axis=1).mean(axis=1) if ensemble else bt.run().returns
    return pd.DataFrame(cols)
def walk_forward(matrix, train_years=10, test_years=2, metric=M.sharpe, anchored=True):
    """Walk-forward sobre una matriz T×K de rentabilidades por configuración: en cada ventana elige la mejor por `metric` con datos pasados
    y aplica sus rentabilidades al tramo siguiente. Devuelve la serie fuera de muestra encadenada, la elección por ventana y la eficiencia
    (métrica fuera de muestra / métrica de la mejor configuración fija elegida con todo el historial)."""
    X = matrix.dropna(); n = len(X); tr = int(train_years * 252); te = int(test_years * 252); out = []; picks = []
    a = tr
    while a < n:
        lo = 0 if anchored else a - tr; sc = X.iloc[lo:a].apply(lambda c: metric(c.values)); best = sc.idxmax(); seg = X[best].iloc[a:a + te]
        out.append(seg); picks.append(dict(start=seg.index[0], end=seg.index[-1], pick=best, train_metric=float(sc.max()), test_metric=float(metric(seg.values)) if len(seg) > 20 else np.nan)); a += te
    oos = pd.concat(out); full = X.loc[oos.index]; best_fixed = X.apply(lambda c: metric(c.values)).idxmax()
    return dict(oos=oos, picks=pd.DataFrame(picks), oos_metric=float(metric(oos.values)), best_fixed=best_fixed, best_fixed_metric_same_period=float(metric(full[best_fixed].values)),
                median_config_metric=float(full.apply(lambda c: metric(c.values)).median()), efficiency=float(metric(oos.values) / metric(full[best_fixed].values)))
