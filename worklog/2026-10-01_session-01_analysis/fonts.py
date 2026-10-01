import pymupdf, glob, os, collections
P = "src/lamarholdingpppaipartnerround2assignment/candidate_pack"
for f in sorted(glob.glob(P + "/*.pdf")):
    doc = pymupdf.open(f)
    name = os.path.basename(f)
    stats = collections.Counter()
    for pno, page in enumerate(doc, 1):
        d = page.get_text("dict")
        for b in d["blocks"]:
            if b["type"] != 0:
                print(f"{name} p{pno} IMAGE block bbox={[round(x) for x in b['bbox']]}")
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    key = (round(s["size"],1), s["font"], hex(s["color"]), l["dir"] != (1.0, 0.0))
                    stats[key] += 1
                    t = s["text"].strip()
                    # report unusual spans
                    if t and (s["size"] < 8.5 or s["color"] not in (0,) or (s["flags"] & 1)):
                        if s["color"] == 0 and s["size"] >= 8.5: pass
                        print(f"{name} p{pno} size={s['size']:.1f} font={s['font']} color={hex(s['color'])} flags={s['flags']} y={s['bbox'][1]:.0f} dir={tuple(round(x,2) for x in l['dir'])} | {t[:110]}")
        # annotations / links / widgets
        annots = list(page.annots() or [])
        if annots: print(name, pno, "ANNOTS", [a.type for a in annots])
        links = page.get_links()
        if links: print(name, pno, "LINKS", links)
        draws = page.get_drawings()
        fills = [dr for dr in draws if dr.get('fill') not in (None,)]
    print(name, "STYLE SUMMARY:", sorted(stats.items(), key=lambda kv: -kv[1])[:12])
    print(name, "metadata", doc.metadata, "embedded files", doc.embfile_count(), "layers", doc.layer_ui_configs() if hasattr(doc,'layer_ui_configs') else None)
