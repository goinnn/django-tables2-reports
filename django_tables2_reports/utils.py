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

from django.http import HttpResponse
from django_tables2_reports import csv_to_xls

DEFAULT_PARAM_PREFIX = 'report'
REQUEST_VARIABLE = 'table_to_report'
REPORT_CONTENT_TYPES = {
    'csv': 'text/csv',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}
REPORT_MYMETYPE = REPORT_CONTENT_TYPES['xls']  # backwards compatible


def create_report_http_response(table, request):
    report_format = request.GET.get(table.param_report)
    report = table.as_report(request, report_format=report_format)
    extension = get_extension_report(report_format)
    filename = '%s.%s' % (table.param_report, extension)
    response = HttpResponse(report, content_type=REPORT_CONTENT_TYPES[extension])
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response = table.treatement_to_response(response, report_format=report_format)
    return response


def get_excel_support():
    # If you don't specify a xls library, this function will autodetect the library to use for xls writing. Default to xlwt.
    from django.conf import settings
    return getattr(settings, "EXCEL_SUPPORT", None) or csv_to_xls.get_xls_support()


def get_extension_report(report_format):
    if report_format == 'xls' and get_excel_support() == "openpyxl":
        return 'xlsx'
    return report_format


def generate_prefixto_report(table, prefix_param_report=None):
    param_report = prefix_param_report or DEFAULT_PARAM_PREFIX
    table_class = table.__class__
    prefix = table.prefix
    param_report = "%s-%s" % (param_report, table_class.__name__.lower())
    if prefix:
        param_report = "%s-%s" % (prefix, param_report)
    return param_report
