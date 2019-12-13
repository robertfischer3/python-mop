.. image:: https://publicdomainvectors.org/photos/secchio-e-spugna-archite-01.png
    :width: 150px
    :align: left
    :height: 150px
    :alt: alternate text

=======================
The Mop Project (alpha)
=======================
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

Welcome to Mop project!

Why Mop? You need mop to clean up your cloud mess!

Organizations large and small love the agility of the cloud.  Most embrace the cloud for the ability to create compute
assets quickly. However, that creation process is usually weak in applying standards and compliance.  Let us face it cloud
governance is hard

The Mop project seeks to build cloud comprehensions to feed machine learning.  This open source project is in the nascent
stages. Currently the project framework in directed to adopting the framework controls found in the
three major cloud providers: Azure, AWS, and Google Cloud.

Why three public clouds? Why not focus on just one? Mop seek to foster the understand of utility computing by eventualing
employing artificial intelligence to the comprehensions obtained by the framework

Mop is open source Python project used to compile Public Cloud resource compliance information.  This project is in the
early stages of development focus first on Azure.

Project Stages:
-Create a compliance reporting framework

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
