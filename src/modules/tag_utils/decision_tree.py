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

class Question(object):

    def __init__(self, previousQuestion = None):
        self.previousQuestion = previousQuestion
        self._answers = None

    def answer(self, answers):
        self._answers = answers

    @property
    def originalItems(self):
        return previousQuestion.items

    @property
    def items(self):
        for i in self.originalItems:
            if not self.passesAnswer(i):
                continue

            yield i

    @property
    def refiningQuestions(self):
        """Returns a list of questions which can refine the list of items.
        """

        # contains values of taggings with context == None
        noContextTagging = set()
        contexts = set()

        for item in self.items:
            for tagging in item.taggings:
                if tagging.context == None:
                    noContextTagging.add(tagging.value)
                else:
                    contexts.add(tagging.context)

        for nct in noContextTagging:
            # TODO prevent already filtered items from being added

            yield TagQuestion(nct)

        for context in contexts:
            # TODO prevent already filtered items from being added

            yield ContextQuestion(context)

    @property
    def priorizedRefiningQuestions(self):
        rqs = [q for q in self.refiningQuestions]
        rqs.sort(lambda q1, q2: cmp(-q1.priority, -q2.priority))

        return rqs

    @property
    def nextQuestion(self):
        # TODO return next question
        pass

class TagQuestion(Question):

    def __init__(self, taggingValue):
        self.taggingValue = taggingValue

    @property
    def questionText(self):
        return 'Is the item ' + self.taggingValue + '?'

    @property
    def priority(self):
        # TODO
        pass

    @property
    def answers(self):
        return ['yes', 'no']

    def passesAnswer(self, item):
        if self._answers == None or len(self._answers) == 2:
            return True

        if len(self._answers) == 0:
            return False

        answer = self._answers[0]

        # TODO
        pass

class ContextQuestion(Question):

    def __init__(self, context):
        self.context = context

    @property
    def questionText(self):
        return 'Which tag is valid for the context ' + self.context + '?'
        
    @property
    def contextValues(self):
        # TODO
        return []

    @property
    def answers(self):
        return self.questionText + ['None']

class RootQuestion(Question):

    def __init__(self, db):
        self.db = db

    @property
    def items(self):
        return db.items

def findItem(db):
    q = RootQuestion(db)

    return q.nextQuestion
