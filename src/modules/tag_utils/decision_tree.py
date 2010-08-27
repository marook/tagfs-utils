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

import logging

class Question(object):

    def __init__(self, previousQuestion = None):
        self.previousQuestion = previousQuestion
        self._answers = None

    def answer(self, answers):
        self._answers = answers

    @property
    def originalItems(self):
        return self.previousQuestion.items

    def findItems(self, items, answers):
        for i in items:
            if not self.passesAnswer(i, answers):
                continue

            yield i

    @property
    def items(self):
        return self.findItems(self.originalItems, self._answers)

    @property
    def refiningQuestions(self):
        """Returns a list of questions which can refine the list of items.
        """

        if self._answers is None:
            logging.debug('No refinements questions for %s as there are no answers specified yet' % self)

            # prevent endless recursion
            return

        # contains values of taggings with context == None
        noContextTagging = set()
        contexts = set()

        for item in self.items:
            for tagging in item.taggings:
                if tagging.context == None:
                    noContextTagging.add(tagging.value)
                else:
                    contexts.add(tagging.context)

        for tagging in noContextTagging:
            # TODO prevent already filtered items from being added

            yield TagQuestion(self, tagging)

        for context in contexts:
            # TODO prevent already filtered items from being added

            yield ContextQuestion(self, context)

    @property
    def priorizedRefiningQuestions(self):
        rqs = list(self.refiningQuestions)
        rqs.sort(lambda q1, q2: cmp(-q1.priority, -q2.priority))

        return rqs

    @property
    def nextQuestion(self):
        qs = self.priorizedRefiningQuestions

        if len(qs) == 0:
            return None

        return qs[0]

    def __str__(self):
        return '[q: ' + self.questionText + '; a: ' + ', '.join(self.answers) + ']'

class TagQuestion(Question):

    def __init__(self, previousQuestion, taggingValue):
        super(TagQuestion, self).__init__(previousQuestion)
        self.taggingValue = taggingValue

    @property
    def questionText(self):
        return 'Is the item ' + self.taggingValue + '?'

    @property
    def priority(self):
        items = list(self.originalItems)

        allItemCount = len(items)

        matchItemCount = len(list(self.findItems(items, ['yes',])))

        return 1.0 - abs(matchItemCount / float(allItemCount) - 0.5) * 2.0

    @property
    def answers(self):
        return ['yes', 'no']

    def passesAnswer(self, item, answers):
        if answers is None or len(answers) == 2:
            return True

        if len(answers) == 0:
            return False

        answer = answers[0]

        if answer == 'yes':
            return item.isTagged(self.taggingValue)
        else:
            return not item.isTagged(self.taggingValue)

class ContextQuestion(Question):

    def __init__(self, previousQuestion, context):
        super(ContextQuestion, self).__init__(previousQuestion)
        self.context = context

    @property
    def questionText(self):
        return 'Which tag is valid for the context ' + self.context + '?'
        
    @property
    def priority(self):
        # TODO
        return 0.1

    @property
    def contextValues(self):
        values = set()

        for i in self.items:
            values = values.union(frozenset(i.getContextValues(self.context)))

        return values

    @property
    def answers(self):
        return list(self.contextValues) + ['None', ]

    def passesAnswer(self, item, answers):
        if answers == None:
            return True

        for v in item.getContextValues(self.context):
            if v in answers:
                return True

        return False

class RootQuestion(Question):

    def __init__(self, db):
        super(RootQuestion, self).__init__()
        self.db = db

        self.answer([])

    @property
    def originalItems(self):
        return self.db.items

    @property
    def items(self):
        return self.originalItems

def findItem(db):
    q = RootQuestion(db)

    return q.nextQuestion
