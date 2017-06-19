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

import django

from django_tables2.views import SingleTableView

from django_tables2_reports.config import RequestConfigReport
from django_tables2_reports.utils import create_report_http_response


class ReportTableView(SingleTableView):

    def get_table(self, **kwargs):
        """
        Return a table object to use. The table has automatic support for
        sorting and pagination.
        """
        options = {}
        table_class = self.get_table_class()
        table = table_class(self.get_table_data(), **kwargs)
        args = ()
        if django.VERSION >= (1,8,0):
            args = (table, )
        paginate = self.get_table_pagination(*args)
        if paginate is not None:
            options['paginate'] = paginate
        self.table_to_report = RequestConfigReport(self.request, **options).configure(table)
        return table

    def render_to_response(self, context, **response_kwargs):
        if self.table_to_report:
            return create_report_http_response(self.table_to_report, self.request)
        return super(ReportTableView, self).render_to_response(context, **response_kwargs)
