.. image:: mop.png
    :width: 150px
    :align: left
    :height: 150px
    :alt: alternate text

=======================
The Mop Project (alpha)
=======================

Welcome to Mop project!

.. image:: https://img.shields.io/badge/tests-current%20tests-yellow
https://github.com/robertfischer3/python-mop/blob/master/testingresults/test-16-dec-2019.html


https://img.shields.io/github/commit-activity/w/robertfischer3/python-mop
https://github.com/robertfischer3/python-mop/pulse


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
================
-Create a compliance reporting framework (in progress)

-Develop analysis layer to aggregate data (in progress)

-Apply machine learning to develop idea configuration models


License
========
* Free software: MIT license

Installation
============

::

    pip install mop

You can also install the in-development version with::

    pip install https://github.com/robertfischer3/python-mop/archive/master.zip


Database
=============
This framework does not require the use of a database.  However, there are analysis code
blocks that make use of a database.  For this version, the framework makes use of a SQL Server
2019 for Linux docker image.  Microsoft provides a easy set up here:

Quickstart: Run SQL Server container images with Docker
https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash#docker-demo

Framework Features
==================

Nanscent pluggable architectures using Pluggy

.. image:: https://pluggy.readthedocs.io/en/latest/_static/img/plug.png
    :width: 150px
    :align: left
    :height: 150px
    :alt: alternate text

Easy data storage and analysis using databases and Alchemy ORM

.. image:: https://www.sqlalchemy.org/img/sqla_logo.png
    :width: 150px
    :align: left
    :height: 25px
    :alt: alternate text


Test Coverage
=============

This project currently calls directly against Azure services.  While Azure never charges for ingress traffic, outbound
traffic is charged.  Further the test results below has executed against a very large dataset.

The test dataset included over 490 Azure production subscriptions. This framework mines security information.  Hence hosting
this testing on Travis or others.  To protect the test data owners, the testing could only occur on private networks.  Given
this product is alpha, there are still some bug fixes to be aware of.  The latest build and test result will
be posted here going forward:

https://github.com/robertfischer3/python-mop/blob/master/testingresults/test-16-dec-2019.html

Documentation
=============

Documentation is forthcoming...

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
