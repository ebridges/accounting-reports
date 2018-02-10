'''
Accounting Reports

Usage:
  accounting-reports chart-of-accounts --db=<PATH> [--output=<FORMAT>] [--verbose]
  accounting-reports balances --db=<PATH> [--accounts=<ACCOUNTS>] [--begin=<BEGIN_DATE>]
                     [--end=<END_DATE>] [--output=<FORMAT>] [--verbose]
  accounting-reports budget --db=<PATH> [--begin=<BEGIN_DATE>]
                     [--budget-accounts=<ACCOUNTS>] [--actual-accounts=<ACCOUNTS>]
                     [--output=<FORMAT>] [--verbose]
  accounting-reports -h | --help
  accounting-reports --version
  accounting-reports --verbose

Options:
  --db=<PATH>                  Path to SQLite file.
  --accounts=<ACCOUNTS>        Comma separated list of accounts. Default: all.
  --actual-accounts=<ACCOUNTS> Comma separated list of actual accounts. Required.
  --budget-accounts=<ACCOUNTS> Comma separated list of budget accounts. Required.
  --begin=<BEGIN_DATE>         Begin date of balances (yyyy-mm-dd).  Default: first day of the year.
  --end=<END_DATE>             Date to get balances as-of (yyyy-mm-dd).  Default: last day of
                               previous month.
  --output=<FORMAT>            Format to output results in (csv, json). [Default: csv]
  --verbose                    Verbose logging.
  -h --help                    Show this screen.
  --version                    Show version.
'''

from decimal import Decimal
from logging import error, info, debug
from docopt import docopt
from piecash import open_book

from .version import __version__
from .util import (configure_logging, csv_to_list, filter_list, begin_or_default,
                   end_or_default, output_arg, list_of_months_from)


def budget_report(database, actual_accounts, budget_accounts, begin, output_func):
  """
  Prints a report for the given accounts with the budgeted amount and the actual balance.
  """
  debug('budget_report called with [%s] [%s]' % (database, begin))
  with open_book(database) as book:
    all_accounts = book.accounts
    acctlist = dict(zip(filter_list(all_accounts, actual_accounts),
                        filter_list(all_accounts, budget_accounts)))
    datelist = list_of_months_from(begin)

    for end in datelist:
      for actual, budget in acctlist.items():
        actual_balance = balance_of(actual, begin, end.date())
        budget_balance = balance_of(budget, begin, end.date())
        result = {
            'date' : end.date().strftime('%Y-%m'),
            'account_code' : actual.code if actual.code else None,
            'account' : actual.fullname,
            'budget_balance': budget_balance,
            'actual_balance': actual_balance
        }
        output_func(result)


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
          'balance' : balance_of(account, begin, end.date())
      }
      output_func(result)


def balance_of(account, begin, end):
  """
  Returns the balance of the given account over the given date range.
  """
  balance = 0
  if end:
    for split in account.splits:
      transaction = split.transaction
      post_date = transaction.post_date.date()
      if post_date >= begin and post_date <= end:
        debug('post_date (%s) is between (%s--%s)' % (post_date, begin, end))
        balance += split.value * account.sign
  else:
      balance = account.get_balance()
  balance = Decimal(balance)
  debug('balance_of account:[%s] over [%s--%s]: [%d]' % (account.fullname, begin, end, balance))
  return balance.quantize(Decimal('0.01'))


def chart_of_accounts(database, output_func):
  """
  Outputs the chart of accounts for the given book of accounts.
  """
  with open_book(database) as book:
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
  begin = begin_or_default(args['--begin'])

  output_func = output_arg(args['--output'])

  info('accounting-reports called with args: [%s]' % args)
  if args['chart-of-accounts']:
    accounts = csv_to_list(args['--accounts'])
    end = end_or_default(args['--end'])
    chart_of_accounts(db_file, output_func)

  if args['balances']:
    accounts = csv_to_list(args['--accounts'])
    end = end_or_default(args['--end'])
    account_balances(db_file, accounts, begin, end, output_func)

  if args['budget']:
    actual_accounts = csv_to_list(args.get('--actual-accounts'))
    actual_len = len(actual_accounts)
    budget_accounts = csv_to_list(args.get('--budget-accounts'))
    budget_len = len(budget_accounts)
    if actual_len != budget_len:
      error('count of actual & budget accounts must be equal.')
      return
    if actual_len == 0 and budget_len == 0:
      error('no accounts specified')
      return
    budget_report(db_file, actual_accounts, budget_accounts, begin, output_func)
