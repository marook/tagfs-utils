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
import os

from tag_utils import dom
from tag_utils import tag_io

class PassThroughParser(object):
    """Parses which just passes the supplied valie through.
    """

    def parse(self, v):
        return v

class DateTimeParser(object):
    """Parser which a string to a datetime.
    """

    def __init__(self, dateFormat):
        self.dateFormat = dateFormat

    def parse(self, v):
        from datetime import datetime

        return datetime.strptime(v, self.dateFormat)

class PassThroughFormatter(object):
    """Formatter which just passes the supplied value through.
    """

    def __init__(self, context):
        self.context = context

    def format(self, v):
        return v

class DateTimeFormatter(object):
    """Formatter which formats a datetime to a string.
    """

    def __init__(self, context, dateFormat):
        self.context = context
        self.dateFormat = dateFormat

    def format(self, v):
        return v.strftime(self.dateFormat)

class Sheet(object):
    """A sheet consists of multiple data rows.
    """

    def __init__(self):
        self.rows = []

    def parseCSV(self, fileName, colParsers, csvStartRow = 0, delimiter = ';', quotechar = '"'):
        """Parses the rows from the target CSV file.

        The parser intances are supplied through the colParsers parameter. The
        parser's index in the list must match the column index in the CSV
        table.

        The csvStartRow defines the row index of the first parsed row.
        """

        import csv

        logging.debug('Parsing CSV %s' % fileName)

        with open(fileName) as f:
            rows = [row for row in csv.reader(f, delimiter = delimiter, quotechar = quotechar)]

            for inRow in rows[csvStartRow:]:
                e = []

                for i, p in enumerate(colParsers):
                    v = p.parse(inRow[i])

                    e.append(v)

                self.rows.append(e)

class AbstractSheetToTagsMerger(object):
    """Abstract base class for Sheet to tag merge classes.

    Classes which extend this class need to fullfil the following requirements:
    * self.colFormatters must be set to a list of formatters. There must be
      a formatter in the list for every column in the merged Sheets.
    * self.getTagFileName(self, row, sheet) must return a pathname for the
      target tag file. the tag file should correspond to the supplied row and
      sheet.
    """

    def __init__(self, defaultTagFileName = '.tag'):
        self.defaultTagFileName = defaultTagFileName

    def getTagFileName(self, row, sheet):
        """Calculates a tag file name through a root dir and a tag file name.
        """

        return os.path.join(self.rootTagDir, self.getItemDirName(row, sheet), self.defaultTagFileName)

    def postProcessItem(self, item, row, sheet):
        """Is called after a row is merged into an Item

        Default behavior is to do nothing.
        """
        pass

    def mergeRowToTags(self, row, sheet):
        tagFileName = self.getTagFileName(row, sheet)

        tagDir, tagFileName2 = os.path.split(tagFileName)

        if not os.path.exists(tagDir):
            os.makedirs(tagDir)

        item = dom.Item()
        if os.path.exists(tagFileName):
            tag_io.appendEntriesFromFile(item, tagFileName)

        for i, f in enumerate(self.colFormatters):
            s = f.format(row[i])

            if len(s) == 0:
                continue

            item.setContextValue(f.context, s)

        self.postProcessItem(item, row, sheet)

        # TODO track changes to be able to skip writing
        tag_io.writeFile(item, tagFileName)
        

    def mergeToTags(self, sheet):
        for row in sheet.rows:
            self.mergeRowToTags(row, sheet)
