#!/usr/bin/env python

from setuptools import setup


requires = [
    'Beaker',
    'abjad',
    'configobj',
    'enum34',
    'matplotlib',
    'mongoengine',
    'numpy',
    'pyfftw',
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_mako',
    'pytest',
    'scikit-learn',
    'scikits.audiolab',
    'sqlalchemy',
    'waitress',
    'webhelpers',
    'WebTest',
    ]


def main():
    setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        entry_points='''\
            [paste.app_factory]
            main = sasha:main
            ''',
        install_requires=requires,
        name='sasha',
        packages=[
            'sasha',
            'sashamedia',
            ],
        tests_require=requires,
        test_suite='sasha.tests',
        url='sasha.mbrsi.org',
        version='0.1',
        zip_safe=False,
        )


if __name__ == '__main__':
    main()