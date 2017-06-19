.. contents::

======================
django-tables2-reports
======================

.. image:: https://travis-ci.org/goinnn/django-tables2-reports.svg?branch=master
    :target: https://travis-ci.org/goinnn/django-tables2-reports

.. image:: https://coveralls.io/repos/goinnn/django-tables2-reports/badge.png?branch=master
    :target: https://coveralls.io/r/goinnn/django-tables2-reports

.. image:: https://badge.fury.io/py/django-tables2-reports.svg
    :target: https://pypi.python.org/pypi/django-tables2-reports

With django-tables2-reports you can get a report (CSV, XLS) of any `table <http://pypi.python.org/pypi/django-tables2/>`_  with **minimal changes** to your project

Requirements
============

* `Python <http://python.org>`_ (supports 2.7, 3.3, 3.4, 3.5, 3.6)
* `Django <http://pypi.python.org/pypi/django/>`_ (supports 1.3, 1.4, 1.5, 1.6, 1.7, 1.8. 1.9, 1.10, 1.11)
* `django-tables2 <http://pypi.python.org/pypi/django-tables2/>`_ 
* `xlwt <http://pypi.python.org/pypi/xlwt/>`_, `openpyxl <http://pythonhosted.org/openpyxl/>`_ or `pyExcelerator <http://pypi.python.org/pypi/pyExcelerator/>`_  (these are optionals, to export to xls; defaults to xlwt if available)


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

1.a Now your table should extend of 'TableReport'

::

    ############### Before ###################

    import django_tables2 as tables


    class MyTable(tables.Table):

        ...

    ############### Now ######################

    from django_tables2_reports.tables import TableReport


    class MyTable(TableReport):

        ...

1.b If you want to exclude some columns from report (e.g. if it is a column of buttons), you should set 'exclude_from_report' - the names of columns (as well as property 'exclude' in `table <http://pypi.python.org/pypi/django-tables2/>`_)

::

    class MyTable(TableReport):

        class Meta:
            exclude_from_report = ('column1', ...)
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


Development
===========

You can get the last bleeding edge version of django-tables2-reports by doing a clone
of its git repository::

  git clone https://github.com/goinnn/django-tables2-reports


Test project
============

In the source tree, you will find a directory called 'test_project'. It contains
a readily setup project that uses django-tables2-reports. You can run it as usual:

::

    python manage.py syncdb --noinput
    python manage.py runserver
