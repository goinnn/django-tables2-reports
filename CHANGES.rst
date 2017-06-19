Releases
========

0.1.0 (2017-06-19)
------------------
* maintenance release, 
* Django 1.8, 1.9, 1.10, 1.11 support,
* openpyxl > 2.0.0 support,
* recent django-tables2 support,
* new maintainer `Michał Pasternak <https://github.com/mpasternak>`_

0.0.10 (2014-10-13)
-------------------
* Fixes for xlsx Content-Type:
    * django-tables2-reports throws 500 Sever Error when report format is not recognized. 404 is more appropriate in this case.
    * django-tables2-reports sets Content-Type to application/vnd.ms-excel for xlsx files which causes warnings in Firefox. application/vnd.openxmlformats-officedocument.spreadsheetml.sheet is the correct Content-Type for xlsx
* Support to Django 1.7 (I'm sorry to the delay)
* Adding new feature: exclude_from_report
* And a little details
* Thanks to:
    * `Ramana Varanasi <https://github.com/sramana>`_
    * `Mihas <https://github.com/mihasK>`_
    * `Paulgueltekin <https://github.com/paulgueltekin>`_
    * `David Ray <https://github.com/daaray>`_

0.0.9 (2013-11-30)
------------------
* Compatible with the future version  of Django (>=1.7)
* Update the tests
* Refactor the code
* Fix a bug when the title of the sheet is longer than 31
* Thanks to:
    * `Pavel Zaytsev <https://github.com/stelzzz>`_


0.0.8 (2013-11-14)
------------------
* `Refactor the csv_to_excel module <https://github.com/goinnn/django-tables2-reports/commit/51c8cee2500f73ba8b823a81fc5ad9b3f2a62d83>`_. In the next release this package will be a pypi egg.
* Support for `openpyxl <http://pythonhosted.org/openpyxl/>`_
* Integration with travis and coveralls
* Fix an error if you use the theme paleblue
* Fix test with python 3
* Fix some details
* Test project
* Thanks to:
    * `Michał Pasternak <https://github.com/mpasternak>`_
    * `Mark Jones <https://github.com/mark0978>`_

0.0.7 (2013-08-29)
------------------

* Russian translations
* Thanks to:
    * `Armicron <https://github.com/armicron>`_


0.0.6  (2013-08-22)
-------------------

* Python3 support
* Polish translation
* Thanks to:
    * `Michał Pasternak <https://github.com/mpasternak>`_

0.0.5  (2013-07-03)
-------------------

* Improvements in the README
* Exportable to XLS with `xlwt <http://pypi.python.org/pypi/xlwt/>`_
* Thanks to:
    * `Crashy23 <https://github.com/Crashy23>`_
    * `Gamesbook <https://github.com/gamesbook>`_
    * And spatially to `Austin Phillips <https://github.com/austinphillips2>`_


0.0.4  (2013-05-17)
-------------------

* Escape csv data correctly during output
* The fields with commas now are not split into multiple columns
* Thanks to:
    * `Austin Phillips <https://github.com/austinphillips2>`_

0.0.3  (2012-07-19)
-------------------

* Fix a little error, when a column has line breaks. Now these are changed to espaces
* Details

0.0.2  (2012-07-18)
-------------------

* Add a default view (https://docs.djangoproject.com/en/dev/topics/class-based-views/)
* Exportable to XLS
* Update the README

0.0.1  (2012-07-17)
-------------------

* Initial release
