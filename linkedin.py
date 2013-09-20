#! /usr/bin/env python
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

import cgi
import codecs
from lxml import etree
import re
import requests
import StringIO
import sys

from dateconverter import DateConverter
from xpathmanipulator import XpathManipulator

def create_tag(tagName, tagContent):
	return "<" + tagName + ">" + tagContent + "</" + tagName + ">\n"

if len(sys.argv) != 3:
	print 'Usage: linkedin.py <profile_address> <output_file>'
	sys.exit(1)

profile_url = sys.argv[1]
output_file = sys.argv[2]

pos_nb = 0
lan_nb = 0
edu_nb = 0

f = codecs.open(output_file, 'w', 'utf-8')

dc = DateConverter()

res = requests.get(profile_url)

xpm = XpathManipulator(StringIO.StringIO(res.content), "linkedin.xml")

xpm.set_silent_error(True)
xpm.set_default_null(False)

output = '<?xml version="1.0" encoding="UTF-8"?>\n'
output += "<resume>\n"

output += create_tag("profile_url", profile_url)

fullname = xpm.get_node("fullname")
if not fullname is None:
	output += "<name>\n"
	xpm.set_variable_from_node("fullname", fullname)
	output += create_tag("firstname", xpm.get_value("firstname"))
	output += create_tag("lastname", xpm.get_value("lastname"))
	output += "</name>\n"

listPositions = xpm.get_node_list("positions")

output += "<positions>\n"

for position in listPositions:
	pos_nb += 1
	xpm.set_variable_from_node("position", position)
	output += "<position>\n"
	output += create_tag("title", xpm.get_value("position_title"))
	output += create_tag("company", xpm.get_value("position_company"))
	output += create_tag("location", xpm.get_value("position_location"))
	period = xpm.get_node("position_period")
	if not period is None:
		output += "<period>\n"
		xpm.set_variable_from_node("period", period)
		output += create_tag("from", dc.dict_sub(xpm.get_value("position_period_from")))
		output += create_tag("to", dc.dict_sub(xpm.get_value("position_period_to")))
		output += create_tag("duration", xpm.get_value("position_period_duration"))
		output += "</period>\n"
	output += create_tag("description", xpm.get_value("position_description"))
	output += "</position>\n"

output += "</positions>\n"

languages = xpm.get_node_list("languages")

output += "<languages>\n"

for language in languages:
	lan_nb += 1
	output += "<competency>\n"
	xpm.set_variable_from_node("language", language)
	output += create_tag("language", xpm.get_value("language_name"))
	output += create_tag("proficiency", re.sub("[()]", "", xpm.get_value("language_proficiency")))
	output += "</competency>\n"

output += "</languages>\n"

educations = xpm.get_node_list("educations")

output += "<education>\n"

for education in educations:
	edu_nb += 1
	xpm.set_variable_from_node("education", education)
	output += "<position>\n"
	output += create_tag("summary", xpm.get_value("education_summary"))
	output += create_tag("degree", xpm.get_value("education_degree"))
	output += create_tag("major", xpm.get_value("education_major"))
	period = xpm.get_node("education_period")
	if not period is None:
		xpm.set_variable_from_node("period", period)
		output += "<period>\n"
		output += create_tag("from", dc.dict_sub(xpm.get_value("education_period_from")))
		output += create_tag("to", dc.dict_sub(xpm.get_value("education_period_to")))
		output += "</period>\n"
	details = xpm.get_value_list("education_details")
	details_text = ""
	for detail in details:
		details_text += detail + "\n"
	output += create_tag("details", details_text.strip())
	output += "</position>\n"

output += "</education>\n"

skills = xpm.get_value_list("skills")

output += "<skills>\n"

for skill in skills:
	output += create_tag("skill", skill)

output += "</skills>\n"

output += "</resume>"

f.write(output)

f.close()

print "Profile " + profile_url+ " successfully scraped"
print "with " + str(pos_nb) + " positions,",
print str(lan_nb) + " languages,",
print "and " + str(edu_nb) + " education positions."
print "Output in " + output_file