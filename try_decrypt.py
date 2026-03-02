import msoffcrypto

with open('RegionDataFinal.xlsx','rb') as f:
    of = msoffcrypto.OfficeFile(f)
    print('is encrypted', of.is_encrypted())
    try:
        of.load_key(password='')
        with open('decrypted.xlsx','wb') as out:
            of.decrypt(out)
        print('decryption attempted, saved to decrypted.xlsx')
    except Exception as e:
        print('decryption failed:', e)
