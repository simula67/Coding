# -*- coding: utf-8 -*-
#
# Author: Chris Oliver (excid3@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import consts, logging, os
from logging.handlers import RotatingFileHandler

# Make sure the directory existsv
if not os.path.exists(consts.dirLog): os.mkdir(consts.dirLog)

try:
    __logHandler = RotatingFileHandler(consts.fileLog, maxBytes=0, backupCount=2)
    __logHandler.doRollover()
    __logHandler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)-7s %(message)s', datefmt='%y-%m-%d %H:%M:%S'))

    logger = logging.getLogger(consts.appNameShort)
    logger.setLevel(logging.INFO)
    logger.addHandler(__logHandler)
except:
    print 'Unable to start Keryx'
    print 'Make sure no other instances of Keryx are still running.'
    import sys
    sys.exit(1)

def info(status):
    """ Prints status to log file and to console """
    logger.info(status)
    print status

def error(status):
    """ Prints error to log file and to console """
    logger.error(status)
    print status
