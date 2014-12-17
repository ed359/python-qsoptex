#!/usr/bin/env python

import sys, os
from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    HAVE_CYTHON = False

# Determine usage of Cython
USE_CYTHON = HAVE_CYTHON
if 'USE_CYTHON' in os.environ:
    USE_CYTHON = os.environ['USE_CYTHON'].lower() in ('1', 'yes')

if USE_CYTHON and not HAVE_CYTHON:
    sys.stderr.write('Cython was not found!\n')
    sys.exit(-1)

# Add include dirs specified by environment variables
include_dirs = []
if 'GMP_INCLUDE_DIR' in os.environ:
    include_dirs.append(os.environ['GMP_INCLUDE_DIR'])
if 'QSOPTEX_INCLUDE_DIR' in os.environ:
    include_dirs.append(os.environ['QSOPTEX_INCLUDE_DIR'])

# Add library dirs specified by environment variables
library_dirs = []
if 'GMP_LIBRARY_DIR' in os.environ:
    library_dirs.append(os.environ['GMP_LIBRARY_DIR'])
if 'QSOPTEX_LIBRARY_DIR' in os.environ:
    library_dirs.append(os.environ['QSOPTEX_LIBRARY_DIR'])

ext = '.pyx' if USE_CYTHON else '.c'
extensions = [Extension('qsoptex', ['qsoptex'+ext],
                include_dirs=include_dirs,
                libraries=['gmp', 'qsopt_ex'],
                library_dirs=library_dirs)]

if USE_CYTHON:
    extensions = cythonize(extensions, include_path=include_dirs)

# Read long description
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='python-qsoptex',
    version='0.1',
    license='GPLv3+',
    url='https://github.com/jonls/qsopt-ex',
    author='Jon Lund Steffensen',
    author_email='jonlst@gmail.com',

    description='Python bindings for QSopt_ex, an exact linear programming solver',
    long_description=long_description,

    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Cython',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Scientific/Engineering :: Mathematics'],

    ext_modules = extensions
)
