import pymupdf, glob, os, collections
P = "src/lamarholdingpppaipartnerround2assignment/candidate_pack"
for f in sorted(glob.glob(P + "/*.pdf")):
    doc = pymupdf.open(f); name=os.path.basename(f).split("_")[0]
    for pno, page in enumerate(doc,1):
        c=collections.Counter()
        for d in page.get_drawings():
            fill = tuple(round(x,2) for x in d["fill"]) if d.get("fill") else None
            col = tuple(round(x,2) for x in d["color"]) if d.get("color") else None
            c[(d["type"], fill, col)] += 1
        print(name, pno, dict(c))
