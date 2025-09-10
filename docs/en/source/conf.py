import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'XLeRobot'
copyright = "2025, XLeRobot Contributors"
author = 'Vector & Nicole'
release = '0.3.0'

import importlib.util
import logging
logger = logging.getLogger(__name__)


def skip_mani_skill(app):
    if importlib.util.find_spec("mani_skill") is None:
        app.logger.warning("mani_skill not installed, skipping related docs")
        # You could use logic to dynamically skip files here

def skip_unresolvable(app):
    try:
        import mani_skill
    except ImportError:
        logging.warning("mani_skill not installed — skipping API imports.")
    try:
        import sapien
    except ImportError:
        logging.warning("sapien not installed — skipping API imports.")

# def setup(app):
#     app.connect("builder-inited", skip_mani_skill)
#     app.connect("builder-inited", skip_unresolvable)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx_subfigure",
    "sphinxcontrib.video",
    "sphinx_togglebutton",
    "sphinx_design"
]

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = ["colon_fence", "dollarmath"]
# https://github.com/executablebooks/MyST-Parser/issues/519#issuecomment-1037239655
myst_heading_anchors = 4

templates_path = ["_templates"]
# exclude_patterns = ["Hardware/reference/_autosummary/*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_logo = "_static/logo_black.png"
html_favicon = "_static/favicon.svg"


# json_url = "https://maniskill.readthedocs.io/en/latest/_static/version_switcher.json"
json_url = "_static/version_switcher.json"
version_match = os.environ.get("READTHEDOCS_VERSION")
# if version_match is None:
#     version_match = "v" + __version__
# html_sidebars = {
#   "**": []
# }
html_theme_options = {
    # "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Vector-Wangel/XLeRobot",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Website", 
            "url": "https://twitter.com/VectorWang2",
            "icon": "fa-solid fa-globe",
        },
        {
            "name": "Language",
            "icon": "fa-solid fa-language",
            "type": "dropdown",  # Changed from "custom" to "dropdown"
            "items": [
                {
                    "name": "English",
                    "url": "index.html",  # Changed from "#"
                },
                {
                    "name": "中文",
                    "url": "README_CN.html",  # Changed from "#"
                }
            ]
        }
    ],
    # "external_links": [
    #     {"name": "Latest Updates", "url": "https://twitter.com/VectorWang2"},
    # ],
    "logo": {
        "image_dark": "_static/logo_white.png",
    },
    # "navbar_center": ["version-switcher", "navbar-nav"],
    "show_version_switcher": False,
    "show_version_warning_banner": False,
    # "switcher": {
    #     "json_url": json_url,
    #     "version_match": version_match,
    # },
}
html_context = {
    "display_github": True,
    "github_user": "haosulab",
    "github_repo": "ManiSkill",
    "github_version": "main",
    "conf_py_path": "/source/",
    "doc_path": "docs/source"
}
html_css_files = [
    'css/custom.css',
]
html_static_path = ['_static']
html_js_files = ['js/lang-switch.js']

### Autodoc configurations ###
autodoc_typehints = "signature"
autodoc_typehints_description_target = "all"
autodoc_default_flags = ['members', 'show-inheritance', 'undoc-members']

autosummary_generate = True

# remove_from_toctrees = ["_autosummary/*"]

intersphinx_mapping = {'gymnasium': ('https://gymnasium.farama.org/', None)}
