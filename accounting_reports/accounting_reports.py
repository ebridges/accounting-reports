'''
Accounting Reports

Usage:
  accounting-reports chart-of-accounts --db=<PATH> [--output=<FORMAT>] [--verbose]
  accounting-reports balances --db=<PATH> [--accounts=<ACCOUNTS>] [--begin=<BEGIN_DATE>]
                     [--end=<END_DATE>] [--output=<FORMAT>] [--verbose]
  accounting-reports budget --db=<PATH> --accounts=<ACCOUNTS> [--begin=<BEGIN_DATE>]
                     [--end=<END_DATE>] [--output=<FORMAT>] [--verbose]
  accounting-reports display-accounts --db=<PATH> --accounts=<ACCOUNTS> [--open-if-locked=<BOOL>]
  accounting-reports -h | --help
  accounting-reports --version
  accounting-reports --verbose

Options:
  --db=<PATH>                  Path to SQLite file.
  --accounts=<ACCOUNTS>        Comma separated list of accounts. Default: all.
  --begin=<BEGIN_DATE>         Begin date of balances (yyyy-mm-dd).  Default: first day of the year.
  --end=<END_DATE>             Date to get balances as-of (yyyy-mm-dd).  Default: last day of
                               previous month.
  --output=<FORMAT>            Format to output results in (csv, json). [Default: csv]
  --open-if-locked=<BOOL>      Open the GNUCash DB if it's already open elsewhere. [Default: False]
  --verbose                    Verbose logging.
  -h --help                    Show this screen.
  --version                    Show version.
'''

import os
from pprint import pprint
from decimal import Decimal
from logging import error, info, debug
from docopt import docopt
from piecash import open_book

from version import __version__
from util import (configure_logging, csv_to_list, filter_list, begin_or_default,
                  end_or_default, output_arg, list_of_months_from, split_value, read_list_from_file)


def display_accounts(database, accounts, open_if_lock=False):
  """
  Prints out detailed information about the given accounts for debugging purposes.
  """
  debug('displaying accounts [%s]' % (accounts))
  with open_book(database, open_if_lock=open_if_lock) as book:
    account_list = filter_list(book.accounts, accounts)
    for account in account_list:
      print('account name: %s' % account.name)
      print('account type: %s' % account.type)
      print('account sign: %s' % account.sign)
      pprint(vars(account))
      print('='*50)
      # display the first 10 splits
      for split in account.splits[:10]:
        print('split transaction: %s' % split.transaction.description)
        print('split post date: %s' % split.transaction.post_date)
        print('split amount: %s' % split_value(split))
        pprint(vars(split))
        print('-'*50)


def budget_report(database, accounts, begin, end, output_func):
  """
  Prints a report for the given accounts with the budgeted amount and the actual balance.
  """
  debug('budget_report called with [%s] [%s]' % (database, begin))
  with open_book(database, open_if_lock=True) as book:
    all_accounts = book.accounts
    acctlist = filter_list(all_accounts, accounts)
    datelist = list_of_months_from(begin, end)

    for end in datelist:
      for account in acctlist:
        (budget_balance, actual_balance) = budget_balance_of(account, begin, end.date())

        result = {
            'date' : end.date().strftime('%Y-%m'),
            'account_code' : account.code if account.code else None,
            'account' : account.fullname,
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
          'balance' : balance_of(account, begin, end)
      }
      output_func(result)


def budget_balance_of(account, begin, end):
  """
  Returns a tuple of (budgeted,actual) amounts for the given budget account.
  """
  budget_balance = 0
  actual_balance = 0
  for split in account.splits:
    transaction = split.transaction
    post_date = transaction.post_date.date()
    if post_date >= begin and post_date <= end:
      debug('post_date (%s) is between (%s--%s)' % (post_date, begin, end))
      if split.value >= 0:
        budget_balance += split.value
      if split.value < 0:
        actual_balance += split.value

  budget_balance = Decimal(budget_balance)
  actual_balance = Decimal(actual_balance)
  debug('account:[%s] over [%s--%s]: (%d/%d)' %
        (account.fullname, begin, end, budget_balance, actual_balance))
  return (budget_balance.quantize(Decimal('0.01')), actual_balance.quantize(Decimal('0.01')))


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
    for account in sorted(book.accounts,
                          key=lambda account: int(account.code) if account.code else 0):
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
  end = end_or_default(args['--end'])

  if os.path.isfile(args['--accounts']):
    accounts = read_list_from_file(args['--accounts'])
  else:
    accounts = csv_to_list(args['--accounts'])

  output_func = output_arg(args['--output'])

  info('accounting-reports called with args: [%s]' % args)
  if args['chart-of-accounts']:
    chart_of_accounts(db_file, output_func)

  if args['balances']:
    account_balances(db_file, accounts, begin, end, output_func)

  if args['budget']:
    budget_report(db_file, accounts, begin, end, output_func)

  if args['display-accounts']:
    open_if_locked = args['--open-if-locked']
    display_accounts(db_file, accounts, open_if_locked)


if __name__ == '__main__':
    main()
