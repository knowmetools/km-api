#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Know Me API documentation build configuration file, created by
# sphinx-quickstart on Thu Jul  6 11:04:47 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

from __future__ import print_function

import os
import re
import shutil
import sys

import django

sys.path.insert(0, os.path.abspath('../km_api'))

# Set Django settings so we can use autodoc.
os.environ['DJANGO_SETTINGS_MODULE'] = 'km_api.test_settings'
django.setup()


# Paths relative to the directory this file is in should be built with
# os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_issues',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain',
    'sphinxcontrib.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Know Me API'
copyright = '2017, Chathan Driehuys'
author = 'Chathan Driehuys'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.2.0'
# The full version, including alpha/beta/rc tags.
release = '0.2.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# If the site is being published by readthedocs, we want to use their
# default theme. Otherwise we're in a dev environment and want to
# specify the readthedocs theme.
if os.environ.get('READTHEDOCS') == 'True':
    html_theme = 'default'
else:
    html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'KnowMeAPIdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'KnowMeAPI.tex', 'Know Me API Documentation',
     'Chathan Driehuys', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'knowmeapi', 'Know Me API Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'KnowMeAPI', 'Know Me API Documentation',
     author, 'KnowMeAPI', 'One line description of project.',
     'Miscellaneous'),
]


# apidoc settings

APIDOC_EXCLUDE_PATTERNS = (
    '*/conftest.py',
    'km_api/*/admin.py',
    'km_api/*/apps.py',
    'km_api/*/factories.py',
    'km_api/*/urls.py',
    'km_api/*/migrations/',
    'km_api/*/tests/',
    'km_api/km_api/',
)
APIDOC_OUTPUT = os.path.join(BASE_DIR, '_internal-api')


# Issues Configuration

issues_github_path = 'knowmetools/km-api'


def run_apidoc(*args):
    """
    Autogenerate internal API docs.

    References:
        https://github.com/rtfd/readthedocs.org/issues/1139

    Args:
        args:
            Swallow all given arguments and ignore them.
    """
    if os.path.isdir(APIDOC_OUTPUT):
        print("Found existing autogenerated API docs. Removing them...")

        # Wipe out existing autogenerated docs
        shutil.rmtree(APIDOC_OUTPUT)

    # Autogenerate the documentation
    from sphinx import apidoc

    cur_dir = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(cur_dir, '..', 'km_api')

    apidoc_args = ['--force', '-o', APIDOC_OUTPUT, module]

    project_root = os.path.dirname(BASE_DIR)
    full_exclude_paths = []
    for pattern in APIDOC_EXCLUDE_PATTERNS:
        full_exclude_paths.append(os.path.join(project_root, pattern))

    apidoc_args.extend(full_exclude_paths)

    print('Running sphinx-apidoc', ' '.join(apidoc_args))

    apidoc.main(apidoc_args)

    # Then we patch the generated index file to allow for a nested
    # output.
    module_list_path = os.path.join(APIDOC_OUTPUT, 'modules.rst')

    assert os.path.isfile(module_list_path), 'Failed to find module list.'

    with open(module_list_path) as f:
        content = f.read()

    r = re.compile(r'^   ([^:\n]+)$', re.MULTILINE)
    content = r.sub(r'   _internal-api/\1', content)

    with open(module_list_path, 'w') as f:
        f.write(content)

    print('Wrote new modules.rst')


def setup(app):
    """
    Connect custom build steps to the build process.

    Args:
        app:
            The app being built.
    """
    app.connect('builder-inited', run_apidoc)
