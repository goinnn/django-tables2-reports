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


    def test_csv_no_pagination(self):
        """Ensure that table pagination doesn't affect output."""

        data = [
            {
                'name': 'page 1',
                'item_num': 1,
            },
            {
                'name': 'page 2',
                'item_num': 2,
            },
        ]

        table = TableReportForTesting(data)
        table.paginate(per_page=1)

        response = table.as_csv(HttpRequest())

        # Ensure that even if table paginated, output is all row
        # data.
        self.assertEqual(
            response.content,
            ('Name,Item Num\r\n'
             'page 1,1\r\n'
             'page 2,2\r\n')
        )


class TestExcelGeneration(TestCase):

    def test_excel_simple_input(self):
        """Test ability to generate excel output with simple input data."""

        if not django_tables2_reports.csv_to_excel.EXCEL_SUPPORT:
            return

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
            {
                'name': u'String with ' + unichr(0x16c) + ' char',
                'item_num': 4,
            }
        ]

        table = TableReportForTesting(data)
        response = table.treatement_to_response(
            table.as_csv(HttpRequest()),
            format='xls')

        # No assertions.  Expect conversion to xls to succeed, even with
        # unicode chars.  Uncomment the following line and open test-file.xls
        # manually using Excel to verify that content is correct.
        open('test-file.xls', 'wb').write(response.content)
