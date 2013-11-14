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

import csv
import collections
import sys
import xlwt

from .base import get_content

PY3 = sys.version_info[0] == 3


def convert(response, encoding='utf-8', title_sheet='Sheet 1',  content_attr='content', csv_kwargs=None):
    """Replace HttpResponse csv content with excel formatted data using xlwt
    library.
    """
    csv_kwargs = csv_kwargs or {}
    # Styles used in the spreadsheet.  Headings are bold.
    header_font = xlwt.Font()
    header_font.bold = True

    header_style = xlwt.XFStyle()
    header_style.font = header_font

    wb = xlwt.Workbook(encoding=encoding)
    ws = wb.add_sheet(title_sheet)

    # Cell width information kept for every column, indexed by column number.
    cell_widths = collections.defaultdict(lambda: 0)
    content = get_content(response)
    reader = csv.reader(content, **csv_kwargs)
    for lno, line in enumerate(reader):
        if lno == 0:
            style = header_style
        else:
            style = None
        write_row(ws, lno, line, cell_widths, style=style, encoding=encoding)
    # Roughly autosize output column widths based on maximum column size.
    for col, width in cell_widths.items():
        ws.col(col).width = width
    setattr(response, content_attr, '')
    wb.save(response)


def write_row(ws, lno, cell_text, cell_widths, style=None, encoding='utf-8'):
    """Write row of utf-8 encoded data to worksheet, keeping track of maximum
    column width for each cell.
    """
    import xlwt
    if style is None:
        style = xlwt.Style.default_style
    for cno, utf8_text in enumerate(cell_text):
        cell_text = utf8_text
        if not PY3:
            cell_text = cell_text.decode(encoding)
        ws.write(lno, cno, cell_text, style)
        cell_widths[cno] = max(cell_widths[cno],
                               get_xls_col_width(cell_text, style))


# A reasonable approximation for column width is based off zero character in
# default font.  Without knowing exact font details it's impossible to
# determine exact auto width.
# http://stackoverflow.com/questions/3154270/python-xlwt-adjusting-column-widths?lq=1
def get_xls_col_width(text, style):
    return int((1 + len(text)) * 256)
