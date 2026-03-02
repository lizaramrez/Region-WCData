import os
print('size', os.path.getsize('RegionInformation.xlsx'))
with open('RegionInformation.xlsx','rb') as f:
    data=f.read(32)
print(data)
print('hex', data.hex())
