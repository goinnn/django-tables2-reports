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

from django.http import HttpResponse
from django_tables2.tables import Table

DEFAULT_PARAM_PREFIX = 'report'
REQUEST_VARIABLE = 'table_to_report'
REPORT_MYMETYPE = 'application/vnd.ms-excel'


def generate_prefixto_report(table, prefix_param_report=None):
    param_report = prefix_param_report or DEFAULT_PARAM_PREFIX
    if isinstance(table, Table):
        table_class = table.__class__
        prefix = table.prefix
    else:
        table_class = table
        prefix = None
    param_report = "%s-%s" % (param_report, table_class.__name__.lower())
    if prefix:
        param_report = "%s-%s" % (prefix, param_report)
    return param_report


def create_report_http_response(table, request):
    format = request.GET.get(table.param_report)
    report = table.as_report(request, format=format)
    filename = '%s.%s' % (table.param_report, format)
    response = HttpResponse(report, mimetype=REPORT_MYMETYPE)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response = table.treatement_to_response(response, format=format)
    return response
