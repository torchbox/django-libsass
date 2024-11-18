#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-libsass',
    version='0.9',
    description="A django-compressor filter to compile SASS files using libsass",
    author='Matt Westcott',
    author_email='matthew.westcott@torchbox.com',
    url='https://github.com/torchbox/django-libsass',
    py_modules=['django_libsass'],
    license='BSD',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
    ],
    python_requires='>=3.9',
    install_requires=[
        "django-compressor>=1.3",
        "libsass>=0.7.0,<1",
    ],
)
