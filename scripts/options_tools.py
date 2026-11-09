#!/usr/bin/env python3
"""Herramientas de opciones sin dependencias: Black-Scholes-Merton, griegas, IV,
binomial americana (CRR), análisis de covered calls y expected move de eventos.

Convenciones: T en días naturales (--T-days) convertido a años /365; r y q continuos
anuales en decimal; iv en decimal (0.85 = 85 %). Theta por día natural; vega y rho por
1 punto porcentual (0.01)."""
import argparse, csv, json, math, sys

SQ2 = math.sqrt(2.0)

def ncdf(x):
    return 0.5 * (1.0 + math.erf(x / SQ2))

def npdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

def bs(S, K, T, r, q, iv, typ):
    if T <= 0 or iv <= 0:
        intrinsic = max(0.0, S - K) if typ == "call" else max(0.0, K - S)
        return dict(price=intrinsic, delta=(1.0 if (typ == "call" and S > K) else (-1.0 if typ == "put" and S < K else 0.0)),
                    gamma=0.0, vega=0.0, theta=0.0, rho=0.0, d1=float("nan"), d2=float("nan"), prob_itm=float(intrinsic > 0))
    st = iv * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * iv * iv) * T) / st
    d2 = d1 - st
    dfq, dfr = math.exp(-q * T), math.exp(-r * T)
    if typ == "call":
        price = S * dfq * ncdf(d1) - K * dfr * ncdf(d2)
        delta = dfq * ncdf(d1)
        theta = (-S * dfq * npdf(d1) * iv / (2 * math.sqrt(T)) - r * K * dfr * ncdf(d2) + q * S * dfq * ncdf(d1)) / 365
        rho = K * T * dfr * ncdf(d2) / 100
        p_itm = ncdf(d2)
    else:
        price = K * dfr * ncdf(-d2) - S * dfq * ncdf(-d1)
        delta = -dfq * ncdf(-d1)
        theta = (-S * dfq * npdf(d1) * iv / (2 * math.sqrt(T)) + r * K * dfr * ncdf(-d2) - q * S * dfq * ncdf(-d1)) / 365
        rho = -K * T * dfr * ncdf(-d2) / 100
        p_itm = ncdf(-d2)
    gamma = dfq * npdf(d1) / (S * st)
    vega = S * dfq * npdf(d1) * math.sqrt(T) / 100
    return dict(price=price, delta=delta, gamma=gamma, vega=vega, theta=theta, rho=rho, d1=d1, d2=d2, prob_itm=p_itm)

def implied_vol(price, S, K, T, r, q, typ, lo=1e-4, hi=10.0):
    intrinsic = max(0.0, S * math.exp(-q * T) - K * math.exp(-r * T)) if typ == "call" else max(0.0, K * math.exp(-r * T) - S * math.exp(-q * T))
    if price < intrinsic - 1e-9:
        raise ValueError(f"Precio {price} por debajo del valor intrínseco descontado {intrinsic:.4f}")
    f = lambda v: bs(S, K, T, r, q, v, typ)["price"] - price
    if f(hi) < 0:
        raise ValueError("No hay IV < 1000 % que reproduzca el precio")
    # Newton con salvaguarda de bisección
    v = 0.5
    for _ in range(100):
        g = bs(S, K, T, r, q, v, typ)
        diff = g["price"] - price
        if abs(diff) < 1e-8:
            return v
        vega = g["vega"] * 100
        if diff > 0:
            hi = min(hi, v)
        else:
            lo = max(lo, v)
        nv = v - diff / vega if vega > 1e-10 else (lo + hi) / 2
        v = nv if lo < nv < hi else (lo + hi) / 2
    return v

def binomial(S, K, T, r, q, iv, typ, steps=500, american=True):
    dt = T / steps
    u = math.exp(iv * math.sqrt(dt)); d = 1 / u
    a = math.exp((r - q) * dt)
    p = (a - d) / (u - d)
    disc = math.exp(-r * dt)
    vals = []
    for j in range(steps + 1):
        st = S * (u ** j) * (d ** (steps - j))
        vals.append(max(0.0, st - K) if typ == "call" else max(0.0, K - st))
    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            cont = disc * (p * vals[j + 1] + (1 - p) * vals[j])
            if american:
                st = S * (u ** j) * (d ** (i - j))
                ex = max(0.0, st - K) if typ == "call" else max(0.0, K - st)
                cont = max(cont, ex)
            vals[j] = cont
    return vals[0]

def annualize(ret, days):
    return (1 + ret) ** (365.0 / days) - 1 if days > 0 else float("nan")

def covered_call(S, K, T_days, premium, r, q, iv, basis=None):
    T = T_days / 365
    g = bs(S, K, T, r, q, iv, "call") if iv else None
    static = premium / S
    called = (premium + (K - S)) / S
    out = {
        "prima": premium,
        "rend_estatico": static, "rend_estatico_anual": annualize(static, T_days),
        "rend_si_asignada": called, "rend_si_asignada_anual": annualize(called, T_days),
        "breakeven": S - premium,
        "proteccion_bajista_pct": premium / S,
        "upside_cedido_desde_K": "todo lo que supere K=%.2f" % K,
    }
    if g:
        out.update({"delta": g["delta"], "prob_asignacion_rn(N(d2))": g["prob_itm"], "precio_teorico_BS": g["price"],
                    "theta_dia": -g["theta"], "vega_1pt": g["vega"]})
        out["iv_implicita_de_la_prima"] = implied_vol(premium, S, K, T, r, q, "call") if premium > max(0, S - K) else None
    if basis:
        out["resultado_si_asignada_vs_coste"] = (K + premium - basis) / basis
    return out

def fmt(d):
    return json.dumps(d, indent=2, ensure_ascii=False, default=lambda x: round(x, 6))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    def common(p, need_iv=True):
        p.add_argument("--S", type=float, required=True); p.add_argument("--K", type=float, required=True)
        p.add_argument("--T-days", type=float, required=True); p.add_argument("--r", type=float, default=0.04)
        p.add_argument("--q", type=float, default=0.0)
        if need_iv: p.add_argument("--iv", type=float, required=True)
        p.add_argument("--type", choices=["call", "put"], default="call")
    common(sub.add_parser("bs"))
    p = sub.add_parser("iv"); common(p, need_iv=False); p.add_argument("--price", type=float, required=True)
    p = sub.add_parser("binomial"); common(p); p.add_argument("--steps", type=int, default=500); p.add_argument("--european", action="store_true")
    p = sub.add_parser("covered-call")
    for a in ("S", "K", "T-days", "premium"): p.add_argument("--" + a, type=float, required=True)
    p.add_argument("--r", type=float, default=0.04); p.add_argument("--q", type=float, default=0.0)
    p.add_argument("--iv", type=float, default=None); p.add_argument("--basis", type=float, default=None)
    p = sub.add_parser("cc-chain", help="CSV con strike,bid,ask[,iv]")
    p.add_argument("--S", type=float, required=True); p.add_argument("--T-days", type=float, required=True)
    p.add_argument("--r", type=float, default=0.04); p.add_argument("--q", type=float, default=0.0)
    p.add_argument("--csv", required=True); p.add_argument("--target-delta", type=float, default=0.25)
    p = sub.add_parser("event-move")
    p.add_argument("--S", type=float, required=True); p.add_argument("--straddle", type=float, required=True)
    p.add_argument("--hist", default="", help="movimientos históricos en eventos, decimales separados por coma (ej. 0.32,-0.55)")
    p = sub.add_parser("forward-vol", help="IV de evento aislada entre dos vencimientos")
    p.add_argument("--iv1", type=float, required=True); p.add_argument("--t1-days", type=float, required=True)
    p.add_argument("--iv2", type=float, required=True); p.add_argument("--t2-days", type=float, required=True)
    p.add_argument("--normal-iv", type=float, default=None, help="IV 'normal' sin evento para aislar la varianza del evento")
    a = ap.parse_args()

    if a.cmd == "bs":
        print(fmt(bs(a.S, a.K, a.T_days / 365, a.r, a.q, a.iv, a.type)))
    elif a.cmd == "iv":
        v = implied_vol(a.price, a.S, a.K, a.T_days / 365, a.r, a.q, a.type)
        print(fmt({"iv": v, "check_price": bs(a.S, a.K, a.T_days / 365, a.r, a.q, v, a.type)["price"]}))
    elif a.cmd == "binomial":
        T = a.T_days / 365
        am = binomial(a.S, a.K, T, a.r, a.q, a.iv, a.type, a.steps, not a.european)
        eu = bs(a.S, a.K, T, a.r, a.q, a.iv, a.type)["price"]
        print(fmt({"precio_binomial": am, "americana": not a.european, "bs_europea": eu, "prima_ejercicio_anticipado": am - eu}))
    elif a.cmd == "covered-call":
        print(fmt(covered_call(a.S, a.K, a.T_days, a.premium, a.r, a.q, a.iv, a.basis)))
    elif a.cmd == "cc-chain":
        rows = []
        with open(a.csv) as fh:
            for row in csv.DictReader(fh):
                K = float(row["strike"]); bid = float(row["bid"]); ask = float(row["ask"]); mid = (bid + ask) / 2
                T = a.T_days / 365
                try:
                    iv = float(row["iv"]) if row.get("iv") else implied_vol(mid, a.S, K, T, a.r, a.q, "call")
                except ValueError:
                    continue
                g = bs(a.S, K, T, a.r, a.q, iv, "call")
                rows.append(dict(strike=K, bid=bid, ask=ask, mid=mid, spread_pct=(ask - bid) / mid if mid else None, iv=iv,
                                 delta=g["delta"], p_itm=g["prob_itm"], rend_estatico_anual=annualize(bid / a.S, a.T_days),
                                 rend_asignada_anual=annualize((bid + K - a.S) / a.S, a.T_days)))
        rows.sort(key=lambda x: abs(x["delta"] - a.target_delta))
        print(fmt({"mas_cercano_a_delta_objetivo": rows[0] if rows else None, "cadena": sorted(rows, key=lambda x: x["strike"])}))
        print("Nota: rendimientos con el BID (lo que realmente cobras vendiendo a mercado).", file=sys.stderr)
    elif a.cmd == "event-move":
        em = a.straddle / a.S
        out = {"expected_move_pct": em, "rango_1sigma_aprox": [a.S * (1 - em), a.S * (1 + em)]}
        if a.hist:
            h = [abs(float(x)) for x in a.hist.split(",") if x.strip()]
            h_sorted = sorted(h)
            med = h_sorted[len(h) // 2] if len(h) % 2 else (h_sorted[len(h) // 2 - 1] + h_sorted[len(h) // 2]) / 2
            out.update({"hist_n": len(h), "hist_media_abs": sum(h) / len(h), "hist_mediana_abs": med,
                        "ratio_implicito_vs_media": em / (sum(h) / len(h)), "ratio_implicito_vs_mediana": em / med,
                        "lectura": "ratio > 1: opciones caras vs historia; < 1: baratas (muestra pequeña: cautela)"})
        print(fmt(out))
    elif a.cmd == "forward-vol":
        t1, t2 = a.t1_days / 365, a.t2_days / 365
        var_fwd = a.iv2 ** 2 * t2 - a.iv1 ** 2 * t1
        out = {"varianza_forward_total": var_fwd,
               "iv_forward_anualizada": math.sqrt(var_fwd / (t2 - t1)) if var_fwd > 0 else None}
        if a.normal_iv is not None:
            ev = a.iv2 ** 2 * t2 - a.normal_iv ** 2 * t2
            out["varianza_evento"] = ev
            out["movimiento_evento_1sigma_pct"] = math.sqrt(ev) if ev > 0 else None
        print(fmt(out))

if __name__ == "__main__":
    main()
