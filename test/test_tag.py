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

import unittest

class TestItem(unittest.TestCase):

    def testParse(self):
        tag.Item(fileName)
        pass

class AbstractSubjectTest(unittest.TestCase):

    def validateSubject(self, s):
        c = s.connection

        data = c.read()

        c.close()

        self.assertTrue(len(data) > 0)
        

class TestFileSubject(AbstractSubjectTest):

    def testReadData(self):
        """Tries to read data from a FileSubject
        """

        s = dom.FileSubject('src/brainfs')

        self.validateSubject(s)

        self.assertEqual('brainfs', s.name)

if __name__ == "__main__":
    unittest.main()
