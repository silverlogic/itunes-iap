from __future__ import with_statement

from setuptools import setup


def get_version():
    with open('itunesiap/version.txt') as f:
        return f.read().strip()


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''


setup(
    name='tsl-itunes-iap',
    version=get_version(),
    description='Itunes In-app purchase verification api.',
    long_description=get_readme(),
    author='Ryan Pineo',
    author_email='ry@tsl.io',
    url='https://github.com/silverlogic/itunes-iap',
    packages=(
        'itunesiap',
    ),
    package_data={
        'itunesiap': ['version.txt']
    },
    install_requires=[
        'requests', 'tsl-prettyexc>=0.5.2', 'six'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
     ],
)

