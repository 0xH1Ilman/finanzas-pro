"""Informes: gráficos, Markdown, Excel y PDF. Todo informe distingue datos observados, reconstruidos y sintéticos (tabla de procedencia)."""
import pathlib, re, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
PAL = ["#b8860b", "#4c72b0", "#333333", "#999999", "#c44e52", "#55a868", "#8172b3"]
def _style(ax):
    ax.spines[["top", "right"]].set_visible(False); ax.grid(alpha=.2, lw=.6); ax.tick_params(labelsize=8)
def fig_equity(series, path, title="Crecimiento de 10.000", shade=None):
    """series: dict nombre → Serie de equity (base 1). shade: (inicio, fin, etiqueta) para marcar un tramo (p. ej. fuera de muestra)."""
    fig, ax = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={"height_ratios": [3, 1.5]}, sharex=True)
    for i, (n, s) in enumerate(series.items()):
        ax[0].plot(s.index, s * 10000, label=n, color=PAL[i % len(PAL)], lw=1.7 if i == 0 else 1.1); ax[1].plot(s.index, (s / s.cummax() - 1) * 100, color=PAL[i % len(PAL)], lw=.9)
    ax[0].set_yscale("log"); ax[0].legend(frameon=False, fontsize=8); ax[0].set_title(title, loc="left", fontsize=10); ax[1].set_title("Caída desde máximos (%)", loc="left", fontsize=9)
    if shade: ax[0].axvspan(pd.Timestamp(shade[0]), pd.Timestamp(shade[1]), color="#f3e9c6", alpha=.5); ax[0].text(pd.Timestamp(shade[0]), ax[0].get_ylim()[1] * .5, " " + shade[2], fontsize=8, va="top")
    for a in ax: _style(a)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig); return str(path)
def fig_yearly(table, path, title="Rentabilidad por año (%)"):
    fig, ax = plt.subplots(figsize=(10, 3.4)); n = table.shape[1]; x = np.arange(len(table))
    for i, c in enumerate(table.columns): ax.bar(x + (i - (n - 1) / 2) * 0.8 / n, table[c] * 100, 0.8 / n, label=c, color=PAL[i % len(PAL)])
    ax.set_xticks(x); ax.set_xticklabels(table.index, rotation=90, fontsize=7); ax.axhline(0, color="#333", lw=.6); ax.legend(frameon=False, fontsize=8); ax.set_title(title, loc="left", fontsize=10); _style(ax)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig); return str(path)
def fig_heatmap(g, row, col, value, path, base=None, chosen=None, title="", fmt="{:+.2f}"):
    """Mapa de una rejilla (DataFrame de validate.grid filtrado a un periodo). Si base se da, colorea la diferencia frente a la base."""
    pv = g.pivot(index=row, columns=col, values=value); Mx = pv.values - (base if base is not None else 0); lim = np.nanmax(np.abs(Mx)) or 1
    fig, ax = plt.subplots(figsize=(1.6 + 1.2 * pv.shape[1], 1.2 + 0.5 * pv.shape[0])); ax.imshow(Mx, cmap="RdYlGn", vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(pv.shape[1])); ax.set_xticklabels([str(c) for c in pv.columns], fontsize=8); ax.set_yticks(range(pv.shape[0])); ax.set_yticklabels([str(r) for r in pv.index], fontsize=8); ax.set_xlabel(col, fontsize=8); ax.set_ylabel(row, fontsize=8)
    for i in range(pv.shape[0]):
        for j in range(pv.shape[1]):
            ch = chosen is not None and pv.index[i] == chosen[0] and pv.columns[j] == chosen[1]; ax.text(j, i, fmt.format(Mx[i, j]), ha="center", va="center", fontsize=8, fontweight="bold" if ch else None)
            if ch: ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, lw=2))
    ax.set_title(title, loc="left", fontsize=9); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig); return str(path)
def fig_weights(W, path, title="Pesos efectivos de la cartera"):
    fig, ax = plt.subplots(figsize=(10, 3.2)); m = W.resample("ME").last(); ax.stackplot(m.index, m.values.T * 100, labels=m.columns, colors=PAL[:m.shape[1]], alpha=.9)
    ax.legend(frameon=False, fontsize=8, ncol=m.shape[1], loc="upper center"); ax.set_ylim(0, 100); ax.set_title(title, loc="left", fontsize=10); _style(ax); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig); return str(path)
def fig_hist(values, path, title, mark=None, xlabel=""):
    fig, ax = plt.subplots(figsize=(6, 3)); ax.hist(values, bins=40, color="#999999")
    if mark is not None: ax.axvline(mark, color="#b8860b", lw=2)
    ax.set_title(title, loc="left", fontsize=10); ax.set_xlabel(xlabel, fontsize=8); _style(ax); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig); return str(path)
def pct(x, d=2): return "—" if x is None or x != x else f"{x*100:.{d}f}%"
def md_table(df, fmts=None, index=True):
    """DataFrame → tabla Markdown. fmts: {columna: función o 'pct'|'pct1'|'f2'|'int'}."""
    F = {"pct": lambda v: pct(v), "pct1": lambda v: pct(v, 1), "f2": lambda v: f"{v:.2f}", "f3": lambda v: f"{v:.3f}", "int": lambda v: f"{int(v)}"}; d = df.reset_index() if index else df
    def cell(c, v):
        f = (fmts or {}).get(c); f = F.get(f, f) if isinstance(f, str) else f
        try: return f(v) if f else (f"{v:.4g}" if isinstance(v, (float, np.floating)) else str(v))
        except Exception: return str(v)
    out = ["| " + " | ".join(map(str, d.columns)) + " |", "|" + "---|" * len(d.columns)] + ["| " + " | ".join(cell(c, v) for c, v in zip(d.columns, row)) + " |" for row in d.values]
    return "\n".join(out)
def to_excel(path, sheets):
    """sheets: {nombre de hoja: DataFrame}."""
    with pd.ExcelWriter(path) as xw:
        for n, d in sheets.items(): d.to_excel(xw, sheet_name=n[:31])
    return str(path)
def md_to_pdf(md_path, pdf_path):
    """Convierte un informe Markdown sencillo (títulos, párrafos, listas, tablas e imágenes) a PDF con reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    ss = getSampleStyleSheet(); body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=9, leading=12); cellst = ParagraphStyle("c", parent=body, fontSize=7, leading=8.5)
    esc = lambda t: re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>", re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")))
    flow = []; lines = pathlib.Path(md_path).read_text().splitlines(); i = 0; base = pathlib.Path(md_path).parent; width = A4[0] - 80
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[-| :]+\|$", lines[i]): rows.append([Paragraph(esc(c.strip()), cellst) for c in lines[i].strip("|").split("|")])
                i += 1
            t = Table(rows, repeatRows=1, colWidths=[width / len(rows[0])] * len(rows[0])); t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .3, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke), ("VALIGN", (0, 0), (-1, -1), "TOP")])); flow += [t, Spacer(1, 8)]; continue
        m = re.match(r"!\[.*?\]\((.+?)\)", ln)
        if m:
            p = base / m.group(1)
            if p.exists():
                im = Image(str(p)); r = im.imageHeight / im.imageWidth; im.drawWidth = width; im.drawHeight = width * r; flow += [im, Spacer(1, 6)]
        elif ln.startswith("# "): flow.append(Paragraph(esc(ln[2:]), ss["Title"]))
        elif ln.startswith("## "): flow.append(Paragraph(esc(ln[3:]), ss["Heading2"]))
        elif ln.startswith("### "): flow.append(Paragraph(esc(ln[4:]), ss["Heading3"]))
        elif ln.startswith("- "): flow.append(Paragraph("• " + esc(ln[2:]), body))
        elif ln.strip(): flow.append(Paragraph(esc(ln), body))
        else: flow.append(Spacer(1, 5))
        i += 1
    SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40).build(flow); return str(pdf_path)
