__copyright__ = "Copyright (C) Dmitri Kourbatsky"
__license__ = "MIT License"

import unittest

from beancount import loader
from beancount.parser import cmptest

class TestFilterByTag(cmptest.TestCase):

    @loader.load_doc()
    def test_filter_by_tag(self, entries, errors, __):
        """
           plugin "beancount_filter_by_tag" "{'include':'budget,capital', 'exclude':'trading,commercial'}"

           2021-01-12 open Expenses:Administrative
           2021-01-13 open Assets:Bank

           2022-06-11 * "This should be included" #budget #branch-a
                 id: 442
                 Expenses:Administrative         15.44 EUR
                 Assets:Bank

           2022-06-12 * "This should be excluded" #budget #trading
                id: 443
                Expenses:Administrative         19.01 EUR
                Assets:Bank

           2022-06-12 * "This should be excluded" 
                id: 443
                Expenses:Administrative         44.01 EUR
                Assets:Bank 
        """
        self.assertFalse(errors)
        self.assertEqualEntries("""
           2021-01-12 open Expenses:Administrative
           2021-01-13 open Assets:Bank

           2022-06-11 * "This should be included" #budget #branch-a
                 id: 442
                 Expenses:Administrative         15.44 EUR
                 Assets:Bank                    -15.44 EUR

           2022-06-12 * "This should be excluded" #budget #trading
                id: 443
                Expenses:Administrative         19.01 EUR
                Assets:Bank                      -19.01 EUR
        """, entries)
if __name__ == "__main__":
    unittest.main()
