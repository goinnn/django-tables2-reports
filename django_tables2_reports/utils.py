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

DEFAULT_PARAM_PREFIX = 'report'


def generate_prefixto_report(table, prefix_param_report=None):
    param_report = prefix_param_report or DEFAULT_PARAM_PREFIX
    param_report = "%s-%s" % (param_report, table.__class__.__name__.lower())
    prefix = table.prefix
    if prefix:
        param_report = "%s-%s" % (prefix, param_report)
    return param_report


def create_report_http_response(table, request):
    format = request.GET.get(table.param_report)
    report = table.as_report(request, format)
    filename = '%s.csv' % table.param_report
    response = HttpResponse(report, mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
