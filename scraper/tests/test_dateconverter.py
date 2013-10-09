#! /usr/bin/env python

import unittest

from ..dateconverter import DateConverter

class TestDateConverter(unittest.TestCase):

  def setUp(self):
    self.seq = range(10)

  def test_dict_sub(self):
    dc = DateConverter()
    self.assertEquals("15 Jan. 2013", dc.dict_sub("15 January 2013"))
    self.assertEquals("Now", dc.dict_sub("present"))


if __name__ == '__main__':
  unittest.main()