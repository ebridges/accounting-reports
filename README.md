## Accounting Reports

[![Travis CI Status](https://travis-ci.org/ebridges/accounting-reports.png?branch=master)](https://travis-ci.org/ebridges/accounting-reports)

### Overview & Goals
Command line utility to generate standard reports from a GnuCash database in SQLite format.  Relies on [Piecash](https://github.com/sdementen/piecash) to access the database.

The goal of this project is to provide a user-friendly, scriptable interface to get standard information from a GnuCash database in a flexible way.

### Usage

```
$ accounting-reports --help
  accounting-reports chart-of-accounts --db=<PATH> [--output=<FORMAT>] [--verbose]
  accounting-reports balances --db=<PATH> [--accounts=<ACCOUNTS>] [--begin=<BEGIN_DATE>]
                     [--end=<END_DATE>] [--output=<FORMAT>] [--verbose]
  accounting-reports budget --db=<PATH> [--budget-account=<ACCOUNTS> | --actual-account=<ACCOUNTS>]
                     [--begin=<BEGIN_DATE>] [--output=<FORMAT>] [--verbose]
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
```

### Thanks

* [GnuCash](https://www.gnucash.org/)
* [Piecash](https://github.com/sdementen/piecash)

### License

Copyright (c) 2018 Edward Bridges
[MIT License](LICENSE)
