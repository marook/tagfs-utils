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
import unittest

class TestTagging(unittest.TestCase):
    
    def testTagging(self):
        t = dom.Tagging('context', 'value')

        self.assertTrue(t.tagging)

class TestItem(unittest.TestCase):

    def testConstructor(self):
        i = dom.Item()

        self.assertEqual([], i.entries)

    def testSetContextValueNone(self):
        i = dom.Item()

        i.setContextValue('context', 'value')

        self.assertEqual(1, len(i.entries))
        
        e = i.entries[0]
        self.assertEqual('context', e.context)
        self.assertEqual('value', e.value)

    def testSetContextValueReplace(self):
        i = dom.Item()

        i.entries.append(dom.Tagging('context', 'value'))

        self.assertEqual(1, len(i.entries))
        
        i.setContextValue('context', 'value')

        self.assertEqual(1, len(i.entries))
        
        e = i.entries[0]
        self.assertEqual('context', e.context)
        self.assertEqual('value', e.value)

    def testSetContextValueDuplicate(self):
        i = dom.Item()

        i.entries.append(dom.Tagging('context', 'value'))
        i.entries.append(dom.Tagging('context', 'value'))

        self.assertEqual(2, len(i.entries))
        
        try:
            i.setContextValue('context', 'value')
        except dom.DuplicateContextError as e:
            # that should be

            self.assertEqual(2, len(i.entries))

            return

        # where's my exception!
        self.fail()

    def testAppendTaggingNone(self):
        i = dom.Item()

        i.appendTagging('context', 'value')

        self.assertEqual(1, len(i.entries))

    def testAppendTaggingExists(self):
        i = dom.Item()

        i.entries.append(dom.Tagging('context', 'value'))

        self.assertEqual(1, len(i.entries))

        i.appendTagging('context', 'value')

        self.assertEqual(1, len(i.entries))

    def testIsTagged(self):
        i = dom.Item([dom.Tagging(None, 'tag1'), dom.Tagging(None, 'tag2'), ])

        self.assertTrue(i.isTagged('tag1'))
        self.assertTrue(i.isTagged('tag2'))
        self.assertFalse(i.isTagged('tag3'))
