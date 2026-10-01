import pymupdf, glob, os
P = "src/lamarholdingpppaipartnerround2assignment/candidate_pack"
for f in sorted(glob.glob(P + "/*.pdf")):
    doc = pymupdf.open(f); name = os.path.basename(f)
    for pno, page in enumerate(doc, 1):
        lines=[]
        for d in page.get_drawings():
            for it in d["items"]:
                if it[0]=="l":
                    p1,p2=it[1],it[2]
                    if abs(p1.y-p2.y)<0.5: lines.append((min(p1.x,p2.x),max(p1.x,p2.x),p1.y))
                elif it[0]=="re":
                    r=it[1]
                    if r.height<1.5 and r.width>5: lines.append((r.x0,r.x1,(r.y0+r.y1)/2))
        for b in page.get_text("dict")["blocks"]:
            if b["type"]!=0: continue
            for ln in b["lines"]:
                for s in ln["spans"]:
                    x0,y0,x1,y1=s["bbox"]
                    mid=(y0+y1)/2; h=y1-y0
                    for (a,bx,y) in lines:
                        if a<x1 and bx>x0 and abs(y-mid)<h*0.2 and s["text"].strip():
                            print("POSSIBLE STRIKE", name, pno, s["text"][:80])
        print(name, pno, "hlines:", len(lines))
