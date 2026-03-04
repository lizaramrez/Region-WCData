import pandas as pd
import pandas as pd
import json

# Build region-to-geo mapping from OPG and IC3 CSVs only
geo_mapping = {'APAC': [], 'EMEA': [], 'NOAM': []}
region_to_geo = {}

def extract_regions_and_geos(csv_path):
    # Read the first two rows: first is geo, second is region name
    import csv
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) < 2:
            return
        geo_row = rows[0]
        region_row = rows[1]
        for idx in range(8, len(region_row)):
            region = region_row[idx].strip()
            geo = geo_row[idx].strip()
            region_obj = {"name": region, "regionType": "-", "cloudType": "-"}
            if geo in geo_mapping and region:
                # Only add if not already present (by name)
                if not any(r["name"] == region for r in geo_mapping[geo]):
                    geo_mapping[geo].append(region_obj)
                    region_to_geo[region] = geo


extract_regions_and_geos('OPGRegionData.csv')
extract_regions_and_geos('IC3RegionData.csv')

# Save geo_mapping to region_data.json (now with region objects)
with open('region_data.json', 'w', encoding='utf-8') as f:
    json.dump(geo_mapping, f, indent=2, ensure_ascii=False)
print('Geo mapping saved to region_data.json (with region objects)')
    
