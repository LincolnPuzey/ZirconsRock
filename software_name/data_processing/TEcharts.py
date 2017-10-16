from math import log10
from os import path

from PIL import Image, ImageDraw, ImageColor

from defaults import LINE_COLORS, LINE_MARKERS, \
    CLASS_COLORS, CLASS_MARKERS, CONVEX_HULL_IMAGE_FILE, CONVEX_HULL_IMAGE_DIR, \
    CHART_HEIGHT, CHART_WIDTH, PLOT_HEIGHT, PLOT_WIDTH, PLOT_X_OFFSET, PLOT_Y_OFFSET


def line_chart(sheet_data, sheet_name, workbook):
    """
    Does a line graph of the sheets TrElem and REE
    Each line (series) is a different sample
    Each point on the line is the concentration of a particular element in the sample

    sheet_name is the name of the worksheet containing the data to plotted on the chart
    sheet_data is a 2-dimensional list containing all the data on the worksheet sheet_name
    workbook the xlsxwriter representation of the excel workbook
    """
    # if we have data to graph
    if len(sheet_data) > 1:
        # add chartsheet and chart
        chartsheet = workbook.add_chartsheet("{} Chart".format(sheet_name))
        zircon_chart = workbook.add_chart({'type': 'line'})

        # add data and formatting to chart
        zircon_chart.set_title({'name': 'Trace Element Patterns of Zircons'})
        for i in range(1, len(sheet_data)):
            color = LINE_COLORS[i % len(LINE_COLORS)]
            zircon_chart.add_series({
                'categories': [sheet_name, 0, 2, 0, len(sheet_data[0])-2],
                'values': [sheet_name, i, 2, i, len(sheet_data[0])-2],
                'name': sheet_data[i][1],
                'line': {'width': 1.0, 'color': color},
                'marker': {
                    'type': LINE_MARKERS[i % len(LINE_MARKERS)],
                    'size': 4,
                    'border': {'color': color},
                    'fill': {'none': True}
                }
            })
        zircon_chart.set_x_axis({
            'name': '<--- Increasing Ionic Radius <---',
            'label_position': 'low'
        })
        zircon_chart.set_y_axis({
            'name': 'Zircon/Chrondrite',
            'log_base': 10
        })

        # set chart to chartsheet
        chartsheet.set_chart(zircon_chart)


def bar_chart(rock_type_list, sheet_name, workbook):
    """
    Presents a bar graph of each Classified rock type using Zircon Classification.
    See sheet RT INT in RequiredTE.xls file

    sheet_name is the name of the worksheet containing the data to plotted on the chart
    rock_type_list is the list of rock types to be displayed on the bar chart - one bar per rock type
    workbook the xlsxwriter representation of the excel workbook
    """
    # if we have data to graph
    if len(rock_type_list) > 0:
        # add chartsheet and chart
        chartsheet = workbook.add_chartsheet("{} Chart".format(sheet_name))
        rock_chart = workbook.add_chart({'type': 'column'})

        # add data and formatting to chart
        rock_chart.set_title({'name': 'Modelled Rock Types of Zircons'})
        rock_chart.add_series({
            'categories': [sheet_name, 2, 2, 1+len(rock_type_list), 2],
            'values': [sheet_name, 2, 4, 1+len(rock_type_list), 4]
        })
        rock_chart.set_legend({'none': True})
        rock_chart.set_y_axis({'name': 'Number of Grains'})

        # set chart to chartsheet
        chartsheet.set_chart(rock_chart)


def chart(classifiers, sheet_name, workbook):
    """
    The main funtion for chart Processing
    classifiers = 2D array of the contents of the worksheet containing the data to the plotted on the chart
    is indexed as classifiers[row][column], where row and row are zero-indexed
    sheet_name = the string of name of the worksheet containing the data
    workbook = The xlsxwriter standard of implementing the workbook
    """
<<<<<<< HEAD
    try:
        x_column, y_column, class_column = identify(classifiers)
        if x_column is not None and y_column is not None:
            draw_scatterplot(x_column, y_column, class_column, classifiers, sheet_name, workbook)
    except:
        skip = True
=======
    # Find which columns in classifiers hold data
    x_column, y_column, class_column = identify(classifiers)
    # If we found appropriate data
    if x_column is not None and y_column is not None:
        draw_scatterplot(x_column, y_column, class_column, classifiers, sheet_name, workbook)
>>>>>>> 923b94c75065f0ac5ffcaab6d983f1fea42b48a1


def identify(classifiers):
    """
    Identifies which columns from parameter classifiers are to be used as the x, y and series in the scatterplot

    The following are example columns from classifiers
    Scatterplot of Class
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    ['CART2', 'Carbonite (79%)', 'Carbonite (79%)', 'Syenite (93%)', 'Basalt (94%)', 'Carbonite (79%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Dolerite (71%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Syenite (93%)', 'Carbonite (79%)', 'Basalt (94%)', 'Syenite (93%)', 'Carbonite (79%)', 'Basalt (94%)', 'Syenite (93%)', 'Carbonite (79%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Dolerite (71%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Carbonite (79%)', 'Syenite (93%)', 'Carbonite (79%)', 'Syenite (93%)', 'Basalt (94%)', 'Syenite (93%)', 'Larvikite (72%)', 'Syenite (93%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Carbonite (79%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Carbonite (79%)', 'Carbonite (79%)', 'Carbonite (79%)', 'Carbonite (79%)', 'Basalt (94%)', 'Syenite (93%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Larvikite (72%)', 'Syenite (93%)', 'Syenite (93%)', 'Basalt (94%)', 'Syenite (93%)', 'Larvikite (72%)', 'Carbonite (79%)', 'Carbonite (79%)']
    ['Analysis', 'STDGJ-01', 'STDGJ-02', '91500-01', '610-01', 'MT-01', 'INT1-01', 'INT1-02', 'INT1-03', 'INT1-04', 'INT1-07', 'INT1-08', 'INT1-09', 'INT1-10', 'INT1-11', 'INT1-12', 'STDGJ-03', 'STDGJ-04', '610-02', 'STDGJ-03', 'STDGJ-04', '610-02', '91500-02', 'MT-02', 'INT1-13', 'INT1-14C', 'INT1-14R', 'INT1-15', 'INT1-16', 'INT1-17', 'INT1-18C', 'INT1-18R', 'INT1-19', 'INT1-20', 'INT1-21C', 'INT1-21RI', 'INT1-22C', 'INT1-22R', 'STDGJ-05', 'STDGJ-06', 'STDGJ-05', 'STDGJ-06', '610-03', '91500-03', 'INT1-23', 'INT1-23R', 'INT1-24C', 'INT1-24R', 'INT1-25C', 'INT1-25R', 'INT1-26', 'INT1-27', 'INT1-28', 'INT1-29', 'INT1-30', 'INT1-31', 'INT1-32', 'INT1-33', 'INT1-34', 'STDGJ-07', 'STDGJ-08', 'STDGJ-07', 'STDGJ-08', '610-04', '91500-04', 'INT1-35', 'INT2-01', 'INT2-02', 'INT2-03', 'INT2-04', 'INT2-05', 'INT2-06', 'INT2-07', 'INT2-08', 'INT2-09C', 'INT2-09R', 'INT2-10', 'INT2-11', 'INT2-12', 'INT2-13', 'INT2-14', 'STDGJ-09', 'STDGJ-10']
    Class chart
    Scatterplot of Y-U data
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['U', 289.05, 287.12, 78.67, 487.0, 191.83, 133.66, 47092.73, 148.56, 140.78, 1126.86, 509.08, 149.53, 135.06, 471.74, 1018.04, 287.87, 285.65, 487.0, 287.87, 285.65, 487.0, 83.07, 105.11, 158.56, 626.86, 348.78, 64.9, 146.95, 2220.34, 131.64, 191.0, 261.27, 525.36, 180.97, 334.47, 167.19, 832.58, 288.35, 289.24, 288.35, 289.24, 487.0, 79.64, 702.58, 134.14, 583.52, 545.11, 417.29, 102.82, 183.76, 178.79, 105.99, 251.21, 130.38, 248.05, 25309.41, 149.2, 484.94, 289.72, 291.88, 289.72, 291.88, 487.0, 79.65, 165.91, 155.27, 47.91, 385.77, 75.99, 423.32, 547.25, 487.68, 325.7, 182.41, 250.91, 114.66, 147.5, 121.19, 106.61, 100.54, 294.29, 289.17]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-U data chart
    Scatterplot of Y-Th data
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['Th', 18.47, 18.3, 28.52, 481.0, 170.89, 59.09, 319817.28, 102.36, 84.72, 230.6, 42.75, 88.41, 134.96, 267.62, 610.53, 18.32, 18.05, 481.0, 18.32, 18.05, 481.0, 29.55, 91.59, 81.37, 587.04, 179.74, 53.3, 67.68, 18425.47, 73.32, 52.0, 202.08, 191.07, 184.91, 244.12, 54.23, 259.47, 18.29, 18.03, 18.29, 18.03, 481.0, 29.01, 53.77, 146.89, 415.89, 288.96, 116.34, 65.68, 168.84, 161.88, 78.76, 277.5, 68.14, 119.38, 175891.02, 56.58, 178.7, 18.2, 18.58, 18.2, 18.58, 481.0, 28.51, 97.4, 81.34, 93.5, 104.11, 88.68, 285.06, 235.54, 376.4, 292.48, 236.94, 322.68, 109.06, 116.55, 48.16, 47.78, 55.44, 18.77, 18.49]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-Th data chart
    Scatterplot of Y-YbSm data
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['Yb/Sm', 36.60011092623405, 36.58712541620422, 180.02890173410407, 1.0345572354211663, 30.65635738831615, 62.72795969773299, 0.5754306346600166, 34.61029411764706, 18.808880308880312, 106.51201201201201, 169.08510638297872, 49.84007585335019, 50.32842287694974, 110.87856071964018, 155.13384321223708, 34.39153439153439, 37.016222479721904, 1.0345572354211663, 34.39153439153439, 37.016222479721904, 1.0345572354211663, 146.9230769230769, 37.39196360879454, 37.85920925747349, 61.00061387354206, 176.6764705882353, 73.5863453815261, 90.752, 0.2817658959723605, 48.78787878787879, 73.9871382636656, 69.21308411214955, 122.41573033707866, 23.684258416742495, 23.135761589403973, 64.71487603305786, 14.604536489151874, 35.31147540983606, 33.52331606217617, 35.31147540983606, 33.52331606217617, 1.0345572354211663, 160.48223350253807, 16.063094641962945, 22.64047619047619, 7.2581201945708465, 11.122857142857143, 23.12909836065574, 30.90625, 131.70161290322582, 35.59656084656085, 51.92307692307693, 84.33333333333333, 69.03592814371258, 47.20537428023032, 0.3734584482535895, 59.723557692307686, 63.135135135135144, 39.27272727272727, 34.27319587628866, 39.27272727272727, 34.27319587628866, 1.0345572354211663, 170.13623978201633, 62.3795761078998, 14.715254237288136, 8.882510410469958, 18.543296089385475, 21.706349206349206, 74.18361581920904, 33.37798546209761, 18.301079913606912, 48.18181818181818, 59.56549520766773, 16.355011933174225, 19.436493738819323, 27.471962616822427, 59.31011608623548, 53.97368421052632, 55.44904458598727, 41.43211407315561, 39.203592814371255]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-YbSm data chart
    Scatterplot of Y-NbTa data
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['Nb/Ta', 4.225742574257426, 3.8704061895551254, 2.552132701421801, 1.043620057072972, 1.1698546289211935, 2.9821073558648115, 17.106951583346373, 40.323955669224205, 4.543429844097995, 2.256427604871448, 1.9550858652575958, 3.329928498467824, 2.684331797235023, 8.916666666666666, 6.326647564469913, 4.0371134020618555, 3.713163064833006, 1.043620057072972, 4.0371134020618555, 3.713163064833006, 1.043620057072972, 2.3741007194244603, 1.168021680216802, 6.179001721170396, 24.123853211009173, 11.31578947368421, 3.201856148491879, 2.8358208955223883, 12.53271077600618, 2.8479381443298966, 2.519120458891013, 5.122235157159488, 2.91220556745182, 13.95375070501974, 6.513317191283293, 6.923076923076923, 8.741573033707864, 3.4, 4.099787685774947, 3.4, 4.099787685774947, 1.043620057072972, 2.3990267639902676, 7.284086732818817, 4.634693877551021, 30.08252427184466, 24.576271186440678, 5.69593147751606, 4.213483146067416, 5.216535433070866, 14.589892294946146, 15.18987341772152, 3.685782556750299, 3.028571428571429, 6.53944020356234, 12.953453240790575, 7.1980676328502415, 3.478810879190386, 3.729007633587786, 3.79491833030853, 3.729007633587786, 3.79491833030853, 1.043620057072972, 2.5131894484412474, 6.238053866203301, 3.027065527065527, 15.0926243567753, 3.056379821958457, 3.851044504995459, 3.162970106075217, 4.4338235294117645, 14.51603498542274, 9.315960912052118, 4.102893890675241, 20.647302904564313, 16.14864864864865, 3.6182572614107884, 3.17910447761194, 3.4525547445255476, 3.5815508021390374, 3.6097087378640778, 3.9485148514851485]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-NbTa data chart
    Scatterplot of Y-ThU data
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['Th/U', 0.06389897941532606, 0.06373641682920034, 0.36252701156730643, 0.9876796714579056, 0.8908408486680914, 0.44209187490647917, 6.791224038190184, 0.6890145395799677, 0.6017900269924705, 0.20463944056936978, 0.08397501375029465, 0.5912525914532201, 0.9992595883311122, 0.5673040234027218, 0.5997112097756473, 0.06363983742661618, 0.06318921757395415, 0.9876796714579056, 0.06363983742661618, 0.06318921757395415, 0.9876796714579056, 0.35572408811845435, 0.8713728474931025, 0.5131811301715439, 0.9364770443161151, 0.5153391822925627, 0.8212634822804313, 0.4605648179652944, 8.298490321302143, 0.5569735642661805, 0.27225130890052357, 0.7734527500287061, 0.3636934673366834, 1.021771564347682, 0.7298711394145961, 0.32436150487469345, 0.3116457277378751, 0.063429859545691, 0.06233577651777071, 0.063429859545691, 0.06233577651777071, 0.9876796714579056, 0.3642641888498242, 0.07653220985510546, 1.095049947815715, 0.7127262133260214, 0.5300948432426482, 0.2787989168204366, 0.6387862283602413, 0.9188071397474968, 0.9054197662061637, 0.7430889706576093, 1.1046534771704948, 0.522626169657923, 0.4812739367063092, 6.949629406612007, 0.3792225201072386, 0.36849919577679713, 0.06281927378158221, 0.0636562971084007, 0.06281927378158221, 0.0636562971084007, 0.9876796714579056, 0.3579409918392969, 0.5870652763546501, 0.5238616603336124, 1.9515758714255897, 0.26987583275008425, 1.1669956573233322, 0.67339128791458, 0.4304065783462768, 0.7718175853018372, 0.898004298434142, 1.29894194397237, 1.2860388186999323, 0.9511599511599512, 0.7901694915254237, 0.39739252413565473, 0.4481755932839321, 0.5514223194748358, 0.06378062455401134, 0.06394162603312929]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-ThU data chart
    Scatterplot of Y-CeCe data
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['Ce/Ce', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-CeCe data chart
    Scatterplot of Y-EuEu data
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['Eu/Eu', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-EuEu data chart
    Scatterplot of Y-Hf-Y data
    ['Hf', 7801.4, 7801.4, 5596.66, 458.0, 18128.68, 16939.83, 35851.63, 17530.85, 13899.52, 21317.78, 25596.02, 16998.29, 14636.83, 19166.87, 18189.65, 7801.4, 7801.4, 458.0, 7801.4, 7801.4, 458.0, 5629.75, 10334.09, 9153.0, 10067.87, 11339.13, 10639.95, 10115.69, 18450.81, 8723.89, 9968.48, 9040.46, 9433.87, 9910.75, 11836.09, 12957.16, 13014.79, 7801.4, 7801.4, 7801.4, 7801.4, 458.0, 5609.4, 13332.59, 12963.75, 9753.09, 11233.7, 10495.55, 10352.1, 10531.53, 10586.33, 10106.05, 9063.26, 9785.06, 10872.27, 17940.29, 11638.14, 10516.96, 7832.05, 7820.54, 7832.05, 7820.54, 458.0, 5546.04, 10012.01, 10101.6, 10630.45, 12537.85, 9975.54, 8090.23, 12981.2, 10490.62, 10646.26, 8828.12, 10870.47, 8254.58, 10163.71, 7746.08, 10606.3, 9731.73, 7844.45, 7823.55]
    ['Y', 275.17, 273.51, 135.09, 490.0, 493.41, 957.73, 568349.31, 1068.42, 2183.8, 1999.21, 2933.12, 3133.56, 1964.3, 2160.93, 1951.75, 270.96, 270.56, 490.0, 270.96, 270.56, 490.0, 140.59, 277.28, 1493.34, 2313.36, 590.23, 674.88, 714.16, 360301.38, 1272.73, 809.1, 1149.48, 1296.41, 1064.57, 696.56, 369.66, 1052.49, 269.34, 269.2, 269.34, 269.2, 490.0, 136.13, 808.09, 434.93, 2055.66, 1079.02, 448.63, 268.67, 714.88, 805.32, 809.26, 1826.98, 799.51, 856.39, 387642.94, 774.38, 1032.48, 269.68, 270.18, 269.68, 270.18, 490.0, 136.05, 836.73, 953.87, 1529.04, 446.54, 817.44, 4271.52, 1076.28, 1748.43, 1538.97, 1209.34, 890.49, 479.76, 255.17, 1496.03, 291.55, 612.48, 273.06, 269.01]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Y-Hf-Y data chart
    Scatterplot of Nb-Ta data
    ['Nb', 2.134, 2.001, 1.077, 512.0, 15.29, 4.5, 612387.81, 94.6, 10.2, 33.35, 29.6, 3.26, 1.165, 10.7, 11.04, 1.958, 1.89, 512.0, 1.958, 1.89, 512.0, 0.99, 8.62, 3.59, 52.59, 3.44, 2.76, 4.94, 163061.22, 4.42, 5.27, 4.4, 4.08, 24.74, 13.45, 4.05, 38.9, 1.819, 1.931, 1.819, 1.931, 512.0, 0.986, 19.82, 2.271, 371.82, 116.0, 10.64, 3.0, 5.3, 17.61, 14.4, 6.17, 4.24, 25.7, 388694.66, 4.47, 5.5, 1.954, 2.091, 1.954, 2.091, 512.0, 1.048, 7.18, 4.25, 87.99, 3.09, 4.24, 3.28, 18.09, 49.79, 28.6, 2.552, 99.52, 4.78, 1.744, 4.26, 1.419, 2.679, 1.859, 1.994]
    ['Ta', 0.505, 0.517, 0.422, 490.6, 13.07, 1.509, 35797.6, 2.346, 2.245, 14.78, 15.14, 0.979, 0.434, 1.2, 1.745, 0.485, 0.509, 490.6, 0.485, 0.509, 490.6, 0.417, 7.38, 0.581, 2.18, 0.304, 0.862, 1.742, 13010.85, 1.552, 2.092, 0.859, 1.401, 1.773, 2.065, 0.585, 4.45, 0.535, 0.471, 0.535, 0.471, 490.6, 0.411, 2.721, 0.49, 12.36, 4.72, 1.868, 0.712, 1.016, 1.207, 0.948, 1.674, 1.4, 3.93, 30007.03, 0.621, 1.581, 0.524, 0.551, 0.524, 0.551, 490.6, 0.417, 1.151, 1.404, 5.83, 1.011, 1.101, 1.037, 4.08, 3.43, 3.07, 0.622, 4.82, 0.296, 0.482, 1.34, 0.411, 0.748, 0.515, 0.505]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    Nb-Ta data chart
    Scatterplot of U-Th data
    ['U', 289.05, 287.12, 78.67, 487.0, 191.83, 133.66, 47092.73, 148.56, 140.78, 1126.86, 509.08, 149.53, 135.06, 471.74, 1018.04, 287.87, 285.65, 487.0, 287.87, 285.65, 487.0, 83.07, 105.11, 158.56, 626.86, 348.78, 64.9, 146.95, 2220.34, 131.64, 191.0, 261.27, 525.36, 180.97, 334.47, 167.19, 832.58, 288.35, 289.24, 288.35, 289.24, 487.0, 79.64, 702.58, 134.14, 583.52, 545.11, 417.29, 102.82, 183.76, 178.79, 105.99, 251.21, 130.38, 248.05, 25309.41, 149.2, 484.94, 289.72, 291.88, 289.72, 291.88, 487.0, 79.65, 165.91, 155.27, 47.91, 385.77, 75.99, 423.32, 547.25, 487.68, 325.7, 182.41, 250.91, 114.66, 147.5, 121.19, 106.61, 100.54, 294.29, 289.17]
    ['Th', 18.47, 18.3, 28.52, 481.0, 170.89, 59.09, 319817.28, 102.36, 84.72, 230.6, 42.75, 88.41, 134.96, 267.62, 610.53, 18.32, 18.05, 481.0, 18.32, 18.05, 481.0, 29.55, 91.59, 81.37, 587.04, 179.74, 53.3, 67.68, 18425.47, 73.32, 52.0, 202.08, 191.07, 184.91, 244.12, 54.23, 259.47, 18.29, 18.03, 18.29, 18.03, 481.0, 29.01, 53.77, 146.89, 415.89, 288.96, 116.34, 65.68, 168.84, 161.88, 78.76, 277.5, 68.14, 119.38, 175891.02, 56.58, 178.7, 18.2, 18.58, 18.2, 18.58, 481.0, 28.51, 97.4, 81.34, 93.5, 104.11, 88.68, 285.06, 235.54, 376.4, 292.48, 236.94, 322.68, 109.06, 116.55, 48.16, 47.78, 55.44, 18.77, 18.49]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    U-Th data chart
    Scatterplot of CeCe-EuEu data
    ['Ce/Ce', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ['Eu/Eu', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ['CART1', 'Carbonite', 'Carbonite', 'Syenite', 'Basalt', 'Carbonite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Granitoid (70-75% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Carbonite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Ne-syenite&Syenite Pegmatites', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Ne-syenite&Syenite Pegmatites', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Carbonite', 'Carbonite', 'Basalt', 'Syenite', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Dolerite', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Granitoid (>65% SiO2)', 'Dolerite', 'Granitoid (>65% SiO2)', 'Carbonite', 'Carbonite', 'Basalt', 'Carbonite', 'Dolerite', 'Carbonite', 'Carbonite']
    CeCe-EuEu data chart
    """

    # work out which columns of classifiers hold the data and class names
    width = len(classifiers[0])
    x_column = width-2
    y_column = width-1
    class_column = width-3
    # check columns contain numbers
    if isinstance(classifiers[1][x_column], float) and isinstance(classifiers[1][y_column], float):
        return x_column, y_column, class_column
    else:
        return None, None, None


def draw_scatterplot(x_column, y_column, class_column, classifiers, sheet_name, workbook):
    """
    Creates a worksheet in a workbook that plots the data with a colour of their classified type.
    Calculates the points that make a convex hull around each series, then generates an image to
    overlay over the chart to illustrate the convex hulls.
    sheet_name cannot contain any of the characters ' [ ] : * ? / \ ' and it must be less than 20 characters.
    x_column, y_column and class_column are indexes of columns in classifiers to use as x-values, y-values and
    series names, respectively.
    """

    # build the list of series to add to chart, each series specifies a range of data
    series_list = []
    current_series_name = classifiers[1][class_column]
    current_series_start, current_series_end = 1, 1
    series_data = {
        current_series_name: []
    }

    x_axis_min = 1
    x_axis_max = 10
    y_axis_min = 1
    y_axis_max = 10

    for i in range(1, len(classifiers)):

        # keep track of x/y min/max
        x_axis_min = x_axis_min/10 if classifiers[i][x_column] < x_axis_min else x_axis_min
        x_axis_max = x_axis_max*10 if classifiers[i][x_column] > x_axis_max else x_axis_max
        y_axis_min = y_axis_min/10 if classifiers[i][y_column] < y_axis_min else y_axis_min
        y_axis_max = y_axis_max*10 if classifiers[i][y_column] > y_axis_max else y_axis_max

        if current_series_name == classifiers[i][class_column]:
            # still in same series - update end index
            current_series_end = i
            # add values

        else:
            # encountered new series - add previous one to list
            series_list.append({
                'categories': [sheet_name, current_series_start, x_column, current_series_end, x_column],
                'values': [sheet_name, current_series_start, y_column, current_series_end, y_column],
                'name': current_series_name,
                'marker': CLASS_MARKERS.get(
                    current_series_name,
                    {
                        # default marker
                        'type': 'square',
                        'size': 7,
                        'border': {'color': '#808080'},
                        'fill': {'color': '#808080'}
                    }
                )
            })
            # new series
            current_series_start = i
            current_series_end = i
            current_series_name = classifiers[i][class_column]
            series_data[current_series_name] = []

        series_data[current_series_name].append((classifiers[i][x_column], classifiers[i][y_column]))

    # add last series:
    series_list.append({
        'categories': [sheet_name, current_series_start, x_column, current_series_end, x_column],
        'values': [sheet_name, current_series_start, y_column, current_series_end, y_column],
        'name': current_series_name,
        'marker': CLASS_MARKERS.get(
            current_series_name,
            {
                # default marker
                'type': 'square',
                'size': 7,
                'border': {'color': '#808080'},
                'fill': {'color': '#808080'}
            }
        )
    })
    #

    # create a chartsheet in the workbook for the plot
    # a chartsheet is a worksheet that only contains a chart.
    scatterplot_worksheet = workbook.add_worksheet("{} Plot".format(sheet_name))

    # the scatter plot
    scatterplot = workbook.add_chart({'type': 'scatter'})
    scatterplot.set_title({'name': "{} vs {} in Zircon".format(classifiers[0][y_column], classifiers[0][x_column])})
    # default size is 480 x 288 pixels
    # we want 2x default size
    scatterplot.set_size({'width': CHART_WIDTH, 'height': CHART_HEIGHT})
    scatterplot.set_chartarea({'border': {'none': True}})
    scatterplot.set_plotarea({
        'layout': {
            'x': PLOT_X_OFFSET,
            'y': PLOT_Y_OFFSET,
            'width': PLOT_WIDTH,
            'height': PLOT_HEIGHT
        }
    })
    scatterplot.set_x_axis({
        'name': [sheet_name, 0, x_column],
        'max': x_axis_max,
        'min': x_axis_min,
        'log_base': 10,
        'major_gridlines': {'visible': True},
        'major_tick_mark': 'outside',
        'minor_tick_mark': 'inside'
    })
    scatterplot.set_y_axis({
        'name': [sheet_name, 0, y_column],
        'max': y_axis_max,
        'min': y_axis_min,
        'log_base': 10,
        'major_gridlines': {'visible': True},
        'major_tick_mark': 'outside',
        'minor_tick_mark': 'inside'
    })

    for series in series_list:
        scatterplot.add_series(series)

    scatterplot_worksheet.insert_chart('A1', scatterplot)

    # generate and add convex hull image
    image = generate_convex_hull_image(sheet_name, series_data, x_axis_max, x_axis_min, y_axis_max, y_axis_min)
    scatterplot_worksheet.insert_image(
        'A1',
        image,
        {
            'x_offset': int(PLOT_X_OFFSET*CHART_WIDTH),
            'y_offset': int(PLOT_Y_OFFSET*CHART_HEIGHT)
        }
    )


def generate_convex_hull_image(sheet_name, series_data, x_axis_max, x_axis_min, y_axis_max, y_axis_min):
    """
    Generates a image to use as background in the chart containing the convex hulls
    Saves image at location specified in defaults.CONVEX_HULL_IMAGE_FILE

    Alex talking about Convex charts:
    how to do convex hull to get a region for a set of points:
    tldr version is
    take the bottommost point, leftmost if there's a tie.
    sort all other points by angle with that point and x-axis (use cross product or something).
    add each point, such that each point added means a line segment between the point and the previous point,
    if this results in the line segment causing the current shape to be non-convex,
    remove the previous point and try adding this point again.
    once through all points, add line segment between final point and your original point.
    that's a tldr of convex hull
    """

    image = Image.new('RGBA', (int(CHART_WIDTH * PLOT_WIDTH), int(CHART_HEIGHT * PLOT_HEIGHT)), '#FFFFFF00')
    draw = ImageDraw.Draw(image)

    for class_name, points in series_data.items():
        edge_points = convex_hull(transform_points(points, x_axis_max, x_axis_min, y_axis_max, y_axis_min))
        if edge_points is not None:

            color = ImageColor.getrgb(CLASS_COLORS.get(class_name, '#00000000'))+(255,)

            draw.line(edge_points, fill=color, width=2)

    image_file_path = path.join(CONVEX_HULL_IMAGE_DIR, CONVEX_HULL_IMAGE_FILE.format(sheet_name))
    image.save(image_file_path)
    return image_file_path


def convex_hull(points):
    """
    Based on Code from:
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain#Python
    Used here under terms of the Creative Commons Attribution-ShareAlike License:
    https://creativecommons.org/licenses/by-sa/3.0/

    Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates with set().
    points = sorted(set(points))

    # Boring case: 0-2 unique points
    if len(points) < 3:
        return None

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of lower is omitted because it is repeated at the beginning of upper list.
    return lower[:-1] + upper


def transform_points(points, x_axis_max, x_axis_min, y_axis_max, y_axis_min):
    """
    takes a list of points in form [(x,y), (x,y), ...]
    and transforms the from raw x and y data values to x and y coordinate values suitable for drawing on the image
    """
    x_axis_max_log = log10(x_axis_max)
    x_axis_min_log = log10(x_axis_min)
    y_axis_max_log = log10(y_axis_max)
    y_axis_min_log = log10(y_axis_min)
    x_axis_range = x_axis_max_log-x_axis_min_log
    y_axis_range = y_axis_max_log-y_axis_min_log

    points_transformed = []

    for point in points:
        points_transformed.append(
            (
                int((log10(point[0]) - x_axis_min_log) / x_axis_range * PLOT_WIDTH * CHART_WIDTH),
                int((y_axis_max_log - log10(point[1])) / y_axis_range * PLOT_HEIGHT * CHART_HEIGHT)
            )
        )

    return points_transformed
