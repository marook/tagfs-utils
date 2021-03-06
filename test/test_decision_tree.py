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

    def answerQuestion(self, q, answers):
        for a in answers:
            self.assertTrue(a in q.answers, msg = 'Can\'t find answer %s in %s' % (a, ', '.join(q.answers)))

        q.answer(answers)

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

        logging.debug('Question is %s' % q)

        # TODO self.validateQuestionInterface(q)

    def testSimpleContext(self):
        """A simpe context test case for the decision tree
        """

        #import sys
        #sys.setrecursionlimit(100)

        db = dom.DB()

        i1 = dom.Item([dom.Tagging('color', 'blue'), ])
        db.items.append(i1)

        i2 = dom.Item([dom.Tagging('color', 'red'), ])
        db.items.append(i2)

        q = dt.findItem(db)

        self.validateQuestionInterface(q)

        self.assertEqual(2, len(list(q.items)))
        self.assertEqual(2, len(list(q.originalItems)))

        logging.debug('Question is %s' % q)

        a = list(q.answers)
        a.sort()

        self.assertEqual('None', a[0])
        self.assertEqual('blue', a[1])
        self.assertEqual('red', a[2])

        self.answerQuestion(q, ['blue', ])

        q.answer(['blue', ])

        items = list(q.items)
        self.assertTrue(1, len(items))
        self.assertTrue(i1 is items[0])

    def testMixedQuestions(self):
        """Tests a decision tree with mixed questions
        """

        #import sys
        #sys.setrecursionlimit(100)

        db = dom.DB()
        db.items.append(dom.Item([dom.Tagging('color', 'blue'), dom.Tagging(None, 'funny')]))
        db.items.append(dom.Item([dom.Tagging('color', 'red'), dom.Tagging(None, 'funny')]))
        db.items.append(dom.Item([dom.Tagging('color', 'red'), ]))
        db.items.append(dom.Item([dom.Tagging('color', 'red'), ]))

        q1 = dt.findItem(db)
        self.validateQuestionInterface(q1)

        logging.debug('Question is %s(p=%s)' % (q1, q1.priority))

        self.answerQuestion(q1, ['yes', ])

        self.validateQuestionInterface(q1)

        logging.debug('Possible items: %s' % ', '.join([str(i) for i in q1.items]))
        logging.debug('Possible questions: %s' % ', '.join([str(q) for q in q1.priorizedRefiningQuestions]))

        q2 = q1.nextQuestion
        self.validateQuestionInterface(q2)

        logging.debug('Question is %s' % q2)
