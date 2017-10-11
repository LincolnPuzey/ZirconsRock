from .common import *
from .TEcharts import *
from .StyleOfTE import *
from defaults import BeginningCell, EndingCell, SheetName, allChondriteElements, ChondriteValues


def classify(cart, t, z="zircon eg. STDGJ-01"):
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


def data(t, zircon, element):
    """
    Provided the 2D array t with zircons against elements what number would I get from zircon on element?
    zircon eg = 'STDGJ-01'
    element eg = 'Ce'
    """
    e=[False,element]
    if "/" in element:
        e=element.split("/")
        if e[0]!=e[1]:
            return record(data(t,zircon,e[0]),data(t,zircon,e[1]))
    r=0
    c=0
    try:
        while t[r][1]!=zircon:
            r=r+1
        while e[1]!=t[0][c]:
            c=c+1
        Ce = t[r][c]
        La = record(t[r][c-1])
        Pr = record(t[r][c+1])
        if e[0]:
            return record(Ce,(La+Pr)/2)
        return record(Ce)
    except Exception as e:
        print(e)
        print("For the",t[0][1],"spreadsheet:")
        print("Cannot find value for Element:",element,"for zircon",zircon,"?")
        return eval(input("Please enter the value here: "))


def getElements(file):
    """
    Returns all Trace Elements given a specific file
    """
    t=table(file)
    r=begr(t,BeginningCell)
    e=begr(t[r:],EndingCell)
    return column(t[r+1:r+e],0)


def summary(full, Classifiers, workbook):
    """
    Creates the Summary spreadsheets
    """
    i=-1
    zircons = column(Classifiers,1)
    for s in Classifiers[0]:
        i=i+1
        if "CART" in s:
            sheet=workbook.add_worksheet(s)
            sheet.write(0,0,"Zircon Classification: "+s)
            sheet.write(1,0,"Sample")
            sheet.write(1,1,"Total Analysis")
            stn = standard(zircons)
            for r in range(len(stn)):
                sheet.write(r+2,0,stn[r])
                total = 0
                for z in zircons:
                    if stn[r] in z:
                        total=total+1
                sheet.write(r+2,1,total)
            sheet.write(1,2,"Rock type")
            sheet.write(1,3,"Percentage")
            sheet.write(1,4,"Number of Analysis")
            rocks = column(Classifiers,i)
            rocktype = standard(rocks[2:],"Gives a distinct list of rock types")
            for row in range(len(rocktype)):
                sheet.write(row+2,2,rocktype[row])
                n=0
                for rock in range(len(rocks)):
                    if rocks[rock]==rocktype[row]:
                        n=n+1
                sheet.write(row+2,4,n)
            for p in range(len(rocktype)):
                r = p+2
                sheet.write(r,3,"=(E"+str(r+1)+"/SUM($E$3:$E$"+str(len(rocktype)+2)+"))*100")   
    elements = full[0][3:]
    z = standard(column(full,1)[1:])
    zirconClassification(sheet,workbook)
    avg = workbook.add_worksheet("Summary of "+full[0][1])
    avg.write(1,0,"Sample")
    for e in range(len(elements)):
        r=1
        n=5
        el = elements[e]
        avg.write(r,n*e+1,"sum "+el)
        avg.write(r,n*e+2,"count "+el)
        avg.write(r,n*e+3,"mean "+el)
        avg.write(r,n*e+4,"stdev "+el)
        avg.write(r,n*e+5,"median "+el)
        for r in range(2,len(z)+2):
            vals = values(full,e+2,z[r-2])
            avg.write(r,0,z[r-2])
            total = sum(vals)
            count = len(vals)
            i = count/2
            if type(i)==type(3):
                median = (vals[i]+vals[i+1])/2
            if type(i)==type(3.4):
                median = vals[round(i)-1]
            mean = total/count
            stdev = 0
            for v in vals:
                stdev=stdev+(mean-v)/count
            avg.write(r,n*e+1,total)
            avg.write(r,n*e+2,count)
            avg.write(r,n*e+3,mean)
            avg.write(r,n*e+4,stdev)
            avg.write(r,n*e+5,median)
    styleSummary(avg,workbook)


def values(t, c, c0):
    v = []
    for r in t:
        if r[0] == c0:
            v.append(r[c])
    return v


def getChondrite(file, unknown, detected):
    if type(unknown)!=type(["list"]):
        return table(file)
    chond = readln(file)
    if chond[2].split(',')[1]=="Excluded Zircons or Standards":
        known = []
        for d in detected:
            if d not in unknown:
                known.append(d)
        un = str(known).replace("[","").replace("]","").replace("\'","")
        text = ',Excluded Zircons or Standards,' + un
        writeln(2,text,file)
    return table(file)


def te(files, output, ChondFile):
    """
    Main function that will call everything as needed
    """
    # Parameters to add
    control = ['STDGJ','MT','91500']
    unknown = ['INT1','INT2']

    print("This particular python file will read the data recorded by the Laser device for Trace Elements.")
    print("Please ensure you are using Python version 3.6.2 on your computer")
    print("This program was created and developed by Mark Collier September 2017 [Contact:+61466523090]")
    print("You have to specify the name of the csv file and input the range of numbers within that name:")
    print("This program uses chondrite_values.csv file:")
    print("     Column A lists the names of the sheets you will use in the Output xl file")
    print("     Every other column beside it will have 4 rows")
    print("     Row 1: You may add or remove as many elements you like")
    print("     Row 2: Enter the Chondrite values for each element")
    print("     Row 3: Include a list of zircons or standards that you wish to exclude")
    print("     Row >3: indicats the CART classification that you wish to be done for this given data")
    print("         Column B here Always states CARTS followed by the name of the new Spreadsheet")
    workbook = xlsxwriter.Workbook(output)
    t = getChondrite(ChondFile,unknown,standard(getAllZircons(files)))
    NotDoneClassifiers = True
    for i in teSheetNamesIndicies(t):
        full=addTESheet(files,workbook.add_worksheet(t[i][0]),nospaces(t[i][1:]),nospaces(t[i+1][1:]),nospaces(t[i+2][2:]))
        full[0][1] = t[i][0]
        k=3
        if True:
            while i+k<len(t) and len(t[i+k])>1 and t[i+k][1]=="CARTS":
                carts = nospaces(t[i+k][3:])
                if len(carts)>0:
                    worksheet = workbook.add_worksheet(t[i+k][2])
                    Classifiers = addClassifier(full,worksheet,carts)
                    chart(Classifiers,t[i+k][2],workbook)
                    if NotDoneClassifiers:
                        summary(full,Classifiers,workbook)
                    NotDoneClassifiers=False
                    #workbook = chart(Classifiers,worksheet,t[i+k][2],workbook)
                k=k+1
        '''
        except Exception as e:
            if True:
                print("Ignore list index out of range error. This error was:")
                print(e)
    '''
    try:
        workbook.close()
    except Exception as e:
        print(e)
        input("You must close "+output+" before continuing")
        workbook.close()


def addClassifier(full, sheet, carts):
    """
    Adds a sheet based upon the outline of a Classification sheet
    full = 2D array of the table
    sheet = the actual sheet we use in the spreadsheet
    carts = the list of examples to classify
    """
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


def test():
    """
    Testing some our functions
    """
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


def getAllZircons(files):
    """
    Returns all of the zircons listed in a Trace Element File List
    """
    zlist = []
    for f in files:
        t = table(f)
        bi=begr(t,BeginningCell)
        for row in t[bi]:
            if row != BeginningCell:
                zlist.append(row)
    return zlist


def addTESheet(files, sheet, includedElements, Chondrites, excludedZircons):
    """
    Add a spreadsheet of zircons against elements with it's included Chondrite values and Elements to be included in the list
    Choose particular isotopes and zircons to be excluded from this spreadsheet
    """
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
            if t[bi+x][0] in includedElements:
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


def chond(element):
    """
    Returns the Chondrite value of a specific element
    """
    i=0
    for e in allChondriteElements:
        if element in e:
            return ChondriteValues[i]
        i=i+1
