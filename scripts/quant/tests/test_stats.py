import numpy as np, pandas as pd, pytest
from fpq import validate as V, metrics as M, portfolio as PF, attribution as AT, regimes as RG, factors as F, engine as E
RNG = np.random.default_rng(3)
def test_psr_dsr():
    r = RNG.normal(0, 0.01, 5000); assert 0.2 < V.psr(r) < 0.8; g = RNG.normal(0.001, 0.01, 5000); assert V.psr(g) > 0.99
    assert V.deflated_sharpe(g, 1000, np.random.default_rng(0).normal(0, 1, 100))["dsr"] < V.deflated_sharpe(g, 2)["dsr"]; assert V.min_track_record(g) < V.min_track_record(g, 1.0)
def test_pvalue_adjust():
    p = [0.01, 0.04, 0.03, 0.2]; assert np.allclose(V.adjust_pvalues(p, "bonferroni"), [0.04, 0.16, 0.12, 0.8]); assert np.allclose(V.adjust_pvalues(p, "holm"), [0.04, 0.09, 0.09, 0.2]); assert np.allclose(V.adjust_pvalues(p, "bh"), [0.04, 0.16 / 3, 0.16 / 3, 0.2])
def test_bootstrap_and_mc():
    ix = V.stationary_indices(500, 20, np.random.default_rng(0)); assert ix.min() >= 0 and ix.max() < 500 and (np.diff(ix) == 1).mean() > 0.85
    r = RNG.normal(0.0005, 0.01, 3000); ci = V.bootstrap_ci(r, n=300); assert ci["lo"] < ci["point"] < ci["hi"]
    m = pd.DataFrame(RNG.normal([0.01, 0.005], [0.04, 0.04], (400, 2)), columns=["a", "b"]); o = V.monte_carlo(m, 10, 2000, bench="b"); assert o.loc["a", "CAGR_p50"] > o.loc["b", "CAGR_p50"] and o.loc["a", "P_beat_b"] > 0.6
def test_pbo_and_reality_check():
    noise = RNG.normal(0, 0.01, (2520, 20)); assert 0.25 < V.pbo(noise, 8)["pbo"] < 0.75; assert V.reality_check(noise, n=300)["p_value"] > 0.1
    skill = noise.copy(); skill[:, 0] += 0.001; assert V.pbo(skill, 8)["pbo"] < 0.1; assert V.reality_check(skill, n=300)["p_value"] < 0.05
def test_cv_splits():
    for tr, te in V.purged_kfold(1000, 5, embargo=10, purge=5): assert len(set(tr) & set(te)) == 0 and all(abs(t - te[0]) > 5 or t > te[-1] for t in tr[(tr < te[0])][-1:])
    sp = list(V.cpcv(600, 6, 2)); assert len(sp) == 15 and all(len(set(a) & set(b)) == 0 for a, b in sp)
def test_walk_forward():
    X = pd.DataFrame(RNG.normal(0.0003, 0.01, (5040, 6)), index=pd.bdate_range("2000-01-03", periods=5040)); w = V.walk_forward(X, 8, 2); assert len(w["oos"]) == 5040 - 8 * 252 and len(w["picks"]) == 6
def test_grid_plateau_placebo(synth):
    from tests.test_core import SPEC
    g = V.grid(synth, SPEC(), {"regime.signal.window": [10, 20, 40], ("regime.signal.exit", "regime.signal.enter"): [(.30, .20), (.35, .25)]}, {"all": (None, None)}); assert len(g) == 6
    pl = V.plateau(g, {"regime.signal.window": 20, "regime.signal.exit+regime.signal.enter": (.35, .25)}); assert 1 <= pl["all"]["Sharpe_rank"] <= 6 and "CAGR_neighbors" in pl["all"]
    pt = V.placebo_test(E.Backtest(synth, SPEC()), 50); assert 0 <= pt["p"]["Sharpe"] <= 1 and pt["episodes"] > 0
def test_portfolio():
    R = pd.DataFrame(RNG.normal(0, [0.01, 0.02, 0.005, 0.015], (3000, 4)), columns=list("abcd")); R["b"] += 0.5 * R["a"]; S = PF.cov(R)
    w = PF.risk_budget(S); assert np.allclose(PF.risk_contribution(w, S)["pct"], 0.25, atol=1e-3); h = PF.hrp(R); assert h.sum() == pytest.approx(1) and (h > 0).all()
    mv = PF.min_variance(S); assert PF.port_vol(mv, S) <= PF.port_vol(w, S) + 1e-9 and PF.port_vol(mv, S) <= PF.port_vol(np.full(4, .25), S)
    b = PF.risk_budget(S, [.4, .2, .2, .2]); assert PF.risk_contribution(b, S)["pct"][0] == pytest.approx(0.4, abs=2e-3); assert PF.diversification(np.full(4, .25), S)["ratio"] > 1
def test_attribution():
    d, c = AT.brinson({"a": .6, "b": .4}, {"a": .5, "b": .5}, {"a": .10, "b": .02}, {"a": .08, "b": .03}); assert c["excess"] == pytest.approx(c["explained"])
    wp = pd.DataFrame({"a": [.6, .7], "b": [.4, .3]}); wb = pd.DataFrame({"a": [.5, .5], "b": [.5, .5]}); rp = pd.DataFrame({"a": [.1, -.02], "b": [.02, .03]}); rb = pd.DataFrame({"a": [.08, -.01], "b": [.03, .02]})
    d, c = AT.brinson_multi(wp, wb, rp, rb); assert c["excess"] == pytest.approx(c["explained"], abs=1e-9)
    f = pd.DataFrame(RNG.normal(0, 0.01, (2000, 2)), columns=["m", "v"]); y = 0.0002 + 1.2 * f["m"] - 0.5 * f["v"] + RNG.normal(0, 0.001, 2000); o = AT.factor_attribution(y, f); assert o["betas"]["m"] == pytest.approx(1.2, abs=0.02) and o["alpha_annual"] == pytest.approx(0.0504, abs=0.02)
def test_regimes():
    x = np.r_[RNG.normal(0, 0.005, 1500), RNG.normal(0, 0.03, 500), RNG.normal(0, 0.005, 1000)]; m = RG.hmm_fit(x, 2); assert m["path"][1600:1900].mean() > 0.9 and m["path"][200:1300].mean() < 0.1
    assert np.sqrt(m["var"][:, 0]) == pytest.approx([0.005, 0.03], rel=0.15); fl = RG.hmm_filter(x, m); assert np.allclose(fl.sum(1), 1)
    g = RG.garch11(x); assert 0 < g["persistence"] < 1; lab, c = RG.kmeans(np.c_[np.r_[np.zeros(50), np.ones(50) * 5], RNG.normal(0, 1, 100)], 2); assert len(set(lab[:50])) == 1
    assert len(RG.cusum_breaks(np.r_[np.zeros(200), np.ones(200) * 3] + RNG.normal(0, 1, 400))) >= 1
def test_factors():
    R = pd.DataFrame(RNG.normal(0.0003, 0.01, (1500, 9)), index=pd.bdate_range("2010-01-01", periods=1500), columns=list("abcdefghi")); ch = pd.DataFrame(np.tile(np.arange(9.0), (1500, 1)), index=R.index, columns=R.columns)
    R2 = R + ch * 0.0002; s = F.sort_portfolios(R2, ch, n=3); assert s["factor"].mean() > 0; pf = F.build_price_factors(R); assert {"MOM", "LOWVOL", "TREND"} <= set(pf.columns)
