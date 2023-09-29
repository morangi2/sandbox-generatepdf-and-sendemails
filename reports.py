#!/usr/bin/env python3

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
#above imports == Flowables == chunks of a doc that reportlab can arrange to make a complete report
from reportlab.lib.styles import getSampleStyleSheet
#above import == helps define the style we want
from reportlab.lib import colors
#above == to add more style to the pdf and make it more readable
from reportlab.graphics.shapes import Drawing
#above == to add graphics, piecharts, etc on the pdf being generated
from reportlab.graphics.charts.piecharts import Pie
#above== to be able to generate a pdf with a pie chat
from reportlab.lib.units import inch

fruit = {
  "elderberries": 1,
  "figs": 1,
  "apples": 2,
  "durians": 3,
  "bananas": 5,
  "cherries": 8,
  "grapes": 13
}

report = SimpleDocTemplate("python_andthe_os/capstone/report.pdf") #add the path and name you want the pdf file to be generated
styles = getSampleStyleSheet() #similar to HTML style settings

report_title = Paragraph("Title: A complete inventory of my fruits", styles["h1"])

#now build the pdf
#report.build([report_title]) #cgenerats a pdf with a title only

#now let's add data to our pdf
# we need 2D data == a list of lists
table_data = []

for k, v in fruit.items():
    table_data.append([k,v])

print(table_data) #OUTPUT: [['elderberries', 1], ['figs', 1], ['apples', 2], ['durians', 3], ['bananas', 5], ['cherries', 8], ['grapes', 13]]
report_table = Table(data = table_data)
report.build([report_title, report_table]) #generates a report with a title and the fruits data

# let's add some style to the pdf and make it more readable
# first import colors above
table_style = [("GRID", (0,0), (-1,-1), 1, colors.black)]
report_table = Table(data = table_data, style = table_style, hAlign = "LEFT")
report.build([report_title, report_table]) #generates a more readable pdf file!

# let's add a Pie chart to the pdf
# first import Drawing and Pie and inch
report_pie = Pie(width = 3*inch, height = 3*inch)

# now, add data t the pie chart
# create 2 lists, 1 for data, 1 for labels
report_pie.data = []
report_pie.labels = []

# append the lists in alphabetical order
for fruit_name in sorted(fruit):
    report_pie.data.append(fruit[fruit_name])
    report_pie.labels.append(fruit_name)

print()
print("Printing the labels and data for the Pie graph....")
print(report_pie.data) #OUTPUT: [2, 5, 8, 3, 1, 1, 13]
print(report_pie.labels) #OUTPUT: ['apples', 'bananas', 'cherries', 'durians', 'elderberries', 'figs', 'grapes']

report_chart = Drawing()
report_chart.add(report_pie) #adds data and labels to the chat

#now add the drawing to the report pdf
report.build([report_title, report_table, report_chart])


#for QWIKLABS
def generate(filename, title, aditional_info, table_data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h1"])
  report_info = Paragraph(additional_info, styles["BodyText"])
  table_style = [("GRID", (0,0), (-1,-1), 1, colors.black), 
                  ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
                  ("ALIGN", (0,0), (-1,-1), "CENTER")]
  report_table = Table(data=table_data, tyle=table_style, hAlign="LEFT")
  empty_line = Spacer(1,20)
  report.build([report_title, empty_line, report_info, empty_line, report_table])