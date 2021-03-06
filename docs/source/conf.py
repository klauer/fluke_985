# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import sphinx_rtd_theme

module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '../../')
sys.path.insert(0, module_path)

# -- Project information -----------------------------------------------------

project = 'fluke_985'
author = 'SLAC National Accelerator Laboratory'

from datetime import datetime

year = datetime.now().year
copyright = str(year) + ', SLAC National Accelerator Laboratory'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'numpydoc',
    'recommonmark',
    'doctr_versions_menu',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

autosummary_generate = True


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
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
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'cookiecutterproject_namedoc'


# -- Options for LaTeX output ------------------------------------------------

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
    (master_doc, 'fluke_985.tex', 'fluke_985 Documentation',
     'SLAC National Accelerator Laboratory', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'fluke_985', 'fluke_985 Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'fluke_985', 'fluke_985 Documentation',
     author, 'fluke_985', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


import re

from docutils import nodes, statemachine
from docutils.parsers.rst import Directive, directives
from sphinx.ext.autosummary import Autosummary, get_documenter
from sphinx.util.inspect import safe_getattr

html_context = {
    'css_files': [
        '_static/theme_overrides.css',  # override wide tables in RTD theme
    ],
}


class PVGroupSummary(Directive):
    required_arguments = 1
    """Number of required directive arguments."""

    optional_arguments = 0
    """Number of optional arguments after the required arguments."""

    final_argument_whitespace = False
    """May the final argument contain whitespace?"""

    option_spec = None
    """Mapping of option names to validator functions."""

    has_content = False
    """May the directive have content?"""

    option_spec = dict(
        methods=directives.unchanged,
        attributes=directives.unchanged
    )

    def _document_pv_properties(self, cls):
        table = []

        def add_row(*items):
            items = iter(items)
            table.append(f'* - {next(items)}')
            for item in items:
                table.append(f'  - {item}')

        add_row(
            'Attribute',
            'Information',
            'PV',
            'Value',
            'Notes',
            'Alarm Group',
        )

        for attr, prop in sorted(cls._pvs_.items()):
            pvspec = prop.pvspec
            if hasattr(pvspec.dtype, '__name__'):
                data_type = pvspec.dtype.__name__
            else:
                data_type = pvspec.dtype

            if pvspec.max_length:
                data_type = f'{data_type}[{pvspec.max_length}]'

            notes = ', '.join(
                item for item in (
                    (pvspec.get and 'getter') or '',
                    (pvspec.put and 'putter') or '',
                    (pvspec.startup and 'startup') or '',
                    (pvspec.shutdown and 'shutdown') or '',
                    (pvspec.read_only and 'read-only') or '',
                )
                if item
            )

            if prop.record_type:
                pvname = f'{pvspec.name} ({prop.record_type})'
            else:
                pvname = pvspec.name

            add_row(
                attr,
                pvspec.doc or '',
                pvname,
                f'{data_type} = {pvspec.value}' if pvspec.value else data_type,
                notes,
                pvspec.alarm_group or '',
            )

        table = directives.tables.ListTable(
            name=cls.__name__,
            arguments=[f'{cls.__name__} pvproperty summary'],
            options={
                'header-rows': 1,
                'stub-columns': 0,
                # 'width': directives.length_or_percentage_or_unitless,
                'widths': 'auto',
                # 'class': directives.class_option,
                # 'name': directives.unchanged,
                'align': 'left',
            },
            content=statemachine.StringList(statemachine.StringList(table)),
            lineno=self.lineno,
            content_offset=self.content_offset,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        )
        return table.run()

    def run(self):
        class_name = self.arguments[0]
        module_name, class_name = class_name.rsplit('.', 1)
        module = __import__(module_name, globals(), locals(), [class_name])
        cls = getattr(module, class_name)
        assert hasattr(cls, '_pvs_'), 'Not a PVGroup'
        return self._document_pv_properties(cls)


def skip_pvproperties(app, what, name, obj, skip, options):
    return skip or type(obj).__name__ == 'pvproperty'


def setup(app):
    app.add_directive('pvgroup', PVGroupSummary)
    app.connect('autodoc-skip-member', skip_pvproperties)
