# spotify/__init__.py
import logging

# Configure logging for the package
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Import submodules
from .config import *
from .spotify_api import *
from .data_processing import *
from .utils import *
