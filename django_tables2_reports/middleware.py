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
from django.template.context import RequestContext
from django.template.loader import get_template

from django_tables2_reports.utils import generate_prefixto_report


class TableReportMiddleware(object):

    def process_response(self, request, response):
        if getattr(request, 'table', None):
            template = get_template('django_tables2_reports/table_report.html')
            context = RequestContext(request, {"table": request.table})
            context.update(request.extra_context)
            request.table.context = context
            param_report = generate_prefixto_report(request.table)
            report = template.render(RequestContext(request,
                                            {'table': request.table,
                                             'param_report': param_report}))
            filename = '%s.csv' % param_report
            response = HttpResponse(report, mimetype='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
        return response
