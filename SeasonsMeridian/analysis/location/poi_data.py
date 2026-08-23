# Verified POI data for the Seasons at Meridian location map (researched Aug 23, 2026).
# Coordinates: OSM/Nominatim geocodes or CoStar property lat/lon; distances straight-line.
# Sources per item are cited in the H45 strength write-up and the research fact sheets.

CATEGORIES = [
    {"id": "emp",    "name": "Employment & medical",        "color": "#3987e5"},
    {"id": "retail", "name": "Retail & dining",             "color": "#eb6834"},
    {"id": "ent",    "name": "Entertainment & recreation",  "color": "#b06fd6"},
    {"id": "edu",    "name": "Schools & higher ed",         "color": "#f2c230"},
    {"id": "park",   "name": "Parks",                       "color": "#57c84d"},
    {"id": "far",    "name": "Metro anchors (beyond 5 mi)", "color": "#9aa7b8"},
]

RINGS_MI = [1, 3, 5]

POIS = [
    # ---- Employment & medical ----
    dict(cat="emp", key=1, lbl=1, name="St. Luke's Meridian", lat=43.599387, lon=-116.352281, d=0.65,
         note="520 S Eagle Rd · 550,000-SF full-service hospital (Level IV trauma, Level II NICU); anchor of the Eagle View Landing / Eagle+I-84 medical node."),
    dict(cat="emp", key=1, lbl=1, name="POWER Engineers HQ bldg", lat=43.596282, lon=-116.341949, d=0.99,
         note="1032 S Silverstone Way · 150,000-SF office (2023, Eagle View Landing); POWER Engineers (global engineering firm) took 90,000 SF in Aug 2025.", loff=[0.0016, 0.002]),
    dict(cat="emp", key=0, lbl=0, name="ICCU Building (Silverstone)", lat=43.596393, lon=-116.350268, d=0.61,
         note="1111 S Silverstone Way · 125,000-SF office (2020); Idaho Central Credit Union administrative hub."),
    dict(cat="emp", key=1, lbl=0, name="Silverstone / El Dorado campus", lat=43.5925, lon=-116.3505, d=0.6,
         note="~175-acre twin business campus at Eagle & Overland: 28 tenant move-ins / ~399,000 SF absorbed in the last 2 years (POWER Engineers, Cottonwood Creek Hospital, GCU office, Disco Hi-Tec America, Nightforce Optics, Ardurra...). 22 office buildings / 914,000 SF built since 2020 within 1.25 mi of the subject.", loff=[-0.004, 0.001]),
    dict(cat="emp", key=0, lbl=0, name="Cottonwood Creek Behavioral Hospital", lat=43.586214, lon=-116.359128, d=0.41,
         note="2131 S Bonito Way (El Dorado campus) · 59,500-SF behavioral hospital, moved in Mar 2025."),
    dict(cat="emp", key=1, lbl=1, name="Scentsy HQ", lat=43.610703, lon=-116.360838, d=1.29,
         note="2701 E Pine Ave · 70-acre Scentsy Commons campus; ~1,000 HQ employees (2025)."),
    dict(cat="emp", key=1, lbl=0, name="Blue Cross of Idaho HQ", lat=43.613854, lon=-116.357163, d=1.52,
         note="3000 E Pine Ave · 850+ employees at HQ.", loff=[0.0016, 0.002]),
    dict(cat="emp", key=1, lbl=1, name="Ten Mile Crossing", lat=43.594664, lon=-116.426931, d=3.29,
         note="I-84 & Ten Mile business park (Brighton/Gardner): Paylocity (125K-SF building), AmeriBen (2nd building underway), Horrocks, Saint Alphonsus surgery center, Scheels."),
    dict(cat="emp", key=1, lbl=1, name="The District at Ten Mile (UC)", lat=43.600, lon=-116.443, d=4.15,
         note="220-acre mixed-use by Ahlquist/Adler; broke ground May 2026. Phase 1 (650,000+ SF): Target (148K SF, May 2027), Life Time ($50.7M / 103K-SF club, spring 2027), In-N-Out, hotels. Location approximate."),
    dict(cat="emp", key=0, lbl=0, name="Amazon DID3 delivery station", lat=43.60758, lon=-116.425825, d=3.42,
         note="2660 W Fred Smith St · 180,000-SF last-mile delivery station (2021); FedEx Ground adjacent."),

    # ---- Retail & dining ----
    dict(cat="retail", key=1, lbl=1, name="The Village at Meridian", lat=43.622481, lon=-116.351337, d=2.16,
         note="Eagle & Fairview · ~1M-SF open-air lifestyle center (CenterCal): Village Cinema luxury theater, summer concert series. Phase II (80,000 SF, 6 buildings — Williams Sonoma, Pottery Barn, The Capital Grille, Culinary Dropout, Vuori, Alo...) opens Sept 2026 – Feb 2027."),
    dict(cat="retail", key=1, lbl=1, name="Scheels (2024)", lat=43.598333, lon=-116.426505, d=3.31,
         note="700 S Wayfinder Ave (Ten Mile Crossing) · 240,000-SF flagship opened Apr 2024 — Idaho's largest sporting-goods store; 56-ft indoor Ferris wheel; ~500 employees."),
    dict(cat="retail", key=1, lbl=0, name="In-N-Out (Idaho's first)", lat=43.619991, lon=-116.351393, d=1.98,
         note="3520 E Fairview Ave (at the Village) · opened Dec 2023 as Idaho's first In-N-Out.", loff=[-0.0032, 0.001]),
    dict(cat="retail", key=1, lbl=0, name="WinCo Foods (24-hr)", lat=43.596211, lon=-116.389733, d=1.47,
         note="1050 S Progress Ave · nearest full grocery, 24 hours."),
    dict(cat="retail", key=0, lbl=0, name="Costco (Boise, Cole Rd)", lat=43.585075, lon=-116.27668, d=4.24,
         note="2051 S Cole Rd, Boise · nearest Costco, straight shot east on Overland/I-84."),

    # ---- Entertainment & recreation ----
    dict(cat="ent", key=1, lbl=1, name="Topgolf", lat=43.59627, lon=-116.347279, d=0.75,
         note="1050 S Silverstone Way (Eagle View Landing) · opened Nov 2022, Idaho's first Topgolf — 33,000 SF, walkable from the subject.", loff=[-0.0035, 0.0015]),
    dict(cat="ent", key=1, lbl=1, name="Roaring Springs & Wahooz", lat=43.5924, lon=-116.3993, d=1.92,
         note="400 W Overland Rd — same road as the subject, 2 mi west · the Northwest's largest waterpark + Wahooz Family Fun Zone (go-karts, bowling, laser tag, arcade): 'Southern Idaho's largest family entertainment complex.'"),

    # ---- Schools & higher ed ----
    dict(cat="edu", key=1, lbl=1, name="Mountain View High School", lat=43.58562, lon=-116.367163, d=0.55,
         note="2000 S Millennium Way · assigned West Ada high school, ~2,400 students, GreatSchools 8/10 — a half-mile from the subject.", loff=[-0.0032, 0]),
    dict(cat="edu", key=1, lbl=0, name="Siena Elementary (10/10)", lat=43.572769, lon=-116.358569, d=1.33,
         note="2870 E Rome Dr · GreatSchools 10/10; likely assigned elementary (West Ada is re-drawing boundaries — verify)."),
    dict(cat="edu", key=0, lbl=0, name="Victory Middle School (10/10)", lat=43.585206, lon=-116.405312, d=2.24,
         note="920 W Kodiak Dr · GreatSchools 10/10; likely assigned middle school."),
    dict(cat="edu", key=1, lbl=1, name="ICOM medical school", lat=43.594253, lon=-116.375969, d=0.77,
         note="1401 E Central Dr · Idaho College of Osteopathic Medicine, $34M / 94,000-SF campus; class size expanded to 220+ seats (2025), growing toward 648 students.", loff=[0.0016, 0.002]),
    dict(cat="edu", key=0, lbl=0, name="ISU Meridian Health Science Center", lat=43.594568, lon=-116.377974, d=0.87,
         note="1311 E Central Dr · Idaho State University's Treasure Valley health-sciences campus (pharmacy, PA, nursing, dental).", loff=[-0.0032, -0.003]),
    dict(cat="edu", key=0, lbl=0, name="Cole Valley Christian (private)", lat=43.614176, lon=-116.39017, d=2.30,
         note="200 E Carlton Ave · private K-12 option."),

    # ---- Parks ----
    dict(cat="park", key=1, lbl=0, name="Julius M. Kleiner Park", lat=43.624394, lon=-116.347026, d=2.33,
         note="58-acre flagship park adjacent to the Village: amphitheater, splash pad, ponds, pickleball."),
    dict(cat="park", key=0, lbl=0, name="Bear Creek Park", lat=43.5829, lon=-116.403598, d=2.22,
         note="2400 S Stoddard Rd · 19-acre neighborhood park."),
    dict(cat="park", key=0, lbl=0, name="Storey Park & Bark Park", lat=43.60258, lon=-116.388273, d=1.55,
         note="Downtown Meridian · 14-acre park + 2.25-acre dog park."),
    dict(cat="park", key=0, lbl=0, name="Discovery Park", lat=43.543371, lon=-116.366942, d=3.37,
         note="2121 E Lake Hazel Rd · 64-acre regional park (Phase II 2023)."),

    # ---- Metro anchors beyond the ring ----
    dict(cat="far", key=1, lbl=0, name="Downtown Boise", lat=43.61512, lon=-116.201382, d=8.14,
         note="~10 mi / ~15 min via I-84-I-184 from the subject's on-ramp."),
    dict(cat="far", key=1, lbl=0, name="Boise Airport (BOI)", lat=43.560057, lon=-116.208075, d=7.90,
         note="~10 mi / ~14 min east on I-84."),
    dict(cat="far", key=0, lbl=0, name="Boise State University", lat=43.603282, lon=-116.19941, d=8.08,
         note="~11 mi / ~20 min."),
    dict(cat="far", key=1, lbl=0, name="Micron Boise campus", lat=43.530141, lon=-116.150825, d=11.02,
         note="8000 S Federal Way · $50B ID1/ID2 fab buildout (first wafers 2027 / 2028, ~3,500 direct jobs; ~17,000 total projected) + $10B research campus reported Aug 2026; ~15 min via I-84."),
    dict(cat="far", key=0, lbl=0, name="Meta Kuna data center", lat=43.474, lon=-116.400, d=8.42,
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
               "POIs verified Aug 23, 2026 (ITD/ACHD/COMPASS traffic data; city, district and press sources; CoStar). "
               "Gray dots = every non-multifamily commercial building &ge;20,000 SF built or under construction since 2020 within 5 mi (CoStar) — toggle on in Layers. "
               "Distances are straight-line from the subject. School assignments are proximity-based — West Ada is re-drawing boundaries; verify by address before quoting. "
               "The District at Ten Mile and Meta Kuna pins are approximate site centroids.")
