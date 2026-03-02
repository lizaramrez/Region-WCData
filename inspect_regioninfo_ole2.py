import olefile

with open('regioninfo_ole_log.txt','w', encoding='utf-8') as log:
    log.write('isOle ' + str(olefile.isOleFile('RegionInformation.xlsx')) + '\n')
    try:
        ole = olefile.OleFileIO('RegionInformation.xlsx')
        for entry in ole.listdir():
            log.write(str(entry) + '\n')
    except Exception as e:
        log.write('ole error ' + str(e) + '\n')
