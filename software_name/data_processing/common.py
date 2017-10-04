"""
File for functions common to TE and U-Pb processing
"""
import copy
import xlsxwriter

    
'''
Tries to evaluate and divide a variable for each record in a table.
Variable = can be a string int or float to be evaluated
d = variable to divide it by
returning value is number and never a string
'''
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
'''
finds all the L's that has by in it
'''
def listfilter(L,by):
    c = []
    for n in L:
        if by in n:
            c.append(n)
    return c
'''
Finds whether the csv file is comma seperated or semi-colon
'''
def getSplitter(file):
    r=read(file)
    if ';' in r:
        return ';'
    if ',' in r:
        return ','
    if '\t' in r:
        return '\t'
'''
Returns a list of lines from a file.
fileName = 'single.txt' will look in current directory
fileName = 'C:/single.txt' will look in C directory
'''
def readln(FileName='C:/untitled.txt'):
    return read(FileName).split('\n')
'''
Return the entire string of a file
fileName = 'single.txt' will look in current directory
fileName = 'C:/single.txt' will look in C directory
'''
def read(FileName='C:/untitled.txt'):
    f=str(FileName).replace('\\','/').replace('\t','/t').replace('\n','/n').replace('\0','/0')
    try:
        with open(f) as infile:
            contents=infile.read()
        infile.close()
    except:
        contents="This file does not exist"
    return str(contents)
'''
For testing whether a particular expression that includes functions return an expected value
eg. we could test the function with following parameters
expected = 3
actual = record(6,2)
message = 'Function record'

'''
def assertEquals(expected,actual,message=""):
    if expected!=actual:
        print(message,"Test failed")
    else:
        print(message,"Test passed!!")
    print("   Expected value was:")
    print("        ",expected)
    print("   But the actual value is:")
    print("        ",actual)
    return expected
'''
Writes a 2D array t into a sheet within a workbook
'''
def addSheet(sheet,t,sheetr=0,sheetc=0):
    for r in range(len(t)):
        for c in range(len(t[r])):
            sheet.write(sheetr+r,sheetc+c,evalif(t[r][c]))
    return t
'''
Return a 2D array from reading a file
fileName = 'single.txt' will look in current directory
fileName = 'C:/single.txt' will look in C directory
'''
def table(FileName='C:/run.csv',Splitter=','):
    f = readln(FileName)
    t=[]
    for r in f:
        t.append(r.split(Splitter))
    return t
'''
Tries to return a number but if it can't just return the string
'''
def evalif(n):
    try:
        return eval(n)
    except:
        return n
'''
Returns column n of t as a list
'''
def column(t,n):
    col = []
    for row in t:
        col.append(row[n])
    return col
'''
Returns a list of files with their corresponding number range
eg. getFileList('example[1-3].csv') = ['example1.csv','example2.csv','example3.csv']
'''
def getFileList(filename="example[1-3].csv"):
    beg = filename.split('[')[0]
    end = filename.split(']')[1]
    nrange = filename.split('[')[1].split(']')[0]
    start = eval(nrange.split('-')[0])
    finish = eval(nrange.split('-')[1])
    files = []
    for i in range(start,finish+1):
        files.append(beg+str(i)+end)
    return files
'''
Removes spaces or empty Strings from a list
'''
def nospaces(slist):
    spacelis = []
    for i in range(len(slist)):
        slist[i]=slist[i].replace(' ','')
        if slist[i]!='':
            spacelis.append(slist[i])
    return spacelis
'''
Return the row number of the first tablename searched in column SearchColumnNo
'''
def begr(t,tablename,SearchColumnNo = 0):
    if type(tablename)==type(3) or type(tablename)==type(0.5):
        return tablename
    cps=0
    while cps<len(t) and t[cps][SearchColumnNo]!=tablename:
        cps=cps+1
    return cps
'''
Removes any digits from string n
'''
def rnums(n):
    result = []
    for i in n:
        if not i.isdigit():
            result.append(i)
    return ''.join(result)
'''
Converts a zircon or a list of zircons into a standard or a standard list
'''
def standard(zirconName,Splitter='-'):
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
'''
Prints and returns n
'''
def see(n):
    print(n)
    return n
