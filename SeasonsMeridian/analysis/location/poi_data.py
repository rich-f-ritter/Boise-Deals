# Verified POI data for the Seasons at Meridian location map (researched Aug 23, 2026).
# Coordinates: OSM/Nominatim geocodes or CoStar property lat/lon; distances straight-line.
# School zoning verified point-in-polygon against West Ada's own ArcGIS attendance layers
# (current zones + adopted 2026-27 redraw: Pepper Ridge ES / Lewis & Clark MS / Mountain View HS).
# Area polygons are approximate outlines drawn from road geometry — illustrative, not parcel-exact.
# Numbers are assigned at build time, restarting at 1 within each category (colour first, then number).

CATEGORIES = [
    {"id": "emp",    "name": "Employment & medical",        "color": "#3987e5"},
    {"id": "retail", "name": "Retail & dining",             "color": "#eb6834"},
    {"id": "ent",    "name": "Entertainment & recreation",  "color": "#b06fd6"},
    {"id": "edu",    "name": "Schools & childcare",         "color": "#f2c230"},
    {"id": "park",   "name": "Parks",                       "color": "#57c84d"},
    {"id": "far",    "name": "Metro anchors (beyond 5 mi)", "color": "#9aa7b8"},
]

RINGS_MI = [1, 3, 5]

POIS = [
    # ---- Employment & medical ----
    dict(cat="emp", name="Silverstone / Eagle View Landing campus", lat=43.5936, lon=-116.3474, d=0.62,
         poly=[[43.6010, -116.3540], [43.6010, -116.3408], [43.5862, -116.3408], [43.5862, -116.3540]],
         badge=[43.5936, -116.3455],
         note="Twin master-planned employment campus east of Eagle Rd: St. Luke's, ICCU Building (125K SF, 2020), POWER Engineers building, Topgolf, Hyatt Place. With El Dorado across Eagle it absorbed 28 tenant move-ins / ~399,000 SF in the last 2 years (GCU, Disco Hi-Tec America, Nightforce Optics, Great West Casualty, Ardurra...); 22 office buildings / 914,000 SF built since 2020 within 1.25 mi of the subject."),
    dict(cat="emp", name="St. Luke's Meridian", lat=43.599387, lon=-116.352281, d=0.65,
         note="520 S Eagle Rd · 550,000-SF full-service hospital (Level IV trauma, Level II NICU); anchor of the Eagle Rd & I-84 medical node."),
    dict(cat="emp", name="POWER Engineers HQ bldg", lat=43.596282, lon=-116.341949, d=0.99,
         note="1032 S Silverstone Way · 150,000-SF office (2023, Eagle View Landing); POWER Engineers (global engineering firm) took 90,000 SF in Aug 2025."),
    dict(cat="emp", name="El Dorado Business Campus", lat=43.5872, lon=-116.3583, d=0.38,
         poly=[[43.5906, -116.3625], [43.5906, -116.3542], [43.5838, -116.3542], [43.5838, -116.3625]],
         badge=[43.5868, -116.3600],
         note="85-acre office/medical campus at the SW corner of Eagle & Overland, directly across from the subject: Cottonwood Creek Behavioral Hospital (59,500 SF, Mar 2025), Veranda Plaza & Catalina Place medical, ICOM admin offices, Northpoint Recovery."),
    dict(cat="emp", name="Scentsy Commons (HQ)", lat=43.610703, lon=-116.360838, d=1.29,
         poly=[[43.6135, -116.3640], [43.6135, -116.3565], [43.6068, -116.3565], [43.6068, -116.3640]],
         badge=[43.6102, -116.3603],
         note="2701 E Pine Ave · 70-acre Scentsy Commons campus; ~1,000 HQ employees (2025)."),
    dict(cat="emp", name="Blue Cross of Idaho HQ", lat=43.613854, lon=-116.357163, d=1.52,
         note="3000 E Pine Ave · 850+ employees at HQ."),
    dict(cat="emp", name="Ten Mile Crossing", lat=43.5962, lon=-116.4292, d=3.35,
         poly=[[43.6002, -116.4345], [43.6002, -116.4238], [43.5928, -116.4238], [43.5928, -116.4345]],
         badge=[43.5962, -116.4292],
         note="Business park at I-84 & Ten Mile (Brighton/Gardner): Paylocity (125K-SF building), AmeriBen (2nd building underway), Horrocks, Saint Alphonsus surgery center, Scheels flagship, Ten Mile Medical Office Complex (270K SF)."),
    dict(cat="emp", name="The District at Ten Mile (UC)", lat=43.5985, lon=-116.4465, d=3.90,
         poly=[[43.6048, -116.4522], [43.6048, -116.4408], [43.5922, -116.4408], [43.5922, -116.4522]],
         badge=[43.5985, -116.4465],
         note="220-acre mixed-use by Ahlquist/Adler; broke ground May 2026. Phase 1 (650,000+ SF): Target (148K SF, May 2027), Life Time ($50.7M / 103K-SF club, spring 2027), In-N-Out, hotels. Outline approximate."),
    dict(cat="emp", name="Amazon DID3 delivery station", lat=43.60758, lon=-116.425825, d=3.42,
         note="2660 W Fred Smith St · 180,000-SF last-mile delivery station (2021); FedEx Ground adjacent."),

    # ---- Retail & dining ----
    dict(cat="retail", name="The Village at Meridian", lat=43.622481, lon=-116.351337, d=2.16,
         poly=[[43.6266, -116.3542], [43.6266, -116.3468], [43.6198, -116.3468], [43.6198, -116.3542]],
         badge=[43.6232, -116.3505],
         note="Eagle & Fairview · ~1M-SF open-air lifestyle center (CenterCal): Village Cinema luxury theater, summer concert series. Phase II (80,000 SF, 6 buildings — Williams Sonoma, Pottery Barn, The Capital Grille, Culinary Dropout, Vuori, Alo...) opens Sept 2026 – Feb 2027."),
    dict(cat="retail", name="Scheels (2024)", lat=43.598333, lon=-116.426505, d=3.31,
         note="700 S Wayfinder Ave (Ten Mile Crossing) · 240,000-SF flagship opened Apr 2024 — Idaho's largest sporting-goods store; 56-ft indoor Ferris wheel; ~500 employees."),
    dict(cat="retail", name="Costco #2 — Meridian & Lake Hazel (UC)", lat=43.5465, lon=-116.3935, d=3.53,
         note="S Meridian Rd & W Lake Hazel Rd · ~200,000-SF Costco (one of the chain's largest) + 16-pump fuel station, under construction, opening late 2026 — makes Meridian the only Idaho city with two Costcos. Location approximate."),
    dict(cat="retail", name="In-N-Out (Idaho's first)", lat=43.619991, lon=-116.351393, d=1.98,
         note="3520 E Fairview Ave (at the Village) · opened Dec 2023 as Idaho's first In-N-Out."),
    dict(cat="retail", name="WinCo Foods (24-hr)", lat=43.596211, lon=-116.389733, d=1.47,
         note="1050 S Progress Ave · nearest full grocery, 24 hours."),
    dict(cat="retail", name="Costco (Boise, Cole Rd)", lat=43.585075, lon=-116.27668, d=4.24,
         note="2051 S Cole Rd, Boise · nearest operating Costco, straight shot east on Overland/I-84."),
    dict(cat="retail", name="Hawkins big-box site (proposed)", lat=43.5900, lon=-116.4024, d=2.10,
         note="675 W Waltman Ln at I-84 & Meridian Rd (Tanner Creek site) · preliminary site plan for a ~150,000-SF warehouse retailer + fuel station (retailer undisclosed — press names Costco/Sam's Club/Target-class candidates; BoiseDev 7/27/2026). Staff-level approval path; watch item, not yet real."),

    # ---- Entertainment & recreation ----
    dict(cat="ent", name="Topgolf", lat=43.59627, lon=-116.347279, d=0.75,
         note="1050 S Silverstone Way (Eagle View Landing) · opened Nov 2022, Idaho's first Topgolf — 33,000 SF, walkable from the subject."),
    dict(cat="ent", name="Roaring Springs & Wahooz", lat=43.5924, lon=-116.3993, d=1.92,
         poly=[[43.5948, -116.4022], [43.5948, -116.3962], [43.5898, -116.3962], [43.5898, -116.4022]],
         badge=[43.5923, -116.3992],
         note="400 W Overland Rd — same road as the subject, 2 mi west · the Northwest's largest waterpark + Wahooz Family Fun Zone (go-karts, bowling, laser tag, arcade): 'Southern Idaho's largest family entertainment complex.'"),

    # ---- Schools & childcare (assigned schools verified via West Ada GIS) ----
    dict(cat="edu", name="Mountain View High School (assigned)", lat=43.58562, lon=-116.367163, d=0.55,
         note="2000 S Millennium Way · zoned high school (verified, West Ada GIS incl. 2026-27 redraw) · 2,463 students, GreatSchools 8/10, ~#20 in Idaho (US News) — a half-mile from the subject."),
    dict(cat="edu", name="Lewis & Clark Middle School (assigned)", lat=43.60988, lon=-116.341639, d=1.55,
         note="4141 E Pine Ave · zoned middle school (verified, West Ada GIS incl. 2026-27 redraw) · ~900 students, GreatSchools 7/10."),
    dict(cat="edu", name="Pepper Ridge Elementary (assigned)", lat=43.582585, lon=-116.330102, d=1.42,
         note="2252 S Sumpter Way · zoned elementary (verified, West Ada GIS incl. 2026-27 redraw) · ~500 students, GreatSchools 8/10 / Niche A-."),
    dict(cat="edu", name="ICOM medical school", lat=43.594253, lon=-116.375969, d=0.77,
         note="1401 E Central Dr · Idaho College of Osteopathic Medicine, $34M / 94,000-SF campus; class size expanded to 220+ seats (2025), growing toward 648 students."),
    dict(cat="edu", name="ISU Meridian Health Science Center", lat=43.594568, lon=-116.377974, d=0.87,
         note="1311 E Central Dr · Idaho State University's Treasure Valley health-sciences campus (pharmacy, PA, nursing, dental)."),
    dict(cat="edu", name="The Goddard School of Meridian", lat=43.586594, lon=-116.362579, d=0.39,
         note="2009 S Wells Ave · Idaho's first Goddard School franchise — premium preschool/daycare, a 2-minute drive from the subject."),
    dict(cat="edu", name="Primrose School of South Meridian", lat=43.576978, lon=-116.353816, d=1.07,
         note="3060 S Eagle Rd · new Primrose location (12,700 SF, opened late 2025 per CoStar) — second national early-education brand at the node."),
    dict(cat="edu", name="Everbrook Academy", lat=43.560468, lon=-116.350828, d=2.22,
         note="4845 S Tavistock Ave · new early-education academy (11,300 SF, 2025 per CoStar), south Meridian."),
    dict(cat="edu", name="Cole Valley Christian (private)", lat=43.614176, lon=-116.39017, d=2.30,
         note="200 E Carlton Ave · private K-12 option."),

    # ---- Parks ----
    dict(cat="park", name="Julius M. Kleiner Park", lat=43.624394, lon=-116.347026, d=2.33,
         poly=[[43.6280, -116.3466], [43.6280, -116.3405], [43.6212, -116.3405], [43.6212, -116.3466]],
         badge=[43.6247, -116.3435],
         note="58-acre flagship park adjacent to the Village: amphitheater, splash pad, ponds, pickleball."),
    dict(cat="park", name="Bear Creek Park", lat=43.5829, lon=-116.403598, d=2.22,
         note="2400 S Stoddard Rd · 19-acre neighborhood park."),
    dict(cat="park", name="Storey Park & Bark Park", lat=43.60258, lon=-116.388273, d=1.55,
         note="Downtown Meridian · 14-acre park + 2.25-acre dog park."),
    dict(cat="park", name="Discovery Park", lat=43.543371, lon=-116.366942, d=3.37,
         note="2121 E Lake Hazel Rd · 64-acre regional park (Phase II 2023)."),

    # ---- Metro anchors beyond the ring ----
    dict(cat="far", name="Downtown Boise", lat=43.61512, lon=-116.201382, d=8.14,
         note="~10 mi / ~15 min via I-84-I-184 from the subject's on-ramp."),
    dict(cat="far", name="Boise Airport (BOI)", lat=43.560057, lon=-116.208075, d=7.90,
         note="~10 mi / ~14 min east on I-84."),
    dict(cat="far", name="Boise State University", lat=43.603282, lon=-116.19941, d=8.08,
         note="~11 mi / ~20 min."),
    dict(cat="far", name="Micron Boise campus", lat=43.530141, lon=-116.150825, d=11.02,
         note="8000 S Federal Way · $50B ID1/ID2 fab buildout (first wafers 2027 / 2028, ~3,500 direct jobs; ~17,000 total projected) + $10B research campus reported Aug 2026; ~15 min via I-84."),
    dict(cat="far", name="Meta Kuna data center", lat=43.474, lon=-116.400, d=8.42,
         note="$800M / 960,000-SF data center, completion expected end of 2026 (location approximate)."),
]

ROADS = [
    dict(label="I-84 · 132-142K vehicles/day", at=[43.5985, -116.3080],
         note="COMPASS counts on the segments flanking the Eagle Rd interchange (~2023) — the metro's busiest freeway corridor. Subject sits at Exit 46; two-lane ramp upgrade designed (ITD, construction pending funding)."),
    dict(label="EAGLE RD (SH-55) · 60-65K vehicles/day", at=[43.5745, -116.3541],
         note="ITD: 'Idaho's busiest non-interstate highway' — ~60,000 vehicles/day, doubled since 2000; ACHD counted 64,000+ just north of I-84 and projects 78,000+ by 2040. The Eagle/Overland corner by the subject carries 76,500+ vehicles/day combined."),
    dict(label="Eagle & Fairview — Idaho's busiest intersection", at=[43.6195, -116.3541],
         note="Ranked Idaho's #1 intersection by traffic count since 2005 (ACHD) — the retail gravity center the subject feeds into, 2 mi north."),
]

FOOTER_NOTE = ("Companion to strength H45 (Location) in 'Seasons at Meridian - Strengths &amp; Considerations'. "
               "Numbers restart at 1 within each colour — read colour first, then number; the legend at right carries the full description. "
               "POIs verified Aug 23, 2026 (ITD/ACHD/COMPASS traffic data; city, district and press sources; CoStar). "
               "School assignments verified point-in-polygon against West Ada's own ArcGIS attendance layers (current zones and the adopted 2026-27 redraw agree: Pepper Ridge ES / Lewis &amp; Clark MS / Mountain View HS). "
               "Area outlines are approximate, drawn from road geometry. Gray dots = every non-multifamily commercial building &ge;20,000 SF built or under construction since 2020 within 5 mi (CoStar) — toggle on in Layers. "
               "Distances are straight-line from the subject. The Costco (Lake Hazel), District at Ten Mile and Meta Kuna positions are approximate site centroids.")
