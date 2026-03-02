import pandas as pd
import traceback
with open('excel_inspect_log.txt','w', encoding='utf-8') as log:
    try:
        # check for encryption/DRM first
        try:
            import olefile
            if olefile.isOleFile('RegionDataFinal.xlsx'):
                ole = olefile.OleFileIO('RegionDataFinal.xlsx')
                names = ole.listdir()
                if any('EncryptedPackage' in entry for entry in names) or any('DRM' in part for entry in names for part in entry):
                    log.write('file appears to be DRM/encrypted; aborting inspection\n')
                    raise ValueError('encrypted file')
        except ImportError:
            pass
        # try xlrd since file is actually an old .xls format
        xls = pd.ExcelFile('RegionDataFinal.xlsx', engine='xlrd')
        log.write('sheets ' + str(xls.sheet_names) + "\n")
        for sheet in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet)
                log.write(f"{sheet} {df.shape}\n")
                log.write(df.head().to_string() + "\n")
            except Exception as e:
                log.write(f"error reading sheet {sheet}: {e}\n")
    except Exception as e:
        log.write('exception reading workbook: ' + repr(e) + "\n")
        traceback.print_exc(file=log)
print('inspection complete')
