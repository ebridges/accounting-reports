from logging import basicConfig, INFO, DEBUG, debug
from time import strptime
from datetime import date

def configure_logging(level):
    if not level:
        level = INFO
    else:
        level = DEBUG
    basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        level=level)


def csv_to_list(val):
  if val:
    return val.split(',')
  else:
    return []


def begin_or_default(val):
  if val:
    d = strptime(val, '%Y-%m-%d')
    debug(d)
    return date(d[0], d[1], d[2])
  else:
    today = date.today()
    return date(today.year, 1, 1)


def asof_or_default(val):
  if val:
    d = strptime(val, '%Y-%m-%d')
    debug(d)
    return date(d[0], d[1], d[2])
  else:
    today = date.today()
    # return first day of this month, because comparison is
    # to include all transactions _before_ this date
    return date(today.year, today.month, 1)


# return all accounts if filtered is empty, else return acounts named in filtered_accounts
def filter_list(all_accounts, filtered_accounts):
  if not filtered_accounts or len(filtered_accounts) == 0:
    return all_accounts
  else:
    accounts = []
    for account in all_accounts:
      if account.fullname in filtered_accounts:
        accounts.append(account)
    return accounts
