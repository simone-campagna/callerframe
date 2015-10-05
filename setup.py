# -*- coding: utf-8 -*-
#
# Copyright 2013 Simone Campagna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = "Simone Campagna"

from setuptools import setup
#from setuptools.command.test import test as TestCommand

import glob
import os
import sys


if __name__ == "__main__":
    DIRNAME = os.path.abspath(os.path.dirname(__file__))
    if DIRNAME:
        os.chdir(DIRNAME)
    try:
        py_dirname = DIRNAME
        sys.path.insert(0, py_dirname)
    
        import callerframe
        version = callerframe.__version__
    finally:
        del sys.path[0]
    
    def read_requirements(*filenames):
        requirements = []
        for filename in filenames:
            fpath = os.path.join(os.getcwd(), 'requirements', filename + '.txt')
            with open(fpath, "r") as f_in:
                for line in f_in:
                    requirement = line.strip()
                    if not requirement in requirements:
                        requirements.append(requirement)
        return requirements
    
    # search executables
    scripts = []
    for filepath in glob.glob('bin/*'):
        if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
            scripts.append(filepath)
    
    # search packages
    root_packages = []
    packages = []
    for package in root_packages:
        package_dirname = os.path.join(DIRNAME, package)
        for dirpath, dirnames, filenames in os.walk(package_dirname):
            if '__init__.py' in filenames:
                rdirpath = os.path.relpath(dirpath, DIRNAME)
                packages.append(os.path.normpath(rdirpath).replace(os.sep, '.'))
    
#    # search requirement files
#    data_files = []
#    for data_dirname, patterns in [('requirements', ('*.txt', )),
#                                   ('docs/source', ('conf.py', '*.rst')),
#                                   ('docs/source/examples', ('*.rst',)),
#                                   ('docs/source/img', ('*.png',)),
#                                   ('.', ('tox.ini', 'pylint.ini', 'flake8.ini',)),
#                                  ]:
#        files = []
#        for pattern in patterns:
#            for fpath in glob.glob(os.path.join(DIRNAME, data_dirname, pattern)):
#                files.append(os.path.relpath(fpath, DIRNAME))
#        data_files.append((data_dirname, files))
    
    setup(
        name="callerframe",
        version=version,
        requires=[],
        description="Python library for configuration data",
        author="Simone Campagna",
        author_email="simone.campagna11@gmail.com",
        install_requires=read_requirements('install'),
        package_data={},
        #data_files=data_files,
        url="https://github.com/simone-campagna/callerframe",
        download_url = 'https://github.com/simone-campagna/callerframe/archive/{}.tar.gz'.format(version),
        packages=packages,
        scripts=scripts,
        py_modules=['callerframe'],
        classifiers=[
            # status:
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            # audience:
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            # license:
            'License :: OSI Approved :: Apple Public Source License',
            # language:
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 2.7',
        ],
        keywords='decorator caller frame',
    )

