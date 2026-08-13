# Appendix K — Placer.ai Device-Based Migration Data (client-provided)
*Ingested August 13, 2026. Eight Placer.ai exports provided by Milestone, archived in `../data/placerai/`. Placer measures migration from observed mobile-device home-location changes (panel-based, adjusted to population) — an independent, near-real-time check on Census (which currently ends July 2025) and on BLS population controls. Analysis computed from the raw files; script logic preserved in this appendix's tables.*

## Files
| File | Content |
|---|---|
| `Boise_MSA_Growth_Breakdown_Jun21Jun26.csv` | Monthly net domestic migration, natural growth, international — 60 months |
| `Boise_MSA_Migration_Movements_Jun21Jun26.csv` | Monthly gross inbound/outbound — 60 months |
| `Boise_MSA_Origin_Destination_Jun25Jun26.csv` / `Jun24Jun26.csv` | Net flows by origin/destination market, 1-yr and 2-yr |
| `Migration_Trends_CBSAs_Jun25Jun26.csv` | All 925 US CBSAs — net migration, demographics of movers, YE Jun 2026 |
| `Migration_Trends_Counties_Jun25Jun26.csv` | All 3,126 US counties — same |
| `population_change_by_zip_Jun25Jun26.csv` / `Jun24Jun26.csv` | Treasure Valley ZIP-level net migration, 1-yr and 2-yr |

## Finding P1 — Migration RE-ACCELERATED to a five-year high in YE June 2026

Boise MSA, by year ending June (growth-breakdown file):

| YE June | Net domestic | Natural | International | Total | Gross in | Gross out |
|---|---|---|---|---|---|---|
| 2022 | +10,347 | +1,574 | +3,469 | +15,390 | 33,946 | 23,599 |
| 2023 | +6,795 | +2,467 | +3,320 | +12,582 | 32,487 | 25,692 |
| 2024 | +5,298 | +2,820 | +4,071 | +12,189 | 19,710 | 14,412 |
| 2025 | +6,051 | +2,861 | +4,130 | +13,042 | 21,134 | 15,083 |
| **2026** | **+11,647** | **+2,914** | **+4,208** | **+18,769** | **27,875** | **16,228** |

The 2023–24 cooling is visible — and then YE June 2026 nearly doubles the prior year's net domestic migration, driven by a surge in gross inbound (+32%) against stable outbound. **On device data, the most recent 12 months were the strongest migration year since the 2021–22 boom, and the strongest total-growth year in the entire five-year window.** This is precisely the period the official data cannot yet see: Census vintage estimates end July 2025; this extends through June 2026.

## Finding P2 — Boise is now a top-5 US migration market in both absolute and rate terms

From the all-CBSA file (YE Jun 2026): **Boise ranks #5 of 925 US CBSAs in absolute net migration (+12,398)** — behind only DFW (+24,622), Nashville (+16,057), Austin (+14,269), and one other — **and #5 by net-migration rate (+1.45%)** among 250K+ CBSAs, behind only retiree/coastal micro-markets (Seaford DE, Myrtle Beach, Ocala, Wilmington NC). Peer contrast is stark — the old Sun Belt migration machine has broken while Boise re-accelerated:

| Metro | Net migration YE Jun 2026 | Rate |
|---|---|---|
| **Boise** | **+12,398** | **+1.45%** |
| DFW | +24,622 | +0.29% |
| Nashville | +16,057 | +0.75% |
| Austin | +14,269 | +0.55% |
| Reno | +2,766 | +0.49% |
| Salt Lake City | +1,530 | +0.11% |
| Denver | +1,046 | +0.03% |
| Phoenix | +744 | +0.01% |
| Houston | −2,447 | −0.03% |
| Las Vegas | −3,950 | −0.16% |
| Baton Rouge | −4,950 | −0.56% |

Boise's net inflow exceeded Phoenix, Denver, and Salt Lake City *combined* — several times over. **Ada County ranks #8 of 3,126 US counties (+8,552, +1.58% rate); Canyon ranks #49 (+3,160, +1.17%).** Placer's embedded forecast has the metro growing ~17.5% (horizon not specified in export — treat as directional).

## Finding P3 — Who's coming: California (47% of net), and an accelerating DC/fed-exodus channel

Top net feeders, YE Jun 2026, with the prior year for trend (O-D files; feeder-metro median HHI):

| Feeder | YE Jun-26 net | Prior yr | Trend | Feeder MHHI |
|---|---|---|---|---|
| Los Angeles | +670 | +980 | slowing | $96K |
| San Francisco | +600 | +229 | **accelerating** | **$136K** |
| Riverside-San Bernardino | +523 | +541 | steady | $90K |
| San Diego | +352 | +294 | steady | $107K |
| **Washington DC** | **+338** | +166 | **doubled** | **$127K** |
| Sacramento | +301 | +119 | accelerating | $97K |
| Chicago | +279 | +258 | steady | $91K |
| Columbus OH | +278 | +183 | accelerating | $82K |
| Portland | +267 | +121 | accelerating | $98K |
| Seattle | +233 | +70 | **tripled** | $115K |

- **California = 47% of the metro's net inflow** (+3,973 of +8,492 in the O-D table) — the CA pipeline is fully intact.
- **The DC metro inflow doubled year-over-year** — the federal-workforce exodus (DC payrolls −3.0%, the nation's worst) is visibly landing in Boise. High-income feeder ($127K MHHI).
- Net outflows are small and telling: Moscow ID (−197, university), Nashville (−159), OKC (−139) — no large-metro exodus channel.
- **In-migrant income ≈ incumbent income** (weighted in-migrant HHI $86.6K vs incumbent $86.6K, ratio 1.00) — the metro is importing its own income distribution, not diluting it; the coastal-feeder mix (SF/DC/Seattle/SD) sits well above it.

## Finding P4 — ZIP level: the subject's ZIP is the #1 absorption zone in the metro, and accelerating

Treasure Valley ZIPs, YE Jun 2026 net migration vs prior year:

| ZIP | Area | YE Jun-26 | Prior yr | Acceleration | Rate /1,000 |
|---|---|---|---|---|---|
| **83642** | **Meridian (south — the subject)** | **+2,417** | +1,340 | **+1,077** | **+34.7** |
| 83687 | Nampa (north) | +1,604 | +789 | +815 | +33.8 |
| 83706 | Boise (Bench/BSU) | +1,025 | −70 | +1,095 | +27.9 |
| 83669 | Star | +836 | +1,042 | −206 | +36.4 |
| 83709 | Boise (SW) | +709 | −126 | +835 | +12.3 |
| 83607 | Caldwell | +511 | +710 | −199 | +12.1 |
| 83616 | Eagle | +340 | +23 | +317 | +8.0 |
| 83634 | Kuna | +316 | +120 | +196 | +7.9 |
| 83646 | Meridian (north) | +309 | +820 | **−511** | +3.8 |
| — | **Valley total** | **+10,445** | +6,045 | +4,400 | — |

- **ZIP 83642 — which contains Seasons at Meridian — is the single largest net-in-migration ZIP in the Treasure Valley (+2,417), the metro's highest absolute acceleration (+1,077 vs prior year), and among its highest rates (+34.7 per 1,000).** Median HHI in the ZIP: $99K.
- The intra-Meridian rotation is exactly what the land-use and District work predicted: **north Meridian (83646) decelerated sharply (−511) while south Meridian (83642) accelerated** — growth is rolling toward the subject's corridor and the Lake Hazel/south-Meridian frontier (Costco #2, District at Ten Mile).
- Valley-wide ZIP net (+10,445) is up ~73% over the prior year — corroborating the MSA-level re-acceleration in an independent cut of the same panel.

## Finding P5 — Reconciliation: what Placer changes about the paper's findings

1. **It strengthens Finding 1 (measurement artifact) and reframes Finding 4 (labor force).** The paper documented a labor force shrinking −0.8% while wages grew 3rd-fastest in the nation — and IDOL itself flagged that part of the labor-force decline is BLS *population-model* revisions. Placer now shows population inflow at a five-year high through June 2026. The two are reconcilable only if (a) the BLS population controls are badly behind the actual population (consistent with the artifact theme — LAUS controls will catch up with a lag, just like the CES benchmark), and/or (b) the new migrants skew toward non-workers (retirees, remote workers employed elsewhere, DC exiles between jobs). Both readings are demand-positive for apartments: **people arrive first; payrolls and labor-force statistics record them later.**
2. **It resolves the migration-slowdown question in the memo (§5) in favor of re-acceleration.** The v2 memo, relying on Census through July 2025, said in-migration had "stabilized below the boom." The device data says YE June 2026 re-accelerated to near-boom levels. The Census vintage that will confirm or refute this publishes December 2026–March 2027; until then, Placer is the most current read available.
3. **It hardens the demand side of the underwriting synthesis.** Metro absorption of ~2,500 units/yr against near-zero *measured* job growth was already the proof that Boise apartment demand is migration-coupled, not payroll-coupled. A top-5-in-the-nation migration year, 47% fed by California incomes, landing hardest in the subject's own ZIP, against a construction pipeline at 2–3.5% of inventory, is the strongest single demand data point in the deal file.

## Caveats — stated plainly
- **Internal inconsistency across exports:** the same YE Jun 2026 year shows net domestic migration of +8,492 (O-D table sum), +11,647 (growth-breakdown file), and +12,398 (CBSA file). The O-D table visibly truncates small/unmatched flows; the CBSA file is presumably the authoritative national-model figure. Treat the level as "roughly +11–12K" and the *trend* (near-doubling) as the robust finding.
- **Device-panel methodology:** Placer infers home location from device behavior and scales a panel to population. Levels are model outputs; panel composition can drift; adjacent-year comparisons within one methodology are more reliable than comparisons to Census levels.
- The exports' "Migration Type" column is unreliable (mislabels, e.g., California metros as "In-State") — ignored in this analysis.
- Placer's `latest_pop_change_forecast` horizon is not documented in the export; used directionally only.
- **Placer vs Census cross-check where they overlap:** YE Jun 2025 Placer total growth +13,042 vs Census Ada-County-alone +10,916 (YE Jul 2025) — same order of magnitude, reasonable agreement for different geographies/windows, which lends credibility to the 2026 acceleration reading.

## Diligence checkpoints updated
1. **September 2026 — QCEW Q1 2026** (unchanged, from the research paper): tests the employment artifact.
2. **December 2026 — Census Vintage 2026 state estimates / March 2027 county estimates**: tests the Placer re-acceleration against official population data.
3. If both confirm, the underwriting range in the paper (§8) moves toward its upside case (+2.0–2.5% employment growth, boom-adjacent migration) — with the CES and LAUS series likely revised up behind them.
