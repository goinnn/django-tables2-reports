 # Copyright (c) 2010 by Yaco Sistemas <pmartin@yaco.es>
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU Lesser General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public License
 # along with this programe.  If not, see <http://www.gnu.org/licenses/>.

# Based on http://sujitpal.blogspot.com/2007/02/python-script-to-convert-csv-files-to.html
# Get to https://github.com/Yaco-Sistemas/django-autoreports/blob/master/autoreports/csv_to_excel.py

import csv

try:
    import pyExcelerator
except ImportError:
    HAS_PYEXCELERATOR = False
else:
    HAS_PYEXCELERATOR = True


def openExcelSheet():
    """ Opens a reference to an Excel WorkBook and Worksheet objects """
    workbook = pyExcelerator.Workbook()
    worksheet = workbook.add_sheet("Sheet 1")
    return workbook, worksheet


def validateOpts(response):
    """ Returns option values specified, or the default if none """
    titlePresent = False
    linesPerFile = -1
    sepChar = ","
    return titlePresent, linesPerFile, sepChar


def writeExcelHeader(worksheet, titleCols):
    """ Write the header line into the worksheet """
    cno = 0
    for titleCol in titleCols:
        worksheet.write(0, cno, titleCol)
        cno = cno + 1


def writeExcelRow(worksheet, lno, columns):
    """ Write a non-header row into the worksheet """
    cno = 0
    for column in columns:
        worksheet.write(lno, cno, column.decode('utf-8'))
        cno = cno + 1


def closeExcelSheet(response, workbook):
    """ Saves the in-memory WorkBook object into the specified file """
    response.content = workbook.get_biff_data()


def convert_to_excel(response):
    titlePresent, linesPerFile, sepChar = validateOpts(response)
    workbook, worksheet = openExcelSheet()
    fno = 0
    lno = 0
    titleCols = []
    content = response.content.split('\n')
    reader = csv.reader(content)
    for line in reader:
        if (lno == 0 and titlePresent):
            if (len(titleCols) == 0):
                titleCols = line
            writeExcelHeader(worksheet, titleCols)
        else:
            writeExcelRow(worksheet, lno, line)
        lno = lno + 1
        if (linesPerFile != -1 and lno >= linesPerFile):
            fno = fno + 1
            lno = 0
    closeExcelSheet(response, workbook)
