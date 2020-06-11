# -*- coding: utf-8 -*-
# __init__ is here so that we don't collapse in sys.path with another lega module

__title__ = 'Services Registry'
__version__ = '1.2'
__author__ = 'Sabela de la Torre, Frédéric Haziza'
__author_email__ = 'sabela.delatorre@crg.eu, frederic.haziza@crg.eu'
__license__ = 'Apache License 2.0'
__copyright__ = __title__ + ' @ CRG, Barcelona'

import sys
assert sys.version_info >= (3, 7), "This tool requires python version 3.7 or higher"

# Send warnings using the package warnings to the logging system
# The warnings are logged to a logger named 'py.warnings' with a severity of WARNING.
# See: https://docs.python.org/3/library/logging.html#integration-with-the-warnings-module
import logging
import warnings
logging.captureWarnings(True)
warnings.simplefilter("default")  # do not ignore Deprecation Warnings
