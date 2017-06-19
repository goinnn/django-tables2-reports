# Create your views here.
import django

from django.template import RequestContext

from django_tables2_reports.config import RequestConfigReport as RequestConfig
from django_tables2_reports.tables import TableReport
from django_tables2_reports.utils import create_report_http_response
from django_tables2_reports.views import ReportTableView

from test_app.models import Person


class TestTable(TableReport):

    class Meta:
        model = Person
        attrs = {"class": "paleblue"}


class TestView(ReportTableView):
    table_class = TestTable
    model = Person

def compat_render_to_response(template_name, context, context_instance, request):
    if django.VERSION < (1,10,0):
        from django.shortcuts import render_to_response
        return render_to_response(template_name, context, context_instance=context_instance)
    from django.shortcuts import render
    return render(request, template_name, context)

def index_function_view(request):
    objs = Person.objects.all()
    table = TestTable(objs)
    table_to_report = RequestConfig(request).configure(table)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return compat_render_to_response('test_app/person_list.html',
                                     {'table': table},
                                     context_instance=RequestContext(request), 
                                     request=request)


def index_function_view_middleware(request):
    objs = Person.objects.all()
    table = TestTable(objs, prefix='my-prefix')
    RequestConfig(request).configure(table)
    return compat_render_to_response('test_app/person_list.html',
                              {'table': table},
                              context_instance=RequestContext(request),
                                     request=request)
