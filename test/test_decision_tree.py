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

from tag_utils import decision_tree as dt
from tag_utils import dom
import unittest
import logging

class TestDecisionTree(unittest.TestCase):

    def validateQuestionInterface(self, q):
        self.assertTrue(not q is None)

        self.assertTrue(not q.questionText is None)

        for a in q.answers:
            self.assertTrue(not a is None)

        for i in q.items:
            pass

        for i in q.originalItems:
            pass

        for q2 in q.priorizedRefiningQuestions:
            self.validateQuestionInterface(q2)

        nq = q.nextQuestion
        if nq != None:
            self.validateQuestionInterface(nq)

    def testEmpty(self):
        """Tests a decision tree for an empty DB
        """

        db = dom.DB()

        q = dt.findItem(db)

        # TODO self.validateQuestionInterface(q)

    def testGeneral(self):
        """A general test case for the decision tree
        """

        #import sys
        #sys.setrecursionlimit(100)

        db = dom.DB()
        db.items.append(dom.Item([dom.Tagging('color', 'blue'), ]))
        db.items.append(dom.Item([dom.Tagging('color', 'red'), ]))

        q = dt.findItem(db)

        self.validateQuestionInterface(q)

        self.assertEqual(2, len(list(q.items)))
        self.assertEqual(2, len(list(q.originalItems)))

        logging.debug('Question text is %s' % q.questionText)

        a = list(q.answers)
        a.sort()

        self.assertEqual('None', a[0])
        self.assertEqual('blue', a[1])
        self.assertEqual('red', a[2])

        q.answer(['blue', ])

        items = q.items
        self.assertTrue(1, len(items))
 
        
