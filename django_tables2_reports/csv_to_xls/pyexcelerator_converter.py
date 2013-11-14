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
import pyExcelerator


from .base import get_content


def convert(response, encoding='utf-8', title_sheet='Sheet 1', content_attr='content', csv_kwargs=None):
    csv_kwargs = csv_kwargs or {}
    workbook = pyExcelerator.Workbook()
    worksheet = workbook.add_sheet(title_sheet)
    lno = 0
    content = get_content(response)
    reader = csv.reader(content, **csv_kwargs)
    for line in reader:
        write_row(worksheet, lno, line, encoding=encoding)
        lno = lno + 1
    setattr(response, 'content_attr', workbook.get_biff_data())


def write_row(worksheet, lno, columns, encoding='utf-8'):
    """ Write a non-header row into the worksheet """
    cno = 0
    for column in columns:
        worksheet.write(lno, cno, column.decode(encoding))
        cno = cno + 1
