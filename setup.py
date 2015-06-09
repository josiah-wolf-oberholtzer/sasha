#!/usr/bin/env python

from distutils.core import setup


def main():
    setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        name='sasha',
        version='0.1',
        install_requires=[
            'abjad',
            'configobj',
            'matplotlib',
            'numpy',
            'pytest',
            'scikit-learn',
            'scikits.audiolab',
            'scipy',
            'sqlalchemy',
            ],
        packages=[
            'sasha',
            ],
        )

if __name__ == '__main__':
    main()