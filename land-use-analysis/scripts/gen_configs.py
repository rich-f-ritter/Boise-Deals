"""Generate config.json for both subjects (Canyon Ridge, Seasons at Meridian).

Ada County publishes ONE countywide Zoning layer with a CITY field, so we register one
zoning source per jurisdiction (where=CITY='...') giving per-city-accurate crosswalks with
no cross-city code collisions. Parcels come from the Ada County Assessor Parcels layer
(no owner field — owner/tenure/intent are researched per-site downstream).
"""
import json
from pathlib import Path

PARCELS_URL = "https://services2.arcgis.com/dgGjZc6xAH5m5JyP/arcgis/rest/services/Parcels/FeatureServer/5/query"
ZONING_URL = "https://services2.arcgis.com/dgGjZc6xAH5m5JyP/arcgis/rest/services/Zoning/FeatureServer/22/query"

# canonical (category, threat) pairs
SF   = ("Single-Family Residential", "Low")
TWO  = ("Two-Family / Low-Density Residential", "Low")
TWOm = ("Two-Family / Low-Density Residential", "Medium")
TH   = ("Townhouse / Med-Density Residential", "Medium")
MF   = ("Multifamily Residential", "High")
MIX  = ("Mixed Use", "Medium")
MIXH = ("Mixed Use", "High")
COM  = ("Commercial", "Low")
COMm = ("Commercial", "Medium")
OFF  = ("Office", "Low")
IND  = ("Industrial / Business Park", "Low")
INST = ("Institutional / Governmental", "Low")
PARK = ("Park / Recreation", "Low")
AG   = ("Agricultural / Rural", "Low")
MH   = ("Manufactured Home", "Low")
PLN  = ("Planned / Overlay", "Unknown")

CROSSWALK = {
    "City of Boise": {
        "A-1": AG, "A-2": AG,
        "R-1A": SF, "R-1B": SF, "R-1C": SF,
        "R-2": TWOm, "R-3": MF,
        "MX-1": MIXH, "MX-2": MIXH, "MX-3": MIXH, "MX-4": MIXH,
        "MX-5": MIXH, "MX-U": MIXH, "MX-H": MIXH,
        "I-1": IND, "I-2": IND, "I-3": IND,
        "SP-01": PLN, "SP-02": PLN, "SP-03": PLN, "SP-04": PLN,
    },
    "City of Meridian": {
        "R-2": SF, "R-4": SF, "R-8": TH, "R-15": MF, "R-40": MF,
        "L-O": OFF, "C-N": COM, "C-C": COMm, "C-G": COMm,
        "O-T": MIXH, "TN-R": TH, "TN-C": MIXH,
        "M-E": IND, "H-E": IND, "I-L": IND,
    },
    "Ada County": {
        "RUT": AG, "RR": AG, "RP": AG, "RSW": SF, "R1M": MH,
        "R1": SF, "R2": SF, "R4": SF, "R6": TWO, "R8": TH, "R12": MF, "R20": MF,
        "C1": COM, "C2": COM, "LO": OFF,
        "M1": IND, "M2": IND, "M3": IND, "PC": PLN,
    },
    "City of Kuna": {
        "A": AG, "R-1": SF, "R-2": SF, "R-3": SF, "R-4": SF, "R-5": SF, "R-6": TWO,
        "R-8": TH, "R-12": TH, "R-16": MF, "R-20": MF,
        "C-1": COM, "C-2": COM, "C-3": COM, "CBD": MIX, "L-O": OFF,
        "M-1": IND, "M-2": IND, "P": PARK, "PUD": PLN,
    },
    "City of Eagle": {
        "A": AG, "A-R": AG, "R-E": AG, "APD": PLN,
        "R-1": SF, "R-2": SF, "R-3": SF, "R-4": SF, "R-5": SF, "R-6": TWO, "R-9": TH,
        "R-10": TH, "R-12": MF, "R-15": MF,
        "BP": IND, "M-1": IND, "C-1": COM, "C-2": COM, "C-3": COM, "CBD": MIX,
        "MU": MIX, "L-O": OFF, "PS": INST,
    },
    "City of Garden City": {
        "R-1A": SF, "R-2": TWO, "R-3": MF, "R-20": MF,
        "C-1": COM, "C-2": COM, "LI": IND, "M": IND, "SAP -01": PLN,
    },
    "City of Star": {
        "R-1": SF, "R-2": SF, "R-3": SF, "R-4": SF, "R-5": SF, "R-7": TWO, "R-8": TH,
        "R-10": TH, "R-13": MF, "R-14": MF, "R-R": AG, "RT": AG,
        "C-1": COM, "C-2": COM, "CBD": MIX, "MU": MIX, "L-O": OFF, "LI": IND,
    },
}

ZONE_PLAIN = {
    # Boise
    "A-1": "Boise Open Land/Airport-Ag", "A-2": "Boise Open Land/Ag",
    "R-1A": "Boise Single-Family (large lot)", "R-1B": "Boise Single-Family (medium lot)",
    "R-1C": "Boise Single-Family (compact)", "R-2": "Two-Family / Low-Density",
    "R-3": "Boise Multifamily", "MX-1": "Boise Mixed-Use Neighborhood",
    "MX-2": "Boise Mixed-Use Community", "MX-3": "Boise Mixed-Use Regional",
    "MX-4": "Boise Mixed-Use (Gateway)", "MX-5": "Boise Mixed-Use (high intensity)",
    "MX-U": "Boise Mixed-Use Urban", "MX-H": "Boise Mixed-Use Healthcare",
    "I-1": "Boise Industrial (light)", "I-2": "Boise Industrial (general)",
    "I-3": "Boise Industrial (heavy)", "SP-01": "Specific Plan SP-01",
    "SP-02": "Specific Plan SP-02", "SP-03": "Specific Plan SP-03", "SP-04": "Specific Plan SP-04",
    # Meridian
    "R-4": "Meridian Med-Low Density Res (4 du/ac)", "R-8": "Meridian Medium Density Res (8 du/ac)",
    "R-15": "Meridian Med-High Density Res (15 du/ac)", "R-40": "Meridian High Density Res (40 du/ac)",
    "L-O": "Limited Office", "C-N": "Neighborhood Business", "C-C": "Community Business",
    "C-G": "General Retail & Service Commercial", "O-T": "Old Town (mixed use)",
    "TN-R": "Traditional Neighborhood Residential", "TN-C": "Traditional Neighborhood Center",
    "M-E": "Mixed Employment", "H-E": "High-Density Employment", "I-L": "Light Industrial",
    # Ada County
    "RUT": "County Rural-Urban Transition", "RR": "County Rural Residential",
    "RP": "County Rural Preservation/Foothills", "RSW": "County Residential (subdivision)",
    "R1": "County Residential R1", "R1M": "County Residential R1 (manufactured)",
    "R6": "County Residential R6", "R12": "County Residential R12 (MF)",
    "R20": "County Residential R20 (MF)", "C1": "County Neighborhood Commercial",
    "C2": "County Commercial", "LO": "County Limited Office",
    "M1": "County Manufacturing M1", "M2": "County Manufacturing M2", "M3": "County Manufacturing M3",
    "PC": "County Planned Community",
    # generic
    "A": "Agricultural", "A-R": "Agricultural-Residential", "R-E": "Residential Estates",
    "MU": "Mixed Use", "CBD": "Central Business District", "BP": "Business Park",
    "PS": "Public/Semi-Public", "LI": "Light Industrial", "M": "Manufacturing",
    "PUD": "Planned Unit Development", "APD": "Area of Planned Development", "P": "Public",
}

LANDUSE_SCHEME = {
    "name": "Ada County Assessor Property Code (PROPCODE: R/C/F/L/M)",
    "codes": {
        "R": ["Single Family Residential", "Residential (improved homes, condos, townhomes) - Ada PROPCODE R"],
        "C": ["Commercial", "Commercial property (retail/office/commercial condo) - Ada PROPCODE C"],
        "F": ["Agricultural / Rural", "Farm / agricultural land (ag-exempt acreage) - Ada PROPCODE F"],
        "L": ["Vacant Land", "Land (vacant lots + HOA/condo common-area land) - Ada PROPCODE L"],
        "M": ["Single Family Residential", "Manufactured / mobile home - Ada PROPCODE M"],
    },
    "vacant_buckets": ["Vacant Land"],
    "vacant_note": ("Ada County PROPCODE 'L' = Land (vacant lots incl. HOA/condo common-area land, "
                    "many at $0 value). Treated as undeveloped 'vacant' for the developable-land screen; "
                    "HOA commons, floodplain, foothills-preservation and airport land are then reasoned out "
                    "per parcel. PROPCODE: R=Residential, C=Commercial, F=Farm, L=Land, M=Manufactured."),
    "default_bucket": "Other / Unclassified",
    "public_owner_regex": None,  # Ada GIS publishes no owner; public land handled by reasoning + legal text
}

ZONING_SOURCES = [
    {"jurisdiction": j, "url": ZONING_URL, "code_field": "BASEZONE", "desc_field": "ZONING",
     "where": f"CITY='{j}'", "format": "geojson"}
    for j in ["City of Boise", "City of Meridian", "Ada County", "City of Kuna",
              "City of Eagle", "City of Garden City", "City of Star"]
]

PARCEL_SOURCE = {
    "name": "Ada County Assessor Parcels (AdaCountyGIS)", "county": "Ada",
    "url": PARCELS_URL,
    "fields": {"account": "PARCEL", "situs": "ADDRESS", "landuse_code": "PROPCODE",
               "legal": "LEGAL1", "total_value": "TOTALVALUE"},
    "dedupe_field": "PARCEL", "data_confidence": "full", "page": 1000,
}

SUBJECTS = {
    "CanyonRidge": {
        "name": "Canyon Ridge", "address": "2552 E Gowen Rd, Boise, ID 83716",
        "lat": 43.541734, "lon": -116.151198,
        "location_note": ("287-unit, 4-story apartment community (completed 2024) on the south/southeast "
                          "side of Boise Airport (Gowen Field), Columbia Village / Columbia Town Center area, "
                          "inside the Airport Influence Area along E Gowen Rd. Point from ArcGIS World "
                          "Geocoder (PointAddress, score 100)."),
    },
    "SeasonsMeridian": {
        "name": "Seasons at Meridian", "address": "2700 E Overland Rd, Meridian, ID 83642",
        "lat": 43.591935, "lon": -116.360877,
        "location_note": ("Apartment community on E Overland Rd in southeast Meridian, ~0.5 mi south of I-84 "
                          "near S Eagle Rd. Point from ArcGIS World Geocoder (PointAddress, score 100)."),
    },
}


def build(key):
    s = SUBJECTS[key]
    return {
        "subject": {"name": s["name"], "address": s["address"], "lat": s["lat"], "lon": s["lon"],
                    "location_note": s["location_note"]},
        "analysis_area": {"mode": "radius", "radius_mi": 5.0,
                          "note": f"5.0-mile geodesic radius around {s['name']}"},
        "parcel_sources": [dict(PARCEL_SOURCE)],
        "zoning_sources": [dict(z) for z in ZONING_SOURCES],
        "landuse_scheme": LANDUSE_SCHEME,
        "zoning_crosswalk": {j: {c: list(v) for c, v in tbl.items()} for j, tbl in CROSSWALK.items()},
        "zone_plain": ZONE_PLAIN,
        "nondev_owner_regex": r"\b(CITY|COUNTY|STATE|IDAHO|USA|UNITED STATES|BLM|FEDERAL|SCHOOL|DISTRICT|CHURCH|HOA|HOMEOWNER|OWNERS ASSOC|ASSOCIATION|COMMON|IRRIGATION|CEMETERY|ACHD|HIGHWAY|SEWER|WATER|UNIVERSITY|COLLEGE)\b",
        "company_owner_regex": r"\b(LLC|L\.L\.C|INC|CORP|LP|L\.P|LTD|COMPANY|CO\.|PARTNERS|HOLDINGS|GROUP|PROPERTIES|CAPITAL|TRUST|DEVELOPMENT|BUILDERS|HOMES|CONSTRUCTION)\b",
        "min_acres": 1.0,
        "min_compactness": 0.16,
        "data_gap_label": "No public zoning (data gap)",
        "crs_local": None,
        "branding": {"primary": "#0B4F6C", "accent": "#C9A227"},
    }


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2]
    for key in SUBJECTS:
        cfg = build(key)
        out = base / key / "config.json"
        out.write_text(json.dumps(cfg, indent=2))
        print(f"wrote {out}  ({len(cfg['zoning_crosswalk'])} jurisdictions, "
              f"{sum(len(t) for t in cfg['zoning_crosswalk'].values())} zone codes)")
