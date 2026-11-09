"""Métricas de rendimiento y riesgo. Todo sobre rentabilidades diarias simples (pd.Series o np.array)."""
import numpy as np, pandas as pd
P = 252
def _a(x): return np.asarray(x, dtype=float)
def equity(r, start=1.0): return start * np.cumprod(1 + _a(r))
def cagr(r, periods=P):
    r = _a(r); return float(np.prod(1 + r) ** (periods / len(r)) - 1)
def vol(r, periods=P): return float(np.std(_a(r), ddof=1) * np.sqrt(periods))
def sharpe(r, rf=0.0, periods=P):
    ex = _a(r) - _a(rf); s = np.std(_a(r), ddof=1); return float(ex.mean() / s * np.sqrt(periods)) if s > 0 else np.nan
def downside_dev(r, rf=0.0, periods=P):
    ex = _a(r) - _a(rf); return float(np.sqrt(np.mean(np.minimum(ex, 0) ** 2) * periods))
def sortino(r, rf=0.0, periods=P):
    d = downside_dev(r, rf, periods); return float((_a(r) - _a(rf)).mean() * periods / d) if d > 0 else np.nan
def drawdown(r):
    e = np.r_[1.0, equity(r)]; return (e / np.maximum.accumulate(e) - 1)[1:]
def max_drawdown(r): return float(drawdown(r).min())
def ulcer(r): return float(np.sqrt(np.mean(drawdown(r) ** 2)) * 100)
def upi(r, rf=0.0, periods=P):
    u = ulcer(r) / 100; return float((cagr(r, periods) - cagr(np.broadcast_to(_a(rf), _a(r).shape), periods)) / u) if u > 0 else np.nan
def calmar(r, periods=P):
    m = max_drawdown(r); return float(cagr(r, periods) / abs(m)) if m < 0 else np.nan
def longest_underwater(r, periods=P):
    d = drawdown(r) < 0; best = cur = 0
    for x in d:
        cur = cur + 1 if x else 0; best = max(best, cur)
    return best / periods
def var_cvar(r, q=0.05):
    r = _a(r); v = np.quantile(r, q); return float(v), float(r[r <= v].mean())
def beta_alpha(r, bench, rf=0.0, periods=P):
    x = _a(bench) - _a(rf); y = _a(r) - _a(rf); b = np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1)
    return float(b), float((y.mean() - b * x.mean()) * periods), float(np.corrcoef(y, x)[0, 1])
def summary(r, rf=0.0, bench=None, periods=P):
    r = _a(r); rf_ = np.broadcast_to(_a(rf), r.shape)
    out = dict(CAGR=cagr(r, periods), Vol=vol(r, periods), Sharpe=sharpe(r, rf_, periods), Sortino=sortino(r, rf_, periods),
               MDD=max_drawdown(r), Calmar=calmar(r, periods), Ulcer=ulcer(r), UPI=upi(r, rf_, periods),
               Underwater_y=longest_underwater(r, periods), Worst_day=float(r.min()), Skew=float(pd.Series(r).skew()),
               Kurt=float(pd.Series(r).kurt()), Final=float(np.prod(1 + r)), N=len(r))
    out["VaR5"], out["CVaR5"] = var_cvar(r)
    if bench is not None: out["Beta"], out["Alpha"], out["Corr"] = beta_alpha(r, bench, rf_, periods)
    return out
def yearly(r: pd.Series): return (1 + r).groupby(r.index.year).prod() - 1
def monthly(r: pd.Series): return (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
def rolling_cagr(r: pd.Series, window_days):
    lr = np.log1p(r); return np.expm1(lr.rolling(window_days).sum() * P / window_days)
def worst_periods(r: pd.Series, days=(1, 2, 5, 21)):
    e = (1 + r).cumprod(); return {d: (e.pct_change(d).idxmin(), float(e.pct_change(d).min())) for d in days}
def fmt(m): return f"CAGR {m['CAGR']*100:.2f}% | vol {m['Vol']*100:.1f}% | Sharpe {m['Sharpe']:.2f} | Sortino {m['Sortino']:.2f} | MDD {m['MDD']*100:.1f}% | UPI {m['UPI']:.2f}"
