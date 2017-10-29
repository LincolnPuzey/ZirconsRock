"""
File for functions common to TE and U-Pb processing
"""
import copy
import xlsxwriter
import time
import datetime


def now(form='%A %d/%m/%Y %-I:%M:%S:%f'):
    ts = time.time()
    if form=="micro":
        return str(ts).split('.')[1]
    return datetime.datetime.fromtimestamp(ts).strftime(form)
def allEqual(lis,to=False):
    if type(to)==type(False):
        to=lis[0]
    for li in lis:
        if li!=to:
            return False
    return True

def record(Variable, d=1):
    """
    Tries to evaluate and divide a variable for each record in a table.
    Variable = can be a string int or float to be evaluated
    d = variable to divide it by
    returning value is number and never a string
    """

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


def listfilter(L, by):
    """
    finds all the L's that has by in it
    """

    c = []
    for n in L:
        if by in n:
            c.append(n)
    return c


def getSplitter(file):
    """
    Finds whether the csv file is comma seperated or semi-colon
    """

    r=read(file)
    if ';' in r:
        return ';'
    if ',' in r:
        return ','
    if '\t' in r:
        return '\t'


def readln(FileName='C:/untitled.txt'):
    """
    Returns a list of lines from a file.
    fileName = 'single.txt' will look in current directory
    fileName = 'C:/single.txt' will look in C directory
    """

    return read(FileName).split('\n')


def read(FileName='C:/untitled.txt'):
    """
    Return the entire string of a file
    fileName = 'single.txt' will look in current directory
    fileName = 'C:/single.txt' will look in C directory
    """

    f=str(FileName).replace('\\','/').replace('\t','/t').replace('\n','/n').replace('\0','/0')
    try:
        with open(f) as infile:
            contents=infile.read()
        infile.close()
    except:
        contents="This file does not exist"
    return str(contents)


def write(Text='', File='untitled.txt'):
    with open(File,"w") as outfile:
        print(Text,file=outfile)
    outfile.close()


def writeln(LineNumber=0, Text='', File='untitled.txt'):
    lin=round(abs(LineNumber))
    f=readln(File)
    if lin>=len(f):
        f+=['']*(lin-len(f))
        f.append(Text)
    else:
        f[lin]=Text
    if f[-1] == "" and f[-2] == "":
        f=f[:-2]
    write("\n".join(f),File)


def assertEquals(expected, actual, message=""):
    """
    For testing whether a particular expression that includes functions return an expected value
    eg. we could test the function with following parameters
    expected = 3
    actual = record(6,2)
    message = 'Function record'
    """

    if expected!=actual:
        print(message,"Test failed")
    else:
        print(message,"Test passed!!")
    print("   Expected value was:")
    print("        ",expected)
    print("   But the actual value is:")
    print("        ",actual)
    return expected


def addSheet(sheet, t, sheetr=0, sheetc=0):
    """
    Writes a 2D array t into a sheet within a workbook
    """

    for r in range(len(t)):
        for c in range(len(t[r])):
            sheet.write(sheetr+r,sheetc+c,evalif(t[r][c]))
    return t


def get_table(FileName='C:/run.csv', Splitter=','):
    """
    Return a 2D array from reading a file
    fileName = 'single.txt' will look in current directory
    fileName = 'C:/single.txt' will look in C directory
    """

    f = readln(FileName)
    t=[]
    for r in f:
        t.append(r.split(Splitter))
    return t


def evalif(n):
    """
    Tries to return a number but if it can't just return the string
    """

    try:
        if '-' in n:
            return n
        return eval(n)
    except:
        return n


def column(t, n):
    """
    Returns column n of t as a list
    """

    col = []
    for row in t:
        col.append(row[n])
    return col


def nospaces(slist):
    """
    Removes spaces or empty Strings from a list
    """

    spacelis = []
    for i in range(len(slist)):
        slist[i]=slist[i].replace(' ','')
        if slist[i]!='':
            spacelis.append(slist[i])
    return spacelis


def begr(t, tablename, SearchColumnNo = 0):
    """
    Return the row number of the first tablename searched in column SearchColumnNo
    """

    if type(tablename)==type(3) or type(tablename)==type(0.5):
        return tablename
    cps=0
    while cps<len(t) and t[cps][SearchColumnNo]!=tablename:
        cps=cps+1
    return cps


def rnums(n):
    """
    Removes any digits from string n
    """

    result = []
    for i in n:
        if not i.isdigit():
            result.append(i)
    return ''.join(result)


def standard(zirconName, Splitter='-'):
    """
    Converts a zircon or a list of zircons into a standard or a standard list
    """

    if type(zirconName)==type(["","STDGJ"]):
        stans = []
        for z in zirconName:
            stan = z.split(Splitter)[0]
            if stan not in stans:
                stans.append(stan)
        return stans
    else:
        z = str(zirconName)
        return z.split(Splitter)[0]


def see(n):
    """
    Prints and returns n
    """

    print(n)
    return n
