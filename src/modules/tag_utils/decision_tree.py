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
        self._answer = None

    def answer(self, answers):
        self._answers = answers

    @property
    def items(self):
        # TODO filter items
        pass

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

        rqs = []

        for nct in noContextTagging:
            # TODO prevent already filtered items from being added

            q = TagQuestion(nct)

            rqs.append(q)

        for context in contexts:
            # TODO prevent already filtered items from being added

            q = ContextQuestion(context)

            rqs.append(q)

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
    def answers(self):
        return ['yes', 'no', 'None']

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
