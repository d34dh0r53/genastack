#!/usr/bin/env python
# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import pkgutil
import sys

import setuptools

import genastack
from genastack import roles

packages = [
    'genastack',
    'genastack.arguments',
    'genastack.common',
    'genastack.roles',
    'genastack.engine'
]
for mod, name, package in pkgutil.iter_modules(roles.__path__):
    packages.append('genastack.roles.%s' % name)

with open('requirements.txt') as f:
    required = f.read().splitlines()

if sys.version_info < (2, 6, 0):
    sys.stderr.write("Genastack Presently requires Python 2.6.0 or greater \n")
    raise SystemExit(
        '\nUpgrade python because you version of it is VERY deprecated\n'
    )
elif sys.version_info < (2, 7, 0):
    required.append('argparse')

with open('README', 'rb') as r_file:
    LDINFO = r_file.read()

setuptools.setup(
    name=genastack.__appname__,
    version=genastack.__version__,
    author=genastack.__author__,
    author_email=genastack.__email__,
    description=genastack.__description__,
    long_description=LDINFO,
    license='GNU General Public License v3 or later (GPLv3+)',
    packages=packages,
    url=genastack.__url__,
    install_requires=required,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ('License :: OSI Approved :: GNU General Public License v3 or later'
         ' (GPLv3+)'),
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        "console_scripts": ["genastack = genastack.run:executable"]
    }
)
