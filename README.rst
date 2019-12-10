========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
        | |codeclimate|
    * - package
      - | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-mop/badge/?style=flat
    :target: https://readthedocs.org/projects/python-mop
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/robertfischer3/python-mop.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/robertfischer3/python-mop.svg?token=GfKWzWQRa9YAeNYM2ptG&branch=master

.. |codeclimate| image:: https://codeclimate.com/github/robertfischer3/python-mop/badges/gpa.svg
   :target: https://codeclimate.com/github/robertfischer3/python-mop
   :alt: CodeClimate Quality Status

.. |commits-since| image:: https://img.shields.io/github/commits-since/robertfischer3/python-mop/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/robertfischer3/python-mop/compare/v0.0.1...master



.. end-badges

A Python library used to compile Azure resource compliance information

* Free software: MIT license

Installation
============

::

    pip install mop

You can also install the in-development version with::

    pip install https://github.com/robertfischer3/python-mop/archive/master.zip


Documentation
=============


https://python-mop.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
