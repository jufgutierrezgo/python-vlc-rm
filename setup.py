#!/usr/bin/env python
# -*- encoding: utf-8 -*-

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
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


setup(
    name='vlc-rm',
    use_scm_version={
        'local_scheme': 'dirty-tag',
        'write_to': 'src/vlc_rm/_version.py',
        'fallback_version': '1.3.1',
    },
    license='BSD-3-Clause',
    description='The package implements a recursive model to simulate a VLC system inside of rectangular empty room.',
    long_description='{}\n{}'.format(
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst')),
    ),
    author='Juan F. Gutierrez',
    author_email='jufgutierrezgo@unal.edu.co',
    url='https://github.com/jufgutierrezgo/python-vlc-rm',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://python-vlc-rm.readthedocs.io/',
        'Changelog': 'https://python-vlc-rm.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/jufgutierrezgo/python-vlc-rm/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.10',
    install_requires=[
        'numpy>=2.0.0',
        'luxpy>=1.9.8',
        'scipy>=1.9.3',        
        'matplotlib>=3.1.2',  
        'pytest>=8.0.0',  
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'pytest-runner',
        'setuptools_scm>=3.3.1',
    ],
    entry_points={
        'console_scripts': [
            'vlc-rm-cli = vlc_rm.cli:main',
        ]
    },
)
