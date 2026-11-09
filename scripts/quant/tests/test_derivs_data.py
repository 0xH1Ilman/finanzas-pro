import json, math, numpy as np, pandas as pd, pytest
from fpq import derivs as D, providers as P, store, panel as PN, audit as A, monitor as MO, experiments as X, engine as E, report as R
def test_bs_reference_and_parity():
    c = float(D.bs(100, 100, 1, .05, .2)); p = float(D.bs(100, 100, 1, .05, .2, kind="put")); assert c == pytest.approx(10.4506, abs=1e-4) and p == pytest.approx(5.5735, abs=1e-4) and c - p == pytest.approx(100 - 100 * math.exp(-.05))
    import options_tools as L; o = L.bs(100, 100, 1, .05, 0, .2, "call"); g = D.greeks(100, 100, 1, .05, .2); assert o["price"] == pytest.approx(c) and o["delta"] == pytest.approx(float(g["delta"])) and o["vega"] == pytest.approx(float(g["vega"])) and o["theta"] == pytest.approx(float(g["theta"]))
    assert L.implied_vol(c, 100, 100, 1, .05, 0, "call") == pytest.approx(0.2, abs=1e-5); assert L.binomial(100, 100, 1, .05, 0, .2, "call", 800, False) == pytest.approx(c, abs=0.02); assert L.binomial(100, 100, 1, .05, 0, .2, "put", 500, True) > p
    cc = L.covered_call(100, 105, 30, 2.0, .05, 0, .25); assert cc["breakeven"] == 98 and cc["rend_si_asignada"] == pytest.approx(0.07)
def test_greeks_finite_difference():
    h = 1e-3; g = D.greeks(100, 95, .5, .03, .25, .01); f = lambda S=100, s=.25: float(D.bs(S, 95, .5, .03, s, .01))
    assert float(g["delta"]) == pytest.approx((f(100 + h) - f(100 - h)) / (2 * h), abs=1e-5); assert float(g["gamma"]) == pytest.approx((f(100 + h) - 2 * f() + f(100 - h)) / h ** 2, abs=1e-4); assert float(g["vega"]) == pytest.approx((f(s=.25 + h) - f(s=.25 - h)) / (2 * h) / 100, abs=1e-5)
def test_models():
    assert D.heston_call(100, 100, 1, .05, .04, 2, .04, 1e-4, 0) == pytest.approx(10.4506, abs=2e-3); assert D.heston_call(100, 100, 1, .05, .04, 2, .04, .5, -.7) < 10.4506
    K = np.array([80, 90, 100, 110, 120.]); iv = D.sabr_vol(100, K, 1, 2.0, .5, -.4, .6); f = D.sabr_fit(100, K, 1, iv); assert f["rho"] == pytest.approx(-.4, abs=1e-3) and iv[0] > iv[2]
    p, e = D.svi_fit(np.log(K / 100), iv, 1); assert e < 1e-3; sk = D.skew_metrics(K, iv, 100, 1); assert sk["rr25"] < 0
    lv = D.local_vol_dupire(K, [0.5, 1, 1.5], np.full((3, 5), .2), 100); assert np.nanmedian(lv[1, 1:-1]) == pytest.approx(0.2, abs=0.02)
def test_strategies_and_futures():
    t = D.payoff_table([dict(kind="stock", qty=100), dict(kind="call", K=110, T=.25, sigma=.3, qty=-1)], np.linspace(60, 140, 81), cost=9800); assert t.attrs["breakevens"][0] == pytest.approx(98) and t.pnl.max() == pytest.approx(1200)
    S = 100 * np.cumprod(1 + np.random.default_rng(0).normal(0, 0.03, 63)); h = D.delta_hedge_sim(S, 100, .25, 0, .2); assert h["realized_vol"] > .3 and h["final_pnl"] < 0
    idx = pd.bdate_range("2024-01-01", periods=60); a = pd.Series(100.0, index=idx[:40]); b = pd.Series(102.0, index=idx); s, rolls = D.continuous_series({idx[39]: a, idx[59]: b}); assert len(rolls) == 1 and s.pct_change().abs().max() < 1e-12
    assert D.roll_yield(100, 102) < 0 and D.curve_state([100, 101, 103])["state"] == "contango"
    v = D.rv_close(pd.Series(100 * np.cumprod(1 + np.random.default_rng(1).normal(0, 0.01, 500)))); assert v.iloc[-1] == pytest.approx(0.16, abs=0.06)
def test_parsers():
    y = {"chart": {"result": [{"timestamp": [1704205800, 1704292200], "indicators": {"quote": [{"open": [1, 2], "high": [2, 3], "low": [.5, 1], "close": [1.5, 2.5], "volume": [10, 20]}], "adjclose": [{"adjclose": [1.4, 2.4]}]}}]}}
    d = P.parse_yahoo_chart(json.dumps(y)); assert list(d.adj_close) == [1.4, 2.4] and str(d.index[0].date()) == "2024-01-02"
    assert P.parse_stooq_csv("Date,Open,High,Low,Close,Volume\n2024-01-02,1,2,0.5,1.5,10\n").close.iloc[0] == 1.5; assert P.parse_fred_csv("observation_date,DTB3\n2024-01-02,5.2\n2024-01-03,.\n").DTB3.isna().sum() == 1
    fr = "Texto\n\n,Mkt-RF,SMB,HML,RF\n19260701,  0.10, -0.24, -0.28,  0.009\n19260702,  0.45, -0.32, -0.08,  0.009\n\n Annual\n,Mkt-RF,SMB,HML,RF\n1927, 29.47, -2.46, -3.75, 3.12\n"
    t = P.parse_french_csv(fr); assert t.shape == (2, 4) and t["Mkt-RF"].iloc[1] == pytest.approx(0.0045); assert P.parse_french_csv(fr, 1).index[0].year == 1927
    ed = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [{"end": "2023-12-31", "val": 100, "filed": "2024-02-01", "form": "10-K", "fy": 2023, "fp": "FY"}, {"end": "2023-12-31", "val": 101, "filed": "2024-05-01", "form": "10-K/A", "fy": 2023, "fp": "FY"}]}}}}}
    e = P.parse_edgar_facts(json.dumps(ed), "Revenues"); assert store.as_of(e, "2024-03-01")["val"].iloc[0] == 100 and store.as_of(e, "2024-06-01")["val"].iloc[0] == 101
def test_store_quality():
    idx = pd.bdate_range("2024-01-01", periods=50); d = pd.DataFrame({"px": np.linspace(100, 110, 50)}, index=idx); d.iloc[30, 0] = 300; d = pd.concat([d, d.iloc[[5]]]); i = store.put("q", d, "test"); assert any("salto" in w for w in i["quality"]) and i["rows"] == 50
    store.put("q", pd.DataFrame({"px": [1.0, 2.0]}, index=pd.to_datetime(["2024-01-02", "2025-01-02"])), "test", incremental=True); g = store.get("q"); assert len(g) == 51 and g.loc["2024-01-02", "px"] != 1.0 and store.info("q")["version"] == 2
def test_panel_bundled(bundled):
    assert {"TQQQ", "AVUV", "AVDV", "KMLM", "GOLD", "QQQ", "SPY", "CASH", "TLT", "BITU"} <= set(bundled.columns) and str(bundled.index[0].date()) == "1986-01-02"
    y = (1 + bundled["QQQ"]).groupby(bundled.index.year).prod() - 1; assert y[1999] == pytest.approx(1.00, abs=0.03) and y[2008] == pytest.approx(-0.417, abs=0.01) and bundled.loc["1987-10-19", "QQQ"] == pytest.approx(-0.151, abs=0.005)
    assert PN.synthetic_share(["KMLM", "SPY"], "2000-01-01", "2020-01-01") == {"KMLM": 1.0, "SPY": 0.0}
def test_regression_gpa(bundled):
    """Regresión: resultados de referencia sobre el panel incluido. Si cambian sin haber cambiado los datos, hay un error en el motor."""
    m = E.Backtest(bundled, E.preset("gpa"), "1986-01-02", "2024-03-28").median_calendars(); assert m["CAGR"] == pytest.approx(0.1930, abs=0.002) and m["Sharpe"] == pytest.approx(0.88, abs=0.01) and m["MDD"] == pytest.approx(-0.380, abs=0.005)
    h = E.Backtest(bundled, E.preset("hmea"), "1986-01-02", "2024-03-28").median_calendars(); assert h["CAGR"] == pytest.approx(0.1714, abs=0.002)
    r = E.Backtest(bundled, E.preset("gpa"), "1986-01-02", "1994-12-30").run(); assert r.returns.loc["1987-10-19"] == pytest.approx(-0.169, abs=0.005) and r.signal.loc["1987-10-19"] == 0 and r.signal.loc["1987-10-21"] == 1
def test_audit_monitor_experiments(bundled):
    res = E.Backtest(bundled, E.preset("gpa"), "1995-01-03", "2024-03-28").run(weights=True); f = A.audit(res, context=dict(trials=40)); assert not A.verdict(f)["apto_para_validar"]
    s2 = E.preset("gpa"); s2["regime"]["delay"] = 0; f2 = A.audit(E.Backtest(bundled, s2, "1995-01-03", "2024-03-28").run(weights=True)); assert "Sesgo de anticipación" in set(f2.control)
    st = MO.signal_status(bundled["QQQ"].loc[:"2020-03-02"], E.preset("gpa")["regime"]["signal"]); assert st["state"] == "risk-off" or st["value"] > 0.3
    ex = MO.exposure_check({"TQQQ": .55, "AVUV": .1, "AVDV": .1, "KMLM": .1, "GOLD": .15}, E.preset("gpa")); assert ex.action.iloc[0] == "REBALANCEO COMPLETO"
    i = X.log("t", "h", "m", {"a": 1}, res.metrics(), trials=5); assert X.get(i)["trials"] == 5 and X.reproducible(i)["code_same"]; X.promote(i, "rejected", conclusion="x"); assert X.get(i)["phase"] == "rejected"
def test_report(tmp_path):
    d = pd.DataFrame({"CAGR": [0.1], "Sharpe": [0.8]}, index=["a"]); md = "# T\n\ntexto **negrita**\n\n" + R.md_table(d, {"CAGR": "pct", "Sharpe": "f2"}); assert "10.00%" in md; (tmp_path / "r.md").write_text(md); R.md_to_pdf(tmp_path / "r.md", tmp_path / "r.pdf"); assert (tmp_path / "r.pdf").stat().st_size > 1000
def test_research_study_smoke(bundled, tmp_path):
    from fpq import research
    o = research.study(bundled, E.preset("gpa"), start="1995-01-03", split="2005-01-01", end="2015-12-31", placebos=30, mc_paths=300, out_dir=tmp_path, grid={"regime.signal.window": [10, 20, 40], ("regime.signal.exit", "regime.signal.enter"): [(.30, .20), (.35, .25), (.40, .30)]})
    assert (tmp_path / "report.md").exists() and (tmp_path / "report.pdf").exists() and (tmp_path / "report.xlsx").exists() and len(o["verdict"]) >= 4 and o["experiment"] and 0 <= o["overfit"]["pbo"]["pbo"] <= 1
def test_ml_temporal_discipline():
    from fpq import ml
    r = pd.Series(np.random.default_rng(0).normal(0.0003, 0.01, 2500), index=pd.bdate_range("2005-01-03", periods=2500)); X = ml.features(r); y = ml.labels(r, 21)
    assert y.iloc[-21:].isna().all(); pr = ml.walk_forward_probabilities(ml.models()["logistic"], X, y, 1000, 250, 21); assert pr.iloc[:700].isna().all() and pr.notna().sum() > 500
    s = ml.score(pr, y); assert 0.4 < s["auc"] < 0.6          # ruido puro: sin capacidad predictiva
    assert ml.psi(r.values[:1000], r.values[1000:]) < 0.1 and ml.psi(r.values[:1000], r.values[1000:] * 3) > 0.25
def test_engine_reports_backend():
    assert "C" in E.engine_info() or "Python" in E.engine_info()
def test_never_rebuy_on_declines(bundled):
    """Un activo con tope `upper` no tiene banda inferior: en 2000-2002 la cartera sin filtro no recompra TQQQ al caer (regla R5 del usuario)."""
    s = E.preset("gpa"); s.pop("regime"); bt = E.Backtest(bundled, s, "1986-01-02", "2024-03-28"); assert (bt.dn[0] < -1) and bt.dn[1] == pytest.approx(0.1875 - 0.20)
    m = bt.median_calendars(); assert m["MDD"] == pytest.approx(-0.494, abs=0.01) and m["CAGR"] == pytest.approx(0.1815, abs=0.003)
    s["rebalance"]["lower"] = {"TQQQ": 0.05}; assert E.Backtest(bundled, s, "1986-01-02", "2024-03-28").median_calendars()["MDD"] < -0.60     # con recompra a la baja la caída es mucho peor
