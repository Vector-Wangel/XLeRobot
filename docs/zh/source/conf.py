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

# -- Internationalization ---------------------------------------------------
language = 'zh_CN'

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
    "sphinx_design",
    "xl_components",  # docs/_shared/_ext: diagrams, cards, price calculator
]

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = ["colon_fence", "dollarmath"]
# https://github.com/executablebooks/MyST-Parser/issues/519#issuecomment-1037239655
myst_heading_anchors = 4

# Shared by the English and Chinese sites.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "_ext"))
templates_path = ["../../_shared/templates"]
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
# The home page uses a full-width layout; pages without child pages would
# otherwise show an empty "Section Navigation" sidebar. The simulation page
# gives the whole window to the simulator.
html_sidebars = {
    "index": [],
    "demos/index": [],
    "relatedworks/index": [],
    "simulation/index": [],
}
html_theme_options = {
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
    ],
    "logo": {
        "image_dark": "_static/logo_white.png",
    },
    # Language: the navbar link goes to the same page in the other language;
    # the Read the Docs flyout menu also switches languages and versions.
    "navbar_end": ["xl-lang-switch", "theme-switcher", "navbar-icon-links"],
    "header_links_before_dropdown": 6,
    "secondary_sidebar_items": {
        "**": ["page-toc", "sourcelink"],
        "index": [],
        "simulation/index": [],
    },
    "footer_start": ["xl-footer"],
    "footer_center": [],
    "footer_end": [],
    "pygments_light_style": "xcode",
    "pygments_dark_style": "github-dark",
    "show_version_warning_banner": False,
}
html_context = {
    "github_user": "Vector-Wangel",
    "github_repo": "XLeRobot",
    "github_version": "main",
    "doc_path": "docs/zh/source",
    "default_mode": "light",
}
html_css_files = [
    "css/xl-theme.css",
    "css/community-usecases.css",
]
html_static_path = ["_static", "../../_shared/static", "../../community_usecases/static"]
html_js_files = [("js/xl.js", {"defer": "defer"}), "js/community-usecases.js"]

### Autodoc configurations ###
autodoc_typehints = "signature"
autodoc_typehints_description_target = "all"
autodoc_default_flags = ['members', 'show-inheritance', 'undoc-members']

autosummary_generate = True

# remove_from_toctrees = ["_autosummary/*"]

intersphinx_mapping = {'gymnasium': ('https://gymnasium.farama.org/', None)}

# -- Options for LaTeX output -----------------------------------------------
# Support for Chinese PDF generation
latex_engine = "xelatex"
latex_use_xindy = False
latex_elements = {
    "preamble": "\\usepackage[UTF8]{ctex}\n",
}
