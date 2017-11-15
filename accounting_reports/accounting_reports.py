'''
Accounting Reports

Usage:
  accounting-reports -h | --help
  accounting-reports --version
  accounting-reports --verbose
Options:
  --verbose     Verbose logging.
  -h --help     Show this screen.
  --version     Show version.
'''

from .version import __version__

from logging import basicConfig, INFO, DEBUG
from docopt import docopt


def main():
  args = docopt(__doc__, version=__version__)
  if(args['--verbose']):
    basicConfig(level=DEBUG)
  else:
    basicConfig(level=INFO)
