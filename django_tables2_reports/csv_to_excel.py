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
import cStringIO as StringIO
import collections

# Autodetect library to use for xls writing.  Default to xlwt.
EXCEL_SUPPORT = None
try:
    import xlwt
    EXCEL_SUPPORT = 'xlwt'
except ImportError:
    pass

if EXCEL_SUPPORT is None:
    try:
        import pyExcelerator
        EXCEL_SUPPORT = 'pyexcelerator'
    except ImportError:
            pass


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


def convert_to_excel_pyexcelerator(response):
    titlePresent, linesPerFile, sepChar = validateOpts(response)
    workbook, worksheet = openExcelSheet()
    fno = 0
    lno = 0
    titleCols = []
    content = StringIO.StringIO(response.content)
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


# A reasonable approximation for column width is based off zero character in
# default font.  Without knowing exact font details it's impossible to
# determine exact auto width.
# http://stackoverflow.com/questions/3154270/python-xlwt-adjusting-column-widths?lq=1
def get_xls_col_width(text, style):
    return int((1 + len(text)) * 256)


def write_xlwt_row(ws, lno, cell_text, cell_widths, style=None):
    """Write row of utf-8 encoded data to worksheet, keeping track of maximum
    column width for each cell.
    """

    if style is None:
        style = xlwt.Style.default_style

    for cno, utf8_text in enumerate(cell_text):
        cell_text = utf8_text.decode('utf-8')
        ws.write(lno, cno, cell_text, style)
        cell_widths[cno] = max(cell_widths[cno],
                               get_xls_col_width(cell_text, style))


def convert_to_excel_xlwt(response):
    """Replace HttpResponse csv content with excel formatted data using xlwt
    library.
    """
    # Styles used in the spreadsheet.  Headings are bold.
    header_font = xlwt.Font()
    header_font.bold = True

    header_style = xlwt.XFStyle()
    header_style.font = header_font

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet 1')

    # Cell width information kept for every column, indexed by column number.
    cell_widths = collections.defaultdict(lambda: 0)

    content = StringIO.StringIO(response.content)
    reader = csv.reader(content)
    for lno, line in enumerate(reader):
        if lno == 0:
            style = header_style
        else:
            style = None

        write_xlwt_row(ws, lno, line, cell_widths, style)

    # Roughly autosize output column widths based on maximum column size.
    for col, width in cell_widths.iteritems():
        ws.col(col).width = width

    response.content = ''
    wb.save(response)


def convert_to_excel(response):
    if EXCEL_SUPPORT == 'xlwt':
        convert_to_excel_xlwt(response)
    elif EXCEL_SUPPORT == 'pyexcelerator':
        convert_to_excel_pyexcelerator(response)
    else:
        raise RuntimeError("No support for xls generation available")
