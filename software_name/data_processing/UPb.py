import xlsxwriter as writer

from .common import *


csvTableNames = ['GLITTER!: Isotope ratios.',
                 'GLITTER!: Isotopic ratios: 1 sigma uncertainty.',
                 'GLITTER!: Age estimates (ma).',
                 'GLITTER!: Age estimates: 1 sigma uncertainty (ma).',
                 'GLITTER!: Mean Raw CPS background subtracted.']
shortNames = ['Istopic ratios',
              'Ratio 1 sigma uncertainty',
              'Age',
              'Age 1 sigma uncertainty',
              'Mean Raw CPS background']
EndOfTableIndicator = ""
denomTh = 649.9625
denomU = 753.2491
'''
Reads a csv file then filters out the appropriate zircons and elements
sheet = workbook.add_worksheet(f) if you wish to add this sheet to table
csvfile = the string name of file your reading eg. 'run.csv'
IncludedFields = Which fields on the table at csvTableNames[4] you wish to include
excludedZircons = Which zircon do you wish to remove at every table?
'''
def addUPbSheet(sheet,csvfile,IncludedFields,excludedZircons=["610"]):
    t=table(csvfile,getSplitter(csvfile))
    for r in t:
        if standard(r[0]) in excludedZircons or r[0] in excludedZircons:
            t.remove(r)
    t,full = filterfields(t,csvTableNames[4],IncludedFields)
    try:
        addSheet(sheet,t)
    except:
        InvalidSpreadsheet = True
    return t
#Everything below is for testing:
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
def test():
    assertEquals([[1,2],[3,4]],table('new.csv'),"Function table:")
    assertEquals(':',getSplitter('new.csv'),"Function getSplitter")
    assertEquals(['example1.csv','example2.csv'],getFileList('example[1-2].csv'),"Function getFileList")
    assertEquals(['run1.csv','run2.csv','run3.csv'],getFileList('run[1-3].csv'),"Function getFileList")
    assertEquals(['data'],filterfields(['Table Name',['field','data','field'],[0.453324,435234,34.5435]],'Table Name',['data']),"Function filterfields")
'''
Returns the table with a cetain amount of includedFields by specifying the name of table first
t = the table that has it's name above it's contents eg. ['Table Name',['field','data','field']]
tablename = 'Table Name' or 0 if talking about a position
IncludedFields = the fields you wish to include eg. ['data']
'''
def filterfields(t,tablename,IncludedFields):
    current=0
    future=0
    cps = begr(t,tablename)
    nrows=[]
    for rec in t[cps+1]:
        r=cps+1
        if rec in IncludedFields:
            if tablename == -1:
                print(rec,"is in",IncludedFields)
            try:
                while t[r][current]!='':
                    t[r][future]=t[r][current]
                    r=r+1
            except:
                EndWhileOnError = True
            future=future+1
        nrows.append(r-cps-1)
        current=current+1
    r=cps+1
    x = max(nrows)
    for i in range(r,r+x):
        inc = len(IncludedFields)
        #for j in range(len(IncludedFields)-1,len(t[i])):
        t[i]= t[i][:len(IncludedFields)]
    return t,t[cps+1:cps+x+1]
def begr(t,tablename):
    if type(tablename)==type(3) or type(tablename)==type(0.5):
        return tablename
    cps=0
    while cps<len(t) and t[cps][0]!=tablename:
        cps=cps+1
    return cps
def combine(tlist,tablenameIndex,IncludedZircons):
    comb = [tlist[0][begr(tlist[0],csvTableNames[tablenameIndex])+1]]
    for t in tlist:
        r=begr(t,csvTableNames[tablenameIndex])+1   
        while t[r][0]!=EndOfTableIndicator and r<len(t):
            if standard(t[r][0]) in IncludedZircons or t[r][0] in IncludedZircons or '*' in IncludedZircons:
                if t[r][0]!=comb[0][0]:
                    comb.append(t[r])
            r=r+1
        #print(comb)
    return comb
    

def alternate(t,s):
    a = [column(t,0)]
    for i in range(1,len(t[0])):
        a.append(column(t,i))
        a.append(column(s,i))
    alt = [list(x) for x in zip(*a)]
    for j in range(2,len(alt[0]),2):
        alt[0][j] = "1 sigma"
    return alt        
def groups(t):
    if len(t[0])<4:
        t[0].append("Zircon number")
        t[0].append("Sequence number")
    for r in range(1,len(t)):
        for c in range(len(t[0])):
            if c=="Th232":
                t[r][c]=record(t[r][c])/denomTh
            if c=="U238":
                t[r][c]=record(t[r][c])/denomU
        t[r].append(r)
    return t
def rho(ratios):
    t = []
    for i in range(5):
        t.append(column(ratios,-i))
    t = [list(x) for x in zip(*t)]
    t[0].append("RHO")
    for i in range(1,len(t)):
        t[i].append(record(t[i][-1],t[i][-2])/record(t[i][-3],t[i][-4]))
    return t
def sigma(t,sig):
    sigmas = []
    for i in range(len(t[0])):
        if 'sigma' in t[0][i]:
            t[0][i] = str(sig)+' sigma'
            sigmas.append(i)
    for r in range(1,len(t)):
        for c in sigmas:
            t[r][c] = record(t[r][c],1/sig)
    return t
def SplitStandards(sheet,tables,titles):
    c=0
    for t in range(len(tables)):
        sheet.write(0,c,titles[t])
        addSheet(sheet,tables[t],1,c)
        c=c+len(tables[t][0])+1
def UPb():
    print("This particular python file will read the data recorded by the Laser device for U-Pb data.")
    print("You have to specify the name of the csv file and input the range of numbers within that name:")
    print("For example if you type run[1-3].csv then this program will read run1.csv,run2.csv and run3.csv")
    print("Each of these csv files will then be placed into 1 excel spreadsheet with the name of your choice.")
    print("The output excel file will remove sample '610-01' out of the spreadsheet")
    IncludedFields = ['Analysis_#','Pb206','Pb207','Pb208','Th232','U238']
    print("The Mean Raw CPS background table will include only these following fields:")
    print(IncludedFields)
    print("Remember you must name the input csv file with a .csv extention and the output excel spreadsheet with a .xlsx extension eg. runs.xlsx")
    print("This program was created and developed by Mark Collier on 17 August 2017 [Contact:+61466523090]\n")
    files = getFileList('Dec04_RUN[1-4]_UPb.csv')#input("Enter name and number range of run files eg. run[2-4].csv : "))
    output = 'Output.xlsx'#input("Enter the name of the new excel file with a .xlsx extension : ")
    workbook = writer.Workbook(output)#'C:/Users/markc_000/Google Drive/CITS3200/Project/Client/U-Pb and TE data/U-Pb/Output.xlsx')
    tlist = []
    conc = []
    for f in files:
        #If you need the run files in the Output then remove "" below
        tlist.append(addUPbSheet("workbook.add_worksheet(f)",f,IncludedFields))
        conc.append(addUPbSheet("workbook.add_worksheet(f)",f,['Analysis_#','Th232','U238']))
    allZircons=column(combine(tlist,0,'*'),0)
    standards = standard(allZircons)
    for s in standards:
        if s == 'Analysis_#':
            IncludedZircons=allZircons
            s="raw"
        else:
            IncludedZircons=s 
        ratios = alternate(combine(tlist,0,IncludedZircons),combine(tlist,1,IncludedZircons))
        ages = alternate(combine(tlist,2,IncludedZircons),combine(tlist,3,IncludedZircons))
        concentrations = groups(combine(conc,4,IncludedZircons))  
        if s=='raw':
            addSheet(workbook.add_worksheet("Ratios raw"),ratios)
            addSheet(workbook.add_worksheet("Ages raw"),ages)
        else:
            r = sigma(copy.deepcopy(ratios),2)
            tablesToPutOnThisStandard = [r,concentrations,sigma(ages,2)]
            tablesToPutOnThisStandard.append(rho(copy.deepcopy(ratios)))
            titlesOfEachTable = ["Ratios","Concentrations","Ages","Normal Concordia data"]
            SplitStandards(workbook.add_worksheet(s),tablesToPutOnThisStandard,titlesOfEachTable)
    try:    
        workbook.close()
    except:
        input("You must close "+output+" before continuing...")
        UPb()
UPb()