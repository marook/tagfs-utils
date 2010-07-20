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

from tag_utils import tag_io
import unittest

class TestParseLine(unittest.TestCase):
    
    def testParseComment(self):
        e = tag_io.parseLine('   ')

        print e

    def testParseTagging(self):
        e = tag_io.parseLine('tag')

        print e

    def testParseContextTagging(self):
        e = tag_io.parseLine('context: tag')

        print e

class TestParseFile(unittest.TestCase):

    def testParse(self):
        i = tag_io.parseFile('etc/test/tag1')

        print i

if __name__ == "__main__":
    unittest.main()
