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

import os

def driveFreeSpace():
    """ retrieves the cwd's filesystem stats """
    if os.name == 'posix': # get free space if they have statvfs
        data = os.statvfs(os.getcwd())
        return convert_file_size(float(data[0] * data[4]))
    if os.name == 'nt':
        import win32file
        drive = os.path.splitdrive(os.getcwd())[0] # Gets drive letter
        d_size = win32file.GetDiskFreeSpaceEx(drive)
        return convert_file_size(d_size[2])
    # unsupported OS, return error
    return 'Unavailable'
    
def convert_file_size(bytes):
    """ Converts file size from bytes to appropriate size """
    kb = bytes / 1024.0
    if kb < 1000:
        return '%.1f %s' % (kb, 'KiB')
    mb = kb / 1024.0
    if mb < 1000:
        return '%.1f %s' % (mb, 'MiB')
    gb = mb / 1024.0
    return '%.2f %s' % (gb, 'GiB')

def browserOpen(url):
    """ Opens default browser to url """
    import webbrowser
    webbrowser.open(url)

def utf(desc):
    """ Returns string in fully UTF compatible format """
    new_word = ''
    for letter in desc:
        if ord(letter) > 128:
            letter = chr(127)
        new_word += letter
    return new_word

def joinUrl(first, last):
    """ Returns full URL """
    if first.endswith('/'):
        if last.startswith('/'): return first + last[1:]
        else:                    return first + last
    else:
        if last.startswith('/'): return first + last
        else:                    return first + '/' + last



