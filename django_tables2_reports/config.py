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


from django_tables2.config import RequestConfig


class RequestConfigReport(RequestConfig):

    def __init__(self, request, paginate=True, paginate_report=False, param_report='report'):
        self.request = request
        self.paginate = paginate
        self.paginate_report = paginate_report
        self.param_report = param_report

    def configure(self, table):
        param_report = self.param_report
        if table.prefix:
            param_report = '%s-%s' % (param_report, table.prefix)
        is_report = self.request.GET.get(param_report)
        if is_report:
            self.paginate = self.paginate_report
            self.request.table = table
        super(RequestConfigReport, self).configure(table)
