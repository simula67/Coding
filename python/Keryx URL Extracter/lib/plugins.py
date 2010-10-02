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

import consts, log, os.path, sys, re

OSPluginList = []
InterfacePluginList = []
app = None
fail = False

class pluginBase:
    """ Used to make sure plugins have necessary functions """
    def __init__(self):                pass
    def IsOS(self):                    pass
    def cleanup(self):                 pass
    
    # Interface plugins
    def getWidgets(self, instance):    self.app = instance
    
    # OS Plugins
    def createProject(self):           pass
    def loadProject(self):             pass
    def loadLocalPackageList(self):    pass
    def loadInternetPackageList(self): pass
    def getDependencies(self):         pass
    def getSources(self):              pass


def load(dir, instance, load_interface_plugins=True):
    """ Enumerates a list of plugins in a directory """
    app = instance

    # Make sure dir exists
    if not os.path.isdir(dir):
        log.info(_('Cannot find ') + consts.dirPlugins + _(', exiting.'))
        return

    # Try to load each file in plugins dir
    sys.path.insert(0, dir)
    for file in os.listdir(dir):
        if file.endswith('.py'):
            status = initialize(file)
            if status != None: # Plugin loaded correctly
                status[1].getWidgets(instance) # Give all interface plugins widget tree
                # FIXME: Give plugins that have the attribute set only
                if status[2] == 'OS':          OSPluginList.append(status)
                elif status[2] == 'Interface' and load_interface_plugins: 
                    #status[1].getWidgets(instance) # Give all interface plugins widget tree
                    InterfacePluginList.append(status)
                    
    if fail: log.info(_('Plugin(s) have failed to load. This may be due to not having python-wxversion installed.'))

def initialize(file):
    """ Initializes plugin given filename and returns its instance """
    try:
        plugin = __import__(re.sub('\.pyc?$', '', file))
        if not hasattr(plugin, 'PLUGIN_NAME'): return
        name = getattr(plugin, 'PLUGIN_NAME')
        instance = getattr(plugin, name)()
        ptype = getattr(plugin, 'PLUGIN_TYPE')
        version = getattr(plugin, 'PLUGIN_VERSION')
        log.info(_('Plugin loaded: ') + file[:-3] + ' v' + version)
        return [name, instance, ptype, version]
    except:
        log.error(file + _(' failed to load.'))
        fail = True # a plugin failed to load
        return
