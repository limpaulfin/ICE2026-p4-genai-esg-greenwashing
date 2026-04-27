#!/usr/bin/env python3
"""Task 02: Process GHG Emissions & Renewable Energy Data."""

import json
import pandas as pd
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(BASE, 'data', 'processed')
YEAR_MIN, YEAR_MAX = 2010, 2022

def load_json(filename):
    with open(os.path.join(PROCESSED, filename)) as f:
        return json.load(f)

def filter_years(df):
    return df[(df['year'] >= YEAR_MIN) & (df['year'] <= YEAR_MAX)].sort_values('year').reset_index(drop=True)

def main():
    korea_ghg = filter_years(pd.DataFrame(load_json('wb-korea-ghg-cleaned.json')))
    korea_ren = filter_years(pd.DataFrame(load_json('wb-korea-renewable-cleaned.json')))
    multi_ghg = filter_years(pd.DataFrame(load_json('wb-multi-country-ghg-cleaned.json')))

    # Build Korea ESG indicators
    indicators = korea_ghg[['year', 'value']].rename(columns={'value': 'ghg_mt_co2e'})
    ren_merge = korea_ren[['year', 'value']].rename(columns={'value': 'renewable_pct'})
    indicators = indicators.merge(ren_merge, on='year', how='outer').sort_values('year')
    indicators['ghg_yoy_change_pct'] = indicators['ghg_mt_co2e'].pct_change() * 100

    indicators.to_csv(os.path.join(PROCESSED, 'korea-esg-indicators.csv'), index=False)
    print("=== Korea ESG Indicators (2010-2022) ===")
    print(indicators.to_string(index=False))

    # Descriptive statistics
    for col, label in [('ghg_mt_co2e', 'GHG (Mt CO2e)'), ('renewable_pct', 'Renewable (%)')]:
        print(f"\n=== Descriptive Stats: {label} ===")
        print(indicators[col].dropna().describe().to_string())

    # Multi-country pivot
    ghg_pivot = multi_ghg.pivot_table(index='year', columns='country_name', values='value').sort_index()
    ghg_pivot.to_csv(os.path.join(PROCESSED, 'multi-country-ghg-comparison.csv'))
    print("\n=== Multi-Country GHG (Mt CO2e) ===")
    print(ghg_pivot.to_string())

    # Key findings
    g10, g22 = indicators.query('year==2010')['ghg_mt_co2e'].values[0], indicators.query('year==2022')['ghg_mt_co2e'].values[0]
    peak = indicators.loc[indicators['ghg_mt_co2e'].idxmax()]
    r10, r22 = indicators.query('year==2010')['renewable_pct'].values[0], indicators.query('year==2022')['renewable_pct'].values[0]
    print(f"\n=== KEY FINDINGS ===")
    print(f"GHG 2010: {g10:.1f} | 2022: {g22:.1f} | Peak: {peak['ghg_mt_co2e']:.1f} ({int(peak['year'])})")
    print(f"Change: {((g22-g10)/g10*100):.1f}% | Renewable: {r10:.1f}% -> {r22:.1f}%")

if __name__ == '__main__':
    main()
