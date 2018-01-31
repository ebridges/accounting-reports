'''
Accounting Reports

Usage:
  accounting-reports chart-of-accounts --db=<PATH> [--output=<FORMAT>] [--verbose]
  accounting-reports balances --db=<PATH> [--accounts=<ACCOUNTS>] [--begin=<BEGIN_DATE>] [--end=<END_DATE>] [--output=<FORMAT>] [--verbose]
  accounting-reports budget --db=<PATH> [--accounts=<ACCOUNTS>] [--begin=<BEGIN_DATE>] [--end=<END_DATE>] [--output=<FORMAT>] [--verbose]
  accounting-reports -h | --help
  accounting-reports --version
  accounting-reports --verbose
Options:
  --db=<PATH>           Path to SQLite file.
  --accounts=<ACCOUNTS> Comma separated list of accounts to get balances for. Default: all.
  --begin=<BEGIN_DATE>  Begin date of balances (yyyy-mm-dd).  Default: first day of the year.
  --end=<END_DATE>      Date to get balances as-of (yyyy-mm-dd).  Default: last day of previous month.
  --output=<FORMAT>     Format to output results in (csv, json). [Default: csv]
  --verbose             Verbose logging.
  -h --help             Show this screen.
  --version             Show version.
'''

from decimal import Decimal
from logging import info, debug
from docopt import docopt
from piecash import open_book

from .version import __version__
from .util import (configure_logging, csv_to_list, filter_list, begin_or_default,
                   end_or_default, output_arg)


def budget_report(database, accounts, begin, end, output_func):
  """
  Prints a report for the given accounts and whether they're over or under budget.
  """
  debug('budget_report called with [%s] [%s] [%s--%s]' % (database, accounts, begin, end))
  with open_book(database) as book:
    acctlist = filter_list(book.accounts, accounts)

def account_balances(database, accounts, begin, end, output_func):
  """
  Prints the balances for the given accounts in the specified format.
  """
  debug('account_balance called with [%s] [%s] [%s--%s]' % (database, accounts, begin, end))
  with open_book(database) as book:
    acctlist = filter_list(book.accounts, accounts)
    for account in acctlist:
      result = {
          'account_code' : account.code if account.code else None,
          'account_name' : account.fullname,
          'balance' : balance_of(account, begin, end)
      }
      output_func(result)


def balance_of(account, begin, end):
  """
  Returns the balance of the given account over the given date range.
  """
  debug('balance_of account:[%s] over[%s--%s]' % (account, begin, end))
  balance = 0
  if end:
    for split in account.splits:
      transaction = split.transaction
      post_date = transaction.post_date.date()
      if post_date >= begin and post_date < end:
        debug('post_date (%s) is between (%s--%s)' % (transaction.post_date.date(), begin, end))
        balance += split.value * account.sign
  else:
      balance = account.get_balance()
  balance = Decimal(balance)
  return balance.quantize(Decimal('0.01'))


def chart_of_accounts(db, output_func):
  """
  Outputs the chart of accounts for the given book of accounts.
  """
  with open_book(db) as book:
    for account in book.accounts:
      result = {
          'account_code' : int(account.code) if account.code else None,
          'account_type' : account.type,
          'account_name' : account.fullname,
      }
      output_func(result)


def main():
  '''
  Application entry point.
  '''
  args = docopt(__doc__, version=__version__)
  configure_logging(args['--verbose'])

  db_file = args['--db']
  accounts = csv_to_list(args['--accounts'])
  begin = begin_or_default(args['--begin'])
  end = end_or_default(args['--end'])

  output_func = output_arg(args['--output'])

  if args['chart-of-accounts']:
    chart_of_accounts(db_file, output_func)

  if args['balances']:
    account_balances(db_file, accounts, begin, end, output_func)

  if args['budget']:
    budget_report(db_file, accounts, begin, end, output_func)