# -*- coding: utf-8 -*-
# Copyright (c) 2012 by Pablo Martín <goinnn@gmail.com>
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
import cStringIO as StringIO
import codecs

import django_tables2 as tables

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.utils.html import strip_tags

from django_tables2_reports.csv_to_excel import EXCEL_SUPPORT, convert_to_excel
from django_tables2_reports.utils import DEFAULT_PARAM_PREFIX, generate_prefixto_report


# Unicode CSV writer, copied direct from Python docs:
# http://docs.python.org/2/library/csv.html

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class TableReport(tables.Table):

    def __init__(self, *args, **kwargs):
        if not 'template' in kwargs:
            kwargs['template'] = 'django_tables2_reports/table.html'
        prefix_param_report = kwargs.pop('prefix_param_report', DEFAULT_PARAM_PREFIX)
        super(TableReport, self).__init__(*args, **kwargs)
        self.param_report = generate_prefixto_report(self, prefix_param_report)
        self.formats = [(_('CSV Report'), 'csv')]
        if EXCEL_SUPPORT:
            self.formats.append((_('XLS Report'), 'xls'))

    def as_report(self, request, format='csv'):
        if format == 'csv':
            return self.as_csv(request)
        elif format == 'xls':
            return self.as_xls(request)
        raise ValueError("This format %s is not accepted" % format)

    def as_csv(self, request):
        response = HttpResponse()
        csv_writer = UnicodeWriter(response)

        csv_header = [ column.header for column in self.columns ]
        csv_writer.writerow(csv_header)

        for row in self.rows:
            csv_writer.writerow([ strip_tags(cell) for column, cell in row.items() ])

        return response

    def as_xls(self, request):
        return self.as_csv(request)

    def treatement_to_response(self, response, format='csv'):
        if format == 'xls':
            convert_to_excel(response)
        return response
