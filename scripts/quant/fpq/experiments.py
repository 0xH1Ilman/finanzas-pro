"""Registro de experimentos (SQLite): cada investigación guarda hipótesis, método, parámetros, versión de datos, hash del código,
periodo, universo, costes, métricas, artefactos y conclusiones. Permite comparar y reproducir sin depender de la memoria de nadie.
Separa descubrimiento de validación: un experimento nace en fase 'discovery' y solo pasa a 'validated' con `promote()` tras las pruebas de validate."""
import sqlite3, json, hashlib, datetime as dt, pathlib, pandas as pd
from . import config, store
PHASES = ("discovery", "validation", "validated", "rejected", "live")
def _db():
    con = sqlite3.connect(config.home() / "experiments" / "registry.sqlite")
    con.execute("""CREATE TABLE IF NOT EXISTS experiments(id INTEGER PRIMARY KEY AUTOINCREMENT, created TEXT, name TEXT, phase TEXT, hypothesis TEXT, method TEXT,
        params TEXT, data_versions TEXT, code_hash TEXT, period TEXT, universe TEXT, costs TEXT, metrics TEXT, checks TEXT, conclusion TEXT, artifacts TEXT, parent INTEGER, trials INTEGER)""")
    return con
def code_hash():
    h = hashlib.sha256()
    for f in sorted(pathlib.Path(__file__).parent.glob("*.py")) + sorted(pathlib.Path(__file__).parent.glob("*.c")): h.update(f.read_bytes())
    return h.hexdigest()[:12]
def data_versions(names=("panel",)):
    out = {}
    for n in names:
        try: out[n] = store.version(n)
        except Exception: out[n] = "copia incluida en la skill"
    return out
def log(name, hypothesis, method, params, metrics, period=None, universe=None, costs=None, conclusion="", phase="discovery", checks=None, artifacts=None, parent=None, trials=1, datasets=("panel",)):
    """Registra un experimento y devuelve su id. `trials` = nº de variantes probadas para llegar a este resultado (necesario para el Sharpe deflactado)."""
    assert phase in PHASES; con = _db()
    cur = con.execute("INSERT INTO experiments(created,name,phase,hypothesis,method,params,data_versions,code_hash,period,universe,costs,metrics,checks,conclusion,artifacts,parent,trials) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (dt.datetime.now().isoformat(timespec="seconds"), name, phase, hypothesis, method, json.dumps(params, default=str), json.dumps(data_versions(datasets)), code_hash(), json.dumps(period, default=str),
         json.dumps(universe), json.dumps(costs), json.dumps({k: (float(v) if isinstance(v, (int, float)) or hasattr(v, "item") else str(v)) for k, v in metrics.items()}), json.dumps(checks or {}, default=str), conclusion, json.dumps(artifacts or []), parent, trials))
    con.commit(); return cur.lastrowid
def get(i):
    con = _db(); con.row_factory = sqlite3.Row; r = dict(con.execute("SELECT * FROM experiments WHERE id=?", (i,)).fetchone())
    for k in ("params", "data_versions", "period", "universe", "costs", "metrics", "checks", "artifacts"): r[k] = json.loads(r[k]) if r[k] else None
    return r
def list_(name=None, phase=None):
    q = "SELECT id,created,name,phase,trials,metrics,conclusion FROM experiments WHERE 1=1" + (" AND name LIKE ?" if name else "") + (" AND phase=?" if phase else "")
    d = pd.read_sql(q, _db(), params=[x for x in (f"%{name}%" if name else None, phase) if x])
    if len(d):
        m = d.metrics.apply(json.loads); d["CAGR"] = m.apply(lambda x: x.get("CAGR")); d["Sharpe"] = m.apply(lambda x: x.get("Sharpe")); d["MDD"] = m.apply(lambda x: x.get("MDD"))
    return d.drop(columns="metrics") if len(d) else d
def compare(ids):
    rows = [get(i) for i in ids]; return pd.DataFrame({r["id"]: {"name": r["name"], "phase": r["phase"], **r["metrics"], "data": str(r["data_versions"]), "code": r["code_hash"]} for r in rows})
def promote(i, phase, checks=None, conclusion=None):
    """Cambia de fase (p. ej. a 'validated' o 'rejected') adjuntando las pruebas que lo justifican."""
    assert phase in PHASES; con = _db(); r = get(i); ck = {**(r["checks"] or {}), **(checks or {})}
    con.execute("UPDATE experiments SET phase=?, checks=?, conclusion=? WHERE id=?", (phase, json.dumps(ck, default=str), conclusion or r["conclusion"], i)); con.commit()
def total_trials(name):
    """Suma de variantes probadas en todos los experimentos de una línea de investigación (para deflactar el Sharpe)."""
    d = pd.read_sql("SELECT trials FROM experiments WHERE name LIKE ?", _db(), params=[f"%{name}%"]); return int(d.trials.sum())
def reproducible(i):
    """¿Los datos y el código actuales son los mismos que cuando se registró el experimento?"""
    r = get(i); return dict(code_same=r["code_hash"] == code_hash(), data_same=r["data_versions"] == data_versions(tuple(r["data_versions"])), was=r["data_versions"], code_was=r["code_hash"])
