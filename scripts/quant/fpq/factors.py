"""Investigación factorial: exposiciones (fijas y móviles), construcción de factores por ordenación transversal, momentum y timing de factores,
diversificación entre factores, hacinamiento (crowding) y estabilidad. Factores estándar: mercado, tamaño, valor, momentum, calidad/rentabilidad,
inversión, baja volatilidad, carry, tendencia, liquidez (los cuatro últimos se construyen aquí a partir de precios)."""
import numpy as np, pandas as pd
from . import attribution
def exposures(r, factors, rf=None): return attribution.factor_attribution(r, factors, rf)
def rolling_exposures(r, factors, rf=None, window=252, step=21):
    """Betas móviles (ventana en días). Sirve para ver deriva de estilo y exposiciones que cambian con el régimen."""
    y = (r - (rf if rf is not None else 0)); X = factors.reindex(y.index); ok = y.notna() & X.notna().all(axis=1); y = y[ok]; X = X[ok]; rows = {}
    for e in range(window, len(y) + 1, step):
        A = np.column_stack([np.ones(window), X.values[e - window:e]]); b = np.linalg.lstsq(A, y.values[e - window:e], rcond=None)[0]; rows[y.index[e - 1]] = np.r_[b[0] * 252, b[1:]]
    return pd.DataFrame(rows, index=["alpha_annual"] + list(X.columns)).T
def sort_portfolios(returns, characteristic, n=5, lag=1, rebalance="M", long_short=True):
    """Construye un factor por ordenación: cada periodo ordena los activos por `characteristic` (DataFrame fecha × activo, conocida en esa fecha),
    forma `n` grupos equiponderados y devuelve sus rentabilidades y la del factor (grupo alto − grupo bajo)."""
    ends = returns.index.to_series().groupby(returns.index.to_period(rebalance)).last(); ch = characteristic.reindex(returns.index).ffill().shift(lag)
    grp = pd.DataFrame(np.nan, index=returns.index, columns=returns.columns)
    for d in ends:
        x = ch.loc[d].dropna()
        if len(x) >= n: grp.loc[d, x.index] = pd.qcut(x.rank(method="first"), n, labels=False).values
    grp = grp.ffill().shift(1); out = pd.DataFrame({f"Q{k+1}": returns.where(grp == k).mean(axis=1) for k in range(n)})
    if long_short: out["factor"] = out[f"Q{n}"] - out["Q1"]
    return out
def build_price_factors(returns, rf=None, vol_window=126, mom=(252, 21), trend_window=250):
    """Factores a partir de precios para cualquier universo: momentum (12-1), baja volatilidad, reversión a corto, tendencia (serie temporal)."""
    lr = np.log1p(returns); out = pd.DataFrame(index=returns.index)
    out["MOM"] = sort_portfolios(returns, lr.rolling(mom[0]).sum().shift(mom[1]), n=3)["factor"]
    out["LOWVOL"] = sort_portfolios(returns, -returns.rolling(vol_window).std(), n=3)["factor"]
    out["STREV"] = sort_portfolios(returns, -lr.rolling(21).sum(), n=3)["factor"]
    p = (1 + returns).cumprod(); sig = np.sign(p - p.rolling(trend_window).mean()).shift(1); v = returns.rolling(60).std().shift(1) * 252 ** .5
    out["TREND"] = (sig * returns * (0.10 / v)).mean(axis=1)
    return out
def carry_factor(front, second, days_between=63):
    """Carry de futuros: rendimiento anualizado de la curva (precio cercano / siguiente − 1). DataFrames fecha × mercado."""
    return (front / second - 1) * 252 / days_between
def factor_momentum(factors, lookback=252, skip=0):
    """Momentum de factores: sobrepondera los factores con mejor rentabilidad pasada (signo de su rentabilidad de `lookback` días)."""
    s = np.sign(np.log1p(factors).rolling(lookback).sum().shift(1 + skip)); return (s * factors).mean(axis=1)
def factor_timing_test(factor, signal, lag=1):
    """¿Predice `signal` la rentabilidad del factor? Regresión de la rentabilidad mensual del factor sobre la señal del mes anterior."""
    m = (1 + factor).groupby(factor.index.to_period("M")).prod() - 1; s = signal.groupby(signal.index.to_period("M")).last().shift(lag); d = pd.concat([m, s], axis=1).dropna(); d.columns = ["y", "x"]
    b = np.polyfit(d.x, d.y, 1); res = d.y - np.polyval(b, d.x); se = np.sqrt(res.var(ddof=2) / ((d.x - d.x.mean()) ** 2).sum()); return dict(beta=float(b[0]), t=float(b[0] / se), n=len(d), corr=float(d.corr().iloc[0, 1]))
def diversification_table(factors, periods=252):
    c = factors.corr(); s = factors.mean() / factors.std() * np.sqrt(periods); return dict(sharpe=s, corr=c, avg_corr=float((c.values.sum() - len(c)) / (len(c) ** 2 - len(c))))
def crowding(returns, groups, window=63):
    """Indicador de hacinamiento: correlación media por pares dentro de cada grupo de activos (dict grupo → lista de columnas). Valores altos = factor concurrido."""
    out = {}
    for g, cols in groups.items():
        c = returns[cols].rolling(window).corr(); n = len(cols); out[g] = (c.groupby(level=0).sum().sum(axis=1) - n) / (n * n - n)
    return pd.DataFrame(out)
def stability(r, factors, rf=None, splits=4):
    """Estabilidad de exposiciones y alfa por subperiodos iguales."""
    idx = np.array_split(r.dropna().index, splits); rows = {}
    for ix in idx:
        a = attribution.factor_attribution(r.loc[ix], factors, rf); rows[f"{ix[0].date()}→{ix[-1].date()}"] = {"alpha_annual": a["alpha_annual"], "alpha_t": a["alpha_t"], **a["betas"].to_dict(), "r2": a["r2"]}
    return pd.DataFrame(rows).T
