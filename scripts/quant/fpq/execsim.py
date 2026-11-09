"""Simulador de ejecución sobre barras diarias OHLCV (sin bróker): órdenes de mercado y limitadas, huecos de apertura,
ejecución parcial por participación en volumen, horquilla, deslizamiento e impacto. Sirve para medir el coste real de operar una señal."""
import numpy as np, pandas as pd
def simulate(bars, orders, spread_bps=2.0, slippage_bps=1.0, max_participation=0.10, impact_k=0.1, vol_window=20, expire_days=5):
    """bars: DataFrame con open, high, low, close, volume (acciones). orders: lista de dicts
    {date, side: 'buy'|'sell', qty, type: 'moc'|'moo'|'limit', limit: precio}. La orden creada en `date` (tras el cierre) entra a mercado el día siguiente.
    Devuelve DataFrame de ejecuciones con precio medio, coste frente al cierre de la señal (implementation shortfall) y % ejecutado."""
    b = bars.copy(); b["sigma"] = b["close"].pct_change().rolling(vol_window).std(); idx = b.index; fills = []
    for o in orders:
        t0 = idx.searchsorted(pd.Timestamp(o["date"]), side="right"); rem = float(o["qty"]); sgn = 1 if o["side"] == "buy" else -1
        ref = b["close"].iloc[t0 - 1] if t0 > 0 else b["open"].iloc[t0]; got = 0.0; paid = 0.0; d = 0; typ = o.get("type", "moc")
        while rem > 1e-9 and t0 + d < len(idx) and d < expire_days:
            x = b.iloc[t0 + d]; cap = max_participation * x["volume"]; q = min(rem, cap)
            base = x["open"] if typ == "moo" else x["close"]
            if typ == "limit":
                lim = o["limit"]; hit = x["low"] <= lim if sgn == 1 else x["high"] >= lim
                if not hit: d += 1; continue
                base = min(lim, x["open"]) if sgn == 1 else max(lim, x["open"])      # si abre con hueco a favor, ejecuta en la apertura
            part = q / x["volume"] if x["volume"] > 0 else 1.0; sig = x["sigma"] if x["sigma"] == x["sigma"] else 0.02
            px = base * (1 + sgn * (spread_bps / 2 + slippage_bps) / 1e4 + sgn * impact_k * sig * np.sqrt(part)) if typ != "limit" else base
            got += q; paid += q * px; rem -= q; d += 1
        avg = paid / got if got > 0 else np.nan
        fills.append(dict(date=o["date"], side=o["side"], qty=o["qty"], filled=got, fill_pct=got / o["qty"], avg_price=avg, ref_close=ref,
                          shortfall_bps=(sgn * (avg / ref - 1) * 1e4) if got > 0 else np.nan, days=d, gap_bps=(b["open"].iloc[t0] / ref - 1) * 1e4 if t0 < len(idx) else np.nan))
    return pd.DataFrame(fills)
def cost_model(notional, adv_notional, sigma_daily, spread_bps=2.0, impact_k=0.1):
    """Coste esperado en puntos básicos de una orden: media horquilla + impacto raíz cuadrada (k·σ·sqrt(participación))."""
    return spread_bps / 2 + impact_k * sigma_daily * np.sqrt(notional / adv_notional) * 1e4
