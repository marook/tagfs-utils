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

from tag_utils import dom
from tag_utils import tag_io
import unittest

class TestParseLine(unittest.TestCase):
    
    def testParseComment(self):
        """Parses an empty string comment
        """

        s = '   '

        e = tag_io.parseLine(s)

        self.assertEqual(s, e.line)

    def testParseTagging(self):
        """Parses a tagging without context
        """

        e = tag_io.parseLine('tag')

        self.assertEqual(None, e.context)
        self.assertEqual('tag', e.value)
        self.assertEqual('tag', e.line)

    def testParseContextTagging(self):
        """Parses a tagging with context
        """

        e = tag_io.parseLine('context: tag')

        self.assertEqual('context', e.context)
        self.assertEqual('tag', e.value)
        self.assertEqual('context: tag', e.line)

class TestParseFile(unittest.TestCase):

    def testParse(self):
        """Parses entries from a tag file
        """

        fileName = 'etc/test/tag1'

        i = tag_io.parseFile(fileName)

        self.assertEqual(6, len(i.entries))

class TestAppendEntriesFromFile(unittest.TestCase):

    def testAppend(self):
        """Appends entries from a tag file to an item
        """

        fileName = 'etc/test/tag1'
        
        i = dom.Item()

        tag_io.appendEntriesFromFile(i, fileName)

        self.assertEqual(6, len(i.entries))

class TestWriteFile(unittest.TestCase):

    def testWrite(self):
        """Read and write item, test for equality
        """

        import filecmp

        fileName1 = 'etc/test/tag1'
        fileName2 = fileName1 + '.test'

        i = tag_io.parseFile(fileName1)

        tag_io.writeFile(i, fileName2)

        self.assertTrue(filecmp.cmp(fileName1, fileName2))

class TestParseDirectory(unittest.TestCase):

    def testReadEmptyDir(self):
        """Call parseDirectory method with empty directory
        """

        i = tag_io.parseDirectory('etc/test/empty')

        self.assertEqual(0, len(i.entries))

    def testReadTaggedDir(self):
        """Call parseDirectory method with tagged directory
        """

        i = tag_io.parseDirectory('etc/test/tagged')

        self.assertEqual(1, len(i.entries))

if __name__ == "__main__":
    unittest.main()
