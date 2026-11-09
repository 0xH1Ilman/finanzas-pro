"""Motor central de investigación: `study()` ejecuta el protocolo completo sobre una estrategia de reglas y deja un informe reproducible
(Markdown + PDF + Excel + gráficos + CSV) y una entrada en el registro de experimentos. `quick()` da solo las métricas."""
import copy, json, pathlib, datetime as dt, numpy as np, pandas as pd
from . import engine as E, validate as V, metrics as M, signals, audit as A, report as R, panel as PN, experiments as X, config, attribution as AT, portfolio as PF
DEFAULT_GRID = {"regime.signal.window": [10, 15, 20, 25, 30, 40, 60], ("regime.signal.exit", "regime.signal.enter"): [(.25, .15), (.30, .20), (.35, .25), (.40, .30), (.45, .35), (.50, .40)]}
def quick(panel, spec, start=None, end=None):
    bt = E.Backtest(panel, spec, start, end); return bt.median_calendars()
def _no_regime(spec):
    s = copy.deepcopy(spec); s.pop("regime", None); s["name"] = s.get("name", "") + " (sin filtro)"; return s
def _ens(bt): return pd.concat([bt.run(phase=k).returns for k in bt.phases()], axis=1).mean(axis=1)
def study(panel, spec, name=None, hypothesis="", start=None, split=None, end=None, benchmarks=("spy", "qqq"), compare=None, grid=None, chosen=None,
          placebos=400, mc_paths=5000, out_dir=None, log=True, trials_before=0, make_pdf=True):
    """start/split/end: el tramo [start, split) es FUERA de muestra (no usado para elegir parámetros) y [split, end] dentro de muestra; si split=None no se separa.
    compare: {'nombre': spec} de carteras alternativas. grid: rejilla de validate.grid (por defecto ventana × umbrales si hay filtro de volatilidad).
    trials_before: variantes probadas antes de este estudio (se suman a las de la rejilla para deflactar el Sharpe)."""
    name = name or spec.get("name", "estrategia"); slug = "".join(ch if ch.isalnum() else "_" for ch in name.lower())[:40]
    out = pathlib.Path(out_dir) if out_dir else config.home() / "reports" / f"{slug}_{dt.datetime.now():%Y%m%d_%H%M}"; out.mkdir(parents=True, exist_ok=True)
    bt = E.Backtest(panel, spec, start, end); a, b = bt.idx[0], bt.idx[-1]; reg = spec.get("regime"); res = bt.run(weights=True)
    periods = {"Completo": (a, b)}
    if split: periods.update({"Fuera de muestra": (a, pd.Timestamp(split) - pd.Timedelta(days=1)), "Dentro de muestra": (pd.Timestamp(split), b)})
    specs = {name: spec}
    if reg: specs["Misma cartera sin filtro"] = _no_regime(spec)
    specs.update(compare or {}); 
    for k in benchmarks: specs[E.PRESETS[k]["name"]] = E.preset(k)
    T = V.subperiods(panel, specs, periods); S = {}; md = []; P = R.pct
    # 1 resultados
    ens = {n: _ens(E.Backtest(panel, sp, a, b)) for n, sp in specs.items()}; rf = bt.rf; main = ens[name]
    # 2 rejilla y sobreajuste
    G = pl = None; trials = 1 + trials_before; over = {}
    if reg and (grid is not None or reg["signal"].get("type") in ("vol", "downside", "ewma")):
        grid = grid or DEFAULT_GRID; G = V.grid(panel, spec, grid, periods)
        basem = {pn: T[(T.period == pn) & (T.strategy == "Misma cartera sin filtro")].iloc[0].to_dict() for pn in periods}
        chosen = chosen or {"regime.signal.window": reg["signal"]["window"], "regime.signal.exit+regime.signal.enter": (reg["signal"]["exit"], reg["signal"]["enter"])}
        pl = V.plateau(G, chosen, basem); Xm = V.config_matrix(panel, spec, grid, a, b); trials += Xm.shape[1]
        base_r = ens["Misma cartera sin filtro"]; over = dict(pbo=V.pbo(Xm.values, blocks=10), wf=V.walk_forward(Xm, 10, 2) if len(Xm) > 13 * 252 else None,
                    rc=V.reality_check(Xm.sub(base_r, axis=0).values, n=1000), dsr=V.deflated_sharpe(main.values - rf, trials, [M.sharpe(Xm[c].values - rf) for c in Xm]))
    else: over = dict(dsr=V.deflated_sharpe(main.values - rf, max(trials, 1)))
    # 3 placebo, ejecución, proxies
    plc = {}
    if reg:
        for pn, (pa, pb) in periods.items(): plc[pn] = V.placebo_test(E.Backtest(panel, spec, pa, pb), placebos, phase=spec.get("rebalance", {}).get("phase", 0))
        ex = V.execution_sensitivity(bt)
    sh = PN.synthetic_share(bt.cols, a, b); weak = [c for c, v in sh.items() if v > 0.3 and c not in ("TQQQ", "UPRO", "QLD", "SSO", "TMF")]
    px = V.proxy_sensitivity(panel, {k: specs[k] for k in list(specs)[:2]}, [{c: 0.02 for c in weak}, {c: 0.04 for c in weak}], a, b) if weak else None
    # 4 significación y Monte Carlo
    ci = V.bootstrap_ci(main.values - rf, n=1000); psr0 = V.psr(main.values - rf, 0.0); mtr = V.min_track_record(main.values - rf, 0.0)
    mo = pd.DataFrame(ens); mm = (1 + mo).groupby([mo.index.year, mo.index.month]).prod() - 1; bench_name = E.PRESETS[benchmarks[0]]["name"] if benchmarks else None
    mc = V.monte_carlo(mm, 10, mc_paths, bench=bench_name) if len(mm) > 60 else None
    # 5 colas
    wp = M.worst_periods(res.returns, (1, 2, 5, 21)); tails = pd.DataFrame([dict(dias=d, fecha=str(x[0].date()), perdida=x[1], estado_filtro=("fuera" if res.signal.loc[x[0]] else "dentro") if reg else "—") for d, x in wp.items()])
    # 6 atribución
    ct = AT.contribution_to_return(res.weights, panel); rc = AT.contribution_to_risk(res.weights, panel.loc[a:b]); dv = PF.diversification(res.weights.mean().values, panel.loc[a:b, res.weights.columns].cov().values * 252)
    # 7 auditoría
    ctx = dict(trials=trials, dsr=over["dsr"]["dsr"], pbo=(over.get("pbo") or {}).get("pbo"), oos=bool(split), placebo_p=plc.get("Completo", {}).get("p") if reg else None, calendars_reported=True,
               benchmark=bench_name, proxy_sensitivity_done=px is not None, data_end=b, tail_checked=True, costs_included=True if reg and reg.get("cost", 0) > 0 else None)
    ctx = {k: v for k, v in ctx.items() if v is not None}; au = A.audit(res, context=ctx); ver = A.verdict(au)
    # ---- veredicto
    tf = T[(T.period == "Completo")].set_index("strategy"); me = tf.loc[name]; lines = []
    if reg:
        b0 = tf.loc["Misma cartera sin filtro"]; pf = plc["Completo"]["p"]
        risk_ok = pf["MDD"] < 0.05 and pf["Sharpe"] < 0.05; cagr_ok = pf["CAGR"] < 0.05
        lines.append(f"La regla {'es robusta como reductora de riesgo' if risk_ok else 'no se distingue del azar como reductora de riesgo'} (placebo: p = {pf['Sharpe']:.3f} en Sharpe, {pf['MDD']:.3f} en caída máxima).")
        lines.append(f"El CAGR extra frente a la misma cartera sin filtro ({(me.CAGR - b0.CAGR) * 100:+.2f} puntos) {'es significativo' if cagr_ok else 'no es significativo'} (p = {pf['CAGR']:.3f})" + (f"; el parámetro elegido ocupa el puesto {pl['Completo']['CAGR_rank']} de {pl['Completo']['cells']} en CAGR." if pl and 'CAGR_rank' in pl['Completo'] else "."))
        if split: po = plc["Fuera de muestra"]["p"]; lines.append(f"Fuera de muestra: p = {po['Sharpe']:.3f} en Sharpe y {po['MDD']:.3f} en caída máxima con {plc['Fuera de muestra']['episodes']} episodios" + (" (poca potencia estadística)." if plc['Fuera de muestra']['episodes'] < 10 else "."))
    lines.append(f"Sharpe {me.Sharpe:.2f} (IC 95% por bootstrap: {ci['lo']:.2f} a {ci['hi']:.2f}); Sharpe deflactado tras {trials} pruebas: {over['dsr']['dsr']:.3f}.")
    lines.append(f"Auditoría: {ver['alta']} hallazgos de gravedad alta, {ver['media']} media, {ver['baja']} baja.")
    # ---- informe
    fm = {"CAGR": "pct", "Vol": "pct1", "Sharpe": "f2", "Sortino": "f2", "MDD": "pct1", "UPI": "f2", "CAGR_min": "pct", "CAGR_max": "pct", "MDD_worst": "pct1"}
    md += [f"# {name}", f"Informe generado el {dt.date.today()} · periodo {a.date()} → {b.date()} · mediana de {len(list(bt.phases()))} calendarios · fpq {X.code_hash()}", "", "## Veredicto"] + [f"- {l}" for l in lines]
    if hypothesis: md += ["", "## Hipótesis", hypothesis]
    md += ["", "## Metodología", f"- Motor diario con reglas: {json.dumps({k: v for k, v in spec.items() if k != 'name'}, ensure_ascii=False)}", "- Señal al cierre de t, ejecución al cierre de t+retraso; bandas y calendario al cierre.",
           f"- Fuera de muestra: {'tramo anterior a ' + str(split)[:10] if split else 'no separado'}.", "", "## Datos y procedencia", "Tipo de dato por activo (observed = real; reconstructed = proxy; synthetic = simulación):", "",
           R.md_table(PN.provenance(bt.cols, a, b)[["col", "start", "end", "kind", "source"]], index=False), "", f"Fracción del periodo que no es dato observado: {sh}", "", "## Resultados"]
    for pn in periods: md += [f"### {pn} ({str(periods[pn][0])[:10]} → {str(periods[pn][1])[:10]})", R.md_table(T[T.period == pn].drop(columns="period").set_index("strategy"), fm), ""]
    eqs = {n: (1 + r).cumprod() for n, r in ens.items()}; R.fig_equity(eqs, out / "equity.png", shade=(a, split, "fuera de muestra") if split else None); md += ["![](equity.png)", ""]
    yr = pd.DataFrame({n: M.yearly(r) for n, r in list(ens.items())[:4]}); R.fig_yearly(yr, out / "yearly.png"); md += ["![](yearly.png)", ""]; R.fig_weights(res.weights, out / "weights.png"); md += ["![](weights.png)", ""]
    if reg:
        md += ["## ¿Está sobreajustada la regla?"]
        if pl:
            for pn, o in pl.items(): md.append(f"- **{pn}**: de {o['cells']} combinaciones mejoran a la cartera sin filtro {o.get('Sharpe_beats_base','—')} en Sharpe, {o.get('CAGR_beats_base','—')} en CAGR y {o.get('MDD_beats_base','—')} en caída máxima. El parámetro elegido es el {o.get('Sharpe_rank','—')}.º en Sharpe y el {o.get('CAGR_rank','—')}.º en CAGR; vecinos inmediatos: CAGR de {P(o['CAGR_neighbors'][0])} a {P(o['CAGR_neighbors'][2])}." if 'CAGR_neighbors' in o else f"- **{pn}**: {o}")
            g0 = G[G.period == "Completo"]; pc = [c for c in g0.columns if c.startswith("regime") or c == "leveraged_weight"]
            if len(pc) == 2:
                g0 = g0.assign(**{pc[1]: g0[pc[1]].astype(str), pc[0]: g0[pc[0]].astype(str)}); R.fig_heatmap(g0, pc[0], pc[1], "Sharpe", out / "grid_sharpe.png", base=float(tf.loc["Misma cartera sin filtro"].Sharpe), chosen=(str(chosen[pc[0]]), str(chosen[pc[1]])), title="Cambio de Sharpe frente a la misma cartera sin filtro"); md += ["", "![](grid_sharpe.png)"]
            md += ["", f"- **PBO** (probabilidad de sobreajuste por CSCV): {over['pbo']['pbo']:.2f}. Por encima de 0,5, elegir el mejor parámetro del pasado no ayuda en el futuro: usa el valor a priori, no el optimizado.",
                   f"- **Reality Check de White** (¿la mejor variante bate a la cartera sin filtro en rentabilidad más de lo esperable por haber buscado?): p = {over['rc']['p_value']:.3f}."]
            if over.get("wf"): w = over["wf"]; md.append(f"- **Walk-forward** (reelegir parámetros cada 2 años con el pasado): Sharpe {w['oos_metric']:.2f} frente a {w['best_fixed_metric_same_period']:.2f} de la mejor variante fija y {w['median_config_metric']:.2f} de la variante mediana.")
        md += ["", "### Placebo", R.md_table(pd.DataFrame({pn: {"CAGR regla": P(o["real"]["CAGR"]), "CAGR placebo": P(o["placebo_median"]["CAGR"]), "p CAGR": f"{o['p']['CAGR']:.3f}", "p Sharpe": f"{o['p']['Sharpe']:.3f}", "p caída": f"{o['p']['MDD']:.3f}", "episodios": o["episodes"]} for pn, o in plc.items()}).T), "", "### Ejecución", R.md_table(ex, {"CAGR": "pct", "Sharpe": "f2", "MDD": "pct1", "cost": "pct1"}, index=False), ""]
    if px is not None: md += ["## Sensibilidad a los proxies", f"Restando rentabilidad anual a las patas reconstruidas ({', '.join(weak)}):", "", R.md_table(px, {"CAGR": "pct", "Sharpe": "f2", "MDD": "pct1"}, index=False), ""]
    md += ["## Significación estadística", f"- Sharpe {ci['point']:.2f}, intervalo de confianza del 95%: {ci['lo']:.2f} a {ci['hi']:.2f}.", f"- Probabilidad de que el Sharpe verdadero sea mayor que 0: {psr0:.3f}.", f"- Sharpe deflactado ({trials} pruebas; Sharpe esperable por azar {over['dsr']['sr0_annual']:.2f}): {over['dsr']['dsr']:.3f}.", f"- Historial mínimo para confirmar Sharpe > 0 al 95%: {mtr:.1f} años.", ""]
    if mc is not None: md += ["## Monte Carlo a 10 años", "Bloques de 12 meses, los mismos para todas las carteras. Subestima caídas intra-mes y solo recombina lo ocurrido en la muestra.", "", R.md_table(mc, {c: "pct1" for c in mc.columns}), ""]
    md += ["## Colas", R.md_table(tails, {"perdida": "pct1"}, index=False), "", "Una señal calculada al cierre y ejecutada al día siguiente no protege de un crash de un solo día.", "", "## Atribución",
           R.md_table(pd.DataFrame({"contribución a la rentabilidad (múltiplos del capital inicial)": ct["by_asset"], "contribución al riesgo": rc, "peso medio": res.weights.mean()}), {"contribución al riesgo": "pct1", "peso medio": "pct1"}), "", f"Ratio de diversificación {dv['ratio']:.2f}; retorno de diversificación ≈ {P(dv['diversification_return'])} al año.", "",
           "## Auditoría metodológica", R.md_table(au, index=False) if len(au) else "Sin hallazgos.", "", "## Limitaciones", "- Los resultados son simulaciones históricas; no garantizan resultados futuros.", "- Las series anteriores al lanzamiento de cada fondo son reconstrucciones (ver procedencia).", "", "Esto no es asesoramiento financiero."]
    (out / "report.md").write_text("\n".join(md)); mo.to_csv(out / "returns_daily.csv"); T.to_csv(out / "metrics.csv", index=False)
    sheets = {"metricas": T, "anual": yr, "colas": tails, "auditoria": au, "procedencia": PN.provenance(bt.cols, a, b)}
    if G is not None: sheets["rejilla"] = G.astype({c: str for c in G.columns if G[c].dtype == object})
    if mc is not None: sheets["montecarlo"] = mc
    try: R.to_excel(out / "report.xlsx", sheets)
    except Exception as e: S["excel_error"] = str(e)
    if make_pdf:
        try: R.md_to_pdf(out / "report.md", out / "report.pdf")
        except Exception as e: S["pdf_error"] = str(e)
    exp_id = None
    if log:
        exp_id = X.log(name, hypothesis, "fpq.research.study", {k: v for k, v in spec.items() if k != "name"}, {**{k: float(me[k]) for k in ("CAGR", "Sharpe", "MDD", "Vol")}, "DSR": over["dsr"]["dsr"]}, period=[str(a.date()), str(b.date())],
                       universe=bt.cols, costs=dict(turnover=bt.tc, switch=(reg or {}).get("cost", 0), tax=bt.tax), conclusion=" ".join(lines), phase="validation", checks=dict(audit=ver, placebo={k: v["p"] for k, v in plc.items()}, pbo=(over.get("pbo") or {}).get("pbo")), artifacts=[str(out)], trials=trials)
    return dict(dir=str(out), verdict=lines, table=T, grid=G, plateau=pl, placebo=plc, overfit=over, audit=au, montecarlo=mc, tails=tails, experiment=exp_id, notes=S)
