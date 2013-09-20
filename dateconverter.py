# -*- coding: UTF-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2013 Remy Gardette

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

'''
Created on 19 Sept 13

@author: RemyG
'''

import re

class DateConverter:
	'''
	classdocs
	'''

	date_dict = {
		'[Jj]anuary'	: 'Jan.',
		'[Ff]ebruary'	: 'Feb.',
		'[Mm]arch'		: 'Mar.',
		'[Aa]pril'		: 'Apr.',
		'[Mm]ay'		: 'May',
		'[Jj]une'		: 'June',
		'[Jj]uly'		: 'July',
		'[Aa]ugust'		: 'Aug.',
		'[Ss]eptember'	: 'Sept.',
		'[Oo]ctober'	: 'Oct.',
		'[Nn]ovember'	: 'Nov.',
		'[Dd]ecember'	: 'Dec.',
		'[Pp]resent'	: 'Now',

		'[Jj]anvier'	: 'Janv.',
		'[Ff]évrier'	: 'Févr.',
		'[Mm]ars'		: 'Mars',
		'[Aa]vril'		: 'Avril',
		'[Mm]ai'		: 'Mai',
		'[Jj]uin'		: 'Juin',
		'[Jj]uillet'	: 'Juil.',
		'[Aa]oût'		: 'Août',
		'[Ss]eptembre'	: 'Sept.',
		'[Oo]ctobre'	: 'Oct.',
		'[Nn]ovembre'	: 'Nov.',
		'[Dd]écembre'	: 'Déc.'
	}

	def __init__(self):
		'''
		Constructor
		'''

	def dict_sub(self, text):
		""" Replace in 'text' non-overlapping occurences of REs whose patterns are keys
		in dictionary 'd' by corresponding values (which must be constant strings: may
		have named backreferences but not numeric ones). The keys must not contain
		anonymous matching-groups.
		Returns the new string."""
		# Create a regular expression  from the dictionary keys
		regex = re.compile("|".join("(%s)" % k for k in self.date_dict))
		# Facilitate lookup from group number to value
		lookup = dict((i+1, v) for i, v in enumerate(self.date_dict.itervalues()))
		# For each match, find which group matched and expand its value
		return regex.sub(lambda mo: mo.expand(lookup[mo.lastindex]), text)