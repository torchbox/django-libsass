#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-libsass',
    version='0.2',
    description="A django-compressor filter to compile SASS files using libsass",
    author='Matt Westcott',
    author_email='matthew.westcott@torchbox.com',
    url='https://github.com/torchbox/django-libsass',
    py_modules=['django_libsass'],
    license='BSD',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    install_requires=[
        "django-compressor>=1.3",
        "libsass>=0.3.0",
    ],
)
