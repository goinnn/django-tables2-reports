.. contents::

======================
django-tables2-reports
======================

.. image:: https://travis-ci.org/goinnn/django-tables2-reports.png?branch=master
    :target: https://travis-ci.org/goinnn/django-tables2-reports

.. image:: https://coveralls.io/repos/goinnn/django-tables2-reports/badge.png?branch=master
    :target: https://coveralls.io/r/goinnn/django-tables2-reports

.. image:: https://badge.fury.io/py/django-tables2-reports.png
    :target: https://badge.fury.io/py/django-tables2-reports

.. image:: https://pypip.in/d/django-tables2-reports/badge.png
    :target: https://pypi.python.org/pypi/django-tables2-reports

.. image:: https://d2weczhvl823v0.cloudfront.net/goinnn/django-tables2-reports/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

With django-tables2-reports you can get a report (CSV, XLS) of any `table <http://pypi.python.org/pypi/django-tables2/>`_  with **minimal changes** to your project

Requeriments
============

* `django <http://pypi.python.org/pypi/django/>`_ (>=1.3)
* `django-tables2 <http://pypi.python.org/pypi/django-tables2/>`_ (>=0.11.0, tested with 0.14.0)
* `xlwt <http://pypi.python.org/pypi/xlwt/>`_ (>=0.7.5), `openpyxl <http://pythonhosted.org/openpyxl/>`_ (>=1.6.2) or `pyExcelerator <http://pypi.python.org/pypi/pyExcelerator/>`_ (>=0.6.4.1) (These are optionals, to export to xls. Default to xlwt if available)

If you use python3, and you want export to xls use this version of the `xlwt (fork) <https://pypi.python.org/pypi/xlwt-future/>`_ (0.8.0) if this `pull request <https://github.com/python-excel/xlwt/pull/32>`_ is not merged still , or use `openpyxl <http://pythonhosted.org/openpyxl/>`_


Installation
============

* In your settings:

::

    INSTALLED_APPS = (

        'django_tables2_reports',
    )


    TEMPLATE_CONTEXT_PROCESSORS = (

        'django.core.context_processors.static',

    )


    # This is optional

    EXCEL_SUPPORT = 'xlwt' # or 'openpyxl' or 'pyexcelerator'

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
        table_to_report = RequestConfig(request).configure(table)
        if table_to_report:
            return create_report_http_response(table_to_report, request)
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

Under the table appear a CSV icon (and XLS icon if you have `xlwt <http://pypi.python.org/pypi/xlwt/>`_, `openpyxl <http://pythonhosted.org/openpyxl/>`_ or `pyExcelerator <http://pypi.python.org/pypi/pyExcelerator/>`_ in your python path), if you click in this icon, you get a CSV report (or xls report) with every item of the table (without pagination). The ordering works!

Test project
============

In the source tree, you will find a directory called 'test_project'. It contains
a readily setup project that uses django-tables2-reports. You can run it as usual:

::

    python manage.py runserver
