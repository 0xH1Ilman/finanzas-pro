"""Detección de regímenes de mercado: umbrales de volatilidad y tendencia, modelo oculto de Markov gaussiano (EM propio, sin dependencias),
k-medias, componentes principales, cambios estructurales (CUSUM) y rendimiento de una estrategia condicionado al régimen.
Aviso de uso: un HMM ajustado con todo el historial mira al futuro. Para operar, usa `hmm_filter` (probabilidades filtradas) reajustando en ventanas expandidas."""
import numpy as np, pandas as pd
from scipy.special import logsumexp
def vol_trend_regimes(r, vol_window=20, vol_cut=0.25, trend_window=200):
    """Cuatro regímenes simples y sin ajuste: alcista/bajista (precio frente a su media) × calma/tensión (volatilidad realizada)."""
    p = (1 + r).cumprod(); up = p > p.rolling(trend_window).mean(); hv = r.rolling(vol_window).std() * 252 ** .5 > vol_cut
    return pd.Series(np.select([up & ~hv, up & hv, ~up & ~hv], ["alcista calma", "alcista tensión", "bajista calma"], "bajista tensión"), index=r.index)
def _gauss_logpdf(X, mu, var): return -0.5 * (np.log(2 * np.pi * var) + (X[:, None, :] - mu[None]) ** 2 / var[None]).sum(axis=2)
def hmm_fit(X, k=2, n_iter=200, tol=1e-6, seed=0):
    """HMM gaussiano con covarianza diagonal. X: array T×d (p. ej. rentabilidad diaria y |rentabilidad|). Devuelve parámetros, probabilidades suavizadas y camino más probable."""
    X = np.asarray(X, float); X = X[:, None] if X.ndim == 1 else X; T, d = X.shape; rng = np.random.default_rng(seed)
    q = np.argsort(np.argsort(np.abs(X[:, 0]))) * k // T; mu = np.array([X[q == i].mean(0) for i in range(k)]); var = np.array([X[q == i].var(0) + 1e-10 for i in range(k)])
    A = np.full((k, k), 0.02 / max(k - 1, 1)); np.fill_diagonal(A, 0.98); pi = np.full(k, 1 / k); ll_old = -np.inf
    for _ in range(n_iter):
        lb = _gauss_logpdf(X, mu, var); la = np.empty((T, k)); la[0] = np.log(pi) + lb[0]; lA = np.log(A)
        for t in range(1, T): la[t] = lb[t] + logsumexp(la[t - 1][:, None] + lA, axis=0)
        lbt = np.zeros((T, k))
        for t in range(T - 2, -1, -1): lbt[t] = logsumexp(lA + lb[t + 1][None] + lbt[t + 1][None], axis=1)
        ll = logsumexp(la[-1]); g = np.exp(la + lbt - ll); xi = np.exp(la[:-1, :, None] + lA[None] + lb[1:, None, :] + lbt[1:, None, :] - ll)
        pi = g[0] / g[0].sum(); A = xi.sum(0) / xi.sum(0).sum(1, keepdims=True); w = g.sum(0); mu = (g.T @ X) / w[:, None]; var = np.array([(g[:, i:i + 1] * (X - mu[i]) ** 2).sum(0) / w[i] + 1e-10 for i in range(k)])
        if abs(ll - ll_old) < tol * abs(ll): break
        ll_old = ll
    o = np.argsort(var[:, 0]); mu, var, A, pi, g = mu[o], var[o], A[np.ix_(o, o)], pi[o], g[:, o]     # estado 0 = menor varianza
    return dict(mu=mu, var=var, A=A, pi=pi, smoothed=g, path=g.argmax(1), loglik=float(ll), k=k, bic=float(-2 * ll + (k * k - 1 + 2 * k * d) * np.log(T)), expected_duration=1 / (1 - np.diag(A)))
def hmm_filter(X, model):
    """Probabilidades FILTRADAS (solo con información hasta cada día): las únicas válidas para decidir en tiempo real."""
    X = np.asarray(X, float); X = X[:, None] if X.ndim == 1 else X; lb = _gauss_logpdf(X, model["mu"], model["var"]); T, k = lb.shape; out = np.empty((T, k)); a = model["pi"]
    for t in range(T):
        a = a * np.exp(lb[t] - lb[t].max()); a /= a.sum(); out[t] = a; a = a @ model["A"]
    return out
def hmm_walkforward(X, k=2, min_train=1260, refit=252):
    """Estado más probable de cada día usando solo datos anteriores: reajusta el modelo cada `refit` días con ventana expandida."""
    X = np.asarray(X, float); X = X[:, None] if X.ndim == 1 else X; out = np.full(len(X), np.nan)
    for a in range(min_train, len(X), refit):
        m = hmm_fit(X[:a], k); out[a:a + refit] = hmm_filter(X[:a + refit], m)[a:a + refit].argmax(1)
    return out
def kmeans(X, k=3, n_iter=100, seed=0, n_init=10):
    """k-medias sobre variables estandarizadas, con varios arranques (se queda con el de menor inercia). Devuelve etiquetas y centros."""
    X = np.asarray(X, float); Z = (X - X.mean(0)) / X.std(0); rng = np.random.default_rng(seed); best = None
    for _ in range(n_init):
        c = Z[rng.choice(len(Z), k, replace=False)]
        for _ in range(n_iter):
            lab = ((Z[:, None, :] - c[None]) ** 2).sum(2).argmin(1); c2 = np.array([Z[lab == i].mean(0) if (lab == i).any() else c[i] for i in range(k)])
            if np.allclose(c, c2): break
            c = c2
        inertia = ((Z - c[lab]) ** 2).sum()
        if best is None or inertia < best[0]: best = (inertia, lab, c)
    return best[1], best[2]
def pca(returns, n=3):
    """Componentes principales de la matriz de correlaciones: varianza explicada y cargas. La parte del primer componente mide el riesgo sistémico."""
    Z = (returns - returns.mean()) / returns.std(); C = np.corrcoef(Z.dropna().values.T); val, vec = np.linalg.eigh(C); o = np.argsort(val)[::-1]
    return dict(explained=val[o][:n] / val.sum(), loadings=pd.DataFrame(vec[:, o][:, :n], index=returns.columns, columns=[f"PC{i+1}" for i in range(n)]))
def absorption_ratio(returns, window=252, n=1, step=21):
    """Fracción de la varianza explicada por los `n` primeros componentes, móvil. Sube cuando los mercados se acoplan (fragilidad)."""
    out = {}
    for e in range(window, len(returns) + 1, step): out[returns.index[e - 1]] = pca(returns.iloc[e - window:e], n)["explained"].sum()
    return pd.Series(out)
def cusum_breaks(x, threshold=5.0):
    """Cambios estructurales en la media por CUSUM estandarizado: devuelve las posiciones donde la suma acumulada supera `threshold` desviaciones y reinicia."""
    x = np.asarray(x, float); z = (x - np.nanmean(x)) / np.nanstd(x); s_hi = s_lo = 0.0; br = []
    for i, v in enumerate(z):
        s_hi = max(0, s_hi + v - 0.5); s_lo = min(0, s_lo + v + 0.5)
        if s_hi > threshold or s_lo < -threshold: br.append(i); s_hi = s_lo = 0.0
    return br
def conditional_performance(strategy_returns, regime, rf=None, periods=252):
    """Rendimiento de una o varias estrategias por régimen (la etiqueta de régimen se desplaza un día: se conoce al cierre anterior)."""
    R = strategy_returns.to_frame("strategy") if isinstance(strategy_returns, pd.Series) else strategy_returns; g = pd.Series(regime, index=R.index).shift(1); rows = []
    for lab, ix in g.dropna().groupby(g.dropna()).groups.items():
        for c in R.columns:
            x = R.loc[ix, c].dropna(); rows.append(dict(regime=lab, strategy=c, days=len(x), share=len(x) / len(R), ann_return=float(x.mean() * periods), ann_vol=float(x.std() * periods ** .5), sharpe=float((x - (rf.loc[x.index] if rf is not None else 0)).mean() / x.std() * periods ** .5), worst_day=float(x.min())))
    return pd.DataFrame(rows)
def garch11(r, n_iter=300):
    """GARCH(1,1) por máxima verosimilitud (scipy). Devuelve parámetros, volatilidad condicional anualizada y previsión a un día."""
    from scipy.optimize import minimize
    x = np.asarray(r, float) * 100; x = x - x.mean(); v0 = x.var()      # en % para que el optimizador esté bien escalado
    def nll(p):
        w, a, b = p; h = np.empty(len(x)); h[0] = v0
        for t in range(1, len(x)): h[t] = w + a * x[t - 1] ** 2 + b * h[t - 1]
        return 0.5 * (np.log(h) + x ** 2 / h).sum()
    res = minimize(nll, [v0 * 0.05, 0.08, 0.90], bounds=[(1e-12, None), (1e-6, 0.5), (0.3, 0.9999)], constraints=[{"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[2]}], method="SLSQP", options={"maxiter": n_iter})
    w, a, b = res.x; h = np.empty(len(x)); h[0] = v0
    for t in range(1, len(x)): h[t] = w + a * x[t - 1] ** 2 + b * h[t - 1]
    return dict(omega=float(w / 1e4), alpha=float(a), beta=float(b), persistence=float(a + b), cond_vol=np.sqrt(h * 252) / 100, forecast_vol=float(np.sqrt((w + a * x[-1] ** 2 + b * h[-1]) * 252) / 100), long_run_vol=float(np.sqrt(w / max(1 - a - b, 1e-9) * 252) / 100))
