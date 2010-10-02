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

import os, os.path, consts, log, plugins
from threading import Thread

# Make sure the directory exists
if not os.path.exists(consts.dirProjects): os.mkdir(consts.dirProjects)

# List of currently opened projects
projects = []

class Project():
    """
    Stores project information and common tasks
    """
    def __init__(self, name="", dir="", plugin="", comp="", os="", ver="", arch="", kernel=""):
        self.name = name
        self.dir = dir
        self.plugin = plugin
        self.computername = comp
        self.os = os
        self.version = ver
        self.architecture = arch
        self.kernel = kernel
        self.packages = {}

    def GetData(self):
        return [self.name, self.dir, self.os, self.version, self.architecture, self.kernel]

    def SetData(self, name="", dir="", plugin="", comp="", os="", ver="", arch="", kernel=""):
        self.name = name
        self.dir = dir
        self.plugin = plugin
        self.computername = comp
        self.os = os
        self.version = ver
        self.architecture = arch
        self.kernel = kernel
        


    """ Project manipulation functions """
    
    def CreateKeryx(self, name, pluginName, plugin):
        """ Creates a project """
        try:
        #if 1:
            dirProj = os.path.join(consts.dirProjects, name)
            if os.path.exists(dirProj): return False, '' # False, '' means that files were changed
            filename = os.path.join(dirProj, name) + consts.appFileExt
            os.mkdir(dirProj)
            projFile = open(filename, 'wb')
            projFile.write(name + '\n' + pluginName)
            projFile.close()
            log.info('Created project: ' + name)
            plugin.createProject(name) #Create plugin information
            return True, filename
        except:
            return False, name

    def OpenKeryx(self, name):
        """ Opens a project """
        try:
            infile = open(name, 'rb')
            data = infile.read()
            infile.close()
            data = data.split('\n')

            self.name = data[0]
            self.dir = os.path.dirname(name)
            self.plugin_name = data[1]

            #Initialize plugin
            for item in plugins.OSPluginList:
                if item[0] == data[1]:
                    self.plugin = item[1] # Set plugin to correct one
                    info = self.plugin.loadProject(self.dir)

                    self.computername = info[0]
                    self.os = info[1]
                    self.version = info[2]
                    self.architecture = info[3]
                    self.kernel = info[4]                    
                    
                    return True
        except: return False
       
    def getDependencies(self, package):
        """ Gets dependencies for package """
        return self.plugin.getDependencies(os.path.join(self.dir, 'packages'), self.packages, package)

    def getUrls(self):
        return self.plugin.loadInternetPackageList(self.dir, self.architecture)

    def loadLocal(self, jobID, abortEvent):
        self.packages = self.plugin.loadLocalPackageList(self.dir, self.architecture)
        return True

    def getSources(self):
        return self.plugin.getSources(self.dir)
