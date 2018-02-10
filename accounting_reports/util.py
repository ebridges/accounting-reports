'''
Common utility functions.
'''
from logging import basicConfig, INFO, DEBUG, debug
from time import strptime
from datetime import datetime, date, timedelta
from json import dumps, JSONEncoder
from csv import DictWriter
from sys import stdout
from decimal import Decimal
from dateutil.rrule import rrule, MONTHLY


def output_json(values):
  """
  Formats the given data structure as JSON.
  """
  print(dumps(values, cls=DecimalEncoder))


def output_csv(values):
  """
  Formats the given data structure as CSV.
  """
  writer = DictWriter(stdout, values.keys())
  writer.writerow(values)


def output_arg(val):
  """
  Returns the proper output function given the input.
  """
  return {
      'csv' : output_csv,
      'json': output_json,
  }[val]


class DecimalEncoder(JSONEncoder):
  """
  Ensures floats are properly encoded.
  """
  def default(self, o):
    """
    Returns an instance of the proper encoder.
    """
    if isinstance(o, Decimal):
      return float(o)
    return super(DecimalEncoder, self).default(o)


def configure_logging(level):
  """
  Configures logging to INFO if the level is not present, else to DEBUG.
  """
  if not level:
    level = INFO
  else:
    level = DEBUG
  basicConfig(
      format='[%(asctime)s][%(levelname)s] %(message)s',
      datefmt='%Y/%m/%d %H:%M:%S',
      level=level)


def csv_to_list(val):
  """
  Converts the given comma separated list to an array; if `val` is None, returns an empty array.
  """
  if val:
    return val.split(',')
  else:
    return []


def list_of_months_from(begin):
  """
  Returns a list of date objects beginning at the given `begin` up to the current month end.
  """
  from_date = last_day_of_month(begin)
  now = datetime.now()
  until = datetime(now.year, now.month, now.day)
  dates = map(last_day_of_month, [dt for dt in rrule(MONTHLY, dtstart=from_date, until=until)])
  return list(dates)


def first_day_of_month(val):
  """
  Converts the given val to the first day of the given month.
  """
  return datetime(val.year, val.month, 1)


def last_day_of_month(begin_date):
  """
  Converts the given begin_date to the last day of the given month.
  """
  if begin_date.month == 12:
      return begin_date.replace(day=31)
  return begin_date.replace(month=begin_date.month+1, day=1) - timedelta(days=1)


def begin_or_default(val):
  """
  Returns the first day of this year if `val` is None, else returns the given string formatted
  as a `date` instance.
  """
  if val:
    parsed_date = strptime(val, '%Y-%m-%d')
    return date(parsed_date[0], parsed_date[1], parsed_date[2])
  else:
    today = date.today()
    return date(today.year, 1, 1)


def end_or_default(val):
  """
  If `val` is empty returns the last day of this month, else returns `val` formatted as a date.

  Args:
      val: A date formatted as `%Y-%m-%d`. May be None.

  Returns:
      A `date` instance.
  """
  if val:
    parsed_date = strptime(val, '%Y-%m-%d')
    debug(parsed_date)
    return date(parsed_date[0], parsed_date[1], parsed_date[2])
  else:
    today = date.today()
    return last_day_of_month(today)


def filter_list(all_accounts, filtered_accounts):
  """
  Returns all accounts if filtered is empty, else return acounts named in filtered_accounts

  Args:
      all_accounts: The list of Account objects to scan.
      filtered_accounts: Account names to filter `all_accounts` with.

  Returns:
      `all_accounts` if `filtered_accounts` is empty. Else a new list of Account
      objects whose `fullname` matches the list given in `filtered_accounts`.
  """
  if not filtered_accounts:
    return all_accounts
  else:
    accounts = []
    for account in all_accounts:
      if account.fullname in filtered_accounts:
        accounts.append(account)
    return accounts
