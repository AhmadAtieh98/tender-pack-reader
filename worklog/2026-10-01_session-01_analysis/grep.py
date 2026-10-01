import pymupdf, glob, os, re
P = "src/lamarholdingpppaipartnerround2assignment/candidate_pack"
pages=[]
for f in sorted(glob.glob(P + "/*.pdf")):
    doc = pymupdf.open(f); name=os.path.basename(f).split("_")[0]
    for pno, page in enumerate(doc,1):
        lines=[]
        for b in page.get_text("dict")["blocks"]:
            if b["type"]!=0: continue
            for l in b["lines"]:
                if l["dir"]!=(1.0,0.0): continue
                t="".join(s["text"] for s in l["spans"])
                if t.startswith("FICTIONAL DOCUMENT"): continue
                lines.append(t)
        pages.append((name,pno," ".join(lines)))
def find(pat, flags=re.I):
    print(f"\n### /{pat}/")
    for name,pno,t in pages:
        for m in re.finditer(pat,t,flags):
            s=max(0,m.start()-70); print(f"  {name} p{pno}: ...{t[s:m.end()+50]}...")
for pat in [r"local content", r"seventy-two \(72\)", r"sixty per cent|forty per cent", r"Total Nitrogen|\bTN\b", r"one hundred and twenty \(120\)|120-page", r"12 November", r"Proposal Due Date", r"reject|disqualif|non-responsive|disregard|returned unopened|removed before evaluation|own risk|not be scored|forfeit|call the Bid Bond",
            r"Volume III|Drawing|data room|Schedule \d+|Environmental Permit|Direct Agreement|RFQ|Appendix [123AB]",
            r"\bdays?\b"]:
    find(pat)
