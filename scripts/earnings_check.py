#!/usr/bin/env python3
"""Veredicto beat/miss/in-line que se niega a comparar bases distintas.

Entrada JSON:
{"ticker":"XYZ","period":"Q3 FY2026","metrics":[
  {"name":"EPS","basis":"adjusted","actual":1.23,"consensus":1.10,"consensus_basis":"adjusted","consensus_source":"LSEG 2026-11-04"},
  {"name":"Revenue","basis":"reported","actual":2450,"consensus":2400,"unit":"USD M"}]}
basis: gaap | adjusted | reported. Si consensus_basis falta, se asume igual a basis
(y se avisa). Si difieren, la métrica se marca NO_COMPARABLE.
"""
import argparse, json, sys

def verdict(m, inline_pct, eps_abs):
    a, c = m.get("actual"), m.get("consensus")
    basis = (m.get("basis") or "").lower()
    cb = (m.get("consensus_basis") or basis).lower()
    warn = []
    if m.get("consensus_basis") is None and c is not None:
        warn.append("consensus_basis no indicado: se asume igual a basis; verifícalo")
    if c is None:
        return dict(verdict="SIN_CONSENSO", diff=None, diff_pct=None, warnings=warn + ["no hay consenso para esta base: no emitir beat/miss"])
    if basis != cb:
        return dict(verdict="NO_COMPARABLE", diff=None, diff_pct=None, warnings=warn + [f"base real '{basis}' vs consenso '{cb}': comparación inválida"])
    diff = a - c
    pct = diff / abs(c) if c else None
    is_eps = "eps" in m.get("name", "").lower()
    if is_eps:
        thr_hit = abs(diff) <= max(eps_abs, abs(c) * 0.02)
    else:
        thr_hit = pct is not None and abs(pct) <= inline_pct
    v = "IN_LINE" if thr_hit else ("BEAT" if diff > 0 else "MISS")
    if is_eps and c < 0:
        warn.append("consenso negativo: 'beat' = pérdida menor de lo esperado")
    return dict(verdict=v, diff=diff, diff_pct=pct, warnings=warn)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", required=True)
    ap.add_argument("--inline-pct", type=float, default=0.01)
    ap.add_argument("--eps-abs", type=float, default=0.01)
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.json))
    rows = []
    for m in data["metrics"]:
        r = verdict(m, a.inline_pct, a.eps_abs)
        rows.append({**m, **r})
    if a.markdown:
        print(f"**{data.get('ticker','')} {data.get('period','')}**\n")
        print("| Métrica | Base | Real | Consenso (fuente) | Dif. | Veredicto |\n|---|---|---|---|---|---|")
        for r in rows:
            d = "" if r["diff"] is None else (f"{r['diff']:+.4g}" + (f" ({r['diff_pct']:+.1%})" if r["diff_pct"] is not None else ""))
            cons = "—" if r.get("consensus") is None else f"{r['consensus']} ({r.get('consensus_source','fuente?')})"
            print(f"| {r['name']} | {r.get('basis')} | {r.get('actual')} | {cons} | {d} | {r['verdict']} |")
        ws = [f"- {r['name']} ({r.get('basis')}): {w}" for r in rows for w in r["warnings"]]
        if ws:
            print("\nAvisos:\n" + "\n".join(ws))
    else:
        print(json.dumps({"ticker": data.get("ticker"), "period": data.get("period"), "results": rows}, indent=2, ensure_ascii=False))
    if any(r["verdict"] == "NO_COMPARABLE" for r in rows):
        sys.exit(2)

if __name__ == "__main__":
    main()
