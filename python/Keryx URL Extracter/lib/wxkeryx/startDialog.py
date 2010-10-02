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

import lib.project, os.path, platform, wx
import wx.lib.buttons as buttons
from lib import consts, log, plugins
from lib.project import Project

class startDialog(wx.Dialog):
    """ Startup dialog """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetIcon(wx.Icon(consts.fileIco, wx.BITMAP_TYPE_ICO))
        self.bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(consts.fileLogo))
        self.welcomeText = wx.StaticText(self, -1, consts.welcome_message)
        self.newText = wx.StaticText(self, -1, _("To get started, create a new project."))
        self.nameTextCtrl = wx.TextCtrl(self, -1, platform.node())#, size=(120,20))
        self.choice = wx.Choice(self, -1, choices=[], style=wx.CB_SORT)

        # Append the plugins into the combo box
        for name, instance, type, ver in plugins.OSPluginList: self.choice.Append(name)
        self.choice.Select(0)

        self.newProjectButton = buttons.GenBitmapTextButton(self, -1, wx.Bitmap(consts.icon_new), _("New Project"))#, size=(110, 25))
        self.static_line = wx.StaticLine(self, -1)
        self.openTxt = wx.StaticText(self, -1, _("Open a project:"))
        self.openProjBox = wx.Choice(self, -1, choices=[_('Browse...')], style=wx.CB_SORT)
        
        self.projects = []
        for root, dirs, files in os.walk(consts.dirProjects):
            for item in files:
                if item.endswith(consts.appFileExt): 
                    self.openProjBox.Append(item[:-6])
                    self.projects.append(os.path.join(root, item))
                    
        try:    self.openProjBox.Select(1)
        except: self.openProjBox.Select(0)

        self.openProjectButton = buttons.GenBitmapTextButton(self, -1, wx.Bitmap(consts.icon_open), _("Open Project"))#, size=(120, 25))

        self.SetTitle(consts.welcome_message)
        self.welcomeText.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        self.__do_layout()
        self.Bind(wx.EVT_BUTTON, self.OnNewProject, self.newProjectButton)
        self.Bind(wx.EVT_BUTTON, self.OnOpenProject, self.openProjectButton)
        
    def __do_layout(self):
        # begin wxGlade: startDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.bitmap, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1.Add(self.welcomeText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 3)
        sizer_1.Add(self.newText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 3)
        sizer_2.Add(self.nameTextCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_2.Add(self.choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_2.Add(self.newProjectButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_1.Add(sizer_2, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 3)
        sizer_1.Add(self.static_line, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        sizer_3.Add(self.openTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_3.Add(self.openProjBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_3.Add(self.openProjectButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_3, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        self.Centre()
        
    def OnNewProject(self, event): # wxGlade: startDialog.<event_handler>
        projName = self.nameTextCtrl.GetLineText(0)
        plugin = self.choice.GetSelection()

        if projName == '' or plugin == -1: 
            wx.MessageBox(_("Please enter a project name and select an OS plugin."), _("Error"))
            return

        # Append new project
        lib.project.projects.append(Project())
        project = lib.project.projects[len(lib.project.projects) - 1]
        
        # Grab the plugin entry
        plugin_index = -1
        name = self.choice.GetItems()[plugin]
        for i in range(len(plugins.OSPluginList)):
            if plugins.OSPluginList[i][0]==name: plugin_index = i

        if plugin_index == -1: 
            wx.MessageBox(_("Unable to find plugin"), _("Error"))
            return
        
        if not plugins.OSPluginList[plugin_index][1].IsOS():
            wx.MessageBox(_("Please create the project on the plugin's supported OS."), _("Error"))
            return

        # Create project
        success, filename = project.CreateKeryx(projName, 
                                                plugins.OSPluginList[plugin_index][0],
                                                plugins.OSPluginList[plugin_index][1])
        
        if not success:
            wx.MessageBox(_("Unable to create project. Make sure a project by this name does not already exist."), _("Error"))
            return

        success = project.OpenKeryx(filename)

        if success: self.EndModal(wx.ID_OK)
        else:
            log.error(_("Unable to open project"))
            wx.MessageBox(_("Make sure you have a plugin loaded to support this project."), _("Unable to open project."))

    def OnOpenProject(self, event): # wxGlade: startFrame.<event_handler>
        val = self.openProjBox.GetItems()[self.openProjBox.GetSelection()]
        if val != _('Browse...'): 
            # Find the entry in self.projects for the current val's information
            index = -1
            for i in range(len(self.projects)):
                if self.projects[i].find(val+consts.appFileExt) != -1: index = i #
            
            if index == -1: return # Return if we didnt find it

            result = self.openPath(self.projects[index])
            if result == True: self.EndModal(wx.ID_OK)
        else:
            dlg = wx.FileDialog(self, message=_("Choose a file"),
                            defaultDir=consts.dirProjects, 
                            defaultFile="",
                            wildcard=consts.wildcard,
                            style=wx.OPEN | wx.CHANGE_DIR)

            # Show the dialog and retrieve the user response. If it is the OK response, 
            # process the data
            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()
                dlg.Destroy()
                result = self.openPath(paths[0])
                if result == True: self.EndModal(wx.ID_OK)

    def openPath(self, path):
        # Append a new project
        lib.project.projects.append(Project())
        project = lib.project.projects[len(lib.project.projects) - 1]

        # Load the project from file
        if project.OpenKeryx(path):
            log.info(_("Opened project") + ": " + project.name)
            return True
        else:
            # Remove project
            lib.project.projects.pop()
            log.error(_("Unable to open project"))
            wx.MessageBox(_("Make sure you have a plugin loaded to support this project."), _("Unable to open project."))
            return False
                
# end of class startDialog
