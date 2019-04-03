'''
Unit tests for util functions
'''

from datetime import date
from unittest import TestCase, main
from accounting_reports import util


class TestUtil(TestCase):
    '''
    Tests for misc. `accounting_reports.util` methods
    '''

    def test_last_day_of_month_normal(self):
        '''
        case: normal case
        '''
        self.assertEqual(util.last_day_of_month(date(2017, 1, 1)), date(2017, 1, 31))
        self.assertEqual(util.last_day_of_month(date(2017, 2, 1)), date(2017, 2, 28))
        self.assertEqual(util.last_day_of_month(date(2017, 3, 1)), date(2017, 3, 31))
        self.assertEqual(util.last_day_of_month(date(2017, 4, 1)), date(2017, 4, 30))
        self.assertEqual(util.last_day_of_month(date(2017, 5, 1)), date(2017, 5, 31))
        self.assertEqual(util.last_day_of_month(date(2017, 6, 1)), date(2017, 6, 30))
        self.assertEqual(util.last_day_of_month(date(2017, 7, 1)), date(2017, 7, 31))
        self.assertEqual(util.last_day_of_month(date(2017, 8, 1)), date(2017, 8, 31))
        self.assertEqual(util.last_day_of_month(date(2017, 9, 1)), date(2017, 9, 30))
        self.assertEqual(util.last_day_of_month(date(2017, 10, 1)), date(2017, 10, 31))
        self.assertEqual(util.last_day_of_month(date(2017, 11, 1)), date(2017, 11, 30))
        self.assertEqual(util.last_day_of_month(date(2017, 12, 1)), date(2017, 12, 31))


    def test_last_day_of_month_leap(self):
        '''
        case: leap years
        '''
        self.assertEqual(util.last_day_of_month(date(2016, 1, 1)), date(2016, 1, 31))
        self.assertEqual(util.last_day_of_month(date(2016, 2, 1)), date(2016, 2, 29))
        self.assertEqual(util.last_day_of_month(date(2016, 3, 1)), date(2016, 3, 31))
        self.assertEqual(util.last_day_of_month(date(2016, 4, 1)), date(2016, 4, 30))
        self.assertEqual(util.last_day_of_month(date(2016, 5, 1)), date(2016, 5, 31))
        self.assertEqual(util.last_day_of_month(date(2016, 6, 1)), date(2016, 6, 30))
        self.assertEqual(util.last_day_of_month(date(2016, 7, 1)), date(2016, 7, 31))
        self.assertEqual(util.last_day_of_month(date(2016, 8, 1)), date(2016, 8, 31))
        self.assertEqual(util.last_day_of_month(date(2016, 9, 1)), date(2016, 9, 30))
        self.assertEqual(util.last_day_of_month(date(2016, 10, 1)), date(2016, 10, 31))
        self.assertEqual(util.last_day_of_month(date(2016, 11, 1)), date(2016, 11, 30))
        self.assertEqual(util.last_day_of_month(date(2016, 12, 1)), date(2016, 12, 31))

        '''
        case: exceptional leap years
        '''
        self.assertEqual(util.last_day_of_month(date(1900, 2, 1)), date(1900, 2, 28))
        self.assertEqual(util.last_day_of_month(date(2000, 2, 1)), date(2000, 2, 29))


    def test_end_or_default_empty(self):
        '''
        case: empty string as parameter
        '''
        today = date.today()
        last_day = util.last_day_of_month(today)
        expected = date(today.year, today.month, last_day.day)
        actual = util.end_or_default('')
        self.assertEqual(expected, actual)


    def test_end_or_default_none(self):
        '''
        case: `None` as parameter
        '''
        today = date.today()
        last_day = util.last_day_of_month(today)
        expected = date(today.year, today.month, last_day.day)
        actual = util.end_or_default(None)
        self.assertEqual(expected, actual)


    def test_end_or_default_normal(self):
        '''
        Normal case
        '''
        test_case = '2018-06-30'
        expected = date(2018, 6, 30)
        actual = util.end_or_default(test_case)
        self.assertEqual(expected, actual)


    def test_begin_or_default_empty(self):
        '''
        case: empty string as parameter
        '''
        expected = date(date.today().year, 1, 1)
        actual = util.begin_or_default('')
        self.assertEqual(expected, actual)


    def test_begin_or_default_none(self):
        '''
        case: `None` as parameter
        '''
        expected = date(date.today().year, 1, 1)
        actual = util.begin_or_default(None)
        self.assertEqual(expected, actual)


    def test_begin_or_default_normal(self):
        '''
        Normal case
        '''
        test_case = '2018-06-30'
        expected = date(2018, 6, 30)
        actual = util.begin_or_default(test_case)
        self.assertEqual(expected, actual)


    def test_list_of_months_from_dec(self):
        '''
        confirms that the list of months returned:
        - handles YoY overlap
        - handles leap years
        - properly includes begin/end dates
        '''
        begin = date(2015, 12, 1)
        end = date(2017, 3, 1)

        actual = util.list_of_months_from(begin, end)
        self.assertEqual(len(actual), 16)
        self.assertEqual(actual[0], date(2015, 12, 31))
        self.assertEqual(actual[1], date(2016, 1, 31))
        self.assertEqual(actual[2], date(2016, 2, 29))
        self.assertEqual(actual[3], date(2016, 3, 31))
        self.assertEqual(actual[4], date(2016, 4, 30))
        self.assertEqual(actual[5], date(2016, 5, 31))
        self.assertEqual(actual[6], date(2016, 6, 30))
        self.assertEqual(actual[7], date(2016, 7, 31))
        self.assertEqual(actual[8], date(2016, 8, 31))
        self.assertEqual(actual[9], date(2016, 9, 30))
        self.assertEqual(actual[10], date(2016, 10, 31))
        self.assertEqual(actual[11], date(2016, 11, 30))
        self.assertEqual(actual[12], date(2016, 12, 31))
        self.assertEqual(actual[13], date(2017, 1, 31))
        self.assertEqual(actual[14], date(2017, 2, 28))
        self.assertEqual(actual[15], date(2017, 3, 31))

    def test_csv_to_list_normal(self):
        '''
        normal case
        '''
        expected = ['a', 'b', 'c']
        actual = util.csv_to_list('a,b,c')
        self.assertSequenceEqual(expected, actual)

    def test_csv_to_list_empty(self):
        '''
        empty string case
        '''
        expected = []
        actual = util.csv_to_list('')
        self.assertSequenceEqual(expected, actual)

    def test_csv_to_list_none(self):
        '''
        `None` string case
        '''
        expected = []
        actual = util.csv_to_list(None)
        self.assertSequenceEqual(expected, actual)

    def test_csv_to_list_one_comma(self):
        '''
        String with one comma case
        '''
        expected = ['', '']
        actual = util.csv_to_list(',')
        self.assertSequenceEqual(expected, actual)


if __name__ == '__main__':
    main()
