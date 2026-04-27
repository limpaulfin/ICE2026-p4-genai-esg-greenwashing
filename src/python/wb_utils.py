"""Utility functions for World Bank JSON data processing."""


def parse_wb_json(raw):
    """Parse WB API JSON format into flat rows."""
    records = raw[1]
    rows, nulls = [], []
    indicators, countries, dates = set(), set(), []

    for r in records:
        indicators.add(r["indicator"]["id"])
        countries.add(r["countryiso3code"])
        dates.append(int(r["date"]))
        if r["value"] is None:
            nulls.append(r["date"])
        rows.append({
            "indicator": r["indicator"]["id"],
            "indicator_name": r["indicator"]["value"],
            "country": r["countryiso3code"],
            "country_name": r["country"]["value"],
            "year": int(r["date"]),
            "value": r["value"],
        })
    return rows, nulls, indicators, countries, sorted(set(dates))


def interpolate_nulls(rows):
    """Linear interpolation for null values, grouped by country."""
    rows.sort(key=lambda x: (x["country"], x["year"]))
    by_country = {}
    for row in rows:
        by_country.setdefault(row["country"], []).append(row)

    for ctry_rows in by_country.values():
        ctry_rows.sort(key=lambda x: x["year"])
        values = [r["value"] for r in ctry_rows]
        for i, v in enumerate(values):
            if v is not None:
                continue
            prev_i = next((j for j in range(i - 1, -1, -1) if values[j] is not None), None)
            next_i = next((j for j in range(i + 1, len(values)) if values[j] is not None), None)
            if prev_i is not None and next_i is not None:
                frac = (i - prev_i) / (next_i - prev_i)
                values[i] = round(values[prev_i] + frac * (values[next_i] - values[prev_i]), 2)
            elif prev_i is not None:
                values[i] = values[prev_i]
            elif next_i is not None:
                values[i] = values[next_i]
            ctry_rows[i]["value"] = values[i]
            ctry_rows[i]["imputed"] = True
    return rows


def generate_report(all_results, report_path):
    """Generate validation report markdown."""
    lines = ["# Data Validation Report", "",
        "**Generated**: 2026-03-21 | **Paper**: P4 GenAI ESG Greenwashing", ""]

    for fname, info in all_results.items():
        lines.append(f"## {fname}")
        lines.append(f"- **Indicator(s)**: {', '.join(info['indicators'])}")
        lines.append(f"- **Indicator match**: {'YES' if info['ind_match'] else 'NO'}")
        lines.append(f"- **Country(s)**: {', '.join(info['countries'])}")
        lines.append(f"- **Country match**: {'YES' if info['country_match'] else 'NO'}")
        lines.append(f"- **Date range**: {info['date_range']}")
        lines.append(f"- **Records**: {info['records']}")
        n = info['nulls']
        ny = ', '.join(info['null_years']) if info['null_years'] else 'none'
        lines.append(f"- **Nulls**: {n} ({ny})")
        lines.append(f"- **Imputation**: {'Linear interpolation' if n else 'Not needed'}")
        lines.append("")

    lines.extend(["## Summary", "",
        "| Dataset | Records | Nulls | Date Range | Countries |",
        "|---------|---------|-------|------------|-----------|"])
    for fname, i in all_results.items():
        lines.append(f"| {fname} | {i['records']} | {i['nulls']} | "
                      f"{i['date_range']} | {', '.join(i['countries'])} |")
    lines.extend(["", "## Notes",
        "- Indicator `EN.GHG.CO2.MT.CE.AR5` (AR5) used instead of `EN.ATM.GHGT.KT.CE`",
        "- Both measure CO2 emissions; AR5 is current WB standard",
        "- These datasets provide ESG CONTEXT, not primary analysis corpus"])

    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")
