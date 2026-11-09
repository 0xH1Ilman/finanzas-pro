import math, numpy as np, pandas as pd, pytest
from fpq import metrics as M, engine as E, signals, wengine as W, execsim
def test_metrics_hand():
    r = np.array([0.10, -0.10, 0.05, -0.05]); assert M.max_drawdown(r) == pytest.approx(0.9875250 / 1.1 - 1, abs=1e-6); assert M.equity(r)[-1] == pytest.approx(1.1 * .9 * 1.05 * .95)
    assert M.cagr(np.full(252, 0.001)) == pytest.approx(1.001 ** 252 - 1); assert M.vol(np.array([0.01, -0.01] * 126)) == pytest.approx(np.std([0.01, -0.01] * 126, ddof=1) * math.sqrt(252))
    assert M.longest_underwater(np.array([0.1, -0.05, 0.01, 0.01, 0.2])) == pytest.approx(3 / 252)
def test_metrics_vs_legacy():
    import perf_metrics as L
    r = np.random.default_rng(1).normal(0.0004, 0.01, 2000); v = [1.0] + list(M.equity(r)); o = L.metrics(v)
    assert o["cagr"] == pytest.approx(M.cagr(r), rel=1e-3); assert o["max_drawdown"] == pytest.approx(M.max_drawdown(r), abs=1e-12)
def SPEC(): return dict(weights={"TQQQ": .25, "A": .25, "B": .25, "G": .25}, rebalance=dict(every_months=12, phase=11, upper={"TQQQ": .5}, dev=.2),
                        regime=dict(signal=dict(type="vol", asset="QQQ", window=20, exit=.35, enter=.25), assets=["TQQQ"], refuge={"K": .5, "G": .5}, delay=1, cost=.001))
def test_engine_c_equals_python(synth):
    s = SPEC(); s["trim"] = [dict(asset="A", at=.30, to=.25, recipients=["B", "G"])]; s["tax"] = dict(rate=.2); s["costs"] = dict(turnover=.001); s["flows"] = dict(amount=.01, every_months=1)
    bt = E.Backtest(synth, s); a = bt.run(weights=True); b = bt.run(engine="py", weights=True)
    assert np.allclose(a.equity.values, b.equity.values, rtol=1e-10); assert np.allclose(a.weights.values, b.weights.values, atol=1e-10); assert a.stats == pytest.approx(b.stats)
    assert np.allclose(a.weights.sum(axis=1), 1.0); assert a.stats["switches"] > 0 and a.stats["taxes"] > 0
def test_engine_buy_and_hold(synth):
    r = E.run(synth, dict(weights={"A": 1.0}, rebalance=dict(every_months=0))); assert np.allclose(r.returns.values, synth["A"].values)
def test_engine_flows_do_not_change_twr(synth):
    s = dict(weights={"A": .5, "B": .5}, rebalance=dict(every_months=12)); a = E.run(synth, s); s2 = dict(s, flows=dict(amount=0.05, every_months=1)); b = E.run(synth, s2)
    assert np.allclose(a.equity.values, b.equity.values, rtol=1e-9); assert b.value.iloc[-1] > a.value.iloc[-1]
def test_engine_always_off_equals_refuge(synth):
    s = dict(weights={"TQQQ": 1.0}, rebalance=dict(every_months=0), regime=dict(signal=dict(type="vol", asset="QQQ", window=20, exit=.35, enter=.25), assets=["TQQQ"], refuge={"K": 1.0}, delay=0, cost=0.0))
    bt = E.Backtest(synth, s); r = bt.run(state=np.ones(len(synth), np.int8)); assert np.allclose(r.returns.values, synth["K"].values)
def test_engine_no_lookahead(synth):
    """Cambiar los datos de mañana no altera el resultado hasta hoy."""
    s = SPEC(); a = E.run(synth, s); p2 = synth.copy(); p2.iloc[2000:] = p2.iloc[2000:] * -1; b = E.run(p2, s); assert np.allclose(a.equity.values[:2000], b.equity.values[:2000])
def test_calendar_phases_and_bands(synth):
    bt = E.Backtest(synth, SPEC()); assert len(list(bt.phases())) == 12; m = bt.median_calendars(); assert m["CAGR_min"] <= m["CAGR"] <= m["CAGR_max"]
    s = SPEC(); s["rebalance"]["upper"]["TQQQ"] = .26; assert E.run(synth, s).stats["band_rebalances"] > E.run(synth, SPEC()).stats["band_rebalances"]
def test_signals():
    v = np.array([.1, .4, .3, .2, .3, .4]); assert list(signals.hysteresis(v, .35, .25)) == [0, 1, 1, 0, 0, 1]
    r = np.random.default_rng(0).normal(0, 0.01, 5000); assert np.nanmean(signals.downside_vol(r) / signals.realized_vol(r)) == pytest.approx(1 / math.sqrt(2), abs=0.05)
    st = np.zeros(1000, np.int8); st[100:150] = 1; st[400:420] = 1; p = signals.placebo(st, np.random.default_rng(1)); assert p.sum() == 70 and len(signals.episodes(p, np.arange(1000))) <= 2
def test_wengine(synth):
    R = synth[["A", "B", "G"]]; o = W.backtest(R, pd.DataFrame(1 / 3, index=R.index, columns=R.columns), rf=synth["CASH"]); assert o["metrics"]["avg_gross"] == pytest.approx(1.0, abs=0.01)
    c = W.backtest(R, W.w_momentum(R, 60, 5, 1), rf=synth["CASH"], rebalance="M", commission=0.001); f = W.backtest(R, W.w_momentum(R, 60, 5, 1), rf=synth["CASH"], rebalance="M")
    assert c["metrics"]["CAGR"] < f["metrics"]["CAGR"]; ls = W.backtest(R, W.w_meanrev(R), rf=synth["CASH"]); assert abs(ls["metrics"]["avg_net"]) < 0.05
    assert W.letf(pd.Series([0.01]), 3, 0.05).iloc[0] == pytest.approx(0.03 - 2 * 0.054 / 252 - 0.0095 / 252)
def test_execsim():
    idx = pd.bdate_range("2024-01-01", periods=30); b = pd.DataFrame(dict(open=100.0, high=101.0, low=99.0, close=100.0, volume=1e5), index=idx)
    f = execsim.simulate(b, [dict(date=idx[5], side="buy", qty=5e3), dict(date=idx[5], side="buy", qty=5e4), dict(date=idx[5], side="buy", qty=100, type="limit", limit=98.0)])
    assert f.fill_pct[0] == 1 and f.shortfall_bps[0] > 0 and f.days[1] == 5 and f.shortfall_bps[1] > f.shortfall_bps[0] and f.filled[2] == 0
