"""Opciones y futuros avanzados. Opciones: Black-Scholes-Merton y griegas vectorizadas, volatilidad implícita, estimadores de volatilidad realizada,
sonrisa SVI, SABR (Hagan), Heston (función característica), volatilidad local (Dupire), asimetría y estructura temporal, estrategias de varias patas
con griegas agregadas y simulación de cobertura delta. Futuros: series continuas, rendimiento de roll, contango/backwardation.
Regla: no se reconstruyen cadenas históricas ni superficies cuando no hay datos; estas funciones se alimentan de cotizaciones reales que aporte el usuario."""
import numpy as np, pandas as pd
from scipy.stats import norm
from scipy.optimize import brentq, minimize, least_squares
from scipy.integrate import quad
# ---------------- Black-Scholes-Merton
def bs(S, K, T, r, sigma, q=0.0, kind="call"):
    S, K, T, sigma = map(lambda x: np.asarray(x, float), (S, K, T, sigma)); sq = sigma * np.sqrt(T); d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / sq; d2 = d1 - sq
    c = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2); return c if kind == "call" else c - S * np.exp(-q * T) + K * np.exp(-r * T)
def greeks(S, K, T, r, sigma, q=0.0, kind="call"):
    """delta, gamma, vega (por 1 punto de vol = 0,01), theta (por día natural), rho (por 1 punto de tipo)."""
    sq = sigma * np.sqrt(T); d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / sq; d2 = d1 - sq; pdf = norm.pdf(d1); sg = 1 if kind == "call" else -1
    delta = sg * np.exp(-q * T) * norm.cdf(sg * d1); gamma = np.exp(-q * T) * pdf / (S * sq); vega = S * np.exp(-q * T) * pdf * np.sqrt(T) / 100
    theta = (-S * np.exp(-q * T) * pdf * sigma / (2 * np.sqrt(T)) - sg * r * K * np.exp(-r * T) * norm.cdf(sg * d2) + sg * q * S * np.exp(-q * T) * norm.cdf(sg * d1)) / 365
    rho = sg * K * T * np.exp(-r * T) * norm.cdf(sg * d2) / 100; return dict(delta=delta, gamma=gamma, vega=vega, theta=theta, rho=rho)
def implied_vol(price, S, K, T, r, q=0.0, kind="call"):
    f = lambda s: float(bs(S, K, T, r, s, q, kind)) - price
    try: return brentq(f, 1e-4, 6.0, xtol=1e-8)
    except ValueError: return np.nan
# ---------------- volatilidad realizada
def rv_close(close, window=20): return np.log(close).diff().rolling(window).std() * np.sqrt(252)
def rv_parkinson(high, low, window=20): return np.sqrt((np.log(high / low) ** 2).rolling(window).mean() / (4 * np.log(2)) * 252)
def rv_garman_klass(o, h, l, c, window=20): return np.sqrt((0.5 * np.log(h / l) ** 2 - (2 * np.log(2) - 1) * np.log(c / o) ** 2).rolling(window).mean() * 252)
def rv_yang_zhang(o, h, l, c, window=20):
    on = np.log(o / c.shift()); oc = np.log(c / o); rs = np.log(h / c) * np.log(h / o) + np.log(l / c) * np.log(l / o); k = 0.34 / (1.34 + (window + 1) / (window - 1))
    return np.sqrt((on.rolling(window).var() + k * oc.rolling(window).var() + (1 - k) * rs.rolling(window).mean()) * 252)
def variance_risk_premium(implied, realized_fwd): return implied ** 2 - realized_fwd ** 2
# ---------------- sonrisa y superficie
def svi(k, a, b, rho, m, s): return a + b * (rho * (k - m) + np.sqrt((k - m) ** 2 + s ** 2))     # varianza total w(k), k = ln(K/F)
def svi_fit(k, iv, T):
    """Ajusta SVI crudo a una fila de vencimiento. k = ln(K/F). Devuelve parámetros y error cuadrático medio en vol."""
    w = np.asarray(iv) ** 2 * T; k = np.asarray(k, float)
    res = least_squares(lambda p: svi(k, *p) - w, [w.min() * 0.9, 0.1, -0.5, 0.0, 0.1], bounds=([-1, 1e-6, -0.999, -2, 1e-4], [2, 5, 0.999, 2, 3]))
    return dict(zip(("a", "b", "rho", "m", "s"), res.x)), float(np.sqrt(np.mean((np.sqrt(np.maximum(svi(k, *res.x), 1e-12) / T) - iv) ** 2)))
def sabr_vol(F, K, T, alpha, beta, rho, nu):
    """Volatilidad implícita lognormal de SABR (fórmula de Hagan 2002)."""
    F, K = float(F), np.asarray(K, float); fk = (F * K) ** ((1 - beta) / 2); lg = np.log(F / K); z = nu / alpha * fk * lg; x = np.log((np.sqrt(1 - 2 * rho * z + z * z) + z - rho) / (1 - rho))
    zx = np.where(np.abs(z) < 1e-8, 1.0, z / np.where(np.abs(x) < 1e-12, 1.0, x)); den = fk * (1 + (1 - beta) ** 2 / 24 * lg ** 2 + (1 - beta) ** 4 / 1920 * lg ** 4)
    corr = 1 + ((1 - beta) ** 2 / 24 * alpha ** 2 / fk ** 2 + rho * beta * nu * alpha / (4 * fk) + (2 - 3 * rho ** 2) / 24 * nu ** 2) * T; return alpha / den * zx * corr
def sabr_fit(F, K, T, iv, beta=0.5):
    res = least_squares(lambda p: sabr_vol(F, K, T, p[0], beta, p[1], p[2]) - iv, [np.mean(iv) * F ** (1 - beta), -0.3, 0.5], bounds=([1e-4, -0.999, 1e-3], [10, 0.999, 10]))
    return dict(alpha=res.x[0], beta=beta, rho=res.x[1], nu=res.x[2], rmse=float(np.sqrt(np.mean(res.fun ** 2))))
def heston_call(S, K, T, r, v0, kappa, theta, sigma, rho, q=0.0):
    """Precio de una call europea en Heston por integración de la función característica (formulación estable)."""
    def cf(u, j):
        b = kappa - rho * sigma if j == 1 else kappa; uj = 0.5 if j == 1 else -0.5; d = np.sqrt((rho * sigma * 1j * u - b) ** 2 - sigma ** 2 * (2 * uj * 1j * u - u * u)); g = (b - rho * sigma * 1j * u - d) / (b - rho * sigma * 1j * u + d)
        C = (r - q) * 1j * u * T + kappa * theta / sigma ** 2 * ((b - rho * sigma * 1j * u - d) * T - 2 * np.log((1 - g * np.exp(-d * T)) / (1 - g))); D = (b - rho * sigma * 1j * u - d) / sigma ** 2 * (1 - np.exp(-d * T)) / (1 - g * np.exp(-d * T))
        return np.exp(C + D * v0 + 1j * u * np.log(S))
    P = [0.5 + quad(lambda u: (np.exp(-1j * u * np.log(K)) * cf(u, j) / (1j * u)).real, 1e-8, 200, limit=200)[0] / np.pi for j in (1, 2)]
    return S * np.exp(-q * T) * P[0] - K * np.exp(-r * T) * P[1]
def local_vol_dupire(strikes, maturities, iv, S, r=0.0, q=0.0):
    """Volatilidad local por Dupire a partir de una rejilla de volatilidades implícitas (maturities × strikes), con la fórmula de Gatheral en varianza total
    w = σ²T y log-moneyness y = ln(K/F): σ_loc² = ∂w/∂T / (1 − y/w·∂w/∂y + ¼(−¼ − 1/w + y²/w²)(∂w/∂y)² + ½·∂²w/∂y²). Exacta para una superficie plana."""
    K = np.asarray(strikes, float); T = np.asarray(maturities, float); iv = np.asarray(iv, float); w = iv ** 2 * T[:, None]; out = np.full_like(w, np.nan)
    dT = np.gradient(w, T, axis=0)
    for i, t in enumerate(T):
        y = np.log(K / (S * np.exp((r - q) * t))); dy = np.gradient(w[i], y); d2y = np.gradient(dy, y)
        den = 1 - y / w[i] * dy + 0.25 * (-0.25 - 1 / w[i] + y ** 2 / w[i] ** 2) * dy ** 2 + 0.5 * d2y
        out[i] = np.sqrt(np.where((den > 1e-8) & (dT[i] > 0), dT[i] / den, np.nan))
    return out
def skew_metrics(strikes, iv, S, T, r=0.0, q=0.0):
    """Asimetría 25-delta (put − call), riesgo de reversión y butterfly a partir de una sonrisa."""
    K = np.asarray(strikes, float); iv = np.asarray(iv, float); dc = np.array([greeks(S, k, T, r, v, q, "call")["delta"] for k, v in zip(K, iv)]); o = np.argsort(dc)
    f = lambda d: float(np.interp(d, dc[o], iv[o])); c25, p25, atm = f(0.25), f(0.75), f(0.50); return dict(atm=atm, rr25=c25 - p25, bf25=(c25 + p25) / 2 - atm, skew_put_minus_call=p25 - c25)
def term_structure(maturities, atm_iv):
    T = np.asarray(maturities, float); v = np.asarray(atm_iv, float); fwd = np.sqrt(np.maximum(np.diff(v ** 2 * T) / np.diff(T), 0)); return dict(slope=float(v[-1] - v[0]), forward_vols=fwd, contango=bool(v[-1] > v[0]))
# ---------------- estrategias de varias patas
def legs_value(legs, S, r=0.0, q=0.0, t_elapsed=0.0):
    """legs: lista de dicts {kind:'call'|'put'|'stock', K, T, sigma, qty, mult=100}. Valor y griegas agregadas para un precio S (escalar o array)."""
    S = np.asarray(S, float); val = np.zeros_like(S); G = dict(delta=np.zeros_like(S), gamma=np.zeros_like(S), vega=np.zeros_like(S), theta=np.zeros_like(S))
    for L in legs:
        m = L.get("mult", 100) * L["qty"]
        if L["kind"] == "stock": val += L["qty"] * S; G["delta"] += L["qty"]; continue
        T = max(L["T"] - t_elapsed, 1e-9); val += m * bs(S, L["K"], T, r, L["sigma"], q, L["kind"]); g = greeks(S, L["K"], T, r, L["sigma"], q, L["kind"])
        for k in G: G[k] += m * g[k]
    return val, G
def payoff_table(legs, spots, cost=None):
    """Resultado a vencimiento (todas las patas con el mismo vencimiento) para una rejilla de precios; cost = prima neta pagada (positiva) o cobrada (negativa)."""
    S = np.asarray(spots, float); pay = np.zeros_like(S)
    for L in legs:
        m = L.get("mult", 100) * L["qty"]; pay += L["qty"] * S if L["kind"] == "stock" else m * np.maximum((S - L["K"]) if L["kind"] == "call" else (L["K"] - S), 0)
    out = pd.DataFrame({"spot": S, "payoff": pay}); 
    if cost is not None:
        out["pnl"] = pay - cost; v = out["pnl"].values; be = [float(S[i]) for i in range(len(S)) if abs(v[i]) < 1e-9]
        be += [float(S[i] - v[i] * (S[i + 1] - S[i]) / (v[i + 1] - v[i])) for i in range(len(S) - 1) if v[i] * v[i + 1] < 0 and abs(v[i]) >= 1e-9 and abs(v[i + 1]) >= 1e-9]
        out.attrs["breakevens"] = sorted(be)
    return out
def delta_hedge_sim(prices, K, T, r, sigma_implied, kind="call", qty=-1, mult=100, rebalance_every=1, cost_bps=1.0):
    """Cobertura delta de una opción sobre una trayectoria real de precios diarios. P&L ≈ gamma·(vol realizada² − vol implícita²). Devuelve P&L final y serie."""
    S = np.asarray(prices, float); n = len(S); dt = 1 / 252; prem = float(bs(S[0], K, T, r, sigma_implied, 0, kind)) * mult * qty; cash = -prem; pos = 0.0; pnl = []
    for i in range(n):
        tau = max(T - i * dt, 1e-9)
        if i % rebalance_every == 0 and i < n - 1:
            tgt = -qty * mult * float(greeks(S[i], K, tau, r, sigma_implied, 0, kind)["delta"]); cash -= (tgt - pos) * S[i] + abs(tgt - pos) * S[i] * cost_bps / 1e4; pos = tgt
        cash *= np.exp(r * dt); opt = float(bs(S[i], K, tau, r, sigma_implied, 0, kind)) * mult * qty if i < n - 1 else mult * qty * max((S[i] - K) if kind == "call" else (K - S[i]), 0); pnl.append(cash + pos * S[i] + opt)
    return dict(final_pnl=pnl[-1], path=np.array(pnl), realized_vol=float(np.std(np.diff(np.log(S))) * np.sqrt(252)), implied_vol=sigma_implied)
# ---------------- futuros
def continuous_series(contracts, roll_days_before=5, method="ratio"):
    """Serie continua a partir de contratos individuales. contracts: dict {fecha_vencimiento: Serie de precios}. method 'ratio' (rentabilidades correctas)
    o 'panama' (diferencias). Devuelve la serie ajustada y las fechas de roll."""
    exps = sorted(contracts); idx = sorted(set().union(*[c.dropna().index for c in contracts.values()])); out = pd.Series(index=idx, dtype=float); rolls = []; cur = 0
    for d in idx:
        while cur < len(exps) - 1 and (pd.Timestamp(exps[cur]) - d).days <= roll_days_before and d in contracts[exps[cur + 1]].dropna().index: rolls.append((d, exps[cur], exps[cur + 1])); cur += 1
        out[d] = contracts[exps[cur]].get(d, np.nan)
    adj = out.copy()
    for d, a, b in reversed(rolls):
        pa, pb = contracts[a].get(d, np.nan), contracts[b].get(d, np.nan)
        if pa == pa and pb == pb:
            if method == "ratio": adj[adj.index < d] *= pb / pa
            else: adj[adj.index < d] += pb - pa
    return adj, rolls
def roll_yield(front, second, days_between=30):
    """Rendimiento de roll anualizado: positivo en backwardation (cercano > siguiente), negativo en contango."""
    return (front / second - 1) * 365 / days_between
def curve_state(prices_by_maturity):
    """prices_by_maturity: Serie indexada por vencimiento (ordenada). Devuelve pendiente y estado de la curva."""
    p = np.asarray(prices_by_maturity, float); return dict(state="contango" if p[-1] > p[0] else "backwardation", slope_pct=float(p[-1] / p[0] - 1), monotonic=bool(np.all(np.diff(p) > 0) or np.all(np.diff(p) < 0)))
def futures_excess_return(adjusted, raw_front): return adjusted.diff() / raw_front.shift().abs()
