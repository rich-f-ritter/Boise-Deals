# Appendix E — Trailing-3-Month Employment Calculations
*Computed August 13, 2026 directly from raw BLS CES flat files (`download.bls.gov/pub/time.series/sm/sm.data.13.Idaho` and `sm.data.54.TotalNonFarm.All`) and FRED (`BOIS216LFN`, `BOIS216URN`, `PAYNSA`). Method: average of the 3 months ending in the stated month (NSA) vs. the same 3-month average one year earlier. NSA-on-NSA T3M comparisons are seasonally clean because the windows align. Machine-readable results: `t3m_sectors.json`.*

## BLS series IDs used

| Series | ID |
|---|---|
| Boise MSA total nonfarm | SMU16142600000000001 |
| Mining/logging/construction | SMU16142601500000001 |
| Manufacturing | SMU16142603000000001 |
| Trade/transport/utilities | SMU16142604000000001 |
| Information | SMU16142605000000001 |
| Financial activities | SMU16142605500000001 |
| Prof & business services | SMU16142606000000001 |
| Education & health | SMU16142606500000001 |
| Leisure & hospitality | SMU16142607000000001 |
| Other services | SMU16142608000000001 |
| Government | SMU16142609000000001 |
| Salt Lake City-Murray MSA total nonfarm | SMU49416200000000001 |
| Phoenix-Mesa-Chandler MSA | SMU04380600000000001 |
| Reno MSA | SMU32399000000000001 |
| Spokane-Spokane Valley MSA | SMU53440600000000001 |

## Boise total nonfarm — T3M YoY history

| T3M ending | YoY % | YoY jobs |
|---|---|---|
| Jun 2023 | +2.85% | +10,933 |
| Dec 2023 | +3.24% | +12,667 |
| Jun 2024 | +2.70% | +10,633 |
| Dec 2024 | +1.77% | +7,133 |
| Jun 2025 | +2.48% | +10,033 |
| Sep 2025 | +2.20% | +8,933 |
| Dec 2025 | +0.91% | +3,733 |
| Mar 2026 | +0.51% | +2,067 |
| **Jun 2026** | **+0.42%** | **+1,733** |

## Sectors — T3M (Apr–Jun 2026 avg) YoY

| Sector | T3M level (000s) | YoY jobs | YoY % |
|---|---|---|---|
| Total nonfarm | 416.4 | +1,733 | +0.42% |
| Mining/logging/construction | 39.7 | +900 | +2.32% |
| Other services | 14.5 | +367 | +2.59% |
| Financial activities | 23.6 | +500 | +2.17% |
| Trade/transport/utilities | 79.8 | +1,333 | +1.70% |
| Prof & business services | 62.5 | +667 | +1.08% |
| Education & health | 67.0 | +433 | +0.65% |
| Manufacturing | 31.1 | −100 | −0.32% |
| Government | 53.4 | −400 | −0.74% |
| Information | 4.3 | −200 | −4.44% |
| Leisure & hospitality | 40.5 | −1,767 | −4.18% |

## Sector T3M YoY history (windows ending Jun-24 | Jun-25 | Mar-26 | Jun-26)

| Sector | Jun-24 | Jun-25 | Mar-26 | Jun-26 |
|---|---|---|---|---|
| Mining/logging/construction | +5.04% | +7.39% | +0.72% | +2.32% |
| Manufacturing | +0.11% | +1.52% | −0.43% | −0.32% |
| Trade/transport/utilities | +2.29% | +1.25% | −0.34% | +1.70% |
| Information | −0.68% | −7.53% | −5.19% | −4.44% |
| Financial activities | −1.31% | +1.76% | +0.88% | +2.17% |
| Prof & business services | +0.82% | +0.43% | +1.65% | +1.08% |
| Education & health | +6.33% | +6.28% | +2.27% | +0.65% |
| Leisure & hospitality | +0.97% | +1.44% | −2.68% | −4.18% |
| Other services | +3.19% | +1.19% | +2.63% | +2.59% |
| Government | +4.76% | +1.77% | +0.93% | −0.74% |

## Peers & labor market — T3M (Apr–Jun 2026) YoY

| Series | T3M level | YoY | YoY % |
|---|---|---|---|
| Salt Lake City-Murray | 855.8k | +17,533 | +2.09% |
| Reno | 287.1k | +4,600 | +1.63% |
| Phoenix-Mesa-Chandler | 2,473.5k | +22,800 | +0.93% |
| **Boise** | **416.4k** | **+1,733** | **+0.42%** |
| US total nonfarm (NSA) | 159,282k | +383k | +0.24% |
| Spokane-Spokane Valley | 266.3k | −2,267 | −0.84% |
| Boise labor force | 452,743 | −3,596 | **−0.79%** |
| Boise unemployment rate (T3M avg) | 3.37% | +0.07pp | (Jun-24: 3.20% · Jun-25: 3.30%) |

## Key readings vs. single-month figures

1. **Total growth is ~+0.4%, not the +1.2% of the June single-month print** — June 2026 was the strongest month of the year and flatters the trend. The staircase (+2.9% → +2.5% → +0.9% → +0.4%) has not yet found a floor.
2. **Education & health decelerated from +6.3% to +0.65% in two years** — the sharpest sector swing; hospital capex is running far ahead of hiring, which arrives with the 2028–2030 openings.
3. **Construction is +2.3% smoothed** (vs +4.8% single-month) — still the leader, carried by Micron/hospitals/airport.
4. **Trade/transport/utilities re-accelerated** (−0.3% in the Mar-26 window → +1.7%) — logistics is genuinely improving, consistent with the Tractor Supply/Amazon buildout.
5. **On smoothed data Boise trails Phoenix** and sits next-to-last in its peer set — a real change from 2021–23 when it led.
6. **The labor force is contracting (−0.79%)** while unemployment stays low — a supply-constrained, not demand-collapsed, labor market; consistent with in-migration pausing.

*Reproduction: `scratchpad/t3m_flat.py` logic — download the two BLS flat files, filter to the series IDs above, compute 3-month means, compare to the year-ago window. CES metro data are NSA and subject to annual benchmark revisions (material in this MSA — see Appendix A flags).*
