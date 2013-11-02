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

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from test_app.models import Person


class TestRenderDT2R(TestCase):

    def _test_check_render(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response

    def test_check_render_class_view(self):
        url = reverse('index')
        response = self._test_check_render(url)
        return response

    def test_check_render_function_view(self):
        url = reverse('index_function_view')
        response = self._test_check_render(url)
        return response

    def test_equal_render_class_view_and_function_view(self):
        response_clv = self.test_check_render_class_view()
        response_fv = self.test_check_render_function_view()
        self.assertEqual(response_clv.status_code, response_fv.status_code)
        self.assertEqual(response_clv.content, response_fv.content)

    def _test_check_report_csv(self, url, report_format='csv'):
        url = url + '?report-testtable=%s' % report_format
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        if report_format == 'csv':
            num_lines = len([line for line in response.content.split('\n') if line])
            self.assertEqual(num_lines - 1, Person.objects.all().count())
        return response

    def test_check_report_csv_class_view(self, report_format='csv'):
        url = reverse('index')
        response = self._test_check_report_csv(url, report_format=report_format)
        return response

    def test_check_report_csv_function_view(self, report_format='csv'):
        url = reverse('index_function_view')
        response = self._test_check_report_csv(url, report_format=report_format)
        return response

    def test_equal_report_class_view_and_function_view(self, report_format='csv'):
        response_clv = self.test_check_report_csv_class_view(report_format=report_format)
        response_fv = self.test_check_report_csv_function_view(report_format=report_format)
        self.assertEqual(response_clv.status_code, response_fv.status_code)
        self.assertEqual(response_clv.content, response_fv.content)

    def test_check_report_xls_class_view(self):
        return self.test_check_report_csv_class_view('xls')

    def test_check_report_xls_function_view(self):
        return self.test_check_report_csv_function_view('xls')

    def test_equal_report_class_view_and_function_view_xls(self):
        response_clv = self.test_check_report_xls_class_view()
        response_fv = self.test_check_report_xls_function_view()
        self.assertEqual(response_clv.status_code, response_fv.status_code)
        self.assertEqual(response_clv.content, response_fv.content)

    def test_check_report_csv_function_view_middleware(self):
        report_format = 'csv'
        response = self.test_check_report_csv_function_view(report_format=report_format)
        url = reverse('index_function_view_middleware')
        try:
            self._test_check_report_csv(url, report_format=report_format)
            raise AssertionError("The call to _test_check_report_csv method should get an AssertionError exception")
        except AssertionError:
            pass
        original_middlewares = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES += ('django_tables2_reports.middleware.TableReportMiddleware',)
        self.client.handler.load_middleware()
        response_with_middleware = self._test_check_report_csv(url, report_format=report_format)
        self.assertEqual(response.content, response_with_middleware.content)
        settings.MIDDLEWARE_CLASSES = original_middlewares
        self.assertEqual('django_tables2_reports.middleware.TableReportMiddleware' in settings.MIDDLEWARE_CLASSES,
                         False)
        self.client.handler.load_middleware()
