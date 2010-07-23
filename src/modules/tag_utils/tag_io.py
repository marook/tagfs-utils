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

import dom
import os
import re

COMMENT_LINE_MATCHER = re.compile('^[\s]*$')

def parseLine(line):
    if COMMENT_LINE_MATCHER.match(line):
        entry = dom.Comment(line)
    else:
        i = line.find(':')

        if i == -1:
            context = None
            value = line.strip()
        else:
            context = line[0:i].strip()
            value = line[i + 1:len(line)].strip()

        entry = dom.Tagging(context, value)

    return entry

def parseDirectory(path, tagFileName = '.tag'):
    """Parse taggings for a directory.

    This method parses taggings which are applied to a directory. This is
    done by looking into the directory for a tag file. If no tag file exists
    within the directory, then an empty Item instance is returned.
    """

    tagFileName = os.path.join(path, tagFileName)

    if os.path.exists(tagFileName):
        return parseFile(tagFileName)
    else:
        return dom.Item()

def parseFile(fileName):
    i = dom.Item()

    appendEntriesFromFile(i, fileName)

    return i


def appendEntriesFromFile(item, fileName):
    with open(fileName) as f:
        for line in f:
            s = line[0:len(line) - 1]

            entry = parseLine(s)
                
            item.entries.append(entry)
    

def writeFile(item, fileName):
    with open(fileName, 'w') as f:
        for e in item.entries:
            f.write(e.line)
            f.write('\n')
