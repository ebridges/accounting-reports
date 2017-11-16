'''
Accounting Reports

Usage:
  accounting-reports chart-of-accounts --db=<PATH>
  accounting-reports -h | --help
  accounting-reports --version
  accounting-reports --verbose
Options:
  --db=<PATH>   Path to SQLite file.
  --verbose     Verbose logging.
  -h --help     Show this screen.
  --version     Show version.
'''

from .version import __version__

from logging import basicConfig, INFO, DEBUG
from docopt import docopt
from piecash import open_book


def chart_of_accounts(db):
  with open_book(db) as book:
      for acc in book.accounts:
          if(acc.code):
            print('%d\t%s\t%s' % (int(acc.code), acc.type, acc.fullname))


def main():
  args = docopt(__doc__, version=__version__)
  if(args['--verbose']):
    basicConfig(level=DEBUG)
  else:
    basicConfig(level=INFO)

  db_file = args['--db']

  if(args['chart-of-accounts']):
    chart_of_accounts(db_file)
