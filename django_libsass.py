import base64
import json
import re
import os
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static as django_static

import sass
from compressor.filters.base import FilterBase


def static(path):
    """
    Use the Django builtin static file resolver to return an absolute path
    usable as CSS url() argument. Sass equivalent of the 'static' template
    tag.
    """
    return '"{}"'.format(django_static(path))


OUTPUT_STYLE = getattr(settings, 'LIBSASS_OUTPUT_STYLE', 'nested')
SOURCE_COMMENTS = getattr(settings, 'LIBSASS_SOURCE_COMMENTS', settings.DEBUG)
CUSTOM_FUNCTIONS = getattr(settings, 'LIBSASS_CUSTOM_FUNCTIONS', {'static': static})
SOURCEMAPS = getattr(settings, 'LIBSASS_SOURCEMAPS', False)
SOURCEMAP_PREFIX = getattr(settings, 'LIBSASS_SOURCEMAP_PREFIX', None)

if SOURCEMAPS and SOURCEMAP_PREFIX is None:
    raise ImproperlyConfigured('LIBSASS_SOURCEMAP_PREFIX must be set when'
                               ' LIBSASS_SOURCEMAPS = True')


def get_include_paths():
    """
    Generate a list of include paths that libsass should use to find files
    mentioned in @import lines.
    """
    include_paths = []

    # Look for staticfile finders that define 'storages'
    for finder in get_finders():
        try:
            storages = finder.storages
        except AttributeError:
            continue

        for storage in storages.values():
            try:
                include_paths.append(storage.path('.'))
            except NotImplementedError:
                # storages that do not implement 'path' do not store files locally,
                # and thus cannot provide an include path
                pass

    return include_paths


INCLUDE_PATHS = None  # populate this on first call to 'compile'


def prefix_sourcemap(sourcemap, prefix):
    decoded_sourcemap = json.loads(sourcemap)
    sources = ['/'.join([prefix, source])
               for source in decoded_sourcemap['sources']]

    decoded_sourcemap['sources'] = sources
    return json.dumps(decoded_sourcemap)


def embed_sourcemap(output, sourcemap):
    encoded_sourcemap = base64.standard_b64encode(
        sourcemap.encode('utf-8')
    )
    sourcemap_fragment = 'sourceMappingURL=data:application/json;base64,{} '\
        .format(encoded_sourcemap.decode('utf-8'))
    url_re = re.compile(r'sourceMappingURL=[^\s]+', re.M)
    output = url_re.sub(sourcemap_fragment, output)

    return output


def compile(**kwargs):
    """Perform sass.compile, but with the appropriate include_paths for Django added"""
    global INCLUDE_PATHS
    if INCLUDE_PATHS is None:
        INCLUDE_PATHS = get_include_paths()

    kwargs = kwargs.copy()
    kwargs['include_paths'] = (kwargs.get('include_paths') or []) + INCLUDE_PATHS

    custom_functions = CUSTOM_FUNCTIONS.copy()
    custom_functions.update(kwargs.get('custom_functions', {}))
    kwargs['custom_functions'] = custom_functions

    if SOURCEMAPS and kwargs.get('filename', None):
        # We need to pass source_map_file to libsass so it generates
        # correct paths to source files.
        prefix = os.path.dirname(kwargs['filename'])
        sourcemap_filename = os.path.join(prefix, 'sourcemap.map')
        kwargs['source_map_filename'] = sourcemap_filename

        libsass_output, sourcemap = sass.compile(**kwargs)
        # Prefix sourcemap output with SOURCEMAP_PREFIX, which
        # will be something like STATIC_URL/scss
        sourcemap = prefix_sourcemap(sourcemap, SOURCEMAP_PREFIX)
        output = embed_sourcemap(libsass_output, sourcemap)
    else:
        output = sass.compile(**kwargs)
    return output


class SassCompiler(FilterBase):
    def __init__(self, content, attrs=None, filter_type=None, charset=None, filename=None):
        # FilterBase doesn't handle being passed attrs, so fiddle the signature
        super(SassCompiler, self).__init__(content, filter_type, filename)

    def input(self, **kwargs):
        if self.filename:
            return compile(filename=self.filename,
                           output_style=OUTPUT_STYLE,
                           source_comments=SOURCE_COMMENTS)
        else:
            return compile(string=self.content,
                           output_style=OUTPUT_STYLE)
