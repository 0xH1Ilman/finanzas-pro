"""Almacén local de datos: Parquet (o CSV si no hay pyarrow) + manifiesto con procedencia, versión y control de calidad.
Cada dataset guarda: fuente, fecha de descarga, tipo (observed | reconstructed | synthetic | estimate), hash de contenido y avisos de calidad.
Punto en el tiempo: los datasets con columna `asof` (fecha de publicación) se consultan con `as_of()` para no usar datos futuros."""
import json, hashlib, datetime as dt, pandas as pd, numpy as np
from . import config
KINDS = ("observed", "reconstructed", "synthetic", "estimate")
def _dir(): return config.home() / "store"
def _mf(): return _dir() / "manifest.json"
def manifest():
    return json.loads(_mf().read_text()) if _mf().exists() else {}
def _hash(df): return hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values.tobytes()).hexdigest()[:16]
def quality(df, max_gap_days=7, jump=0.5):
    """Control de calidad genérico. Devuelve lista de avisos (vacía = sin incidencias)."""
    w = []
    if isinstance(df.index, pd.DatetimeIndex):
        if df.index.has_duplicates: w.append(f"fechas duplicadas: {int(df.index.duplicated().sum())}")
        if not df.index.is_monotonic_increasing: w.append("fechas desordenadas")
        g = pd.Series(df.index[1:] - df.index[:-1]).dt.days
        if len(g) and g.max() > max_gap_days and g.median() <= 3: w.append(f"hueco máximo de {int(g.max())} días naturales")
    for c in df.select_dtypes("number").columns:
        s = df[c]; n = int(s.isna().sum())
        if n: w.append(f"{c}: {n} valores faltantes ({n/len(s):.1%})")
        if (s.dropna() > 0).all() and len(s) > 3:
            ch = s.dropna().pct_change().abs()
            if ch.max() > jump: w.append(f"{c}: salto de {ch.max():.0%} el {ch.idxmax()} (¿split o error?)")
        if s.nunique(dropna=True) > 5 and (s.diff() == 0).rolling(10).sum().max() >= 10: w.append(f"{c}: 10+ valores idénticos seguidos")
    return w
def clean(df):
    """Normaliza: índice de fechas sin zona horaria, ordenado, sin duplicados (conserva el último)."""
    if not isinstance(df.index, pd.DatetimeIndex): df.index = pd.to_datetime(df.index)
    if df.index.tz is not None: df.index = df.index.tz_localize(None)
    df.index = df.index.normalize() if (df.index == df.index.normalize()).mean() > 0.9 else df.index
    return df[~df.index.duplicated(keep="last")].sort_index()
def put(name, df, source, kind="observed", note="", segments=None, incremental=False):
    """Guarda un dataset. incremental=True añade solo fechas nuevas y conserva lo anterior (los valores antiguos no se reescriben)."""
    assert kind in KINDS, kind
    df = clean(df.copy()); m = manifest()
    if incremental and name in m:
        old = get(name); df = pd.concat([old, df[~df.index.isin(old.index)]]).sort_index()
    try:
        path = _dir() / f"{name}.parquet"; df.to_parquet(path)
    except Exception:
        path = _dir() / f"{name}.csv.gz"; df.to_csv(path)
    ver = m.get(name, {}).get("version", 0) + 1
    m[name] = dict(file=path.name, source=source, kind=kind, note=note, segments=segments or [], version=ver, hash=_hash(df),
                   rows=len(df), cols=list(map(str, df.columns)), start=str(df.index[0])[:10], end=str(df.index[-1])[:10],
                   saved=dt.datetime.now().isoformat(timespec="seconds"), quality=quality(df))
    _mf().write_text(json.dumps(m, indent=1, ensure_ascii=False)); return m[name]
def get(name):
    m = manifest()
    if name not in m: raise KeyError(f"dataset '{name}' no está en el almacén ({_dir()}); usa fpq_cli.py data build o data fetch")
    p = _dir() / m[name]["file"]
    return pd.read_parquet(p) if p.suffix == ".parquet" else pd.read_csv(p, index_col=0, parse_dates=True)
def info(name=None):
    m = manifest(); return m if name is None else m[name]
def version(name): i = info(name); return f"{name}@v{i['version']}:{i['hash']}"
def as_of(df, date, asof_col="asof"):
    """Punto en el tiempo: de un dataset con una fila por (periodo, fecha de publicación) devuelve lo conocido en `date`."""
    d = df[pd.to_datetime(df[asof_col]) <= pd.Timestamp(date)]
    return d.sort_values(asof_col).groupby(level=0).last()
def lag_publication(s, days):
    """Para series sin fecha de publicación: desplaza `days` días hábiles (retraso conservador de publicación)."""
    return s.shift(days)
def sql(query):
    """Consulta SQL sobre el almacén con DuckDB (opcional). Las tablas se llaman como los datasets."""
    import duckdb
    con = duckdb.connect()
    for n, i in manifest().items():
        if i["file"].endswith(".parquet"): con.execute(f"CREATE VIEW \"{n}\" AS SELECT * FROM read_parquet('{_dir() / i['file']}')")
    return con.execute(query).df()
