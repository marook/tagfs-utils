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

class Tagging(Entry):
    
    def __init__(self, context, value):
        self.context = context
        self.value = value
        self.tagging = True

    @property
    def line(self):
        s = ''

        if self.context:
            s = s + self.context + ': '

        s = s + self.value

        return s

class Item(object):

    def __init__(self):
        self.entries = []

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
        

    def __str__(self):
        s = '['

        for e in self.entries:
            s = s + str(e) + '|'

        s = s + ']'

        return s
