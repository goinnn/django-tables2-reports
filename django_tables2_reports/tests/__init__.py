from django.test import TestCase
from django.http import HttpRequest


import django_tables2
import django_tables2_reports.tables
import django_tables2_reports.views


class TableReportForTesting(django_tables2_reports.tables.TableReport):
    name = django_tables2.Column()
    item_num = django_tables2.Column()


class ReportTableViewForTesting(django_tables2_reports.views.ReportTableView):
    table_class = TableReportForTesting


class TestCsvGeneration(TestCase):
    """Test csv generation on sample table data."""

    def test_csv_simple_input(self):
        """Test ability to generate csv with simple input data."""

        # Mix of integer and string data.  Ensure that commas and
        # quotes are escaped properly.
        data = [
            {
                'name': 'Normal string',
                'item_num': 1,
            },
            {
                'name': 'String, with, commas',
                'item_num': 2,
            },
            {
                'name': 'String with " quote',
                'item_num': 3,
            },
        ]

        table = TableReportForTesting(data)
        response = table.as_csv(HttpRequest())

        # Expect cells containing commas to be escaped with quotes.
        self.assertEqual(
            response.content,
            'Name,Item Num\r\n'
            'Normal string,1\r\n'
            '"String, with, commas",2\r\n'
            '"String with "" quote",3\r\n')

    def test_csv_with_unicode(self):
        """Test that unicode cell values are converted correctly to csv."""

        data = [
            {
                'name': 'Normal string',
                'item_num': 1,
            },
            {
                'name': u'String with ' + unichr(0x16c) + ' char',
                'item_num': 2,
            },
        ]

        table = TableReportForTesting(data)
        response = table.as_csv(HttpRequest())

        # Expect csv content to be utf-8 encoded.
        self.assertEqual(
            response.content,
            ('Name,Item Num\r\n'
             'Normal string,1\r\n'
             'String with ' + unichr(0x16c) + ' char,2\r\n').encode('utf-8'))
