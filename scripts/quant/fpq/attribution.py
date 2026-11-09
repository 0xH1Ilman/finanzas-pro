"""Atribución: de dónde viene la rentabilidad y el riesgo. Contribución por activo, Brinson (asignación / selección / interacción),
atribución factorial por regresión, por periodos, por estrategias, coste de las reglas y comparación con benchmark."""
import numpy as np, pandas as pd
def contribution_to_return(weights, returns):
    """Contribución de cada activo a la rentabilidad total (pesos reales al inicio de cada día). Encadenada para que la suma coincida con la rentabilidad compuesta."""
    W = weights.shift(1).fillna(weights.iloc[0]); c = W * returns.reindex(W.index)[W.columns]; pr = c.sum(axis=1); k = (1 + pr).cumprod().shift(1).fillna(1.0)
    tot = c.mul(k, axis=0).sum(); return dict(by_asset=tot, total=float((1 + pr).prod() - 1), check=float(tot.sum()))
def contribution_to_risk(weights, returns, periods=252):
    """Contribución media de cada activo a la varianza de la cartera (con los pesos medios)."""
    w = weights.mean().values; S = returns[weights.columns].cov().values * periods; v = w @ S @ w; rc = w * (S @ w) / v; return pd.Series(rc, index=weights.columns)
def brinson(wp, wb, rp, rb):
    """Brinson-Fachler de un periodo. wp/wb: pesos de cartera/benchmark por segmento; rp/rb: rentabilidades por segmento.
    Devuelve asignación, selección e interacción por segmento; su suma es el exceso de rentabilidad."""
    wp, wb, rp, rb = (pd.Series(x, dtype=float) for x in (wp, wb, rp, rb)); RB = float((wb * rb).sum())
    d = pd.DataFrame({"allocation": (wp - wb) * (rb - RB), "selection": wb * (rp - rb), "interaction": (wp - wb) * (rp - rb)}); d["total"] = d.sum(axis=1)
    return d, dict(excess=float((wp * rp).sum() - RB), explained=float(d["total"].sum()))
def brinson_multi(wp, wb, rp, rb):
    """Brinson encadenado en varios periodos (DataFrames periodo × segmento) con suavizado de Cariño para que los efectos sumen el exceso compuesto."""
    Rp = (wp * rp).sum(axis=1); Rb = (wb * rb).sum(axis=1); P, B = (1 + Rp).prod() - 1, (1 + Rb).prod() - 1
    kt = np.where(np.isclose(Rp, Rb), 1 / (1 + Rp), (np.log1p(Rp) - np.log1p(Rb)) / (Rp - Rb)); k = (np.log1p(P) - np.log1p(B)) / (P - B) if not np.isclose(P, B) else 1 / (1 + P)
    A = ((wp - wb) * rb.sub(Rb, axis=0)).mul(kt / k, axis=0).sum(); S = (wb * (rp - rb)).mul(kt / k, axis=0).sum(); I = ((wp - wb) * (rp - rb)).mul(kt / k, axis=0).sum()
    d = pd.DataFrame({"allocation": A, "selection": S, "interaction": I}); d["total"] = d.sum(axis=1); return d, dict(excess=float(P - B), explained=float(d["total"].sum()))
def factor_attribution(r, factors, rf=None, periods=252):
    """Regresión de la rentabilidad en exceso sobre factores: alfa anual, betas, t-estadísticos, R² y parte de la rentabilidad explicada por cada factor."""
    y = (r - (rf if rf is not None else 0)).dropna(); X = factors.reindex(y.index).dropna(); y = y.reindex(X.index); A = np.column_stack([np.ones(len(X)), X.values])
    b, *_ = np.linalg.lstsq(A, y.values, rcond=None); res = y.values - A @ b; s2 = res @ res / (len(y) - A.shape[1]); se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
    contrib = pd.Series(b[1:] * X.mean().values * periods, index=X.columns)
    return dict(alpha_annual=float(b[0] * periods), alpha_t=float(b[0] / se[0]), betas=pd.Series(b[1:], index=X.columns), t=pd.Series(b[1:] / se[1:], index=X.columns),
                r2=float(1 - res.var() / y.values.var()), contribution_annual=contrib, unexplained_annual=float(b[0] * periods), total_excess_annual=float(y.mean() * periods))
def by_period(r, bench=None, freq="Y"):
    g = (1 + r).groupby(r.index.to_period(freq)).prod() - 1; out = g.to_frame("portfolio")
    if bench is not None: out["benchmark"] = (1 + bench.reindex(r.index)).groupby(r.index.to_period(freq)).prod() - 1; out["excess"] = out["portfolio"] - out["benchmark"]
    return out
def rule_value(results):
    """Valor de cada regla: diferencia de métricas entre variantes de una misma cartera. results: {'nombre': dict de métricas}; la primera es la referencia."""
    names = list(results); base = results[names[0]]; return pd.DataFrame({n: {k: results[n][k] - base[k] for k in ("CAGR", "Sharpe", "MDD", "Vol")} for n in names[1:]})
def cost_drag(result):
    """Arrastre anual de costes e impuestos de un Result del motor de reglas."""
    y = len(result.returns) / 252; return dict(costs_annual=result.stats["costs"] / y, taxes_annual=result.stats["taxes"] / y, turnover_annual=result.stats["turnover"] / y)
