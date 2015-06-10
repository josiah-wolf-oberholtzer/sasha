#!/usr/bin/env python

from setuptools import setup


requires = [
    'abjad',
    'configobj',
    'matplotlib',
    'numpy',
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_mako',
    'pytest',
    'scikit-learn',
    'scikits.audiolab',
    'sqlalchemy',
    'waitress',
    'webhelpers',
    ]


def main():
    setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        entry_points='''\
            [paste.app_factory]
            main = sashaweb:main
            ''',
        install_requires=requires,
        name='sashaweb',
        packages=[
            'sasha',
            'sashaweb',
            ],
        url='sasha.mbrsi.org',
        version='0.1',
        zip_safe=False,
        )


if __name__ == '__main__':
    main()