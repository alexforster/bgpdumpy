# -*- coding: utf-8 -*-
########################################################################################################################
# Copyright © 2019 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.
########################################################################################################################

import os
from subprocess import check_call

from setuptools import setup
from setuptools.command.install_lib import install_lib as install_lib

PACKAGE_NAME = 'bgpdumpy'
PACKAGE_VERSION = '1.1.4'


class custom_install_lib(install_lib):

    def run(self):
        install_lib.run(self)

        cwd = os.path.join(os.getcwd(), self.install_dir)
        cwd = os.path.join(cwd, PACKAGE_NAME)

        print('Running mkdeps in ' + cwd)

        check_call([os.path.join(cwd, 'mkdeps')], cwd=cwd)
        check_call([os.path.join(cwd, 'mkdeps'), 'clean'], cwd=cwd)


with open('README.md', 'r') as fd:
    long_description = fd.read()


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author='Alex Forster',
    author_email='alex@alexforster.com',
    maintainer='Alex Forster',
    maintainer_email='alex@alexforster.com',
    url='https://github.com/AlexForster/bgpdumpy',
    description='A libbgpdump Python CFFI wrapper for analyzing MRTv1 and MRTv2 BGP table dump files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='3-Clause ("New") BSD license',
    download_url='https://pypi.python.org/pypi/bgpdumpy',
    zip_safe=False,
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: '.'},
    package_data={PACKAGE_NAME: [
        'mkdeps',
        'deps/*.gz',
        'README*',
        'LICENSE',
        'requirements.txt',
    ]},
    install_requires=[
        'cffi',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    cmdclass={
        'install_lib': custom_install_lib,
    },
)
