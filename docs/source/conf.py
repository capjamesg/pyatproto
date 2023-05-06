# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

project = "pyatproto"
copyright = "2023, capjamesg"
author = "capjamesg"
release = "0.1.0"
version = "0.1.0"

sys.path.insert(0, os.path.abspath("../../src/"))
print(sys.path)

# -- General configuration

extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

# -- Options for EPUB output
epub_show_urls = "footnote"

html_static_path = ["_static"]
