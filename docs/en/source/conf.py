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
# Pages without child pages would otherwise show an empty "Section Navigation" sidebar.
html_sidebars = {
    "demos/index": [],
    "relatedworks/index": [],
}
html_theme_options = {
    # "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Vector-Wangel/XLeRobot",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "X (Twitter)",
            "url": "https://twitter.com/VectorWang2",
            "icon": "fa-brands fa-x-twitter",
        },
        # Language switching is handled by the Read the Docs flyout menu.
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
    "github_user": "Vector-Wangel",
    "github_repo": "XLeRobot",
    "github_version": "main",
    "doc_path": "docs/en/source",
}
html_css_files = [
    'css/custom.css',
    'css/community-usecases.css',
]
html_static_path = ['_static', '../../community_usecases/static']
html_js_files = ['js/lang-switch.js', 'js/community-usecases.js']

### Autodoc configurations ###
autodoc_typehints = "signature"
autodoc_typehints_description_target = "all"
autodoc_default_flags = ['members', 'show-inheritance', 'undoc-members']

autosummary_generate = True

# remove_from_toctrees = ["_autosummary/*"]

intersphinx_mapping = {'gymnasium': ('https://gymnasium.farama.org/', None)}
