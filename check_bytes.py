with open('RegionDataFinal.xlsx','rb') as f:
    data = f.read(32)
print('bytes:', data)
print('hex:', data.hex())
