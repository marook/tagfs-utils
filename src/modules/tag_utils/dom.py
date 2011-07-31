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

class ValueError(Exception):
    
    pass

class DuplicateContextError(Exception):

    def __init__(self, context):
        self.context = context

class Entry(object):

    def __str__(self):
        return self.line

class Comment(Entry):

    def __init__(self, line):
        self.line = line
        self.tagging = False

    def duplicateEntry(self, e):
        return self is e

class Tagging(Entry):
    
    def __init__(self, context, value):
        self.context = context
        self.value = value
        self.tagging = True

        if value is None:
            raise ValueError()

    @property
    def line(self):
        s = ''

        if self.context:
            s = s + self.context.strip() + ': '

        s = s + self.value.strip()

        return s

    def duplicateEntry(self, e):
        if not e.tagging:
            return False

        return ((self.context == e.context) and (self.value == e.value))

class Item(object):

    def __init__(self, entries = []):
        # entries must be copied or all Items without default constructor get
        # the same entries list instance
        self.entries = list(entries)

    @property
    def taggings(self):
        return [e for e in self.entries if e.tagging]

    def appendEntry(self, entry):
        for e in self.entries:
            if entry.duplicateEntry(e):
                return False

        self.entries.append(entry)

        return True

    def appendTagging(self, context, value):
        for e in self.entries:
            if not e.tagging:
                continue

            if e.context != context or e.value != value:
                continue

            # abort, as tagging already exists
            return False

        self.entries.append(Tagging(context, value))

        return True

    def isTagged(self, value):
        for e in self.taggings:
            if e.value != value:
                continue

            return True

        return False

    def getContextValues(self, context):
        for e in self.taggings:
            if e.context != context:
                continue

            yield e.value

    def setContextValue(self, context, value):
        entry = None

        for e in self.entries:
            if not e.tagging:
                continue

            if not context == e.context:
                continue

            if not entry is None:
                raise DuplicateContextError(context)

            entry = e

        if entry is None:
            entry = Tagging(context, value)

            self.entries.append(entry)
        else:
            entry.value = value

    def renameContext(self, oldName, newName):
        for t in self.taggings:
            if t.context != oldName:
                continue

            t.context = newName

    def __str__(self):
        s = '['

        for e in self.entries:
            s = s + str(e) + '|'

        s = s + ']'

        return s

class DB(object):

    def __init__(self, items = []):
        # items must be copied or all DBs without default constructor get
        # the same items list instance
        self.items = list(items)

    @property
    def contexts(self):
        retunedContexts = set()

        for i in self.items:
            for t in i.taggings:
                if t.context in retunedContexts:
                    continue

                retunedContexts.add(t.context)

                yield t.context

    @property
    def values(self):
        returnedValues = set()

        for i in self.items:
            for t in i.taggings:
                if t.value in returnedValues:
                    continue

                returnedValues.add(t.value)

                yield t.value
