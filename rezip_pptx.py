import zipfile

in_file = 'vhr_13classes_deck.pptx'
out_file = 'vhr_13classes_deck_rezipped.pptx'

with zipfile.ZipFile(in_file, 'r') as zin:
    with zipfile.ZipFile(out_file, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            # read original data (directories will return b'')
            data = zin.read(info.filename)
            # write with same name
            zout.writestr(info.filename, data)

print('rezipped', out_file)
