import pymupdf, glob, os, collections
P = "src/lamarholdingpppaipartnerround2assignment/candidate_pack"
for f in sorted(glob.glob(P + "/*.pdf")):
    doc = pymupdf.open(f); name = os.path.basename(f)[:6]
    for pno, page in enumerate(doc, 1):
        d = page.get_text("dict")
        for b in d["blocks"]:
            if b["type"] != 0: continue
            for l in b["lines"]:
                for s in l["spans"]:
                    t = s["text"].strip()
                    if not t: continue
                    hdr = s["color"] == 0x5a5a5a or t.startswith("FICTIONAL DOCUMENT") 
                    wm = l["dir"] != (1.0, 0.0)
                    if hdr or wm: continue
                    unusual = s["size"] < 8.2 or s["color"] not in (0x1a1a1a, 0xffffff) or (s["flags"] & 1)
                    if unusual:
                        print(f"{name} p{pno} size={s['size']:.1f} {s['font']} col={hex(s['color'])} sup={s['flags']&1} y={s['bbox'][1]:.0f} x={s['bbox'][0]:.0f} | {t[:120]}")
    # watermark text and rotated
    wmset=set()
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b["type"]!=0: continue
            for l in b["lines"]:
                if l["dir"]!=(1.0,0.0):
                    wmset.add("".join(s["text"] for s in l["spans"]))
    print(name, "rotated text:", wmset)
