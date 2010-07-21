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

class Entry(object):

    def __str__(self):
        return self.line

class Comment(Entry):

    def __init__(self, line):
        self.line = line

class Tagging(Entry):
    
    def __init__(self, context, value):
        self.context = context
        self.value = value

    @property
    def line(self):
        s = ''

        if self.context:
            s = s + self.context + ': '

        s = s + self.value

        return s

class Item(object):

    def __init__(self, entries, itemFileName = None):
        self.itemFileName = itemFileName
        self.entries = entries

    def findTaggingsByContext(self, context):
        pass

    def appendTagging(self, t):
        pass

    def __str__(self):
        s = '['

        for e in self.entries:
            s = s + str(e) + '|'

        s = s + ']'

        return s
        
