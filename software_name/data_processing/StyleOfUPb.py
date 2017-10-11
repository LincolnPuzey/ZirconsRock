def styleUPb(FileLocation,StandardList):
    formatReport('Report')
    formatCommonPb('ToBeCommonLeadCorrected')
    styleStandards(StandardList)
def formatReport(sheetName):
    return "The formatted version of Sheet: Report"
def formatCommonPb(sheetName):
    return "The formatted version of Sheet: ToBeCommonLeadCorrected"

def styleStandards(StandardList):
    '''
        Style each of the Spreadsheets with different Standards
        An example of the StandardList = STDGJ, 91500, MT, INT1, INT2
        This example is shown on test_upb_output.xlsx
        You need to format the style of this sheet into the way that was provided by Irina on RequiredUPb.xlsx
    '''
    return 'Styled sheet whether it has concordia, inverse concordia sheets on it or not'

