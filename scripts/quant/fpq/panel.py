"""Panel diario de rentabilidades 1986→hoy con series reales donde existen y proxies donde no.
Cada columna lleva sus tramos (fechas, tipo observed/reconstructed/synthetic y fuente) en el manifiesto.
build() necesita las fuentes de GitHub (providers.github_clone / etf_release); load() usa el almacén o la copia incluida en la skill."""
import warnings, numpy as np, pandas as pd
from . import providers as P, store, config
warnings.filterwarnings("ignore")
START = "1985-12-31"
SECT = {"comm": ["CORN", "WHEAT", "SOYBEAN", "SUGAR11", "COTTON2", "LIVECOW", "GOLD", "SILVER", "HEATOIL", "CRUDE_W_mini", "GAS_US", "COPPER"],
        "fx": ["AUD", "GBP", "CAD", "CHF", "JPY", "EUR"], "bond": ["US10", "US20", "GILT", "CAD10", "JGB", "BUND"]}
def _ols(X, y):
    b = np.linalg.lstsq(X, y, rcond=None)[0]; f = X @ b; return b, 1 - ((y - f) ** 2).sum() / ((y - y.mean()) ** 2).sum()
class Builder:
    def __init__(s, raw=None):
        s.raw = raw or P.raw_dir(); s.seg = []; s.diag = {}
    def _letf(s, f, col="adj_close"):
        d = pd.read_csv(s.raw / "letf" / "data" / f); d = d[d.date.str.len() == 10]; d.index = pd.to_datetime(d.date); return d[col].astype(float)
    def fut(s, i, cal):
        """Rentabilidad diaria en exceso de un futuro: Δprecio ajustado / precio del contrato vigente (t−1)."""
        p = s.raw / "pst" / "data" / "futures"
        a = pd.read_csv(p / "adjusted_prices_csv" / f"{i}.csv", index_col=0, parse_dates=True)["price"]; a = a.groupby(a.index.normalize()).last().reindex(cal).ffill()
        m = pd.read_csv(p / "multiple_prices_csv" / f"{i}.csv", index_col=0, parse_dates=True)["PRICE"]; m = m.groupby(m.index.normalize()).last().reindex(cal).ffill()
        return (a.diff() / m.shift().abs()).clip(-0.3, 0.3), a
    def add(s, col, a, b, kind, src): s.seg.append(dict(col=col, start=str(a)[:10], end=str(b)[:10], kind=kind, source=src))
    def letf_sim(s, idx_ret, L, er, real, borrow, name, cal):
        sim = lambda sp: L * idx_ret - (L - 1) * (borrow + sp) / 252 - er / 252
        ov = real.reindex(cal).dropna().index
        sp = min(np.arange(-0.01, 0.03, 0.0005), key=lambda x: abs(np.log1p(sim(x)[ov]).sum() - np.log1p(real[ov]).sum())) if len(ov) > 250 else 0.004
        x = sim(sp)
        if len(ov): s.diag[name] = dict(spread=round(float(sp), 4), corr=round(float(np.corrcoef(x[ov], real[ov])[0, 1]), 4), te=round(float((x[ov] - real[ov]).std() * 252 ** .5), 4))
        out = real.reindex(cal).fillna(x)
        if len(ov): s.add(name, cal[0], ov[0], "synthetic", f"{L}x diario del índice − financiación − comisión {er:.2%}, diferencial calibrado {sp:.2%}"); s.add(name, ov[0], cal[-1], "observed", "ETF real (Tiingo vía ravelab/l-etf)")
        else: s.add(name, cal[0], cal[-1], "synthetic", f"{L}x diario sin calibrar")
        return out
    def trend(s, end, ma=250, tv=0.12, fee=0.012, rf=None):
        cal = pd.bdate_range("1980-01-01", end); rfx = rf.reindex(cal).ffill().bfill(); tot = pd.Series(0.0, index=cal)
        for ins in SECT.values():
            acc = pd.DataFrame(index=cal)
            for i in ins:
                x, a = s.fut(i, cal); sig = np.sign(a - a.rolling(ma).mean()).shift(1); v = x.rolling(60).std().shift(1) * 252 ** .5
                acc[i] = (sig * x / v).where(v > 0)
            tot = tot.add(acc.mean(axis=1).fillna(0) / 3, fill_value=0)
        rv = tot.rolling(250).std().shift(1) * 252 ** .5
        return (tv / rv) * tot + rfx - fee / 252
    def build(s):
        import pyreadr, rdata
        ndx = s._letf("index-nq.csv"); cal = ndx.loc[START:].index; r = pd.DataFrame(index=cal); A = s.add
        borrow = s._letf("rate-borrow.csv", "value").reindex(cal).ffill(); r["BORROW"] = borrow
        f = pyreadr.read_r(str(s.raw / "ffr" / "data" / "factors.rda"))["factors"]; f = f[f.frequency == "day"].copy()
        f["date"] = pd.to_datetime(f.period.astype(str), format="%Y%m%d"); fac = f.pivot_table(index=["region", "date"], columns="factor", values="value", observed=True) / 100
        b = pyreadr.read_r(str(s.raw / "ffr" / "data" / "portfolios_bivariate.rda"))["portfolios_bivariate"]
        b = b[(b.frequency == "day") & (b["sort variable 1"] == "market capitalization") & (b["sort variable 2"] == "book/market") & (b.dividend == "Y") & (b.weights == "value") & (b.field == "return")].copy()
        b["date"] = pd.to_datetime(b.period.astype(str), format="%Y%m%d"); biv = b.pivot_table(index=["region", "date"], columns="portfolio", values="value", observed=True) / 100
        us = fac.loc["US"]; rf_ff = us["risk free rate"]; sgov = s._letf("risk-sgov.csv").pct_change()
        rf = rf_ff.reindex(cal).fillna(sgov.reindex(cal)).fillna(borrow / 252); r["CASH"] = rf
        A("CASH", cal[0], "2021-04-30", "observed", "letras 1 mes (Ken French)"); A("CASH", "2021-05-03", cal[-1], "observed", "SGOV")
        r["QQQ"] = ndx.pct_change().reindex(cal); A("QQQ", cal[0], "1999-03-09", "observed", "Nasdaq-100 con dividendos (índice)"); A("QQQ", "1999-03-10", cal[-1], "observed", "QQQ")
        sp = s._letf("index-sp.csv").pct_change().reindex(cal); r["SPY"] = sp.where(cal >= "1988-04-07", (us["market"] + rf_ff).reindex(cal))
        A("SPY", cal[0], "1988-04-06", "reconstructed", "mercado EE. UU. (Ken French)"); A("SPY", "1988-04-07", cal[-1], "observed", "S&P 500 con dividendos / VOO")
        for nm, src, L, er, fl in [("TQQQ", "QQQ", 3, .0095, "etf-tqqq.csv"), ("QLD", "QQQ", 2, .0095, "etf-qld.csv"), ("UPRO", "SPY", 3, .0091, "etf-upro.csv"), ("SSO", "SPY", 2, .0089, "etf-sso.csv")]:
            r[nm] = s.letf_sim(r[src], L, er, s._letf(fl).pct_change(), borrow, nm, cal)
        # ETFs reales
        try: px = pd.read_parquet(s.raw / "prices.parquet", columns=["date", "ticker", "adj_close"], filters=[("ticker", "in", ["IJS", "IWN", "EFA", "EWJ", "EWU", "EWG", "TLT", "IEF", "GLD", "AGG", "SHY", "VWO"])]).pivot(index="date", columns="ticker", values="adj_close")
        except Exception: px = pd.DataFrame()
        e = px.pct_change().reindex(cal) if len(px) else pd.DataFrame(index=cal)
        last_etf = px.index[-1] if len(px) else cal[0]
        # oro
        gx, _ = s.fut("GOLD", cal); gfut = gx + rf - 0.0009 / 252; gldm = s._letf("risk-gldm.csv").pct_change().reindex(cal)
        gold = e["GLD"] if "GLD" in e else gldm
        r["GOLD"] = gold.fillna(gldm).fillna(gfut); A("GOLD", cal[0], gold.first_valid_index() or cal[-1], "reconstructed", "futuro de oro + letras − 0,09%"); A("GOLD", gold.first_valid_index() or cal[-1], cal[-1], "observed", "GLD / GLDM")
        # tendencia
        fut_end = pd.read_csv(s.raw / "pst/data/futures/adjusted_prices_csv/GOLD.csv", index_col=0, parse_dates=True).index[-1].normalize()
        r["KMLM"] = s.trend(fut_end, rf=rf_ff).reindex(cal); r.loc[r.index > fut_end, "KMLM"] = np.nan
        A("KMLM", cal[0], fut_end, "reconstructed", "réplica propia de tendencia (24 futuros sin renta variable, media 250 sesiones, 12% vol, −1,2% anual). NO es KMLMSIM")
        # bonos
        for nm, fu, etf in [("TLT", "US20", "TLT"), ("IEF", "US10", "IEF")]:
            x, _ = s.fut(fu, cal); real = e[etf] if etf in e else pd.Series(np.nan, index=cal); ok = real.notna() & x.notna()
            beta = _ols(x[ok].values[:, None], (real - rf)[ok].values)[0][0] if ok.sum() > 500 else 1.0
            r[nm] = real.fillna(beta * x + rf); s.diag[nm] = dict(beta_fut=round(float(beta), 3))
            A(nm, cal[0], real.first_valid_index() or cal[-1], "reconstructed", f"{beta:.2f}× futuro {fu} + letras"); A(nm, real.first_valid_index() or cal[-1], cal[-1], "observed", etf)
        r["TMF"] = 3 * r["TLT"] - 2 * (borrow + 0.004) / 252 - 0.0106 / 252; A("TMF", cal[0], cal[-1], "synthetic", "3x diario de TLT − financiación − 1,06% (sin calibrar contra TMF real)")
        # small value EE. UU.
        mk, smb, hml = us["market"], us["SMB"], us["HML"]
        USC = biv.loc["US"][[f"ME{m} BM{k}" for m in (2, 3, 4, 5) for k in (8, 9, 10)]].mean(axis=1); Y = (USC - rf_ff).dropna()
        X = pd.concat([mk, smb, hml], axis=1).reindex(Y.index); bb, r2 = _ols(X.values, Y.values); s.diag["AVUV"] = dict(mkt=round(bb[0], 3), smb=round(bb[1], 3), hml=round(bb[2], 3), r2=round(r2, 3))
        scv = (rf_ff + bb[0] * mk + bb[1] * smb + bb[2] * hml - 0.006 / 252).reindex(cal)
        if {"IJS", "IWN"} <= set(e.columns):
            ok = USC.reindex(cal).notna() & e[["IJS", "IWN"]].notna().all(axis=1); bt, r2t = _ols(e.loc[ok, ["IJS", "IWN"]].values, USC.reindex(cal)[ok].values)
            tail = pd.Series(e[["IJS", "IWN"]].values @ bt, index=cal); s.diag["AVUV"].update(tail_IJS=round(bt[0], 3), tail_IWN=round(bt[1], 3), tail_r2=round(r2t, 3))
        else: tail = pd.Series(np.nan, index=cal)
        r["AVUV"] = scv.fillna(tail); A("AVUV", cal[0], "2021-04-30", "reconstructed", "factores Fama-French ajustados a carteras small value (ME2–5 × BM8–10), −0,6% anual"); A("AVUV", "2021-05-03", cal[-1], "reconstructed", "combinación de IJS e IWN reales ajustada al tramo anterior")
        # small value internacional
        gxu = fac.loc["global (ex US)"]; rfi = gxu["risk free rate"]; IC = lambda k: biv.loc[k][["SMALL HiBM", "ME1 BM4", "ME2 BM4", "ME2 BM5"]].mean(axis=1)
        Yi = (IC("global (ex US)") - rfi).dropna(); Xi = pd.concat([gxu["market"], gxu["SMB"], gxu["HML"]], axis=1).reindex(Yi.index); bi, r2i = _ols(Xi.values, Yi.values)
        iscv = rfi + bi[0] * gxu["market"] + bi[1] * gxu["SMB"] + bi[2] * gxu["HML"]
        reg = pd.concat([IC(k) for k in ["Europe", "JP", "Asia-Pacific (ex JP)"]], axis=1).dropna(); yr = IC("global (ex US)"); ok2 = yr.index.intersection(reg.index)
        br = _ols(reg.loc[ok2].values, yr.loc[ok2].values)[0]; iscv = iscv.combine_first(pd.Series(reg.values @ br, index=reg.index)); s.diag["AVDV"] = dict(mkt=round(bi[0], 3), smb=round(bi[1], 3), hml=round(bi[2], 3), r2=round(r2i, 3))
        intl = iscv.reindex(cal); fac_end = iscv.index[-1]
        cols = [c for c in ["EFA", "EWJ", "EWU", "EWG"] if c in e.columns]
        if cols:
            tg = intl - rf; Xb = e[cols].sub(rf, axis=0); okb = tg.notna() & Xb.notna().all(axis=1) & (cal >= "2003-01-01"); wk = lambda z: z[okb].groupby(pd.Grouper(freq="W")).sum()
            bw, r2w = _ols(wk(Xb).values, wk(tg).values); intl = intl.fillna(pd.Series(Xb.values @ bw, index=cal) + rf); s.diag["AVDV"].update(tail=dict(zip(cols, np.round(bw, 3))), tail_r2_weekly=round(r2w, 3))
        o = rdata.parser.parse_file(str(s.raw / "qrm" / "data" / "NIKKEI.rda")).object.value[0]; at = o.attributes; ix = None
        while at is not None and at.value:
            if at.tag.value.value == b"index": ix = np.asarray(at.value[0].value); break
            at = at.value[1]
        nk = pd.Series(np.asarray(o.value, dtype=float).ravel(), index=pd.to_datetime(ix, unit="s").normalize()).pct_change().reindex(cal).fillna(0)
        jpy, ftse, gbp, hang = (s.fut(k, cal)[0] for k in ("JPY", "FTSE100", "GBP", "HANG"))
        eafe = 0.62 * (nk + 0.007 / 252 + jpy) + 0.30 * (ftse + gbp + rf) + 0.08 * (hang.fillna(0) + rf)
        r["AVDV"] = intl.where(cal >= "1990-07-02", eafe) - 0.007 / 252 * (cal <= fac_end)
        A("AVDV", cal[0], "1990-06-29", "reconstructed", "gran capitalización Japón/Reino Unido/Hong Kong en USD (NO es small value: proxy débil)"); A("AVDV", "1990-07-02", fac_end, "reconstructed", "factores Fama-French ex-EE. UU. ajustados a small value, −0,7% anual"); A("AVDV", fac_end, cal[-1], "reconstructed", "combinación de EFA/EWJ/EWU/EWG reales ajustada al tramo anterior")
        mkt_i = (gxu["market"] + rfi).reindex(cal); r["EFA"] = (e["EFA"] if "EFA" in e else pd.Series(np.nan, index=cal)).fillna(mkt_i).fillna(eafe)
        A("EFA", cal[0], "1990-06-29", "reconstructed", "Japón/Reino Unido/Hong Kong en USD"); A("EFA", "1990-07-02", "2001-08-24", "reconstructed", "mercado ex-EE. UU. (Ken French)"); A("EFA", "2001-08-27", cal[-1], "observed", "EFA")
        # bitcoin
        try:
            c = pd.read_csv(s.raw / "cm" / "csv" / "btc.csv", usecols=["time", "PriceUSD", "ReferenceRateUSD"], parse_dates=["time"]).set_index("time"); p = c.PriceUSD.fillna(c.ReferenceRateUSD).dropna()
            btc = p.reindex(cal, method="ffill").pct_change(); btc[cal > p.index[-1]] = np.nan; r["BTC"] = btc
            r["BITU"] = 2 * btc - borrow / 252 - (0.0095 + 0.108) / 252; A("BTC", p.index[0], p.index[-1], "observed", "Coin Metrics (precio de referencia, días de bolsa)"); A("BITU", p.index[0], p.index[-1], "synthetic", "2x diario de BTC − financiación − 0,95% − 10,8% de coste calibrado en el whitepaper del usuario (no hay BITU real en las fuentes)")
        except Exception as ex: s.diag["BTC"] = f"no disponible: {ex}"
        r = r.loc[cal[1]:]
        if len(px): r.loc[r.index > max(last_etf, cal[0]), [c for c in ["AVUV", "AVDV", "TLT", "IEF", "TMF", "EFA"] if c in r]] = np.nan
        return r
def build(save=True, bundle=False):
    B = Builder(); r = B.build()
    if save: store.put("panel", r, "fpq.panel.build", "reconstructed", note=str(B.diag), segments=B.seg)
    if bundle:
        import json; config.BUNDLED.mkdir(exist_ok=True); r.round(6).to_csv(config.BUNDLED / "panel.csv.gz")
        (config.BUNDLED / "panel_meta.json").write_text(json.dumps(dict(segments=B.seg, diag=B.diag, built=str(pd.Timestamp.now())[:19], end=str(r.index[-1])[:10]), indent=1, ensure_ascii=False, default=str))
    return r, B
def load():
    """Panel desde el almacén; si no existe, la copia incluida en la skill (con su fecha de corte)."""
    try: return store.get("panel")
    except Exception: return pd.read_csv(config.BUNDLED / "panel.csv.gz", index_col=0, parse_dates=True)
def meta():
    import json
    try: i = store.info("panel"); return dict(segments=i["segments"], end=i["end"])
    except Exception: return json.loads((config.BUNDLED / "panel_meta.json").read_text())
def provenance(cols, start=None, end=None):
    """Tramos y tipo de dato de cada columna en el periodo. Úsalo en todo informe: distingue observado de reconstruido o sintético."""
    out = [g for g in meta()["segments"] if g["col"] in cols and (end is None or g["start"] <= str(end)[:10]) and (start is None or g["end"] >= str(start)[:10])]
    return pd.DataFrame(out)
def synthetic_share(cols, start, end):
    """Fracción del periodo (por columna) que NO es dato observado."""
    d = provenance(cols, start, end); a, b = pd.Timestamp(start), pd.Timestamp(end); out = {}
    for c in cols:
        g = d[(d.col == c) & (d.kind != "observed")]; days = sum(max((min(pd.Timestamp(x.end), b) - max(pd.Timestamp(x.start), a)).days, 0) for x in g.itertuples())
        out[c] = round(days / max((b - a).days, 1), 3)
    return out
def splice(panel, user, col, name=None):
    """Sustituye la columna `col` por la serie del usuario donde exista y devuelve diagnóstico del solape (correlación, error de seguimiento, diferencia anual)."""
    u = user.reindex(panel.index); ov = u.notna() & panel[col].notna()
    d = dict(n=int(ov.sum()), corr=float(np.corrcoef(u[ov], panel[col][ov])[0, 1]) if ov.sum() > 20 else None,
             te=float((u[ov] - panel[col][ov]).std() * 252 ** .5) if ov.sum() > 20 else None, ann_diff=float((u[ov] - panel[col][ov]).mean() * 252) if ov.sum() > 20 else None)
    out = panel.copy(); out[col] = u.fillna(panel[col]); return out, d
