"""Proveedores de datos gratuitos. Cada función devuelve un DataFrame con índice de fechas.
En sesiones en la nube solo suelen responder GitHub (clonado, raw y releases) y PyPI: ejecuta `doctor()` una vez
y usa lo que responda. Los proveedores web (Yahoo, Stooq, FRED, French, EDGAR, Tesoro, BCE, Banco Mundial, CBOE)
funcionan en equipos con red abierta. Los analizadores (`parse_*`) están separados y probados sin red."""
import io, json, zipfile, subprocess, datetime as dt, pandas as pd, numpy as np
from . import config
UA = {"User-Agent": "Mozilla/5.0 (fpq research; contacto: usuario)"}
def http_get(url, timeout=30, headers=None, binary=False):
    import requests
    r = requests.get(url, timeout=timeout, headers={**UA, **(headers or {})}); r.raise_for_status()
    return r.content if binary else r.text
def reachable(url, timeout=8):
    try:
        import requests; return requests.get(url, timeout=timeout, headers=UA, stream=True).status_code < 400
    except Exception: return False
PROBES = {"github_raw": "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv",
          "yahoo": "https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=5d&interval=1d",
          "stooq": "https://stooq.com/q/d/l/?s=spy.us&i=d", "fred": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3",
          "french": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip",
          "edgar": "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json",
          "treasury": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/all/all?type=daily_treasury_yield_curve&field_tdr_date_value=all&page&_format=csv",
          "ecb": "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?format=csvdata&lastNObservations=5",
          "worldbank": "https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json&per_page=5",
          "cboe": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
          "testfolio": "https://testfol.io/"}
def doctor():
    """Qué fuentes responden desde este entorno. Ejecutar una sola vez por sesión."""
    return {k: reachable(u) for k, u in PROBES.items()}
# ---------------- analizadores (probados sin red)
def parse_yahoo_chart(js):
    res = (json.loads(js) if isinstance(js, str) else js)["chart"]["result"][0]
    idx = pd.to_datetime(res["timestamp"], unit="s").normalize(); q = res["indicators"]["quote"][0]
    df = pd.DataFrame({k: q[k] for k in ("open", "high", "low", "close", "volume")}, index=idx)
    adj = res["indicators"].get("adjclose"); df["adj_close"] = adj[0]["adjclose"] if adj else df["close"]
    return df.dropna(subset=["close"])
def parse_stooq_csv(txt):
    df = pd.read_csv(io.StringIO(txt), parse_dates=["Date"]).set_index("Date"); df.columns = [c.lower() for c in df.columns]; return df
def parse_fred_csv(txt):
    df = pd.read_csv(io.StringIO(txt)); df.columns = ["date"] + list(df.columns[1:])
    df["date"] = pd.to_datetime(df["date"]); df = df.set_index("date"); return df.apply(pd.to_numeric, errors="coerce")
def parse_french_csv(txt, table=0):
    """CSV de la biblioteca de Ken French: varias tablas separadas por líneas en blanco. Devuelve la tabla `table` en decimales."""
    blocks, cur = [], []
    for ln in txt.splitlines():
        f = ln.split(",")
        if f[0].strip().isdigit() and len(f) > 1: cur.append(ln)
        elif cur: blocks.append(cur); cur = []
        if not f[0].strip().isdigit() and len(f) > 1 and f[0].strip() == "": hdr = [c.strip() for c in f[1:]]; cur = []; blocks.append(("H", hdr))
    if cur: blocks.append(cur)
    tabs, h = [], None
    for b in blocks:
        if isinstance(b, tuple): h = b[1]
        elif b:
            d = pd.read_csv(io.StringIO("\n".join(b)), header=None, index_col=0); d.columns = h[:d.shape[1]] if h else d.columns
            s = d.index.astype(str); fmt = "%Y%m%d" if len(s[0].strip()) == 8 else ("%Y%m" if len(s[0].strip()) == 6 else "%Y")
            d.index = pd.to_datetime(s.str.strip(), format=fmt); tabs.append(d.replace([-99.99, -999], np.nan) / 100)
    return tabs[table]
def parse_edgar_facts(js, concept, unit="USD", taxonomy="us-gaap"):
    """Fundamentales punto en el tiempo: cada dato lleva su fecha de presentación (`asof`)."""
    f = (json.loads(js) if isinstance(js, str) else js)["facts"][taxonomy][concept]["units"][unit]
    d = pd.DataFrame(f); d["period"] = pd.to_datetime(d["end"]); d["asof"] = pd.to_datetime(d["filed"])
    return d.set_index("period")[["val", "asof", "form", "fy", "fp"]].sort_values("asof")
# ---------------- proveedores web
def yahoo(ticker, start="1970-01-01", interval="1d"):
    p1 = int(pd.Timestamp(start).timestamp()); p2 = int(pd.Timestamp.now().timestamp())
    return parse_yahoo_chart(http_get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={p1}&period2={p2}&interval={interval}&events=div%2Csplit"))
def stooq(symbol, interval="d"): return parse_stooq_csv(http_get(f"https://stooq.com/q/d/l/?s={symbol}&i={interval}"))
def fred(series): return parse_fred_csv(http_get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"))
def fred_vintages(series, api_key):
    """ALFRED: todas las revisiones con su fecha de publicación (punto en el tiempo). Requiere clave gratuita de FRED."""
    js = json.loads(http_get(f"https://api.stlouisfed.org/fred/series/observations?series_id={series}&api_key={api_key}&file_type=json&realtime_start=1776-07-04&realtime_end=9999-12-31"))
    d = pd.DataFrame(js["observations"]); d["period"] = pd.to_datetime(d["date"]); d["asof"] = pd.to_datetime(d["realtime_start"])
    d["val"] = pd.to_numeric(d["value"], errors="coerce"); return d.set_index("period")[["val", "asof"]]
def french(name, table=0):
    """name: p. ej. 'F-F_Research_Data_Factors_daily', '6_Portfolios_2x3_daily', 'Developed_ex_US_6_Portfolios_ME_BE-ME_daily'."""
    z = zipfile.ZipFile(io.BytesIO(http_get(f"https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{name}_CSV.zip", binary=True)))
    return parse_french_csv(z.read(z.namelist()[0]).decode("latin-1"), table)
def edgar_facts(cik, concept, unit="USD"):
    return parse_edgar_facts(http_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"), concept, unit)
def treasury_curve():
    d = pd.read_csv(io.StringIO(http_get(PROBES["treasury"]))); d["Date"] = pd.to_datetime(d["Date"]); return d.set_index("Date").sort_index() / 100
def ecb_fx(ccy="USD"):
    d = pd.read_csv(io.StringIO(http_get(f"https://data-api.ecb.europa.eu/service/data/EXR/D.{ccy}.EUR.SP00.A?format=csvdata")))
    return d.set_index(pd.to_datetime(d["TIME_PERIOD"]))[["OBS_VALUE"]].rename(columns={"OBS_VALUE": f"EUR{ccy}"})
def worldbank(indicator, country="US"):
    js = json.loads(http_get(f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=500"))[1]
    return pd.Series({pd.Timestamp(f"{x['date']}-12-31"): x["value"] for x in js}).sort_index().to_frame(indicator)
def cboe_vix():
    d = pd.read_csv(io.StringIO(http_get(PROBES["cboe"]))); d["DATE"] = pd.to_datetime(d["DATE"]); d = d.set_index("DATE"); d.columns = [c.lower() for c in d.columns]; return d
def nasdaq_data_link(code, api_key):
    js = json.loads(http_get(f"https://data.nasdaq.com/api/v3/datasets/{code}.json?api_key={api_key}"))["dataset"]
    return pd.DataFrame(js["data"], columns=js["column_names"]).set_index("Date").sort_index()
# ---------------- fuentes de GitHub (funcionan en la nube)
GITHUB = {"letf": ("ravelab/l-etf", None), "pst": ("robcarver17/pysystemtrade", ["data/futures/adjusted_prices_csv", "data/futures/multiple_prices_csv", "data/futures/csvconfig"]),
          "ffr": ("bautheac/FFresearch", None), "qrm": ("cran/qrmdata", None), "cm": ("coinmetrics/data", ["csv/btc.csv", "csv/eth.csv"])}
ETF_RELEASE = "https://github.com/Johnbrick123/sp500-data/releases/download/data/prices.parquet"
def raw_dir(): return config.home() / "raw"
def github_clone(key, update=False):
    """Clona (superficial y, si procede, parcial) un repositorio de datos en el directorio raw. Devuelve la ruta."""
    repo, sparse = GITHUB[key]; dst = raw_dir() / key
    if dst.exists():
        if update: subprocess.run(["git", "-C", str(dst), "pull", "-q", "--depth", "1"], check=False, timeout=600)
        return dst
    cmd = ["git", "clone", "-q", "--depth", "1"] + (["--filter=blob:none", "--sparse"] if sparse else []) + [f"https://github.com/{repo}", str(dst)]
    subprocess.run(cmd, check=True, timeout=900)
    if sparse: subprocess.run(["git", "-C", str(dst), "sparse-checkout", "set", "--no-cone"] + sparse, check=True, timeout=900)
    return dst
def etf_release(update=False):
    """Parquet (≈240 MB) con precios diarios ajustados de acciones del S&P 500 y ~150 ETFs (SPY, QQQ, IJS, IWN, EFA, EWJ, TLT, IEF, GLD…), actualizado cada noche."""
    p = raw_dir() / "prices.parquet"
    if update or not p.exists(): p.write_bytes(http_get(ETF_RELEASE, timeout=900, binary=True))
    return p
def etf_prices(tickers, col="adj_close"):
    d = pd.read_parquet(etf_release(), columns=["date", "ticker", col], filters=[("ticker", "in", list(tickers))])
    return d.pivot(index="date", columns="ticker", values=col).sort_index()
def load_csv(path, date_col=None, price_cols=None, returns=False):
    """CSV del usuario (export de Testfolio, Yahoo, Portfolio Visualizer…). Detecta la columna de fecha; devuelve rentabilidades diarias."""
    d = pd.read_csv(path); dc = date_col or next(c for c in d.columns if c.lower() in ("date", "fecha", "time", "datetime", "timestamp") or "date" in c.lower())
    d[dc] = pd.to_datetime(d[dc]); d = d.set_index(dc).sort_index().apply(pd.to_numeric, errors="coerce")
    if price_cols: d = d[price_cols]
    return d if returns else d.pct_change().iloc[1:]
