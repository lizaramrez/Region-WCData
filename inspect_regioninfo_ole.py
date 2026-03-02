import olefile
print('isOle', olefile.isOleFile('RegionInformation.xlsx'))
ole = olefile.OleFileIO('RegionInformation.xlsx')
print('streams:')
for entry in ole.listdir():
    print(entry)
