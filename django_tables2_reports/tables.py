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
import codecs
import sys
from functools import wraps

PY3 = sys.version_info[0] == 3

if PY3:
    string = str
    unicode = str
else:
    string = basestring

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import django_tables2 as tables

from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import HttpResponse, Http404
from django.utils.html import strip_tags

from django_tables2_reports import csv_to_xls
from django_tables2_reports.utils import (DEFAULT_PARAM_PREFIX,
                                          get_excel_support,
                                          generate_prefixto_report)


# Unicode CSV writer, copied direct from Python docs:
# http://docs.python.org/2/library/csv.html

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
        self.encoding = encoding

    def writerow(self, row):
        if PY3:
            self.writer.writerow([s for s in row])
            # Fetch UTF-8 output from the queue ...
            data = self.queue.getvalue()
        else:
            self.writer.writerow([s.encode(self.encoding) for s in row])
            # Fetch UTF-8 output from the queue ...
            data = self.queue.getvalue()
            data = data.decode(self.encoding)
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)


class TableReport(tables.Table):

    exclude_from_report = ()  # the names of columns that should be excluded from report

    def __init__(self, *args, **kwargs):
        if not 'template' in kwargs:
            kwargs['template'] = 'django_tables2_reports/table.html'
        prefix_param_report = kwargs.pop('prefix_param_report', DEFAULT_PARAM_PREFIX)
        super(TableReport, self).__init__(*args, **kwargs)
        self.param_report = generate_prefixto_report(self, prefix_param_report)
        self.formats = [(_('CSV Report'), 'csv')]
        if get_excel_support():
            self.formats.append((_('XLS Report'), 'xls'))
        if hasattr(self, 'Meta'):
            self.exclude_from_report = getattr(self.Meta, 'exclude_from_report', ())

    def _with_exclude_from_report(method):
        """ Put to 'exclude' columns from 'exclude_from_report', and revert this after method's call """
        @wraps(method)
        def with_exclude(self, *args, **kwargs):
            origin_exclude = self.exclude
            self.exclude = self.exclude_from_report
            try:
                return method(self, *args, **kwargs)
            finally:
                self.exclude = origin_exclude
        return with_exclude

    def as_report(self, request, report_format='csv'):
        if report_format == 'csv':
            return self.as_csv(request)
        elif report_format == 'xls':
            return self.as_xls(request)
        else:
            raise Http404("This format %s is not accepted" % report_format)

    @_with_exclude_from_report
    def as_csv(self, request):
        response = HttpResponse()
        csv_writer = UnicodeWriter(response, encoding=settings.DEFAULT_CHARSET)
        csv_header = [column.header for column in self.columns]
        csv_writer.writerow(csv_header)
        for row in self.rows:
            csv_row = []
            for column, cell in row.items():
                if isinstance(cell, string):
                    # if cell is not a string strip_tags(cell) get an
                    # error in django 1.6
                    cell = strip_tags(cell)
                else:
                    cell = unicode(cell)
                csv_row.append(cell)
            csv_writer.writerow(csv_row)
        return response

    @_with_exclude_from_report
    def as_xls(self, request):
        return self.as_csv(request)

    def treatement_to_response(self, response, report_format='csv'):
        if report_format == 'xls':
            csv_to_xls.convert(response, get_excel_support(),
                               encoding=settings.DEFAULT_CHARSET,
                               title_sheet=self.param_report[:csv_to_xls.MAX_LENGTH_TITLE_SHEET])
        return response
