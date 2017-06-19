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

import sys

from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
try:
    from django.utils.unittest import skipIf
except ImportError:
    from django.test.utils import skipIf
import django_tables2
import django_tables2_reports.tables
import django_tables2_reports.views


PY3 = sys.version_info[0] == 3
if PY3:
    unichr = chr


class TableReportForTesting(django_tables2_reports.tables.TableReport):
    name = django_tables2.Column()
    item_num = django_tables2.Column()


class ReportTableViewForTesting(django_tables2_reports.views.ReportTableView):
    table_class = TableReportForTesting


class TestCsvGeneration(TestCase):
    """Test csv generation on sample table data."""

    def test_csv_simple_input(self):
        """Test ability to generate csv with simple input data."""

        # Mix of integer and string data.  Ensure that commas and
        # quotes are escaped properly.
        data = [
            {
                'name': 'Normal string',
                'item_num': 1,
            },
            {
                'name': 'String, with, commas',
                'item_num': 2,
            },
            {
                'name': 'String with " quote',
                'item_num': 3,
            },
        ]

        table = TableReportForTesting(data)
        response = table.as_csv(HttpRequest())
        self.assertEqual(response.status_code, 200)
        # Expect cells containing commas to be escaped with quotes.
        content = response.content
        if PY3:
            content = content.decode(settings.DEFAULT_CHARSET).replace('\x00', '')
        self.assertEqual(
            content,
            'Name,Item Num\r\n'
            'Normal string,1\r\n'
            '"String, with, commas",2\r\n'
            '"String with "" quote",3\r\n')

    def test_csv_with_unicode(self):
        """Test that unicode cell values are converted correctly to csv."""

        data = [
            {
                'name': 'Normal string',
                'item_num': 1,
            },
            {
                'name': u'String with ' + unichr(0x16c) + ' char',
                'item_num': 2,
            },
        ]

        table = TableReportForTesting(data)
        response = table.as_csv(HttpRequest())
        self.assertEqual(response.status_code, 200)
        # Expect csv content to be utf-8 encoded.
        content = response.content
        result = ('Name,Item Num\r\n'
                  'Normal string,1\r\n'
                  'String with ' + unichr(0x16c) + ' char,2\r\n')
        if PY3:
            content = content.decode(settings.DEFAULT_CHARSET).replace('\x00', '')
        else:
            result = result.encode(settings.DEFAULT_CHARSET)
        self.assertEqual(content, result)

    def test_csv_no_pagination(self):
        """Ensure that table pagination doesn't affect output."""

        data = [
            {
                'name': 'page 1',
                'item_num': 1,
            },
            {
                'name': 'page 2',
                'item_num': 2,
            },
        ]

        table = TableReportForTesting(data)
        table.paginate(per_page=1)

        response = table.as_csv(HttpRequest())
        self.assertEqual(response.status_code, 200)
        # Ensure that even if table paginated, output is all row
        # data.
        content = response.content
        if PY3:
            content = content.decode(settings.DEFAULT_CHARSET).replace('\x00', '')
        self.assertEqual(
            content,
            ('Name,Item Num\r\n'
             'page 1,1\r\n'
             'page 2,2\r\n')
        )

    def test_exclude_from_report(self):
        """Ensure that exclude-some-columns-from-report works."""
        data = [
            {
                'name': 'page 1',
                'item_num': 1,
            },
            {
                'name': 'page 2',
                'item_num': 2,
            },
        ]

        class TableWithExclude(TableReportForTesting):
            class Meta:
                exclude_from_report = ('item_num',)

        table = TableWithExclude(data)
        table.exclude = ('name', )
        self.assertEqual(table.exclude_from_report, ('item_num',))

        response = table.as_csv(HttpRequest())
        self.assertEqual(response.status_code, 200)
        content = response.content
        if PY3:
            content = content.decode(settings.DEFAULT_CHARSET).replace('\x00', '')

        self.assertEqual(table.exclude, ('name',))  # Attribute 'exclude_from_report' shouldn't overwrite 'exclude'
        self.assertEqual(
            content,
            ('Name\r\n'
             'page 1\r\n'
             'page 2\r\n')
        )


@skipIf(
    not django_tables2_reports.utils.get_excel_support(),
    "No Excel support, please install xlwt, pyExcelerator or openpyxl")
class TestExcelGeneration(TestCase):
    def setUp(self):
        # Mix of integer and string data.  Ensure that commas and
        # quotes are escaped properly.
        self.data = [
            {
                'name': 'Normal string',
                'item_num': 1,
            },
            {
                'name': 'String, with, commas',
                'item_num': 2,
            },
            {
                'name': 'String with " quote',
                'item_num': 3,
            },
            {
                'name': u'String with ' + unichr(0x16c) + ' char',
                'item_num': 4,
            }
        ]
        self.table = TableReportForTesting(self.data)

    def test_excel_simple_input(self, extension='xls'):
        """Test ability to generate excel output with simple input data."""
        excel_support = getattr(settings, 'EXCEL_SUPPORT', django_tables2_reports.utils.get_excel_support())
        response = self.table.treatement_to_response(
            self.table.as_csv(HttpRequest()),
            report_format='xls')
        self.assertEqual(response.status_code, 200)
        open('test-file-%s.%s' % (excel_support, extension),
             'wb').write(response.content)

    def test_pyexcelerator(self):
        if PY3:
            return
        settings.EXCEL_SUPPORT = "pyexcelerator"
        self.test_excel_simple_input()

    def test_xlwt(self):
        settings.EXCEL_SUPPORT = "xlwt"
        self.test_excel_simple_input()

    def test_openpyxls(self):
        settings.EXCEL_SUPPORT = "openpyxl"
        self.test_excel_simple_input(extension='xlsx')
