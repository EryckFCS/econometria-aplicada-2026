import pandas as pd
import requests
import os

def fetch_wb_data(indicator, country='EC'):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=100"
    response = requests.get(url)
    data = response.json()
    if len(data) > 1:
        records = data[1]
        return {r['date']: r['value'] for r in records if r['value'] is not None}
    return {}

print("Fetching Gender Participation Gap indicators...")
male_participation = fetch_wb_data('SL.TLF.CACT.MA.ZS')
female_participation = fetch_wb_data('SL.TLF.CACT.FE.ZS')

# Calculate gap (Male - Female)
gap_data = []
for year in sorted(male_participation.keys()):
    if year in female_participation:
        gap = male_participation[year] - female_participation[year]
        gap_data.append({'year': int(year), 'gender_participation_gap': gap})

df_gap = pd.DataFrame(gap_data)
output_path = "data/raw/gender_gap_data.parquet"
df_gap.to_parquet(output_path)
print(f"Saved gender gap data to {output_path}")
