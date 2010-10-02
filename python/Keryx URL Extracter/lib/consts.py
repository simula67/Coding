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

import os, os.path
from gettext import gettext as _

# Strings
appName      = 'Keryx'
appVersion   = '0.92.3'
appNameShort = 'keryx'
appFileExt   = '.keryx'
appComments  = _('Bringing Updates Home.')
filterDesc = _('Keryx Project Files') + ' | (*' + appFileExt + ')'

authors = 'Chris Oliver\nBuran Ayuthia\nmac9416'
email = 'excid3@gmail.com'
artists = 'Chris Oliver'
docwriters = 'Chris Oliver'
translators = ''
copyright = '(C) 2008-2009 Chris Oliver'
description = appName + _(' is a package manager for computers without internet.')
license = appName + _(""" is free software; you can redistribute it and/or 
modify it under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or (at your option) 
any later version.

Keryx is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. See the GNU General Public License for more details. You 
should have received a copy of the GNU General Public License along with Keryx; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 
330, Boston, MA  02111-1307  USA""")

welcome_message = _('Welcome to ') + appName

parameters="""
Command line parameters:
-h or --help                            Displays this message
-v or --version                         Displays Keryx version number
--create <project name> <plugin name>   Creates a new project in the default 
                                          directory with name of <project name>
                                          and type project <plugin name>
--config <file>                         Uses <file> to as configuration file\n"""

# Proxy
proxy_enabled = False
http_proxy = {}
proxy_username = ''
proxy_password = ''

# URLs
urlBug = 'https://bugs.launchpad.net/keryx'
urlDonate = 'http://keryxproject.org/donate'
urlHelp = 'http://keryxproject.org/forum'
urlHomepage = 'http://keryxproject.org'
urlTranslate = 'https://translations.launchpad.net/keryx'

columns = [(_("S"), 50), (_("Package Name"), 200), (_("Installed Version"), 200), (_("Latest Version"), 200), (_("Description"), 200)]

# Directories
LocalePath = 'locale'
LogPath = 'logs'
#PackagesPath = 'packages'
PixmapsPath = 'pixmaps'
PluginsPath = 'plugins'
ProjectsPath = 'projects'
ThemesPath = PixmapsPath + '/themes'
ThemeDefaultPath = ThemesPath + '/default'
CurrentThemePath = ThemeDefaultPath

dirLocale = os.path.abspath(os.path.join(os.getcwd(), LocalePath))
dirLog = os.path.abspath(os.path.join(os.getcwd(), LogPath))
#dirPackages = os.path.abspath(os.path.join(os.getcwd(), PackagesPath))
dirPixmaps = os.path.abspath(os.path.join(os.getcwd(), PixmapsPath))
dirPlugins = os.path.abspath(os.path.join(os.getcwd(), PluginsPath))
dirProjects = os.path.abspath(os.path.join(os.getcwd(), ProjectsPath))
dirThemes = os.path.abspath(os.path.join(os.getcwd(), ThemesPath))
dirThemeDefault = os.path.abspath(os.path.join(os.getcwd(), ThemeDefaultPath))
dirCurrentTheme = os.path.abspath(os.path.join(os.getcwd(), CurrentThemePath))

# Files
configFilename = appNameShort + '.conf'
file_config = os.path.join(os.getcwd(), configFilename)
fileLog   = os.path.join(dirLog, 'log')

# Filetypes
wildcard = '%s (*.keryx)|*.keryx|' \
           '%s (*.*)|*.*' % (_("Keryx project"), _("All files"))
wildcard_plugin = '%s (*.py)|*.py|' \
                  '%s (*.*)|*.*' % (_("Python File"), _("All files"))

# Logo
fileIco = os.path.join(dirPixmaps,'keryx.ico')
fileLogo = os.path.join(dirPixmaps,'keryx.png')

# Load theme images
icon_about = os.path.join(dirCurrentTheme, 'about.png')
icon_arrow_down = os.path.join(dirCurrentTheme, 'arrow_down.png')
icon_arrow_up = os.path.join(dirCurrentTheme, 'arrow_up.png')
icon_bug_report = os.path.join(dirCurrentTheme, 'bug.png')
icon_close = os.path.join(dirCurrentTheme, 'close.png')
icon_donate = os.path.join(dirCurrentTheme, 'donate.png')
icon_download = os.path.join(dirCurrentTheme, 'download.png')
#icon_download_package = os.path.join(dirCurrentTheme, 'download_package.png')
icon_downloaded = os.path.join(dirCurrentTheme, 'downloaded.png')
icon_error = os.path.join(dirCurrentTheme, 'error.png')
icon_find = os.path.join(dirCurrentTheme, 'find.png')
icon_help = os.path.join(dirCurrentTheme, 'help.png')
icon_home = os.path.join(dirCurrentTheme, 'home.png')
icon_layout = os.path.join(dirCurrentTheme, 'layout.png')
icon_new = os.path.join(dirCurrentTheme, 'new.png')
icon_open = os.path.join(dirCurrentTheme, 'open.png')
icon_options = os.path.join(dirCurrentTheme, 'options.png')
icon_package = os.path.join(dirCurrentTheme, 'package.png')
icon_plugin = os.path.join(dirCurrentTheme, 'plugin.png')
icon_plugin_add = os.path.join(dirCurrentTheme, 'plugin_add.png')
icon_plugin_disable = os.path.join(dirCurrentTheme, 'plugin_disabled.png')
icon_project_details = os.path.join(dirCurrentTheme, 'project_details.png')
icon_quit = os.path.join(dirCurrentTheme, 'quit.png')
icon_refresh = os.path.join(dirCurrentTheme, 'refresh.png')
icon_sources = os.path.join(dirCurrentTheme, 'sources.png')
icon_translate = os.path.join(dirCurrentTheme, 'translate.png')
icon_update = os.path.join(dirCurrentTheme, 'update.png')
icon_updates = os.path.join(dirCurrentTheme, 'get_updates.png')
icon_uptodate = os.path.join(dirCurrentTheme, 'uptodate.png')

#color_error = wx.Color(255,118,106)
#color_update = "light blue"
#color_uptodate = wx.Color(150, 235, 140)
