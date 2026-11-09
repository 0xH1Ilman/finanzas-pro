"""Señales de régimen. Todas devuelven un estado 0/1 por día (1 = fuera de la pata apalancada), calculado con datos hasta el cierre de ese día.
El motor aplica el retraso de ejecución; aquí nunca se desplaza."""
import numpy as np, pandas as pd
def hysteresis(v, exit_, enter):
    """Estado 1 cuando v supera `exit_`; vuelve a 0 cuando baja de `enter` (enter < exit_)."""
    v = np.asarray(v, float); st = np.zeros(len(v), np.int8); s = 0
    for i in range(len(v)):
        x = v[i]
        if x == x:
            if s == 0 and x > exit_: s = 1
            elif s == 1 and x < enter: s = 0
        st[i] = s
    return st
def realized_vol(r, window=20): return pd.Series(np.log1p(np.asarray(r, float))).rolling(window).std().values * np.sqrt(252)
def downside_vol(r, window=20): return np.sqrt(pd.Series(np.minimum(np.log1p(np.asarray(r, float)), 0) ** 2).rolling(window).mean().values * 252)
def ewma_vol(r, halflife=10): return np.sqrt(pd.Series(np.log1p(np.asarray(r, float)) ** 2).ewm(halflife=halflife).mean().values * 252)
def sma_gap(r, window=200):
    p = np.cumprod(1 + np.asarray(r, float)); return -(p / pd.Series(p).rolling(window).mean().values - 1)   # positivo = por debajo de la media
def drawdown_level(r, window=252):
    p = pd.Series(np.cumprod(1 + np.asarray(r, float))); return -(p / p.rolling(window, min_periods=1).max() - 1).values
MEASURES = {"vol": realized_vol, "downside": downside_vol, "ewma": ewma_vol, "sma": sma_gap, "drawdown": drawdown_level}
def make(panel, spec):
    """spec: {'type':'vol'|'downside'|'ewma'|'sma'|'drawdown','asset':'QQQ','window':20,'exit':0.35,'enter':0.25}
    Para 'sma': exit/enter son la distancia por debajo de la media (p. ej. 0.05 / -0.05)."""
    r = panel[spec.get("asset", "QQQ")].fillna(0).values; t = spec.get("type", "vol")
    kw = {"halflife": spec["window"]} if t == "ewma" else {"window": spec.get("window", 20)}
    return hysteresis(MEASURES[t](r, **kw), spec["exit"], spec["enter"])
def episodes(state, index):
    s = np.asarray(state).astype(int); ch = np.flatnonzero(np.diff(np.r_[0, s, 0]) != 0); return [(index[a], index[min(b, len(s)) - 1]) for a, b in zip(ch[0::2], ch[1::2])]
def placebo(state, rng, lo=0, hi=None):
    """Señal aleatoria con el mismo número de episodios y las mismas duraciones que `state` en [lo, hi)."""
    s = np.asarray(state); hi = len(s) if hi is None else hi; q = s[lo:hi].astype(int)
    ch = np.flatnonzero(np.diff(q) != 0) + 1; L = np.diff(np.r_[0, ch, len(q)])
    offs = L[0::2] if q[0] == 0 else L[1::2]; ons = L[1::2] if q[0] == 0 else L[0::2]
    out = np.zeros(len(s), np.int8)
    if len(ons) == 0: return out
    c = rng.permutation(ons); tot = offs.sum(); n = max(len(offs), 1)
    a = np.diff(np.r_[0, np.sort(rng.integers(0, tot + 1, n - 1)), tot]); p = lo
    for i in range(max(len(a), len(c))):
        if i < len(a): p += a[i]
        if i < len(c): out[p:p + c[i]] = 1; p += c[i]
    return out
