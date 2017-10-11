from .common import *
from .StyleOfUPb import *
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
testInputLocation = 'C:/Users/mark/Google Drive/CITS3200/CITS3200/test_files/inputs/Dec04_RUN[1-4]_UPb.csv'
testOutputLocation = 'C:/Users/mark/Google Drive/CITS3200/CITS3200/test_files/outputs/UPbOutput.xlsx'
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
'''
Compares functions to determine whether they work.
'''
def test():
    assertEquals([[1,2],[3,4]],table('new.csv'),"Function table:")
    assertEquals(':',getSplitter('new.csv'),"Function getSplitter")
    assertEquals(['example1.csv','example2.csv'],getFileList('example[1-2].csv'),"Function getFileList")
    assertEquals(['run1.csv','run2.csv','run3.csv'],getFileList('run[1-3].csv'),"Function getFileList")
    assertEquals(['STDGJ', '91500', 'MT', 'INT1', 'INT2'],standard(getAllZircons(getFileList(testInputLocation))),"Function standard(getAllZircons)")
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
'''
Using 1 type of table for every sheet combine this type into one big 2D array
tlist = list of 2D arrays of each csv file contents
tablenameIndex = The index of the table within each sheet
IncludedZircons = Zircons we want to search for or * for all of them
'''
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

'''
For each column in table t:
    Place the next column of s beside it
'''
def alternate(t,s):
    a = [column(t,0)]
    for i in range(1,len(t[0])):
        a.append(column(t,i))
        a.append(column(s,i))
    alt = [list(x) for x in zip(*a)]
    for j in range(2,len(alt[0]),2):
        alt[0][j] = "1 sigma"
    return alt
'''
Add sequence numbers, Zircon numbers and Concentrations together in table t in groups
'''
def groups(t):
    if len(t[0])<4:
        t[0].append("Zircon number")
        t[0].append("Sequence number")
    for r in range(1,len(t)):
        for c in range(len(t[0])):
            if c=="Th232":
                t[r][c]=record(t[r][c])
            if c=="U238":
                t[r][c]=record(t[r][c])
        t[r].append(r)
    return t
'''
Mutates the concentration values
'''
def ThUppm(conc,normalised,ThPPM,UPPM):
    i=0
    for t in range(len(conc)):
        i=i+1
        r=begr(conc[t],csvTableNames[4])
        values = conc[t][r+2:]
        Th = record(avg(values,normalised,1),ThPPM)
        U = record(avg(values,normalised,2),UPPM)
        for i in range(r+2,len(conc[t])-1):
            conc[t][i][1]=record(conc[t][i][1],Th)
            conc[t][i][2]=record(conc[t][i][2],U)
def avg(values,normalised,c):
    sumNormalised = 0
    count = 0
    for z in range(len(values)):
        if normalised in values[z][0]:
            sumNormalised = sumNormalised + record(values[z][c])
            count = count +1
    return record(sumNormalised,count)
'''
Create the Normal Concordia data which calculates the rho values
'''
def rho(ratios):
    t = []
    for i in range(5):
        t.append(column(ratios,-i))
    t = [list(x) for x in zip(*t)]
    t[0].append("RHO")
    for i in range(1,len(t)):
        t[i].append(record(t[i][-1],t[i][-2])/record(t[i][-3],t[i][-4]))
    return t
'''
Create the Inverse Concordia data which calculates the RSD values
'''
def inverse(concordia):
    docols = [1,3]
    for d in docols:
        for r in range(1,len(concordia)):
            concordia[r][d+1]=record(1,concordia[r][d+1])

    for c in range(len(concordia[0])):
        header = concordia[0][c].split("/")
        if len(header)==2:
            concordia[0][c] = header[1]+"/"+header[0]
        elif header[0]=="1 sigma":
            concordia[0][c] = "RSD"
            for r in range(1,len(concordia)):
                av = "/AVERAGE($AJ$3:$AJ$"+str(len(concordia)+1)+")"
                if c==3:
                    av=av.replace("J","L")
                concordia[r][c] = "=100*"+str(concordia[r][c])+av
        if c==len(concordia[0])-1:
            for r in range(len(concordia)):
                concordia[r][c] = ""
    return concordia
        
'''
Change the sigma values by a multiple of sig
t = table with 1 sigma values
sig = multiplier by the 1 sigma values
'''
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
'''
Function that cares for a specified standard names sheet
sheet = The sheet with the name of the Standard
tables = list of 2D table arrays to add to the sheet
titles = list of titles that need to be added to the sheet
'''
def SplitStandards(sheet,tables,titles):
    c=0
    for t in range(len(tables)):
        sheet.write(0,c,titles[t])
        addSheet(sheet,tables[t],1,c)
        c=c+len(tables[t][0])+1
'''
Given a list of run csv files:
    return all of the zircons in the fileList
'''
def getAllZircons(fileList):
    tlist=[]
    for f in fileList:
        tlist.append(addUPbSheet("workbook.add_worksheet(f)",f,['Analysis_#']))
    a = column(combine(tlist,0,'*'),0)
    a.remove('Analysis_#')
    return a
'''
Main Function called to run the entire program
'''

def UPb(control,unknown, files, output):
#Parameters to add{
    normalised = "STDGJ"
    ThPPM = 20
    UPPM = 290
#}
    print("This particular python file will read the data recorded by the Laser device for U-Pb data.")
    print("Please ensure you are using Python version 3.6.2 on your computer")
    print("The output excel file will remove sample '610' out of the spreadsheet")
    IncludedFields = ['Analysis_#','Pb206','Pb207','Pb208','Th232','U238']
    print("The Mean Raw CPS background table will include only these following fields:")
    print(IncludedFields)
    print("This program was created and developed by Mark Collier in September 2017 [Contact:+61466523090]\n")
    # files = getFileList(testInputLocation)#getFileList(input("Enter the location and number range of run files eg. run[2-4].csv : "))
    # output = testOutputLocation#input("Enter the location of the new excel file with a .xlsx extension : ")
    workbook = xlsxwriter.Workbook(output)
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
            commonPb = workbook.add_worksheet("ToBeCommonLeadCorrected")
            addSheet(commonPb,combine(tlist,4,IncludedZircons),3,len(ratios[0])-1)
            addSheet(commonPb,ratios,3)
            '''
            ctrl = workbook.add_worksheet("Control Report")
            norm = workbook.add_worksheet("Normalized Report")
            addSheet(ctrl,alternate(combine(tlist,0,control),combine(tlist,1,control)))
            addSheet(norm,alternate(combine(tlist,0,normalised),combine(tlist,1,normalised)))
            '''
            ThUppm(conc,normalised,ThPPM,UPPM)
            report = workbook.add_worksheet("Report")
            addSheet(report,alternate(combine(tlist,0,unknown),combine(tlist,1,unknown)))
        else:
            r = sigma(copy.deepcopy(ratios),2)
            tablesToPutOnThisStandard = [r,concentrations,sigma(ages,2)]
            titlesOfEachTable = ["Ratios","Concentrations","Ages"]
            if s in unknown:
                concordia = rho(copy.deepcopy(ratios))
                tablesToPutOnThisStandard.append(concordia)
                titlesOfEachTable.append("Normal Concordia Plots")
                if len(concordia)>3:
                    tablesToPutOnThisStandard.append(inverse(copy.deepcopy(concordia)))
                    titlesOfEachTable.append("Inverse Concordia Plots")    
            ss = workbook.add_worksheet(s)
            SplitStandards(ss,tablesToPutOnThisStandard,titlesOfEachTable)
            
    try:
        workbook.close()
    except:
        input("You must close "+output+" before continuing...")
        UPb(control, unknown, files, output)
    styleUPb(output,standards)
