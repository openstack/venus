# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.graphviz',
    'openstackdocstheme',
    'sphinxcontrib.rsvgconverter',
]

# autodoc generation is a bit aggressive and a nuisance when doing heavy
# text edit cycles.
# execute "export SPHINX_DEBUG=1" in your terminal to disable

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# openstackdocstheme options
openstackdocs_repo_name = 'openstack/venus'
openstackdocs_bug_project = 'venus'
openstackdocs_bug_tag = 'doc'
openstackdocs_pdf_link = True

config_generator_config_file = '../../tools/config/venus-config-generator.conf'
sample_config_basename = '_static/venus'

policy_generator_config_file = [
    ('../../tools/config/venus-policy-generator.conf',
     '_static/venus'),
]

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'native'

# -- Options for HTML output ------------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'venusdoc'

# The name for this set of Sphinx documents. If None, it defaults to
# "<project> v<release> documentation".
html_title = 'Venus'
html_theme = 'openstackdocs'

# -- Options for LaTeX output -----------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # openany: Skip blank pages in generated PDFs
    'maxlistdepth': 10,
    'extraclassoptions': 'openany,oneside',
    'preamble': r'\setcounter{tocdepth}{2}',
    'makeindex': '',
    'printindex': '',
}

# Disable usage of xindy https://bugzilla.redhat.com/show_bug.cgi?id=1643664
# Some distros are missing xindy
latex_use_xindy = False

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index',
     'doc-venus.tex',
     'Venus Documentation',
     'OpenStack Foundation', 'manual'),
]
