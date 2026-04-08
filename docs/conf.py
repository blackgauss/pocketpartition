# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Make the src layout visible to autodoc regardless of the CWD when Sphinx runs.
# Resolving relative to __file__ keeps this correct in CI and from the repo root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# -- Project information -----------------------------------------------------

project = 'pocketpartition'
copyright = '2024, Erik Imathiu-Jones'
author = 'Erik Imathiu-Jones'
release = '1.1.3-alpha'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',        # pull docstrings from source
    'sphinx.ext.napoleon',       # NumPy / Google style docstrings
    'sphinx.ext.viewcode',       # [source] links next to each item
    'sphinx.ext.intersphinx',    # cross-links to Python standard library
    'sphinx_autodoc_typehints',  # render PEP 484 type hints as descriptions
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# autodoc settings
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

# napoleon settings
napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_use_param = False      # param/type already handled by typehints ext
napoleon_use_rtype = False

# intersphinx: link to Python built-in types
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = []   # no custom static assets yet
html_title = 'pocketpartition'
