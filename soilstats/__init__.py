"""Documentation about soilstats."""
import logging
# import main modules so they are easily available to the user
from soilstats.soilcollect import SoilCollect
from soilstats.soildata import SoilData

# ruff: noqa: F401

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Barbara Vreede"
__email__ = "b.vreede@gmail.com"
__version__ = "0.1.0"
