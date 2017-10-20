from .common import *
from .TEcharts import *
from .StyleOfTE import *
from defaults import BeginningCell, EndingCell, SheetName, allChondriteElements, ChondriteValues, UnrecognisedInputFileError


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
    t=get_table(file)
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
            bar_chart(rocktype,s,workbook)
    elements = full[0][2:]
    z = standard(column(full, 1)[1:])
    avg = workbook.add_worksheet("Statistics of "+full[0][1])
    avg.write(0, 0, "Sample")
    avg.write(0, 1, "Number of Analyses")
    avg.write(0, 2, "Stat. Parameter")
    for i in range(len(elements)):
        avg.write(0, i+3, elements[i])

    rows_per_sample = 4
    for i in range(len(z)):
        avg.write(1 + (i * rows_per_sample), 0, z[i])
        avg.write(1 + (i * rows_per_sample), 1, len(values(full, 0, z[i])))
        avg.write(1 + (i * rows_per_sample) + 0, 2, "Mean")
        avg.write(1 + (i * rows_per_sample) + 1, 2, "St. Dev. - Population")
        avg.write(1 + (i * rows_per_sample) + 2, 2, "Median")

        for j in range(len(elements)):

            vals = sorted(values(full, j + 2, z[i]))
            if len(vals) > 0:

                total = sum(vals)
                count = len(vals)
                mean = total / count

                middle = count / 2
                if middle % 1 == 0.0:
                    median = (vals[round(middle) - 1] + vals[round(middle)]) / 2
                else:
                    median = vals[round(middle - 0.5)]

                variance = 0
                for v in vals:
                    variance = variance + pow(v - mean, 2)
                variance = variance / count
                stddev = pow(variance, 0.5)

                avg.write(1 + (i * rows_per_sample) + 0, j + 3, mean)
                avg.write(1 + (i * rows_per_sample) + 1, j + 3, stddev)
                avg.write(1 + (i * rows_per_sample) + 2, j + 3, median)


def values(t, c, c0):
    v = []
    for r in t:
        if r[0] == c0:
            v.append(record(r[c]))
    return v


def getChondrite(available,file, unknown, stand, detected,PerformByRockType,PassParameterOnly):
    print(stand)
    print(len(stand))
    if type(unknown)!=type(["list"]) or len(stand)==0:
        return get_table(file)
    chond = get_table(file)
    i=0
    if len(unknown)>0:
        control = copy.deepcopy(unknown)
        control.extend(copy.deepcopy(stand))
    else:
        control = detected
    while i<len(chond) and len(chond[i])>=2:
        if chond[i][1]=="Excluded Zircons or Standards":
            known = []
            for d in detected:
                if d not in control:
                    known.append(d)
            text = ',Excluded Zircons or Standards,' + commas(known)
            writeln(i,text,file)
            if len(unknown)>0:
                control = unknown
            else:
                control = stand
        if chond[i][0]!="":
            includedElements = chond[i][1:]
            for e in range(len(includedElements)):
                for a in range(len(available)):
                    if rnums(includedElements[e])==rnums(available[a]):
                        includedElements[e] = available[a]
            text = chond[i][0]+","+commas(includedElements)
            writeln(i,text,file)
        if not PassParameterOnly:
            if chond[i][1]=="CARTS":
                if PerformByRockType and "CART" not in chond[i][3]:
                    first = commas(chond[i][:3])
                    second = commas(chond[i][3:])
                    writeln(i,first+",CART1,"+second,file)
                if not PerformByRockType and "CART" in chond[i][3]:
                    first = commas(chond[i][:3])
                    second = commas(chond[i][4:])
                    writeln(i,first+","+second,file)
                
        i=i+1
    return get_table(file)



def commas(lis):
    return str(lis).replace("[","").replace("]","").replace("\'","").replace(" ","").replace("\t","")


def te(files, output, ChondFile, control, unknown, ScatterPlotCarts,PassParameterOnly=True):
    """
    Main function that will call everything as needed
    """
    # You have to specify the name of the csv file and input the range of numbers within that name:
    # This program uses chondrite_values.csv file:
    #      Column A lists the names of the sheets you will use in the Output xl file
    #      Every other column beside it will have 4 rows
    #      Row 1: You may add or remove as many elements you like
    #      Row 2: Enter the Chondrite values for each element
    #      Row 3: Include a list of zircons or standards that you wish to exclude
    #      Row >3: indicats the CART classification that you wish to be done for this given data
    #          Column B here Always states CARTS followed by the name of the new Spreadsheet
    PerformByRockType = not ScatterPlotCarts
    print(control)
    print(unknown)
    workbook = xlsxwriter.Workbook(output)
    t = getChondrite(getElements(files[0]),ChondFile,unknown,control,standard(getAllZircons(files)),PerformByRockType,PassParameterOnly)
    NotDoneClassifiers = True
    for i in teSheetNamesIndicies(t):
        full=addTESheet(files,workbook.add_worksheet(t[i][0]),nospaces(t[i][1:]),nospaces(t[i+1][1:]),nospaces(t[i+2][2:]))
        full[0][1] = t[i][0]
        line_chart(full,t[i][0],workbook)
        k=3
        while i+k<len(t) and len(t[i+k])>1 and t[i+k][1]=="CARTS":
            carts = nospaces(t[i+k][3:])
            if len(carts)>0:
                worksheet = workbook.add_worksheet(t[i+k][2])
                Classifiers = addClassifier(full,worksheet,carts, PerformByRockType)
                try:
                    scatterplot(Classifiers, t[i+k][2], workbook, PerformByRockType)
                except:
                    print(t[i+k][2],"cannot produce a chart")
                if NotDoneClassifiers:
                    summary(full,Classifiers,workbook)
                NotDoneClassifiers=False
            k=k+1

    try:
        workbook.close()
        styleTE(output)
        return True
    except Exception as e:
        print(e)
        print("ERROR: Could not create output file - maybe file is open in another program?")
        return False
    


def addClassifier(full, sheet, carts, perform_by_rock_type):
    """
    Adds a sheet based upon the outline of a Classification sheet
    full = 2D array of the table
    sheet = the actual sheet we use in the spreadsheet
    carts = the list of examples to classify
    """

    # build 'classifier'
    classifier = [["Sample", "Analysis"]]
    for c in range(len(carts)):
        classifier[0].append(carts[c])
    for r in range(1, len(full)):
        z = full[r][1]
        classifier.append([full[r][0], z])
        for c in range(len(carts)):
            content = classify(carts[c], full, z)
            classifier[r].append(content)

    # sort 'classifier' except for first row. column to sort on depends on how we want to graph data
    if perform_by_rock_type:
        classifier = [classifier[0]] + sorted(classifier[1:], key=lambda row: row[-3])
    else:
        classifier = [classifier[0]] + sorted(classifier[1:], key=lambda row: row[0])
    # write to excel
    for r in range(len(classifier)):
        for c in range(len(classifier[r])):
            value_to_write = evalif(classifier[r][c])
            if classifier[0][c] == 'Hf' and r > 0:
                # special case - divide by 10,000 to give output as % weight rather than ppm
                try:
                    sheet.write(r, c, value_to_write/10000)
                except TypeError:
                    # if something goes wrong write regular value
                    sheet.write(r, c, value_to_write)
            else:
                # regular case
                sheet.write(r, c, value_to_write)

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
        t = get_table(f)
        bi = begr(t, BeginningCell)
        if bi == len(t):
            raise UnrecognisedInputFileError("Could not read TE data from file")
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
    available = getElements(files[0])
    i=2
    for e in includedElements:
        if e in available:
            sheet.write(0,i,rnums(e))
            full[0][i] = rnums(e)
            i=i+1
    r=1
    for f in files:
        rstart = r
        t = get_table(f)
        ss = f.split('TE')[-1]
        bi=begr(t,BeginningCell)
        i=0 #Column Index starting after 'Element'
        si = [] #Sample Indicies matching from the input
        for row in t[bi]:

            inZirconList = (row not in excludedZircons) and (standard(row) not in excludedZircons)
            '''
            addSheet(ts,[[inZirconList]],1,i)
            addSheet(ts,[['Included Elements'],includedElements],2)
            addSheet(ts,[['Excluded Zircons'],excludedZircons],4)
            '''
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
