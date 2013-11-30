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

#http://stackoverflow.com/questions/3681868/is-there-a-limit-on-an-excel-worksheets-name-length
MAX_LENGTH_TITLE_SHEET = 31


def convert(response, excel_support=None, encoding='utf-8',
            title_sheet='Sheet 1', content_attr='content', csv_kwargs=None):
    if len(title_sheet) > MAX_LENGTH_TITLE_SHEET:
        raise ValueError("The maximum length of a title of a sheet is %s" % MAX_LENGTH_TITLE_SHEET)
    excel_support = excel_support or get_xls_support()
    if excel_support == 'xlwt':
        from .xlwt_converter import convert
    elif excel_support == 'openpyxl':
        from .openpyxl_converter import convert
    elif excel_support == 'pyexcelerator':
        from .pyexcelerator_converter import convert
    else:
        raise RuntimeError("No support for xls generation available")

    convert(response,
            encoding=encoding,
            title_sheet=title_sheet,
            content_attr=content_attr,
            csv_kwargs=csv_kwargs)


def get_xls_support():
    try:
        import xlwt
        return 'xlwt'
    except ImportError:
        pass
    try:
        import openpyxl
        return 'openpyxl'
    except ImportError:
        pass
    try:
        import pyExcelerator
        return 'pyexcelerator'
    except ImportError:
        pass
    return None
