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
Created on 19 Sept 2013

@author: RemyG
'''

from lxml import etree

class XpathManipulator:

	_mapping = { }
	_variables = { }

	_silent_error = False
	_default_null = True

	def __init__(self, page_content, mapping_file):
		"""Create the XpathManipulator.

		Keyword arguments:
		page_content -- the content of the file to scrape
		mapping_file -- the location of the XML mapping file
		"""
		self._page_content = page_content
		self._mapping_file = mapping_file
		parser = etree.HTMLParser()
		self._tree = etree.parse(self._page_content, parser)
		self._create_mapping()

	def _create_mapping(self):
		with open (self._mapping_file, "r") as myfile:
			data = myfile.read().replace('\n', '')
			root = etree.fromstring(data)
			for child in root:
				if child.tag == "parameter":
					self._mapping[child.get("name")] = child.get("value")

	def set_variable(self, name, xpath):
		self._variables[name] = xpath

	def set_variable_from_node(self, name, node):
		self._variables[name] = self._tree.getpath(node)

	def get_value(self, value_name):
		value = self._tree.xpath(self.get_xpath(value_name))
		if len(value) > 0:
			return "".join(value[0].itertext()).strip()
		else:
			return self._return_null_value(value_name)

	def get_value_list(self, value_name):
		node_list = self._tree.xpath(self.get_xpath(value_name))
		value_list = []
		if len(node_list) > 0:
			for node in node_list:
				value_list.append("".join(node.itertext()).strip())
		return value_list

	def get_node(self, value_name):
		value = self._tree.xpath(self.get_xpath(value_name))
		if len(value) > 0:
			return value[0]
		else:
			return self._return_null_node(value_name)

	def get_node_list(self, value_name):
		node_list = self._tree.xpath(self.get_xpath(value_name))
		if len(node_list) > 0:
			return node_list
		else:
			return []

	def get_xpath(self, value_name):
		xpath = self._mapping[value_name]
		for name in self._variables:
			if "$" + name in xpath:
				xpath = xpath.replace("$" + name, self._variables[name])
		return xpath

	def set_silent_error(self, silent_error):
		self._silent_error = silent_error

	def set_default_null(self, default_null):
		self._default_null = default_null

	def _return_null_value(self, value_name):
		if not self._silent_error:
			raise Exception('Xpath not found for value "' + value_name + '"')
		elif self._default_null:
			return None
		else:
			return ""

	def _return_null_node(self, value_name):
		if not self._silent_error:
			raise Exception('Xpath not found for value "' + value_name + '"')
		else:
			return None