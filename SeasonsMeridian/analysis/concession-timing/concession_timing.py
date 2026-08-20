#!/usr/bin/env python3
"""Seasons at Meridian — concession timing reconciliation.

Reproduces the tables in CONCESSION_TIMING_ANALYSIS.md: reconciles the T12
concession GL line against the Yardi Concession Burn Off reports and HelloData,
showing that concessions in the recent T12 months are the delayed posting of
leases signed Feb–Apr 2026 (no lease signed since 4/27/2026 has a concession).

Source documents live on branch claude/seasons-meridian-rent-roll-rinebr under
SeasonsMeridian/documents/. Run from the repo root:

    python3 SeasonsMeridian/analysis/concession-timing/concession_timing.py

Requires: openpyxl, pandas.
"""

import datetime as dt
import subprocess
import tarfile
import tempfile
from pathlib import Path

import openpyxl
import pandas as pd

DOCS_BRANCH = "origin/claude/seasons-meridian-rent-roll-rinebr"
DOCS_PREFIX = "SeasonsMeridian/documents"
RENEWAL_THRESHOLD_DAYS = 45  # lease start > move-in + 45d => renewal


def fetch_documents() -> Path:
    """Extract the source documents from the rent-roll branch into a temp dir."""
    tmp = Path(tempfile.mkdtemp(prefix="sm-concessions-"))
    tar_path = tmp / "docs.tar"
    with open(tar_path, "wb") as f:
        subprocess.run(
            ["git", "archive", DOCS_BRANCH, DOCS_PREFIX],
            check=True, stdout=f,
        )
    with tarfile.open(tar_path) as tar:
        tar.extractall(tmp)
    return tmp / DOCS_PREFIX


def parse_date(s):
    if not s:
        return None
    s = str(s).replace("*", "").strip()  # asterisk = mid-month start footnote
    try:
        return dt.datetime.strptime(s, "%m/%d/%Y").date()
    except ValueError:
        return None


def parse_burnoff(path: Path) -> pd.DataFrame:
    """Parse the main table of a Yardi Concession Burn Off report."""
    ws = openpyxl.load_workbook(path, data_only=True)["Report1"]
    rows = list(ws.iter_rows(values_only=True))
    recs = []
    for r in rows[6:]:
        if r[0] == "Totals":
            break
        if r[0] is None or r[2] is None:
            continue
        recs.append(dict(
            unit=r[0], utype=r[1], res=r[2], name=r[3],
            movein=parse_date(r[4]), leasestart=parse_date(r[5]),
            tot_conc=float(r[6] or 0), cur_conc=float(r[7] or 0),
            conc_rem=float(r[8] or 0), conc_end=parse_date(r[9]),
            term=r[10], mkt=r[11], leaserent=r[12], cur_month=float(r[13] or 0),
        ))
    return pd.DataFrame(recs)


def parse_burnoff_projection(path: Path) -> pd.DataFrame:
    """Parse the 'Projection by Unit' section (forward monthly postings)."""
    ws = openpyxl.load_workbook(path, data_only=True)["Report1"]
    rows = list(ws.iter_rows(values_only=True))
    start = next(i for i, r in enumerate(rows)
                 if r[0] and "Projection" in str(r[0]))
    header = rows[start + 1]
    months = [h for h in header[4:] if h]
    recs = []
    for r in rows[start + 2:]:
        if r[0] == "Totals":
            break
        if r[0] is None:
            continue
        vals = [float(str(v).replace(",", "") or 0) for v in r[4:4 + len(months)]]
        recs.append(dict(unit=r[0], res=r[2], **dict(zip(months, vals))))
    return pd.DataFrame(recs)


def t12_concessions(path: Path) -> pd.Series:
    """Concession GL line (4460-0000) by month from a Yardi 12-month statement."""
    ws = openpyxl.load_workbook(path, data_only=True)["Report1"]
    rows = list(ws.iter_rows(values_only=True))
    header = next(r for r in rows if r[2] and str(r[2]).startswith("Jul"))
    line = next(r for r in rows if r[0] == "4460-0000")
    return pd.Series(line[2:14], index=header[2:14], name="T12 concessions")


def main():
    docs = fetch_documents()

    print("=" * 70)
    print("T12 concession line (4460-0000), Jul 2025 - Jun 2026")
    print("=" * 70)
    t12 = t12_concessions(docs / "t12/T12_Jul2025-Jun2026.xlsx")
    print(t12.map("{:,.0f}".format).to_string())

    b621 = parse_burnoff(docs / "concession-burnoff/ConcessionBurnOff_AsOf_2026-06-21.xlsx")
    b730 = parse_burnoff(docs / "concession-burnoff/ConcessionBurnOff_AsOf_2026-07-30.xlsx")

    print("\nTie-out: 6/21 burn-off 'Current Month' (= Jun 2026 postings, current "
          f"residents): ${b621.cur_month.sum():,.0f}  vs T12 Jun 2026: "
          f"${t12.iloc[11]:,.0f}")

    print("\n" + "=" * 70)
    print("Forward projection (7/30 burn-off, existing leases only)")
    print("=" * 70)
    proj = parse_burnoff_projection(
        docs / "concession-burnoff/ConcessionBurnOff_AsOf_2026-07-30.xlsx")
    totals = proj.drop(columns=["unit", "res"]).sum()
    print(totals[totals != 0].map("{:,.0f}".format).to_string())
    print("(all later months project to $0 — fully burned off)")

    # --- new leases vs renewals ---
    df = b730[b730.leasestart.notna() & b730.movein.notna()].copy()
    df["renewal"] = df.apply(
        lambda r: (r.leasestart - r.movein).days > RENEWAL_THRESHOLD_DAYS, axis=1)
    ren = df[df.renewal]
    print(f"\nRenewals: {len(ren)} total, {(ren.cur_conc < 0).sum()} with a "
          f"concession (${-ren.cur_conc.sum():,.0f} total)")

    new = df[~df.renewal].copy()
    new["ls_month"] = new.leasestart.map(lambda d: f"{d.year}-{d.month:02d}")
    new["hasconc"] = new.cur_conc < 0

    print("\n" + "=" * 70)
    print("New leases by MOVE-IN month (current residents, 7/30 burn-off)")
    print("=" * 70)
    g = new[new.ls_month >= "2025-11"].groupby("ls_month").agg(
        leases=("res", "count"), with_conc=("hasconc", "sum"),
        conc_total=("cur_conc", "sum"))
    g["freq"] = (g.with_conc / g.leases * 100).round(0).astype(int).astype(str) + "%"
    g["avg_conc"] = (-g.conc_total / g.with_conc.replace(0, pd.NA)).round(0)
    print(g.drop(columns="conc_total").to_string())

    # --- cross-tab vs HelloData by signing (off-market) month ---
    hd = pd.read_csv(docs / "hellodata/HelloData_UnitDetails_2026-08-12.csv")
    hd["off"] = pd.to_datetime(hd["Off Market Date"])

    matched = []
    movers = new[(new.movein >= dt.date(2026, 1, 1)) &
                 (new.movein <= dt.date(2026, 7, 30))]
    for _, r in movers.iterrows():
        ep = hd[(hd.Unit == r.unit) &
                (hd.off <= pd.Timestamp(r.movein) + pd.Timedelta(days=5)) &
                (hd.off >= pd.Timestamp(r.movein) - pd.Timedelta(days=150))]
        if not len(ep):
            continue
        ep = ep.sort_values("off").iloc[-1]
        hd_conc = 1 - ep["Last Effective Rent"] / ep["Last Asking Rent"]
        matched.append(dict(
            unit=r.unit, movein=r.movein, sign=ep.off.date(),
            lag_days=(pd.Timestamp(r.movein) - ep.off).days,
            yardi_conc=-r.cur_conc, hd_says=hd_conc > 0.001,
            yardi_says=r.cur_conc < 0))
    m = pd.DataFrame(matched)
    m["sign_m"] = m.sign.map(lambda d: f"{d.year}-{d.month:02d}")

    print("\n" + "=" * 70)
    print(f"HelloData vs Yardi by SIGNING month ({len(m)} matched 2026 move-ins)")
    print("=" * 70)
    ct = m.groupby("sign_m").apply(lambda g: pd.Series({
        "n": len(g),
        "HD_conc": int(g.hd_says.sum()),
        "Yardi_conc": int(g.yardi_says.sum()),
        "both": int((g.hd_says & g.yardi_says).sum()),
        "HD_only": int((g.hd_says & ~g.yardi_says).sum()),
        "Yardi_only": int((~g.hd_says & g.yardi_says).sum()),
    }), include_groups=False)
    print(ct.to_string())

    conceding = m[m.yardi_says]
    last_sign = conceding.sign.max()
    print(f"\nLast concession-bearing signing: {last_sign}")
    print(f"Signing -> move-in lag among conceding leases: median "
          f"{conceding.lag_days.median():.0f} days, max {conceding.lag_days.max()} days")
    print(f"Avg Yardi concession among conceding 2026 new leases: "
          f"${conceding.yardi_conc.mean():,.0f}")


if __name__ == "__main__":
    main()
