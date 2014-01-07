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

from django_tables2_reports.utils import create_report_http_response, REQUEST_VARIABLE, REPORT_CONTENT_TYPES


class TableReportMiddleware(object):

    def process_response(self, request, response):
        table_to_report = getattr(request, REQUEST_VARIABLE, None)
        current_content_type = response.get('Content-Type', None)
        if table_to_report and current_content_type not in REPORT_CONTENT_TYPES:
            return create_report_http_response(table_to_report, request)
        return response
