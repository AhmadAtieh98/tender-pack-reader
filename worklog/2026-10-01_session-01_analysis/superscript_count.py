# Throwaway check run in session 01 (inline at the time; saved verbatim). Counts superscript spans and the text before each.
import pymupdf, glob, os
P="src/lamarholdingpppaipartnerround2assignment/candidate_pack"
n=0
for f in sorted(glob.glob(P+"/*.pdf")):
    d=pymupdf.open(f)
    for pno,pg in enumerate(d,1):
        for b in pg.get_text("dict")["blocks"]:
            if b["type"]!=0: continue
            for l in b["lines"]:
                sp=l["spans"]
                for i,s in enumerate(sp):
                    if s["flags"]&1 and s["text"].strip():
                        prev=sp[i-1]["text"][-6:] if i>0 else ""
                        n+=1; print(os.path.basename(f)[:6],"p%d"%pno, repr(prev), "^", repr(s["text"]), round(s["size"],1))
print("total superscript spans:", n)
