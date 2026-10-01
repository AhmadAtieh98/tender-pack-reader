import pymupdf, glob, os
P = "src/lamarholdingpppaipartnerround2assignment/candidate_pack"
for f in sorted(glob.glob(P + "/*.pdf")):
    doc = pymupdf.open(f); name = os.path.basename(f)
    for pno, page in enumerate(doc, 1):
        a = [x.type for x in page.annots()] ; l = page.get_links(); w = list(page.widgets())
        # white text not over a dark fill
        fills = [d for d in page.get_drawings() if d.get("fill") and sum(d["fill"])/3 < 0.5]
        for b in page.get_text("dict")["blocks"]:
            if b["type"]!=0: continue
            for ln in b["lines"]:
                for s in ln["spans"]:
                    if s["color"]==0xffffff and s["text"].strip():
                        r = pymupdf.Rect(s["bbox"])
                        if not any(pymupdf.Rect(d["rect"]).contains(r) or pymupdf.Rect(d["rect"]).intersects(r) for d in fills):
                            print("WHITE TEXT NOT ON DARK FILL", name, pno, s["text"])
                    if not page.rect.contains(pymupdf.Rect(s["bbox"])) and s["text"].strip():
                        print("OFFPAGE", name, pno, s["text"][:60])
        if a or l or w: print(name, pno, "annots", a, "links", l, "widgets", w)
        imgs = page.get_images(full=True)
        for im in imgs:
            print(name, pno, "image xref", im[0], "bbox", [round(x) for x in page.get_image_bbox(im)])
    print(name, "pages", doc.page_count, "toc", doc.get_toc(), "embedded", doc.embfile_count(), "has_xfa/forms", doc.is_form_pdf)
