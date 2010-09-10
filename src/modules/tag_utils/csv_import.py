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
        self.entries = []

    def parseCSV(self, fileName, csvStartRow, colParsers):
        """Parses the rows from the target CSV file.

        The csvStartRow defines the row index of the first parsed row.

        The parser intances are supplied through the colParsers parameter. The
        parser's index in the list must match the column index in the CSV
        table.
        """

        import csv

        logging.debug('Parsing CSV %s' % fileName)

        rows = [row for row in csv.reader(open(fileName), delimiter=';', quotechar='"')]

        for inRow in rows[csvStartRow:]:
            e = []

            for i, p in enumerate(config['parser']):
                v = p.parse(inRow[i])

                e.append(v)

            self.entries.append(e)
