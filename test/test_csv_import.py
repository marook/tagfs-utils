#!/usr/bin/env python
#
# Copyright 2010 Markus Pielmeier
#
# This file is part of tagfs utils.
#
# tagfs utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tagfs utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tagfs utils.  If not, see <http://www.gnu.org/licenses/>.
#

from tag_utils import csv_import
import unittest

class AbstractTestParser(unittest.TestCase):

    def validateParserInterface(self, parser, validString):
        return parser.parse(validString)

class TestPassThroughParser(AbstractTestParser):

    def testParser(self):
        p = csv_import.PassThroughParser()

        self.assertEqual('abc', self.validateParserInterface(p, 'abc'))

class TestDateTimeParser(AbstractTestParser):

    def testParser(self):
        from datetime import datetime

        p = csv_import.DateTimeParser('%d.%m.%Y')

        self.assertEqual(datetime.strptime('2010-09-10', '%Y-%m-%d'), self.validateParserInterface(p, '10.09.2010'))

# TODO write test case for PassThroughFormatter

# TODO write test case for DateTimeFormatter
