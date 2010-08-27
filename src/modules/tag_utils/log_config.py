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

from os import environ as env
import logging
import sys

def setUpLogging():
    if not 'DEBUG' in env:
        return

    def exceptionCallback(eType, eValue, eTraceBack):
        import cgitb

        txt = cgitb.text((eType, eValue, eTraceBack))

        logging.fatal(txt)
    
        sys.exit(1)

    # configure file logger
    logging.basicConfig(level = logging.DEBUG,
                        format = '%(asctime)s %(levelname)s %(message)s')
    
    # replace default exception handler
    sys.excepthook = exceptionCallback
    
    logging.debug('Logging and exception handling has been set up')
