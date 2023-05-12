django-libsass
==============

A django-compressor filter to compile Sass files using libsass.

Installation
~~~~~~~~~~~~

Starting from a Django project with `django-compressor <https://github.com/django-compressor/django-compressor/>`_ set up::

 pip install django-libsass

and add django_libsass.SassCompiler to your COMPRESS_PRECOMPILERS setting::

 COMPRESS_PRECOMPILERS = (
     ('text/x-scss', 'django_libsass.SassCompiler'),
 )

You can now use the content type text/x-scss on your stylesheets, and have them
compiled seamlessly into CSS::

 {% load compress %}

 {% compress css %}
     <link rel="stylesheet" type="text/x-scss" href="{% static "myapp/css/main.scss" %}" />
 {% endcompress %}


Imports
~~~~~~~

Relative paths in @import lines are followed as you would expect::

 @import "../variables.scss";

Additionally, Django's STATICFILES_FINDERS setting is consulted, and all possible locations
for static files *on the local filesystem* are included on the search path. This makes it
possible to import files across different apps::

 @import "myotherapp/css/widget.scss"


Settings
~~~~~~~~

The following settings can be used to control django-libsass's behaviour:

* ``LIBSASS_SOURCE_COMMENTS`` - whether to enable SASS source comments (adds comments about source lines). Defaults to ``True`` when Django's ``DEBUG`` is ``True``, ``False`` otherwise.
* ``LIBSASS_OUTPUT_STYLE`` - SASS output style. Options are ``'nested'``, ``'expanded'``, ``'compact'`` and ``'compressed'``, although as of libsass 3.0.2 only ``'nested'`` and ``'compressed'`` are implemented. Default is 'nested'. See `SASS documentation for output styles <http://sass-lang.com/documentation/file.SASS_REFERENCE.html#output_style>`_. Note that `django-compressor's settings <http://django-compressor.readthedocs.org/en/latest/settings/>`_ may also affect the formatting of the resulting CSS.
* ``LIBSASS_CUSTOM_FUNCTIONS`` - A mapping of custom functions to be made available within the SASS compiler. By default, a ``static`` function is provided, analogous to Django's ``static`` template tag.
* ``LIBSASS_SOURCEMAPS`` - Enable embedding sourcemaps into file output (default: False)
* ``LIBSASS_PRECISION`` - Number of digits of numerical precision (default: 5)
* ``LIBSASS_ADDITIONAL_INCLUDE_PATHS`` - a list of base paths to be recognised in @import lines, in addition to Django's recognised static file locations


Custom functions
~~~~~~~~~~~~~~~~

The SASS compiler can be extended with custom Python functions defined in the ``LIBSASS_CUSTOM_FUNCTIONS`` setting. By default, a ``static`` function is provided, for generating static paths to resources such as images and fonts::

    .foo {
        background: url(static("myapp/image/bar.png"));
    }

If your ``STATIC_URL`` is '/static/', this will be rendered as::

    .foo {
        background: url("/static/myapp/image/bar.png"));
    }

Why django-libsass?
~~~~~~~~~~~~~~~~~~~

We wanted to use Sass in a Django project without introducing any external (non pip-installable)
dependencies. (Actually, we wanted to use Less, but the same arguments apply...) There are a few
pure Python implementations of Sass and Less, but we found that they invariably didn't match the
behaviour of the reference compilers, either in their handling of @imports or lesser-used CSS
features such as media queries.

`libsass <https://sass-lang.com/libsass>`_ is a mature C/C++ port of the Sass engine, co-developed by the
original creator of Sass, and we can reasonably rely on it to stay in sync with the reference
Sass compiler - and, being C/C++, it's fast. Thanks to Hong Minhee's
`libsass-python <https://github.com/dahlia/libsass-python>`_ project, it has Python bindings and
installs straight from pip.

django-libsass builds on libsass-python to make @import paths aware of Django's staticfiles
mechanism, and provides a filter module for django-compressor which uses the libsass-python API
directly, avoiding the overheads of calling an external executable to do the compilation.


Reporting bugs
~~~~~~~~~~~~~~

Please see the `troubleshooting <https://github.com/torchbox/django-libsass/wiki/Troubleshooting>`_ page for help with some common setup issues.

I do not provide support for getting django-libsass working with your CSS framework of choice. If you believe you've found a bug, please try to isolate it as a minimal reproducible test case before reporting it - ideally this will consist of a few edits / additions to the `hello-django-libsass <https://github.com/gasman/hello-django-libsass>`_ example project. If you cannot demonstrate the problem in a few standalone SCSS files, it is almost certainly not a django-libsass bug - any bug reports that relate to a third-party CSS framework are likely to be closed without further investigation.


Author
~~~~~~

Matt Westcott matthew.westcott@torchbox.com
