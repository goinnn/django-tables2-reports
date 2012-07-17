.. contents::

=====================
Django tables2 report
=====================

With django-tables2-reports you can get a CSV report of any `table <http://pypi.python.org/pypi/django-tables2/>`_  with **minimal changes** to your project

Requeriments
============

* `django-tables2 <http://pypi.python.org/pypi/django-tables2/>`_ (>=0.11.0)

Installation
============

* In your settings:

::

    INSTALLED_APPS = (

        'django_tables2_reports',
    )

    MIDDLEWARE_CLASSES = (

        'django_tables2_reports.middleware.TableReportMiddleware',
    )


Changes in your project
=======================

* Now your table should extend of 'TableReport'

::

    ############### Before ###################

    import django_tables2 as tables


    class MyTable(tables.Table):

        ...

    ############### Now ######################

    from django_tables2_reports.tables import TableReport


    class MyTable(TableReport):

        ...


* Now you should use other RequestConfig:

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

    def my_view(request):
        objs = ....
        table = MyTable(objs)
        RequestConfig(request).configure(table)
        return render_to_response('app1/my_view.html',
                                  {'table': table},
                                  context_instance=RequestContext(request))

Usage
=====

Under the table appear a CSV icon, if you click in this icon, you get a CSV report with every item of the table (without pagination). The ordering works!


Other way to use this application
=================================

You could not use the middleware and to change a little every view, you would get a more efficient code, but you would have to adapt every view