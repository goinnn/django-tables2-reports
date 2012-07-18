.. contents::

=====================
Django tables2 report
=====================

With django-tables2-reports you can get a CSV report of any `table <http://pypi.python.org/pypi/django-tables2/>`_  with **minimal changes** to your project

Requeriments
============

* `django-tables2 <http://pypi.python.org/pypi/django-tables2/>`_ (>=0.11.0)
* `pyExcelerator <http://pypi.python.org/pypi/pyExcelerator/>`_ (>=0.6.4a) (This is optional, to export to xls)


Installation
============

* In your settings:

::

    INSTALLED_APPS = (

        'django_tables2_reports',
    )


Changes in your project
=======================

1. Now your table should extend of 'TableReport'

::

    ############### Before ###################

    import django_tables2 as tables


    class MyTable(tables.Table):

        ...

    ############### Now ######################

    from django_tables2_reports.tables import TableReport


    class MyTable(TableReport):

        ...


2.a. If you use a traditional views, now you should use other RequestConfig and change a little your view:

::

    ############### Before ###################

    from django_tables2 import RequestConfig


    def my_view(request):
        objs = ....
        table = MyTable(objs)
        RequestConfig(request).configure(table)
        return render_to_response('app1/my_view.html',
                                  {'table': table},
                                  context_instance=RequestContext(request))

    ############### Now ######################

    from django_tables2_reports.config import RequestConfigReport as RequestConfig
    from django_tables2_reports.utils import create_report_http_response

    def my_view(request):
        objs = ....
        table = MyTable(objs)
        table_to_csv = RequestConfig(request).configure(table)
        if table_to_csv:
            return create_report_http_response(table_to_csv, request)
        return render_to_response('app1/my_view.html',
                                  {'table': table},
                                  context_instance=RequestContext(request))


If you have a lot of tables in your project, you can activate the middleware, and you do not have to change your views, only the RequestConfig import

::

    # In your settings 

    MIDDLEWARE_CLASSES = (

        'django_tables2_reports.middleware.TableReportMiddleware',
    )

    ############### Now (with middleware) ######################

    from django_tables2_reports.config import RequestConfigReport as RequestConfig

    def my_view(request):
        objs = ....
        table = MyTable(objs)
        RequestConfig(request).configure(table)
        return render_to_response('app1/my_view.html',
                                  {'table': table},
                                  context_instance=RequestContext(request))


2.b. If you use a `Class-based views <https://docs.djangoproject.com/en/dev/topics/class-based-views/>`_:

::

    ############### Before ###################

    from django_tables2.views import SingleTableView


    class PhaseChangeView(SingleTableView):
        table_class = MyTable
        model = MyModel


    ############### Now ######################

    from django_tables2_reports.views import ReportTableView


    class PhaseChangeView(ReportTableView):
        table_class = MyTable
        model = MyModel


Usage
=====

Under the table appear a CSV icon (and XLS icon if you have pyExcelerator), if you click in this icon, you get a CSV report (or xls report) with every item of the table (without pagination). The ordering works!

