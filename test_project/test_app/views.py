# Create your views here.
from django_tables2_reports.tables import TableReport
from django_tables2_reports.views import ReportTableView
from test_app.models import Person


class TestTable(TableReport):
    class Meta:
        model = Person
        attrs = {"class": "paleblue"}


class TestView(ReportTableView):
    table_class = TestTable
    model = Person
