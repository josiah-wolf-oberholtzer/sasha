#!/usr/bin/env python

from distutils.core import setup


requires = [
    'abjad',
    'configobj',
    'matplotlib',
    'numpy',
    'pyramid',
    'pyramid_debugtoolbar',
    'pytest',
    'scikit-learn',
    'scikits.audiolab',
    'scipy',
    'sqlalchemy',
    'waitress',
    ]


def main():
    setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        entry_points='''\
            [paste.app_factory]
            main = sashaweb:main
            ''',
        include_package_data=True,
        install_requires=requires,
        name='sasha',
        packages=[
            'sasha',
            'sashaweb',
            ],
        test_suite='sashaweb',
        tests_require=requires,
        url='sasha.mbrsi.org',
        version='0.1',
        zip_safe=False,
        )


if __name__ == '__main__':
    main()