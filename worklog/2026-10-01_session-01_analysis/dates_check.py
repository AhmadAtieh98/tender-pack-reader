# Throwaway check run in session 01 (inline in the shell at the time; saved here verbatim for the record).
from datetime import date, timedelta as td
def wd(d): return d.weekday() in (6,0,1,2,3)  # Sun..Thu
for s in ["2026-09-14","2026-09-30","2026-10-01","2026-10-08","2026-10-22","2026-11-12","2026-11-26","2026-09-23","2026-09-25","2026-10-05"]:
    d=date.fromisoformat(s); print(s, d.strftime("%A"))
def back_wd(d,n):
    c=0; x=d
    while c<n:
        x-=td(1)
        if wd(x): c+=1
    return x
def fwd_wd(d,n):
    c=0; x=d
    while c<n:
        x+=td(1)
        if wd(x): c+=1
    return x
for pdd in [date(2026,11,12), date(2026,11,26)]:
    print("PDD",pdd,"clar cutoff (10WD back, excl stated date):",back_wd(pdd,10), "| bid bond +180d:", pdd+td(180), "| validity +150d:", pdd+td(150), "| look-back -10y:", pdd.replace(year=pdd.year-10))
print("Add1 +5WD:", fwd_wd(date(2026,10,8),5))
print("WDs from 22 Oct to 26 Nov (excl both):", sum(1 for i in range(1,(date(2026,11,26)-date(2026,10,22)).days) if wd(date(2026,10,22)+td(i))))
print("cal days 22 Oct->26 Nov:", (date(2026,11,26)-date(2026,10,22)).days)
print("cal days 8 Oct->22 Oct:", (date(2026,10,22)-date(2026,10,8)).days)
