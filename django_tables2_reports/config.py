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

from django_tables2.config import RequestConfig

from django_tables2_reports.utils import REQUEST_VARIABLE


class RequestConfigReport(RequestConfig):

    def __init__(self, request, paginate=True, paginate_report=False):
        self.request = request
        self.paginate = paginate
        self.paginate_report = paginate_report

    def configure(self, table, extra_context=None):
        table.is_configured = True
        param_report = table.param_report
        is_report = self.request.GET.get(param_report)
        table_to_report = None
        if is_report:
            self.paginate = self.paginate_report
            table_to_report = table
            setattr(self.request, REQUEST_VARIABLE, table_to_report)
            self.request.extra_context = extra_context or {}
        super(RequestConfigReport, self).configure(table)
        return table_to_report
