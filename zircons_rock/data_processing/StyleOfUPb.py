def styleUPb(FileLocation):
    dirfile=str(FileLocation).replace('\\','/').replace('\t','/t').replace('\n','/n').replace('\0','/0')
    filename = dirfile.split('/')[-1]
