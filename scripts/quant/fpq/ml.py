"""Machine learning aplicado con disciplina temporal (scikit-learn). Reglas que este módulo impone:
1) la validación respeta el orden temporal y purga el solape de etiquetas (purged K-fold con embargo);
2) todo modelo se compara con alternativas sencillas (regla ingenua y regresión logística); si no las mejora después de costes, se descarta;
3) las variables solo usan información disponible al cierre de t; la etiqueta mira de t+1 a t+h.
SHAP, XGBoost y LightGBM son opcionales: se usan si están instalados; si no, importancia por permutación y gradient boosting de scikit-learn."""
import numpy as np, pandas as pd
from . import validate as V, metrics as M
def features(r, extra=None):
    """Variables básicas a partir de una serie de rentabilidades diarias (todas conocidas al cierre de t)."""
    lr = np.log1p(r); X = pd.DataFrame(index=r.index)
    for w in (5, 21, 63, 126, 252): X[f"mom_{w}"] = lr.rolling(w).sum()
    for w in (10, 20, 60): X[f"vol_{w}"] = lr.rolling(w).std() * np.sqrt(252)
    X["vol_ratio"] = X["vol_10"] / X["vol_60"]; X["dd_252"] = (1 + r).cumprod() / (1 + r).cumprod().rolling(252, min_periods=20).max() - 1
    X["downside_20"] = np.sqrt((np.minimum(lr, 0) ** 2).rolling(20).mean() * 252); X["skew_60"] = lr.rolling(60).skew()
    if extra is not None: X = X.join(extra)
    return X
def labels(r, horizon=21, kind="sign"):
    """Etiqueta: rentabilidad de t+1 a t+horizon ('ret') o su signo ('sign')."""
    f = np.log1p(r).rolling(horizon).sum().shift(-horizon); return f if kind == "ret" else (f > 0).astype(float).where(f.notna())
def models(seed=0):
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    m = {"logistic": make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=500)),
         "random_forest": RandomForestClassifier(n_estimators=200, max_depth=4, min_samples_leaf=50, random_state=seed, n_jobs=-1),
         "gradient_boosting": HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=150, random_state=seed)}
    try:
        import xgboost as xgb; m["xgboost"] = xgb.XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, subsample=0.8, random_state=seed)
    except Exception: pass
    try:
        import lightgbm as lgb; m["lightgbm"] = lgb.LGBMClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, subsample=0.8, random_state=seed, verbose=-1)
    except Exception: pass
    return m
def oos_probabilities(model, X, y, k=5, horizon=21, embargo=None):
    """Probabilidades fuera de muestra con purged K-fold: cada observación se predice con un modelo que no vio su vecindad temporal."""
    from sklearn.base import clone
    d = pd.concat([X, y.rename("y")], axis=1).dropna(); Xv = d.drop(columns="y").values; yv = d["y"].values; out = np.full(len(d), np.nan)
    for tr, te in V.purged_kfold(len(d), k, embargo=horizon if embargo is None else embargo, purge=horizon):
        if len(np.unique(yv[tr])) < 2: continue
        out[te] = clone(model).fit(Xv[tr], yv[tr]).predict_proba(Xv[te])[:, 1]
    return pd.Series(out, index=d.index)
def walk_forward_probabilities(model, X, y, min_train=1260, step=63, horizon=21):
    """Probabilidades con ventana expandida estricta (solo pasado, dejando `horizon` días de purga): lo más parecido a operar en vivo."""
    from sklearn.base import clone
    d = pd.concat([X, y.rename("y")], axis=1).dropna(); Xv = d.drop(columns="y").values; yv = d["y"].values; out = np.full(len(d), np.nan)
    for a in range(min_train, len(d), step):
        tr = slice(0, a - horizon)
        if len(np.unique(yv[tr])) < 2: continue
        out[a:a + step] = clone(model).fit(Xv[tr], yv[tr]).predict_proba(Xv[a:a + step])[:, 1]
    return pd.Series(out, index=d.index)
def score(prob, y):
    from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
    d = pd.concat([prob.rename("p"), y.rename("y")], axis=1).dropna(); base = d.y.mean()
    return dict(n=len(d), auc=float(roc_auc_score(d.y, d.p)), brier=float(brier_score_loss(d.y, d.p)), brier_naive=float(base * (1 - base)), logloss=float(log_loss(d.y, d.p.clip(1e-6, 1 - 1e-6))), accuracy=float(((d.p > 0.5) == d.y).mean()), base_rate=float(base))
def calibration(prob, y, bins=10):
    d = pd.concat([prob.rename("p"), y.rename("y")], axis=1).dropna(); d["bin"] = pd.qcut(d.p, bins, duplicates="drop"); g = d.groupby("bin", observed=True).agg(pred=("p", "mean"), obs=("y", "mean"), n=("y", "size"))
    return g, float((g.n * (g.pred - g.obs).abs()).sum() / g.n.sum())      # tabla y error de calibración esperado
def strategy_from_prob(prob, r, rf=None, threshold=0.5, cost=0.0005):
    """Estrategia: dentro del activo cuando P(sube) > umbral, si no en efectivo. La probabilidad de t decide la posición de t+1. Devuelve rentabilidades netas."""
    pos = (prob > threshold).astype(float).reindex(r.index).shift(1).fillna(0); cash = rf.reindex(r.index).fillna(0) if rf is not None else 0
    return pos * r + (1 - pos) * cash - pos.diff().abs().fillna(0) * cost
def compare(r, rf=None, horizon=21, extra=None, threshold=0.5, cost=0.0005, min_train=1260):
    """Compara modelos contra dos referencias sencillas (comprar y mantener; regla de media de 200 sesiones) con walk-forward estricto y costes.
    Un modelo complejo solo se mantiene si mejora el Sharpe de las referencias Y de la regresión logística."""
    X = features(r, extra); y = labels(r, horizon); rows = {}; idx = X.dropna().index[min_train:]
    bh = r.loc[idx]; rows["comprar_y_mantener"] = dict(M.summary(bh.values, rf.loc[idx].values if rf is not None else 0), auc=np.nan)
    p = (1 + r).cumprod(); sma = (p > p.rolling(200).mean()).astype(float); rs = strategy_from_prob(sma, r, rf, 0.5, cost).loc[idx]; rows["regla_media_200"] = dict(M.summary(rs.values, rf.loc[idx].values if rf is not None else 0), auc=np.nan)
    probs = {}
    for nm, mdl in models().items():
        pr = walk_forward_probabilities(mdl, X, y, min_train, 63, horizon); probs[nm] = pr; s = strategy_from_prob(pr, r, rf, threshold, cost).loc[idx]
        rows[nm] = dict(M.summary(s.values, rf.loc[idx].values if rf is not None else 0), auc=score(pr, y)["auc"])
    t = pd.DataFrame(rows).T[["CAGR", "Vol", "Sharpe", "MDD", "auc"]]; best_simple = t.loc[["comprar_y_mantener", "regla_media_200", "logistic"], "Sharpe"].max()
    t["supera_a_lo_sencillo"] = t["Sharpe"] > best_simple + 0.1; return t, probs
def permutation_importance(model, X, y, n_repeats=5, seed=0):
    """Importancia por permutación medida en el último 30% (temporal) tras entrenar en el primer 70% menos la purga."""
    from sklearn.inspection import permutation_importance as pi
    d = pd.concat([X, y.rename("y")], axis=1).dropna(); c = int(len(d) * 0.7); Xa = d.drop(columns="y"); mdl = model.fit(Xa.values[:c - 21], d.y.values[:c - 21])
    r = pi(mdl, Xa.values[c:], d.y.values[c:], n_repeats=n_repeats, random_state=seed, scoring="roc_auc"); return pd.Series(r.importances_mean, index=Xa.columns).sort_values(ascending=False)
def shap_values(model, X):
    """Valores SHAP si la librería está instalada (opcional)."""
    import shap; return shap.TreeExplainer(model).shap_values(X)
def psi(expected, actual, bins=10):
    """Population Stability Index para detectar deriva de una variable o de las probabilidades: <0,1 estable; 0,1–0,25 vigilar; >0,25 deriva."""
    e = np.asarray(expected, float); a = np.asarray(actual, float); q = np.quantile(e[~np.isnan(e)], np.linspace(0, 1, bins + 1)); q[0], q[-1] = -np.inf, np.inf
    pe = np.histogram(e, q)[0] / np.isfinite(e).sum(); pa = np.histogram(a, q)[0] / np.isfinite(a).sum(); pe = np.clip(pe, 1e-6, None); pa = np.clip(pa, 1e-6, None); return float(((pa - pe) * np.log(pa / pe)).sum())
def drift_report(X, split=0.7):
    c = int(len(X) * split); return pd.Series({col: psi(X[col].values[:c], X[col].values[c:]) for col in X.columns}).sort_values(ascending=False)
