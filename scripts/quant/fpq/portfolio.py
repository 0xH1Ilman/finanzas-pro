"""Construcción de carteras: contribución al riesgo, paridad y presupuesto de riesgo, HRP, mínima varianza, máximo Sharpe con restricciones,
objetivo de volatilidad, asignación entre estrategias y rebalanceo por bandas con costes. Solo numpy/scipy."""
import numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform
def cov(returns, periods=252, shrink=None):
    """Covarianza anualizada. shrink en [0,1]: contracción hacia la diagonal (útil con pocas observaciones)."""
    S = returns.cov().values * periods
    if shrink: S = (1 - shrink) * S + shrink * np.diag(np.diag(S))
    return S
def port_vol(w, S): return float(np.sqrt(w @ S @ w))
def risk_contribution(w, S):
    """Contribución marginal y total al riesgo. Las contribuciones porcentuales suman 1."""
    w = np.asarray(w, float); v = port_vol(w, S); mrc = S @ w / v; rc = w * mrc; return dict(marginal=mrc, contribution=rc, pct=rc / v, vol=v)
def diversification(w, S):
    """Ratio de diversificación y retorno de diversificación ≈ ½(Σ wᵢσᵢ² − σₚ²) (cosecha de volatilidad por rebalanceo)."""
    w = np.asarray(w, float); sd = np.sqrt(np.diag(S)); return dict(ratio=float(w @ sd / port_vol(w, S)), diversification_return=float(0.5 * (w @ np.diag(S) - w @ S @ w)))
def _solve(obj, n, bounds=None, cons=None, w0=None):
    bounds = bounds or [(0, 1)] * n; cons = [{"type": "eq", "fun": lambda w: w.sum() - 1}] + (cons or [])
    r = minimize(obj, w0 if w0 is not None else np.full(n, 1 / n), method="SLSQP", bounds=bounds, constraints=cons, options={"maxiter": 500, "ftol": 1e-12}); return r.x
def min_variance(S, bounds=None): return _solve(lambda w: w @ S @ w, len(S), bounds)
def max_sharpe(mu, S, rf=0.0, bounds=None, cons=None): return _solve(lambda w: -(w @ mu - rf) / np.sqrt(w @ S @ w), len(S), bounds, cons)
def risk_budget(S, budget=None, bounds=None):
    """Pesos cuya contribución al riesgo es proporcional a `budget` (por defecto igual para todos = paridad de riesgo)."""
    n = len(S); b = np.full(n, 1 / n) if budget is None else np.asarray(budget, float) / np.sum(budget)
    def obj(w): rc = w * (S @ w); return float(((rc / rc.sum() - b) ** 2).sum())
    return _solve(obj, n, bounds or [(1e-6, 1)] * n, w0=(1 / np.sqrt(np.diag(S))) / (1 / np.sqrt(np.diag(S))).sum())
def hrp(returns):
    """Hierarchical Risk Parity (López de Prado): agrupa por correlación y reparte por varianza inversa de forma recursiva."""
    C = returns.corr().values; S = returns.cov().values; d = np.sqrt(np.clip((1 - C) / 2, 0, 1)); np.fill_diagonal(d, 0)
    order = list(leaves_list(linkage(squareform(d, checks=False), "single"))); w = pd.Series(1.0, index=order); cl = [order]
    def cvar(ix): iv = 1 / np.diag(S[np.ix_(ix, ix)]); iv /= iv.sum(); return iv @ S[np.ix_(ix, ix)] @ iv
    while cl:
        cl = [c[j:k] for c in cl for j, k in ((0, len(c) // 2), (len(c) // 2, len(c))) if len(c) > 1]
        for i in range(0, len(cl), 2):
            a, b = cl[i], cl[i + 1]; va, vb = cvar(a), cvar(b); al = 1 - va / (va + vb); w[a] *= al; w[b] *= 1 - al
    return w.sort_index().values
def mean_variance_costs(mu, S, w_prev, tc, risk_aversion=3.0, bounds=None):
    """Media-varianza penalizando la rotación desde la cartera actual: max w'μ − λ/2 w'Σw − tc·|w − w_prev|."""
    return _solve(lambda w: -(w @ mu) + risk_aversion / 2 * (w @ S @ w) + tc * np.abs(w - w_prev).sum(), len(S), bounds, w0=np.asarray(w_prev, float))
def vol_target_leverage(returns, target=0.10, window=60, max_leverage=2.0):
    return (target / (returns.rolling(window).std() * 252 ** .5)).clip(upper=max_leverage).shift(1)
def allocate_strategies(strategy_returns, method="risk_parity", **kw):
    """Asignación entre estrategias (columnas = estrategias): 'equal', 'inverse_vol', 'risk_parity', 'hrp', 'min_variance', 'max_sharpe'."""
    R = strategy_returns.dropna(); S = cov(R, shrink=kw.get("shrink")); n = R.shape[1]
    w = {"equal": lambda: np.full(n, 1 / n), "inverse_vol": lambda: (1 / np.sqrt(np.diag(S))) / (1 / np.sqrt(np.diag(S))).sum(), "risk_parity": lambda: risk_budget(S),
         "hrp": lambda: hrp(R), "min_variance": lambda: min_variance(S), "max_sharpe": lambda: max_sharpe(R.mean().values * 252, S, kw.get("rf", 0.0))}[method]()
    return pd.Series(w, index=R.columns)
def band_policy_cost(returns, weights, bands=(0.0, 0.02, 0.05, 0.10, 0.20), tc=0.001):
    """Compara bandas de rebalanceo (desviación absoluta) con costes: rentabilidad, volatilidad, rotación y nº de rebalanceos."""
    R = returns.dropna().values; w0 = np.asarray(weights, float); rows = []
    for b in bands:
        w = w0.copy(); eq = 1.0; tr = 0.0; nreb = 0; rets = []
        for t in range(len(R)):
            g = 1 + R[t]; pr = float(w @ g); w = w * g / pr; c = 0.0
            if np.abs(w - w0).max() > b: d = np.abs(w0 - w).sum(); c = tc * d; tr += d / 2; nreb += 1; w = w0.copy()
            rets.append(pr * (1 - c) - 1)
        rets = np.array(rets); rows.append(dict(band=b, CAGR=float(np.prod(1 + rets) ** (252 / len(rets)) - 1), Vol=float(rets.std() * 252 ** .5), turnover_annual=tr / (len(R) / 252), rebalances=nreb))
    return pd.DataFrame(rows)
