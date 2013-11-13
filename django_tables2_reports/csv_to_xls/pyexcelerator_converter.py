# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

# This only works with python 2.x

import csv

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


def convert_to_excel(response, encoding='utf-8', title_sheet='Sheet 1'):
    import pyExcelerator
    titlePresent = False
    linesPerFile = -1
    workbook = pyExcelerator.Workbook()
    worksheet = workbook.add_sheet(title_sheet)
    fno = 0
    lno = 0
    titleCols = []
    content = StringIO(response.content)
    reader = csv.reader(content)
    for line in reader:
        if (lno == 0 and titlePresent):
            if (len(titleCols) == 0):
                titleCols = line
            write_header(worksheet, titleCols)
        else:
            write_row(worksheet, lno, line, encoding=encoding)
        lno = lno + 1
        if (linesPerFile != -1 and lno >= linesPerFile):
            fno = fno + 1
            lno = 0
    response.content = workbook.get_biff_data()


def write_header(worksheet, titleCols):
    """ Write the header line into the worksheet """
    cno = 0
    for titleCol in titleCols:
        worksheet.write(0, cno, titleCol)
        cno = cno + 1


def write_row(worksheet, lno, columns, encoding='utf-8'):
    """ Write a non-header row into the worksheet """
    cno = 0
    for column in columns:
        worksheet.write(lno, cno, column.decode(encoding))
        cno = cno + 1
