import pandas as pd
import json

# Define GEO mapping for regions
geo_mapping = {
    'APAC': ['East Asia', 'Southeast Asia', 'Australia Central', 'Australia Central 2', 'Australia East', 
             'Australia Southeast', 'Japan East', 'Japan West', 'Korea Central', 'Korea South', 
             'Indonesia Central', 'Malaysia South', 'Malaysia West', 'New Zealand North', 'Taiwan North',
             'Taiwan Northwest', 'Jio India Central', 'Jio India West', 'Central India', 'South India', 'West India'],
    'EMEA': ['Austria East', 'Belgium Central', 'North Europe', 'West Europe', 'France Central', 'France South',
             'Germany North', 'Germany West Central', 'Italy North', 'Norway East', 'Norway West', 
             'Poland Central', 'Spain Central', 'Sweden Central', 'Sweden South', 'Switzerland North',
             'Switzerland West', 'Denmark East', 'Israel Central', 'Israel Northwest', 'Qatar Central',
             'South Africa North', 'South Africa West', 'UAE Central', 'UAE North', 'UK South', 'UK West'],
    'NOAM': ['Central US', 'East US', 'East US 2', 'North Central US', 'South Central US', 'West US',
             'West US 2', 'West US 3', 'West Central US', 'Canada Central', 'Canada East', 'Mexico Central',
             'USGov Virginia', 'USGov Texas', 'USGov Arizona', 'USDoD Central', 'USDoD East',
             'USNat East', 'USNat West', 'USSec East', 'USSec West', 'USSec West Central',
             'Central US EUAP', 'East US 2 EUAP', 'East US STG', 'South Central US STG', 'Chile Central']
}

# Read CSV
df = pd.read_csv('RegionDataCSV.csv')

# Extract regions (starting from row 16)
regions = []
region_types_map = {}
cloud_types_map = {}

# Get region types (rows 10-13)
rt_start = None
ct_start = None
for idx, row in df.iterrows():
    if pd.notna(row['Cloud Type']) and row['Cloud Type'] == 'Region Type':
        rt_start = idx + 1
    if pd.notna(row['Cloud Type']) and row['Cloud Type'] == 'Region':
        ct_start = idx + 1
        break

# Map region types
if rt_start:
    for i in range(4):
        if rt_start + i < len(df):
            region_type = df.iloc[rt_start + i, 0]
            if pd.notna(region_type) and region_type not in ['', 'Region']:
                for region in df.iloc[ct_start:, 0]:
                    if pd.notna(region):
                        region_types_map[region] = region_type

# Group regions by GEO
geo_regions = {}
for geo, region_list in geo_mapping.items():
    geo_regions[geo] = []
    for region in region_list:
        if region in df['Cloud Type'].values:
            cloud_type = df[df['Cloud Type'] == region]['Description'].values[0] if len(df[df['Cloud Type'] == region]) > 0 else 'Unknown'
            region_type = 'Standard'  # Default, since we don't have explicit type mapping in clean CSV
            geo_regions[geo].append({
                'name': region,
                'regionType': region_type,
                'cloudType': 'Public'  # Default based on CSV structure
            })

# Save as JSON for the web page
with open('region_data.json', 'w') as f:
    json.dump(geo_regions, f, indent=2)

print("Data processed and saved to region_data.json")
print(f"APAC regions: {len(geo_regions['APAC'])}")
print(f"EMEA regions: {len(geo_regions['EMEA'])}")
print(f"NOAM regions: {len(geo_regions['NOAM'])}")

# === Workloads: try to create workloads.json from available sources ===
workloads = {}

# 1) Try to read Workloads.csv (expected columns: Workload,Region,Status)
try:
    wf = pd.read_csv('Workloads.csv')
    for _, r in wf.iterrows():
        wl = str(r.get('Workload')).strip()
        region = str(r.get('Region')).strip()
        status = str(r.get('Status')).strip() if pd.notna(r.get('Status')) else 'Deployed'
        if wl and wl not in ['nan', 'None']:
            workloads.setdefault(wl, []).append({'region': region, 'status': status})
    print('Loaded workloads from Workloads.csv')
except Exception:
    # 2) Try to read a sheet named 'Workloads' from RegionDataFinal.xlsx
    try:
        import openpyxl
        wb = openpyxl.load_workbook('RegionDataFinal.xlsx', data_only=True)
        sheet_name = None
        for name in wb.sheetnames:
            if 'work' in name.lower():
                sheet_name = name
                break
        if sheet_name:
            ws = wb[sheet_name]
            rows = list(ws.values)
            if rows:
                headers = [str(h).strip() for h in rows[0]]
                for row in rows[1:]:
                    rowd = {headers[i]: row[i] if i < len(row) else None for i in range(len(headers))}
                    wl = str(rowd.get('Workload') or rowd.get('workload') or '').strip()
                    region = str(rowd.get('Region') or rowd.get('region') or '').strip()
                    status = str(rowd.get('Status') or rowd.get('status') or 'Deployed').strip()
                    if wl:
                        workloads.setdefault(wl, []).append({'region': region, 'status': status})
            print(f"Loaded workloads from sheet '{sheet_name}' in RegionDataFinal.xlsx")
    except Exception:
        # no workloads source found — produce empty placeholders for expected workloads
        workloads = {'IC3': [], 'OPG': []}

# Save workloads.json
with open('workloads.json', 'w') as wf:
    json.dump(workloads, wf, indent=2)

print('Workloads processed and saved to workloads.json')
