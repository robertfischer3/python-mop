.. image:: https://publicdomainvectors.org/photos/secchio-e-spugna-archite-01.png
    :width: 150px
    :align: left
    :height: 150px
    :alt: alternate text

=======================
The Mop Project (alpha)
=======================

Welcome to Mop project!

|Test results|![Private Network Testing](https://img.shields.io/badge/tests-current%20tests-yellow)  [Private Test Server Results](https://github.com/robertfischer3/python-mop/blob/master/testingresults/test-16-dec-2019.html)|
|Commits per week|![Commits](https://img.shields.io/github/commit-activity/w/robertfischer3/python-mop)|

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


Test Coverage
=============

This project currently calls directly against Azure services.  While Azure never charges for ingress traffic, outbound
traffic is charged.  Further the test results below has executed against a very large dataset.

The test dataset included over 490 Azure production subscriptions. This framework mines security information.  Hence hosting
this testing on Travis or others.  To protect the test data owners, the testing could only occur on private networks.  Given
this product is alpha, there are still some bug fixes to be aware of.  The latest build and test result will
be posted here going forward

::
----------- coverage: platform linux, python 3.7.3-final-0 -----------
Name                                                 Stmts   Miss Branch BrPart     Cover   Missing
---------------------------------------------------------------------------------------------------
src/mop/__init__.py                                      1      0      0      0   100.00%
src/mop/__main__.py                                      3      1      2      1    60.00%   13->14, 14
src/mop/aws/__init__.py                                  0      0      0      0   100.00%
src/mop/azure/__init__.py                                0      0      0      0   100.00%
src/mop/azure/analysis/__init__.py                       0      0      0      0   100.00%
src/mop/azure/analysis/compile_compliance.py            60     49     24      0    13.10%   14-41, 44-93
src/mop/azure/analysis/policy_analysis.py               65      8     12      1    83.12%   41-57, 104->109
src/mop/azure/connections.py                            72     26      4      1    61.84%   31-33, 40->exit, 55, 105-119, 125-143
src/mop/azure/operations/__init__.py                     0      0      0      0   100.00%
src/mop/azure/operations/policy_definitions.py          34     13      4      0    60.53%   17-20, 33-36, 46-50, 64-82
src/mop/azure/operations/policy_insights.py             43     11      6      0    73.47%   33-36, 67-77, 85-104
src/mop/azure/operations/policy_states.py               73     46      0      0    36.99%   41-46, 55-60, 71-78, 86-91, 103-115, 118-124, 132-138, 147-152, 164-179
src/mop/azure/operations/policy_states_resource.py      16      9      0      0    43.75%   15-18, 26-31
src/mop/azure/resources/__init__.py                      0      0      0      0   100.00%
src/mop/azure/resources/subscriptions.py                58     27     16      0    47.30%   27-36, 58-62, 113-168
src/mop/azure/resources/vm.py                            0      0      0      0   100.00%
src/mop/azure/resources/vnets.py                        31     14      0      0    54.84%   24-28, 31-36, 39-46
src/mop/azure/tests/__init__.py                          0      0      0      0   100.00%
src/mop/azure/tests/test_policy_analysis.py             21      3      0      0    85.71%   27-29
src/mop/azure/tests/test_policy_states.py               74     32      6      1    53.75%   31-42, 50-79, 112->113, 113
src/mop/azure/tests/test_subscriptions.py               24      0      2      0   100.00%
src/mop/azure/tests/test_utils.py                       49      5      4      1    84.91%   53, 77-80, 90->91, 91
src/mop/azure/tests/test_utils_db.py                    54      1      2      1    96.43%   127->128, 128
src/mop/azure/tests/test_vnets.py                       22      3      0      0    86.36%   28-31
src/mop/azure/utils/__init__.py                          0      0      0      0   100.00%
src/mop/azure/utils/atomic_writes.py                    31      7      8      3    74.36%   16-18, 36->37, 37-39, 45->48, 48, 52->58
src/mop/azure/utils/create_configuration.py             27      4      4      1    77.42%   59-61, 64->65, 65
src/mop/azure/utils/create_sqldb.py                     33      0      0      0   100.00%
src/mop/azure/utils/manager.py                          15     11      2      1    29.41%   8-27, 30->31, 31
src/mop/cli.py                                           7      0      0      0   100.00%
src/mop/db/__init__.py                                   0      0      0      0   100.00%
src/mop/db/basedb.py                                    25      0      0      0   100.00%
src/mop/framework/__init__.py                            0      0      0      0   100.00%
src/mop/framework/parameters.py                          0      0      0      0   100.00%
---------------------------------------------------------------------------------------------------
TOTAL                                                  838    270     96     11    64.13%

=================================================================================================================== short test summary info ===================================================================================================================
FAILED src/mop/azure/tests/test_policy_analysis.py::TestAnalysisCompileCompliance::test_summarize_subscriptions - KeyError: 'subscription_id'
FAILED src/mop/azure/tests/test_policy_states.py::TestOperationsPolicyStates::test_policy_states_summarize_for_subscription - KeyError: 'subscription_id'
FAILED src/mop/azure/tests/test_utils.py::TestCaseUtils::test_directory_context_manager - UnboundLocalError: local variable 'tmp' referenced before assignment
FAILED src/mop/azure/tests/test_utils.py::TestConfigParser::test_create_config_file_sections - UnboundLocalError: local variable 'tmp' referenced before assignment
FAILED src/mop/azure/tests/test_utils.py::TestConfigParser::test_read_testvariables_ini - KeyError: 'subscription_id'
FAILED src/mop/azure/tests/test_vnets.py::TestVNetInformation::test_VNetAPIs - KeyError: 'subscription_id'
========================================================================================================== 6 failed, 10 passed in 667.35s (0:11:07) ===========================================================================================================
(python3) robert@ubuntu:~/python3$


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
