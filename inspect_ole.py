import olefile

ole = olefile.OleFileIO('RegionDataFinal.xlsx')
print('storage list:')
for entry in ole.listdir():
    print(entry)
