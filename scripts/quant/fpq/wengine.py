"""Motor de pesos variables: cualquier estrategia expresada como matriz de pesos objetivo por día (long-only, long-short, momentum,
reversión, tendencia, asignación dinámica, futuros). Los pesos de la fila t se deciden con información hasta el cierre de t y se aplican
desde el cierre de t+lag (lag ≥ 1 evita mirar al futuro). Incluye comisiones, horquilla, deslizamiento, impacto de mercado y financiación."""
import numpy as np, pandas as pd
from . import metrics as M
def backtest(returns, weights, rf=None, lag=1, rebalance="D", commission=0.0, spread=0.0, slippage=0.0, borrow_spread=0.005, short_fee=0.003,
             impact_k=0.0, adv=None, capital=1e6, max_participation=None, tol=0.0):
    """returns: DataFrame de rentabilidades diarias. weights: DataFrame de pesos objetivo (pueden ser negativos; el resto es efectivo).
    rebalance: 'D','W','M','Q' o lista de fechas. Costes por unidad negociada: commission + spread/2 + slippage (+ impacto = impact_k·sqrt(participación)).
    Financiación: el apalancamiento (suma de largos > 1) paga rf+borrow_spread; los cortos pagan short_fee y cobran rf sobre el efectivo.
    adv: DataFrame de volumen medio diario en dinero; max_participation limita lo negociado por día (ejecución parcial).
    Devuelve dict con returns, weights (reales), turnover, costs y métricas."""
    R = returns.fillna(0.0); idx = R.index; cols = list(R.columns)
    Wt = weights.reindex(idx).reindex(columns=cols).shift(lag); rfv = (rf.reindex(idx).fillna(0.0).values if rf is not None else np.zeros(len(idx)))
    if isinstance(rebalance, str):
        g = {"D": idx, "W": idx.to_series().groupby(idx.to_period("W")).last(), "M": idx.to_series().groupby(idx.to_period("M")).last(), "Q": idx.to_series().groupby(idx.to_period("Q")).last()}[rebalance]
        rb = idx.isin(pd.DatetimeIndex(g))
    else: rb = idx.isin(pd.DatetimeIndex(rebalance))
    Rv = R.values; Wv = Wt.values; T, N = Rv.shape; w = np.zeros(N); out = np.zeros(T); tv = np.zeros(T); cs = np.zeros(T); Wreal = np.zeros((T, N)); unit = commission + spread / 2 + slippage
    advv = adv.reindex(idx).reindex(columns=cols).values if adv is not None else None; eq = 1.0
    for t in range(T):
        gross_long = w[w > 0].sum(); short = -w[w < 0].sum(); cash = 1 - w.sum()
        fin = cash * rfv[t] if cash >= 0 else cash * (rfv[t] + borrow_spread / 252)
        fin -= short * short_fee / 252
        pr = float(w @ Rv[t]) + fin
        w = w * (1 + Rv[t]); tot = 1 + pr; w = w / tot if tot > 0 else w * 0
        cost = 0.0
        if rb[t] and not np.isnan(Wv[t]).all():
            tg = np.nan_to_num(Wv[t]); d = tg - w
            if tol > 0: d[np.abs(d) < tol] = 0
            if advv is not None and max_participation:
                cap = max_participation * np.nan_to_num(advv[t]) / (capital * eq); d = np.clip(d, -cap, cap)
            tr = np.abs(d).sum(); cost = tr * unit
            if impact_k > 0 and advv is not None:
                part = np.abs(d) * capital * eq / np.where(advv[t] > 0, advv[t], np.inf); cost += float((np.abs(d) * impact_k * np.sqrt(part)).sum())
            w = w + d; tv[t] = tr / 2; cs[t] = cost
        out[t] = (1 + pr) * (1 - cost) - 1; eq *= 1 + out[t]; Wreal[t] = w
    r = pd.Series(out, index=idx); m = M.summary(out, rfv)
    m.update(turnover_annual=float(tv.sum() / (T / 252)), cost_annual=float(cs.sum() / (T / 252)), avg_gross=float(np.abs(Wreal).sum(1).mean()), avg_net=float(Wreal.sum(1).mean()))
    return dict(returns=r, weights=pd.DataFrame(Wreal, index=idx, columns=cols), turnover=pd.Series(tv, index=idx), costs=pd.Series(cs, index=idx), metrics=m)
# ---- constructores de pesos habituales (todos usan solo información hasta t)
def w_momentum(returns, lookback=252, skip=21, top=None, long_short=False):
    """Momentum transversal: rentabilidad de `lookback` días saltando los últimos `skip`. top = nº de activos largos (y cortos si long_short)."""
    lr = np.log1p(returns); mom = lr.rolling(lookback).sum().shift(skip); n = returns.shape[1]; top = top or max(n // 3, 1)
    rk = mom.rank(axis=1, ascending=False); w = (rk <= top).astype(float) / top
    if long_short: w -= (rk > n - top).astype(float) / top
    return w.where(mom.notna().sum(axis=1) >= top, np.nan)
def w_trend(returns, lookback=250, vol_window=60, target_vol=0.10, long_short=True):
    """Tendencia por activo (signo del precio frente a su media) con riesgo igual por activo y objetivo de volatilidad."""
    p = (1 + returns).cumprod(); sig = np.sign(p - p.rolling(lookback).mean()); v = returns.rolling(vol_window).std() * 252 ** .5
    if not long_short: sig = sig.clip(lower=0)
    return (sig * (target_vol / v) / returns.shape[1]).replace([np.inf, -np.inf], np.nan)
def w_meanrev(returns, lookback=5, top=None):
    """Reversión a la media transversal de corto plazo: largo en los que más han caído, corto en los que más han subido."""
    z = -returns.rolling(lookback).sum(); z = z.sub(z.mean(axis=1), axis=0); return z.div(z.abs().sum(axis=1), axis=0)
def w_voltarget(returns, base_weights, target_vol=0.10, window=60, max_leverage=2.0):
    """Escala una cartera base para apuntar a una volatilidad objetivo (con tope de apalancamiento)."""
    pr = (returns * pd.Series(base_weights)).sum(axis=1); lev = (target_vol / (pr.rolling(window).std() * 252 ** .5)).clip(upper=max_leverage)
    return pd.DataFrame(np.outer(lev.values, pd.Series(base_weights).reindex(returns.columns).fillna(0).values), index=returns.index, columns=returns.columns)
def w_inverse_vol(returns, window=60):
    iv = 1 / (returns.rolling(window).std()); return iv.div(iv.sum(axis=1), axis=0)
def letf(index_ret, leverage, rate_annual, expense=0.0095, spread=0.004):
    """Rentabilidad diaria de un ETF apalancado o inverso de reajuste diario: L·r − (L−1)·(tipo+diferencial)/252 − comisión/252."""
    return leverage * index_ret - (leverage - 1) * (rate_annual + spread) / 252 - expense / 252
