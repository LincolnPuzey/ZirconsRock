from .common import *

BeginningCell = "Element" #cell where program begins reading
EndingCell = "" #cell where program ends reading
ChondriteFile = 'Chondrite values.csv'
testInputLocation = 'C:/Users/mark/Google Drive/CITS3200/CITS3200/test_files/inputs/Dec04_RUN[1-4]_TE.csv'

def classify(cart,t,z="zircon eg. STDGJ-01"):
    if cart == "CART1":
        if data(t,z,"Lu")<20.7:
            if data(t,z,"Hf")<6200:
                return "Syenite"
            else:
                if data(t,z,"Lu")>2.7:
                    return "Carbonite"
                else:
                    return "Kimberlite"
        else:
            if data(t,z,"Lu")>601:
                return "Ne-syenite&Syenite Pegmatites"
            else:
                if data(t,z,"Hf")>8000:
                    if data(t,z,"Y")>4433:
                        if data(t,z,"U")>1149:
                            return "Granitoid(>75% SiO2)"
                        else:
                            return "Syenite/Monzonite"
                    else:
                        if data(t,z,"Hf")>10150:
                            if data(t,z,"Yb")>501:
                                return "Granitoid (70-75% SiO2)"
                            else:
                                return "Granitoid (>65% SiO2)"
                        else:
                            return "Dolerite"
                else:
                    return "Basalt"
    elif cart=="CART2":
        if data(t,z,"Lu")<20.7:
            if data(t,z,"Ta")<0.5:
                return "Syenite (93%)"
            else:
                if data(t,z,"Lu")>2.3:
                    return "Carbonite (79%)"
                else:
                    return "Kimberlite (94%)"
        else:
            if data(t,z,"U")<38:
                return "Ne-syenite & Syenite Pegmatites (93%)"
            else:
                if data(t,z,"Ta")<0.58:
                    return "Dolerite (71%)"
                else:
                    if data(t,z,"Hf")<8000:
                        return "Basalt (94%)"
                    else:
                        if data(t,z,"Ce")>3.9:
                            return "Larvikite (72%)"
                        else:
                            if data(t,z,"Nb")>170:
                                return "Granitoid >75% SiO2 (76%)"
                            else:
                                ThDivU = data(t,z,"Th")/data(t,z,"U")
                                if ThDivU>0.44:
                                    return "Granitoid 65-70% SiO2 (47%)"
                                else:
                                    return "Granitoid 70-75% SiO2 (70%)"
    elif cart in t[0]:
        return data(t,z,cart)
    elif '/' in cart:
        return data(t,z,cart)
    elif cart=="CART2000":
        return "At the moment the python file only specifies CART 1 and CART 2"
    else:
        return ""
'''
Provided the 2D array t with zircons against elements what number would I get from zircon on element?
zircon eg = 'STDGJ-01'
element eg = 'Ce'
'''
def data(t,zircon,element):
    if "/" in element:
        e=element.split("/")
        return record(data(t,zircon,e[0]),data(t,zircon,e[1]))
    r=0
    c=0
    try:
        while t[r][1]!=zircon:
            r=r+1
        while t[0][c]!=element:
            c=c+1
        Ce = t[r][c]
        La = t[r][c-1]
        Pr = t[r][c+1]
        ch = chond(element)
        return record(Ce)
    except:
        print("For the",t[0][1],"spreadsheet:")
        print("Cannot find value for Element:",element,"for zircon",zircon,"?")
        return eval(input("Please enter the value here: "))

'''
Main function that will call everything as needed
'''

def te():
    print("This particular python file will read the data recorded by the Laser device for Trace Elements.")
    print("Please ensure you are using Python version 3.6.2 on your computer")
    print("This program was created and developed by Mark Collier September 2017 [Contact:+61466523090]")
    print("You have to specify the name of the csv file and input the range of numbers within that name:")
    print("For example if you type run[1-3].csv then this program will read run1.csv,run2.csv and run3.csv")
    print("Data from every csv file will be added on top into your output spreadsheet.")
    print("This program uses Chondrite values.csv file:")
    print("     Column A lists the names of the sheets you will use in the Output xl file")
    print("     Every other column beside it will have 4 rows")
    print("     Row 1: You may add or remove as many elements you like")
    print("     Row 2: Enter the Chondrite values for each element")
    print("     Row 3: Include a list of zircons or standards that you wish to exclude")
    print("     Row 4: Include a list of elements that you wish to exclude")
    print("Remember you must name the input csv file with a .csv extention and the output excel spreadsheet with a .xlsx extension eg. runs.xlsx")
    print("Please save and close all xlsx files and csv files before continuing!\n")
    filelist = testInputLocation#input("Enter the location and number range of run files eg. run[2-4].csv : ")
    output = input("Enter the location of the new excel file with a .xlsx extension : ")
    files = getFileList(filelist)
    workbook = xlsxwriter.Workbook(output)
    t = table(ChondriteFile)
    for i in teSheetNamesIndicies(t):
        full=addTESheet(files,workbook.add_worksheet(t[i][0]),nospaces(t[i][1:]),nospaces(t[i+1][1:]),nospaces(t[i+2][2:]),nospaces(t[i+3][2:]))
        full[0][1] = t[i][0]
        k=4
        try:
            while i+k<len(t) and t[i+k][1]=="CARTS":
                carts = nospaces(t[i+k][3:])
                if len(carts)>0:
                    addClassifier(full,workbook.add_worksheet(t[i+k][2]),carts)
                k=k+1
        except:
            Finish = True
    try:    
        workbook.close()
    except:
        input("You must close "+output+" before continuing")
        workbook.close()
'''
Adds a sheet based upon the outline of a Classification sheet
full = 2D array of the table
sheet = the actual sheet we use in the spreadsheet
carts = the list of examples to classify
'''
def addClassifier(full,sheet,carts):
    sheet.write('B1','Analysis')
    sheet.write('A1','Sample')
    classifier = [["Sample","Analysis"]]
    for c in range(len(carts)):
        sheet.write(0,c+2,carts[c])
        classifier[0].append(carts[c])
    for r in range(1,len(full)):
        z=full[r][1]
        classifier.append([full[r][0],z])
        sheet.write(r,0,full[r][0])
        sheet.write(r,1,z)
        for c in range(len(carts)):
            content = classify(carts[c],full,z)
            sheet.write(r,c+2,content)
            classifier[r].append(content)
    return classifier
'''
Testing some our functions
'''
def test():
    assertEquals(['Hf177', 'Hf178'],listfilter(["Hf177","Hf178","Pb204"],"Hf"),"Function listfilter")
    assertEquals(['INT1-01', 'INT1-02'],listfilter(["INT1-01","INT2-01","INT1-02"],"INT1"))
    assertEquals(['INT1-01', 'INT2-01', 'INT1-02'],listfilter(["INT1-01","INT2-01","INT1-02"],"INT"))
    assertEquals(['hello'],nospaces([' hello ',' ']),"Function nospaces:")
    assertEquals("Hf",rnums("Hf177"),"Function rnums:")
    assertEquals(2,record(10,5),"Function record:")
    assertEquals("",record('h'))
    assertEquals(4,record(4))
    assertEquals("",record(4,""))
    assertEquals(0.613,chond("Ce"),"Function chond")
'''
Returns all of the zircons listed in a Trace Element File List
'''
def getAllZircons(files):
    zlist = []
    for f in files:
        t = table(f)
        bi=begr(t,BeginningCell)
        for row in t[bi]:
            if row != BeginningCell:
                zlist.append(row)
    return zlist
'''
Add a spreadsheet of zircons against elements with it's included Chondrite values and Elements to be included in the list
Choose particular isotopes and zircons to be excluded from this spreadsheet
'''
def addTESheet(files,sheet,includedElements,Chondrites,excludedZircons,excludedIsotopes):
    sheet.write('B1','Analysis')
    sheet.write('A1','Sample')
    full=[[""]*(3+len(includedElements))]
    full[0][0] = BeginningCell
    excludedZircons.append(BeginningCell)
    for i in range(len(includedElements)):
        sheet.write(0,2+i,rnums(includedElements[i]))
        full[0][2+i] = rnums(includedElements[i])
    r=1
    for f in files:
        rstart = r
        t = table(f)
        bi=begr(t,BeginningCell)
        xe=1
        e=[]
        try:
            while t[bi+xe][0]!=EndingCell:
                e.append(t[bi+xe][0])
                xe=xe+1
        except:
            EndWhileOnError = True
        for inc in includedElements:
            a=listfilter(e,inc)
            if len(a)>1:
                forbidden = []
                for j in range(len(a)):
                    if rnums(a[j])==inc and a[j] not in excludedIsotopes:
                        forbidden.append(a[j])
                if len(forbidden)>1:
                    print(inc,"has",len(forbidden),"possibilities:")
                    print(forbidden)
                    input("Please add "+str(len(forbidden)-1)+" of them to the excludedIsotopes list!")        
        i=0 #Column Index starting after 'Element'  
        si = [] #Sample Indicies matching from the input
        for row in t[bi]:
            inZirconList = (row not in excludedZircons) and (standard(row) not in excludedZircons)
            if inZirconList:
                full.append([""]*(3+len(includedElements)))
                sheet.write(r,1,row)
                sheet.write(r,0,standard(row))
                full[r][1] = row
                full[r][0] = standard(row)
                si.append(i)
                r=r+1
            i=i+1
        x=0
        c=0
        while t[bi+x][0]!=EndingCell:
            if rnums(t[bi+x][0]) in includedElements and t[bi+x][0] not in excludedIsotopes:
                c=c+1
                for y in range(len(si)):
                    data = record(t[bi+x][si[y]],Chondrites[c-1])
                    full[y+rstart][c+1] = data
                    sheet.write(y+rstart,c+1,data)
            x=x+1
    return full
def teSheetNamesIndicies(Chondtable):
    sn=[]
    indicies = []
    for i in range(len(Chondtable)):
        if Chondtable[i][0]!="":
            sn.append(Chondtable[i][0])
            indicies.append(i)
    return indicies

'''
Returns the Chondrite value of a specific element
'''
def chond(element,SheetName = 'TrElem'):
    t=table(ChondriteFile)
    r=0
    try:
        while t[r][0]!=SheetName:
            r=r+1
    except:
        return chond(element,input("Please enter the sheet name in Chondrite values.csv that we read Chondrites from:"))
    c=1
    try:
        while t[r][c]!=element:
            c=c+1
    except:
        return chond(element,input("No such element "+ element + " in sheet "+ SheetName + "\n Please give another sheet name: "))
    return record(t[r+1][c])

