"""Validate and clean World Bank ESG datasets for P4 paper."""
import json
from pathlib import Path
from wb_utils import parse_wb_json, interpolate_nulls, generate_report

BASE = Path("/home/fong/Projects/ICE-2026-HUIT/p4-genai-esg-greenwashing")
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"
PROCESSED.mkdir(exist_ok=True)

FILES = {
    "wb-korea-ghg.json": {"indicator": "EN.GHG.CO2.MT.CE.AR5", "country": "KOR"},
    "wb-korea-renewable.json": {"indicator": "EG.FEC.RNEW.ZS", "country": "KOR"},
    "wb-korea-gdp-growth.json": {"indicator": "NY.GDP.MKTP.KD.ZG", "country": "KOR"},
    "wb-multi-country-ghg.json": {"indicator": "EN.GHG.CO2.MT.CE.AR5", "country": "multi"},
}

all_results = {}

for fname, expected in FILES.items():
    with open(RAW / fname) as f:
        raw = json.load(f)

    rows, nulls, indicators, countries, dates_sorted = parse_wb_json(raw)
    date_range = f"{dates_sorted[0]}-{dates_sorted[-1]}"

    ind_match = expected["indicator"] in indicators
    country_match = len(countries) > 1 if expected["country"] == "multi" else expected["country"] in countries

    if nulls:
        rows = interpolate_nulls(rows)

    out_path = PROCESSED / fname.replace(".json", "-cleaned.json")
    with open(out_path, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"Saved: {out_path} ({len(rows)} records)")

    all_results[fname] = {
        "records": len(rows), "nulls": len(nulls), "date_range": date_range,
        "countries": sorted(countries), "indicators": sorted(indicators),
        "ind_match": ind_match, "country_match": country_match, "null_years": nulls,
    }

report_path = BASE / "data" / "validation-report.md"
generate_report(all_results, report_path)
print(f"\nValidation report: {report_path}")
