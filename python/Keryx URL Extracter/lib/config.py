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

import consts, os.path
#from gettext import gettext as _

def genDir(val): return os.path.abspath(os.path.join(os.getcwd(), val))

def fromFile(filename):
    # Import settings
    try:
        print 'Loading config: ' + filename
        consts.file_config = filename
        data = open(filename, 'r').read()
        data = data.split('\n')
        for item in data:
            try:
                key, val = item.split('=')
                if key == 'LogDir': 
                    consts.LogPath = val
                    consts.dirLog = genDir(val)
                    consts.fileLog = os.path.join(consts.dirLog, 'log')
                if key == 'LocaleDir': 
                    consts.LocalePath = val
                    consts.dirLocale = genDir(val)
#                if key == 'PackagesDir': 
#                    consts.PackagesPath = val
#                    consts.dirPackages = genDir(val)
                if key == 'PixmapsDir': 
                    consts.PixmapsPath = val
                    consts.dirPixmaps = genDir(val)
                    pixmapsChange()
                if key == 'PluginsDir': 
                    consts.PluginsPath = val
                    consts.dirPlugins = genDir(val)
                if key == 'ProjectsDir': 
                    consts.ProjectsPath = val
                    consts.dirProjects = genDir(val)
                if key == 'ThemesDir': 
                    consts.ThemesPath = val
                    consts.dirThemes = genDir(val)
                if key == 'DefaultTheme': 
                    consts.ThemeDefaultPath = val
                    consts.dirThemeDefault = genDir(val)
                if key == 'CurrentTheme': 
                    consts.CurrentThemePath = val
                    consts.dirCurrentTheme = genDir(val)
                    themeChange()
                if key == 'HTTPProxy':
                    consts.proxy_enabled = True
                    consts.http_proxy = {'http':val}
                if key == 'ProxyUsername': consts.proxy_username = val
                if key == 'ProxyPassword': consts.proxy_password = val
            except: pass
        consts.file_config = filename # Set the file_config location, so that if the config is change, settings go back to there
    except Exception, e: print e

def pixmapsChange():
    # Logo
    consts.fileIco = os.path.join(consts.dirPixmaps,'keryx.ico')
    consts.fileLogo = os.path.join(consts.dirPixmaps,'keryx.png')

def themeChange():
    # Load theme images
    consts.icon_about = os.path.join(consts.dirCurrentTheme, 'about.png')
    consts.icon_arrow_down = os.path.join(consts.dirCurrentTheme, 'arrow_down.png')
    consts.icon_arrow_up = os.path.join(consts.dirCurrentTheme, 'arrow_up.png')
    consts.icon_bug_report = os.path.join(consts.dirCurrentTheme, 'bug.png')
    consts.icon_close = os.path.join(consts.dirCurrentTheme, 'close.png')
    consts.icon_donate = os.path.join(consts.dirCurrentTheme, 'donate.png')
    consts.icon_download = os.path.join(consts.dirCurrentTheme, 'download.png')
    #icon_download_package = os.path.join(dirCurrentTheme, 'download_package.png')
    consts.icon_downloaded = os.path.join(consts.dirCurrentTheme, 'downloaded.png')
    consts.icon_error = os.path.join(consts.dirCurrentTheme, 'error.png')
    consts.icon_find = os.path.join(consts.dirCurrentTheme, 'find.png')
    consts.icon_help = os.path.join(consts.dirCurrentTheme, 'help.png')
    consts.icon_home = os.path.join(consts.dirCurrentTheme, 'home.png')
    consts.icon_layout = os.path.join(consts.dirCurrentTheme, 'layout.png')
    consts.icon_new = os.path.join(consts.dirCurrentTheme, 'new.png')
    consts.icon_open = os.path.join(consts.dirCurrentTheme, 'open.png')
    consts.icon_options = os.path.join(consts.dirCurrentTheme, 'options.png')
    consts.icon_package = os.path.join(consts.dirCurrentTheme, 'package.png')
    consts.icon_plugin = os.path.join(consts.dirCurrentTheme, 'plugin.png')
    consts.icon_plugin_add = os.path.join(consts.dirCurrentTheme, 'plugin_add.png')
    consts.icon_plugin_disable = os.path.join(consts.dirCurrentTheme, 'plugin_disabled.png')
    consts.icon_project_details = os.path.join(consts.dirCurrentTheme, 'project_details.png')
    consts.icon_quit = os.path.join(consts.dirCurrentTheme, 'quit.png')
    consts.icon_refresh = os.path.join(consts.dirCurrentTheme, 'refresh.png')
    consts.icon_sources = os.path.join(consts.dirCurrentTheme, 'sources.png')
    consts.icon_translate = os.path.join(consts.dirCurrentTheme, 'translate.png')
    consts.icon_update = os.path.join(consts.dirCurrentTheme, 'update.png')
    consts.icon_updates = os.path.join(consts.dirCurrentTheme, 'get_updates.png')
    consts.icon_uptodate = os.path.join(consts.dirCurrentTheme, 'uptodate.png')
