import pandas as pd

with open('regioninfo_inspect_log.txt', 'w', encoding='utf-8') as log:
    # try openpyxl first
    try:
        xls = pd.ExcelFile('RegionInformation.xlsx', engine='openpyxl')
    except Exception as e:
        log.write('openpyxl failed: ' + str(e) + '\n')
        try:
            xls = pd.ExcelFile('RegionInformation.xlsx', engine='xlrd')
        except Exception as e2:
            log.write('xlrd also failed: ' + str(e2) + '\n')
            raise

    log.write('sheets ' + str(xls.sheet_names) + '\n')
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        log.write(f"{sheet} {df.shape}\n")
        log.write(df.head().to_string() + "\n")
