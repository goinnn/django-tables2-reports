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

import django_tables2 as tables

from django.template.context import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _

from django_tables2_reports.csv_to_excel import HAS_PYEXCELERATOR, convert_to_excel
from django_tables2_reports.utils import DEFAULT_PARAM_PREFIX, generate_prefixto_report


class TableReport(tables.Table):

    template_csv = 'django_tables2_reports/table_report.html'

    def __init__(self, *args, **kwargs):
        if not 'template' in kwargs:
            kwargs['template'] = 'django_tables2_reports/table.html'
        prefix_param_report = kwargs.pop('prefix_param_report', DEFAULT_PARAM_PREFIX)
        super(TableReport, self).__init__(*args, **kwargs)
        self.param_report = generate_prefixto_report(self, prefix_param_report)
        self.formats = [(_('CSV Report'), 'csv')]
        if HAS_PYEXCELERATOR:
            self.formats.append((_('XLS Report'), 'xls'))

    def as_report(self, request, format='csv'):
        if format == 'csv':
            return self.as_csv(request)
        elif format == 'xls':
            return self.as_xls(request)
        raise ValueError("This format %s is not accepted" % format)

    def as_csv(self, request):
        template = get_template(self.template_csv)
        context = RequestContext(request, {"table": self})
        context.update(request.extra_context)
        self.context = context
        param_report = generate_prefixto_report(self)
        return template.render(RequestContext(request,
                               {'table': self,
                                'param_report': param_report}))

    def as_xls(self, request):
        return self.as_csv(request)

    def treatement_to_response(self, response, format='csv'):
        if format == 'xls':
            convert_to_excel(response)
        return response
