#!/usr/bin/env python3
"""fpq — línea de comandos del sistema cuantitativo de finanzas-pro.

  python3 fpq_cli.py doctor                          qué fuentes de datos responden aquí
  python3 fpq_cli.py data fetch [--update]           clona las fuentes de GitHub y descarga el parquet de ETFs
  python3 fpq_cli.py data build                      reconstruye el panel diario 1986→hoy y lo guarda en el almacén
  python3 fpq_cli.py data info [--cols TQQQ AVUV]    procedencia de cada columna (observado / reconstruido / sintético)
  python3 fpq_cli.py data splice --csv mis.csv --map KMLMSIM=KMLM DFSVX=AVUV     sustituye columnas por series del usuario
  python3 fpq_cli.py presets                         estrategias predefinidas
  python3 fpq_cli.py run gpa --start 1986-01-02 --end 2024-03-28 [--set regime.signal.exit=0.40]
  python3 fpq_cli.py study gpa --start 1986-01-02 --split 1995-01-01 --compare hmea --hypothesis "..."
  python3 fpq_cli.py grid gpa --param regime.signal.window=10,20,30 --param regime.signal.exit=0.30,0.35,0.40
  python3 fpq_cli.py placebo gpa -n 400
  python3 fpq_cli.py mc gpa hmea spy --years 10
  python3 fpq_cli.py signal gpa [--state on|off]     estado de la señal al último cierre y movimiento que la activaría
  python3 fpq_cli.py exp list | exp show 3 | exp compare 2 3
  python3 fpq_cli.py test                            batería de pruebas
Una estrategia es un nombre de preset o la ruta de un JSON con la misma estructura (ver engine.PRESETS)."""
import argparse, json, sys, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pandas as pd
from fpq import providers, panel, engine as E, validate as V, research, metrics as M, experiments as X, monitor, store
def spec_of(s, sets=()):
    sp = E.preset(s) if s in E.PRESETS else json.loads(pathlib.Path(s).read_text())
    for kv in sets or ():
        k, v = kv.split("=", 1)
        try: v = json.loads(v)
        except Exception: pass
        sp = E.with_params(sp, {k: v})
    return sp
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor"); sub.add_parser("presets"); sub.add_parser("test")
    d = sub.add_parser("data"); d.add_argument("action", choices=["fetch", "build", "info", "splice"]); d.add_argument("--update", action="store_true"); d.add_argument("--cols", nargs="*"); d.add_argument("--csv"); d.add_argument("--map", nargs="*"); d.add_argument("--returns", action="store_true")
    for c in ("run", "study", "grid", "placebo", "signal"):
        p = sub.add_parser(c); p.add_argument("strategy"); p.add_argument("--start"); p.add_argument("--end"); p.add_argument("--set", action="append")
        if c == "study": p.add_argument("--split"); p.add_argument("--compare", nargs="*", default=[]); p.add_argument("--hypothesis", default=""); p.add_argument("--out"); p.add_argument("--trials-before", type=int, default=0)
        if c == "grid": p.add_argument("--param", action="append", required=True); p.add_argument("--split")
        if c == "placebo": p.add_argument("-n", type=int, default=400)
        if c == "signal": p.add_argument("--state", choices=["on", "off"])
    m = sub.add_parser("mc"); m.add_argument("strategies", nargs="+"); m.add_argument("--years", type=int, default=10); m.add_argument("--start"); m.add_argument("--end"); m.add_argument("-n", type=int, default=10000)
    e = sub.add_parser("exp"); e.add_argument("action", choices=["list", "show", "compare"]); e.add_argument("ids", nargs="*", type=int)
    a = ap.parse_args(); pd.set_option("display.width", 200)
    if a.cmd == "doctor": print(json.dumps(providers.doctor(), indent=1)); return
    if a.cmd == "presets":
        for k, v in E.PRESETS.items(): print(f"{k:10s} {v['name']}: {v['weights']}")
        return
    if a.cmd == "test": sys.exit(subprocess.call([sys.executable, "-m", "pytest", "-q", str(pathlib.Path(__file__).parent / "tests")]))
    if a.cmd == "data":
        if a.action == "fetch":
            for k in providers.GITHUB: print(k, providers.github_clone(k, a.update))
            print(providers.etf_release(a.update))
        elif a.action == "build": r, B = panel.build(); print(r.shape, r.index[0].date(), "→", r.index[-1].date()); print(B.diag)
        elif a.action == "info": print(panel.provenance(a.cols or list(panel.load().columns)).to_string(index=False))
        elif a.action == "splice":
            u = providers.load_csv(a.csv, returns=a.returns); p = panel.load()
            for kv in a.map: src, dst = kv.split("="); p, dg = panel.splice(p, u[src], dst); print(f"{src} → {dst}: {dg}")
            store.put("panel", p, f"panel + series del usuario ({a.csv})", "reconstructed", segments=panel.meta()["segments"] + [dict(col=kv.split('=')[1], start=str(u.index[0])[:10], end=str(u.index[-1])[:10], kind="observed", source=f"usuario: {a.csv}") for kv in a.map])
        return
    p = panel.load()
    if a.cmd == "exp":
        if a.action == "list": print(X.list_().to_string(index=False))
        elif a.action == "show": print(json.dumps(X.get(a.ids[0]), indent=1, ensure_ascii=False, default=str))
        else: print(X.compare(a.ids).to_string())
        return
    if a.cmd == "mc":
        ens = {s: research._ens(E.Backtest(p, spec_of(s), a.start, a.end)) for s in a.strategies}; mo = pd.DataFrame(ens).dropna(); mm = (1 + mo).groupby([mo.index.year, mo.index.month]).prod() - 1
        print(V.monte_carlo(mm, a.years, a.n, bench=a.strategies[-1]).round(3).to_string()); return
    sp = spec_of(a.strategy, a.set)
    if a.cmd == "run":
        bt = E.Backtest(p, sp, a.start, a.end); m = bt.median_calendars(); print(f"{sp.get('name')} · {bt.idx[0].date()} → {bt.idx[-1].date()} · mediana de {m['n_calendars']} calendarios")
        print(M.fmt(m)); print(f"CAGR {m['CAGR_min']*100:.2f}–{m['CAGR_max']*100:.2f}% según calendario · peor caída {m['MDD_worst']*100:.1f}% · cambios/año {m['switches_per_year']:.2f} · tiempo fuera {m['time_out']*100:.0f}%")
        print("No observado:", panel.synthetic_share(bt.cols, bt.idx[0], bt.idx[-1]))
    elif a.cmd == "study":
        o = research.study(p, sp, hypothesis=a.hypothesis, start=a.start, split=a.split, end=a.end, compare={E.PRESETS[c]["name"] if c in E.PRESETS else c: spec_of(c) for c in a.compare}, out_dir=a.out, trials_before=a.trials_before)
        print("\n".join(o["verdict"])); print("Informe:", o["dir"], "· experimento", o["experiment"])
    elif a.cmd == "grid":
        params = {k: json.loads("[" + v + "]") for k, v in (x.split("=", 1) for x in a.param)}; bt = E.Backtest(p, sp, a.start, a.end); per = {"Completo": (bt.idx[0], bt.idx[-1])}
        if a.split: per.update({"Fuera de muestra": (bt.idx[0], pd.Timestamp(a.split)), "Dentro de muestra": (pd.Timestamp(a.split), bt.idx[-1])})
        print(V.grid(p, sp, params, per).round(4).to_string(index=False))
    elif a.cmd == "placebo":
        print(json.dumps(V.placebo_test(E.Backtest(p, sp, a.start, a.end), a.n, phase=sp.get("rebalance", {}).get("phase", 0)), indent=1))
    elif a.cmd == "signal":
        sg = sp["regime"]["signal"]; s = monitor.signal_status(p[sg.get("asset", "QQQ")], sg, None if a.state is None else int(a.state == "off")); print(json.dumps(s, indent=1, default=float, ensure_ascii=False))
if __name__ == "__main__": main()
