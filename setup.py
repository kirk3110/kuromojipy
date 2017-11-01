# -*- coding: utf-8 -*-

import os.path
import codecs
from setuptools import setup
from setuptools import find_packages


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name='kuromojipy',
        version='0.0.1-alpha',
        author='kirk3110',
        author_email='kirk3110@gmail.com',
        url='https://github.com/kirk3110/kuromojipy',
        description='A python I/F for kuromoji (powered by Py4J).',
        long_description=long_description,
        license='AL2',
        zip_safe=False,
        include_package_data=True,
        packages=['kuromojipy'],
        install_requires=['py4j'],
    )


if __name__ == '__main__':
    main()