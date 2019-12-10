#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='mop',
    use_scm_version={
        'local_scheme': 'dirty-tag',
        'write_to': 'src/mop/_version.py',
        'fallback_version': '0.0.1',
    },
    license='MIT',
    description='A Python library used to compile Azure resource compliance information',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Robert Fischer',
    author_email='robert@oakleyrain.com',
    url='https://github.com/robertfischer3/python-mop',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
        'Private :: Do Not Upload',
    ],
    project_urls={
        'Documentation': 'https://python-mop.readthedocs.io/',
        'Changelog': 'https://python-mop.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/robertfischer3/python-mop/issues',
    },
    keywords=['Azure', 'policyinsights', 'policy', 'security'
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.7.*',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        "setuptools_scm>=3.3.1",
        "pytest",
        "pytest-cov",
        "coverage",
        "atomicwrites",
        "python-dotenv",
        "docutils",
        "azure",
        "pandas"
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'setuptools_scm>=3.3.1', "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'mop = mop.cli:main',
        ]
    },
)
