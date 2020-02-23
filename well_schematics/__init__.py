from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

from well_schematics.plots import *
from well_schematics._deprecated import *

__version__ = "0.2.0"