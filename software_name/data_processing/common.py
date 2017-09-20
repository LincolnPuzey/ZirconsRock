import xlsxwriter as writer

"""
File for functions common to TE and U-Pb processing
"""


def record(Variable,d=1):
    if d==1:
        v=str(Variable)
        try:
            return eval(v)
        except:
            return 0
    else:
        try:
            return record(Variable)/record(d)
        except:
            return 0


def getSplitter(file):
    r=read(file)
    if ';' in r:
        return ';'
    else:
        return ','


def readln(FileName='C:/untitled.txt'):
    return read(FileName).split('\n')


def read(FileName='C:/untitled.txt'):
    f=str(FileName)
    try:
        with open(f) as infile:
            contents=infile.read()
        infile.close()
    except:
        contents="This file does not exist"
    return str(contents)


def addSheet(sheet,t,sheetr=0,sheetc=0):
    for r in range(len(t)):
        for c in range(len(t[r])):
            sheet.write(sheetr+r,sheetc+c,evalif(t[r][c]))
    return t


def table(FileName='C:/run.csv',Splitter=','):
    f = readln(FileName)
    t=[]
    for r in f:
        t.append(r.split(Splitter))
    return t


def evalif(n):
    try:
        return eval(n)
    except:
        return n


def column(t,n):
    col = []
    for row in t:
        col.append(row[n])
    return col


def getFileList(filename="example[1-3].csv"):
    """
    Returns a list of files with their corresponding number range
    eg. getFileList('example[1-3].csv') = ['example1.csv','example2.csv','example3.csv']
    """
    beg = filename.split('[')[0]
    end = filename.split(']')[1]
    nrange = filename.split('[')[1].split(']')[0]
    start = eval(nrange.split('-')[0])
    finish = eval(nrange.split('-')[1])
    files = []
    for i in range(start,finish+1):
        files.append(beg+str(i)+end)
    return files


def nospaces(slist):
    spacelis = []
    for i in range(len(slist)):
        slist[i]=slist[i].replace(' ','')
        if slist[i]!='':
            spacelis.append(slist[i])
    return spacelis


def rnums(n):
    result = []
    for i in n:
        if not i.isdigit():
            result.append(i)
    return ''.join(result)


def standard(zirconName):
    if type(zirconName)==type(["","STDGJ"]):
        stans = []
        for z in zirconName:
            stan = z.split('-')[0]
            if stan not in stans:
                stans.append(stan)
        return stans
    else:
        z = str(zirconName)
        return z.split('-')[0]
