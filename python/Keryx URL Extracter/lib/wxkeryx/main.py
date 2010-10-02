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

import os.path, lib, sys, wx
import wx.lib.buttons as buttons
from lib import consts, log, plugins, project
from startDialog import startDialog
from misc import detailsTab, ProportionalSplitter, VirtualList
from options import optionDialog
from delayedresult import thread
from download import download
from editor import FileEditor

class MainApp(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.splitter = ProportionalSplitter(self)#, style=wx.SP_3D|wx.SP_BORDER)
        self.panel = wx.Panel(self.splitter)
        self.notebook = wx.Notebook(self.panel, -1, style=wx.NB_BOTTOM)
        self.project_notebook_pane = wx.Panel(self.notebook, -1, style=wx.TAB_TRAVERSAL)
        self.SetIcon(wx.Icon(consts.fileIco, wx.BITMAP_TYPE_ICO))
        self.statusbar = self.CreateStatusBar(1, 0)

        # Side Buttons
        self.buttonPanel = wx.Panel(self)
        self.downloadButton = buttons.GenBitmapTextButton(self.buttonPanel, -1, wx.Bitmap(consts.icon_download), _("Download"))#, size=(95, 25))
        self.updatesButton = buttons.GenBitmapTextButton(self.buttonPanel, -1, wx.Bitmap(consts.icon_updates), _("Get Updates"))#, size=(95, 25))
        self.refreshButton = buttons.GenBitmapTextButton(self.buttonPanel, -1, wx.Bitmap(consts.icon_refresh), _("Refresh"))#, size=(95, 25))

        self.notebook_il = wx.ImageList(16, 16)
        self.notebook_il.Add(wx.Bitmap(consts.icon_project_details))
        self.notebook.SetImageList(self.notebook_il)

        self.projectDetails = wx.TextCtrl(self.project_notebook_pane, style = wx.TE_MULTILINE | wx.TE_RICH |wx.TE_READONLY)
        self.details = detailsTab(self.notebook)
        
        # Create list view
        self.list = VirtualList(self.splitter, self.details)
        
        # Create Popup menu for self.list
        self.__popup_menu()
        self.__create_menu()
        self.__set_properties()
        self.__do_layout()
        self.__bind_events()

        plugins.load(consts.dirPlugins, self)
        for name, instance, type, ver in plugins.InterfacePluginList: instance.start()

        if len(plugins.OSPluginList) < 1: 
            wx.MessageBox(_("No OS plugins were loaded. Make sure you have OS plugins in ") +
                          consts.dirPlugins + ". " + _("Check the log for more details."))
            sys.exit(1)

    def __popup_menu(self):
        self.popupmenu = wx.Menu()
        #FIXME: popup menu items cannot display bitmap properly?
        item = self.popupmenu.Append(-1, _("Download"))
        self.Bind(wx.EVT_MENU, self.OnDownload, item)
        item = self.popupmenu.Append(-1, _("View Details"))
        self.Bind(wx.EVT_MENU, self.OnDetails, item)
        self.list.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

    def __create_menu(self):
        # Menu Bar
        self.menubar = wx.MenuBar()
        self.fileFile = wx.Menu()
        self.fileClose = wx.MenuItem(self.fileFile, wx.NewId(), _("&Close Project...\tCtrl+X"), _("Closes the current project"), wx.ITEM_NORMAL)
        self.fileClose.SetBitmap(wx.Bitmap(consts.icon_close))
        self.fileFile.AppendItem(self.fileClose)
        self.fileFile.AppendSeparator()
        self.fileQuit = wx.MenuItem(self.fileFile, wx.NewId(), _("&Quit\tCtrl+Q"), _("Quit this application"), wx.ITEM_NORMAL)
        self.fileQuit.SetBitmap(wx.Bitmap(consts.icon_quit))
        self.fileFile.AppendItem(self.fileQuit)
        self.menubar.Append(self.fileFile, _("&File"))
        
        tmp_menu = wx.Menu()
        self.editOptions = wx.MenuItem(tmp_menu, wx.NewId(), _("&Options...\tCtrl+O"), _("Open options dialog"), wx.ITEM_NORMAL)
        self.editOptions.SetBitmap(wx.Bitmap(consts.icon_options))
        tmp_menu.AppendItem(self.editOptions)
        self.menubar.Append(tmp_menu, _("&Edit"))
        
        tmp_menu = wx.Menu()
        self.projRefresh = wx.MenuItem(tmp_menu, wx.NewId(), _("&Refresh\tCtrl+R"), _("Refresh package list"), wx.ITEM_NORMAL)
        self.projRefresh.SetBitmap(wx.Bitmap(consts.icon_refresh))
        tmp_menu.AppendItem(self.projRefresh)
        tmp_menu.AppendSeparator()
        self.projUpdates = wx.MenuItem(tmp_menu, wx.NewId(), _("Get &Updates\tCtrl+U"), _("Grabs all packages that have updates"), wx.ITEM_NORMAL)
        self.projUpdates.SetBitmap(wx.Bitmap(consts.icon_updates))
        tmp_menu.AppendItem(self.projUpdates)
        self.projDownload = wx.MenuItem(tmp_menu, wx.NewId(), _("&Download Package\tCtrl+D"), _("Downloads selected package"), wx.ITEM_NORMAL)
        self.projDownload.SetBitmap(wx.Bitmap(consts.icon_download))
        tmp_menu.AppendItem(self.projDownload)
        tmp_menu.AppendSeparator()
        self.projDetails = wx.MenuItem(tmp_menu, wx.NewId(), _("&View Details\tCtrl+V"), _("Shows details of selected package"), wx.ITEM_NORMAL)
        self.projDetails.SetBitmap(wx.Bitmap(consts.icon_package))
        tmp_menu.AppendItem(self.projDetails)
        tmp_menu.AppendSeparator()
        self.projSources = wx.MenuItem(tmp_menu, wx.NewId(), _("&Edit Sources....\tCtrl+E"), _("Edit project sources"), wx.ITEM_NORMAL)
        self.projSources.SetBitmap(wx.Bitmap(consts.icon_sources))
        tmp_menu.AppendItem(self.projSources)

        self.menubar.Append(tmp_menu, _("&Project"))
        
        tmp_menu = wx.Menu()
        self.helpHomepage = wx.MenuItem(tmp_menu, wx.NewId(), _("&Homepage"), _("Visit the website"), wx.ITEM_NORMAL)
        self.helpHomepage.SetBitmap(wx.Bitmap(consts.icon_home))
        tmp_menu.AppendItem(self.helpHomepage)
        self.helpOnline = wx.MenuItem(tmp_menu, wx.NewId(), _("&Get Help Online"), _("Visit the forums"), wx.ITEM_NORMAL)
        self.helpOnline.SetBitmap(wx.Bitmap(consts.icon_help))
        tmp_menu.AppendItem(self.helpOnline)
        self.helpTranslate = wx.MenuItem(tmp_menu, wx.NewId(), _("&Translate This Application"), _("Help translate to other languages"), wx.ITEM_NORMAL)
        self.helpTranslate.SetBitmap(wx.Bitmap(consts.icon_translate))
        tmp_menu.AppendItem(self.helpTranslate)
        self.helpReport = wx.MenuItem(tmp_menu, wx.NewId(), _("R&eport A Problem"), _("Report a bug"), wx.ITEM_NORMAL)
        self.helpReport.SetBitmap(wx.Bitmap(consts.icon_bug_report))
        tmp_menu.AppendItem(self.helpReport)
        tmp_menu.AppendSeparator()
        self.helpDonate = wx.MenuItem(tmp_menu, wx.NewId(), _("&Donate"), _("Make a donation"), wx.ITEM_NORMAL)
        self.helpDonate.SetBitmap(wx.Bitmap(consts.icon_donate))
        tmp_menu.AppendItem(self.helpDonate)
        tmp_menu.AppendSeparator()
        self.helpAbout = wx.MenuItem(tmp_menu, wx.NewId(), _("&About..."), _("About " + consts.appName), wx.ITEM_NORMAL)
        self.helpAbout.SetBitmap(wx.Bitmap(consts.icon_about))
        tmp_menu.AppendItem(self.helpAbout)
        self.menubar.Append(tmp_menu, _("&Help"))
        self.SetMenuBar(self.menubar)
        # Menu Bar end
        
    def __bind_events(self):
        self.Bind(wx.EVT_MENU, self.OnClose, self.fileClose)
        self.Bind(wx.EVT_MENU, self.OnQuit, self.fileQuit)
        self.Bind(wx.EVT_MENU, self.OnOptions, self.editOptions)
        self.Bind(wx.EVT_MENU, self.OnHomepage, self.helpHomepage)
        self.Bind(wx.EVT_MENU, self.OnHelpOnline, self.helpOnline)
        self.Bind(wx.EVT_MENU, self.OnTranslate, self.helpTranslate)
        self.Bind(wx.EVT_MENU, self.OnReport, self.helpReport)
        self.Bind(wx.EVT_MENU, self.OnDonate, self.helpDonate)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.helpAbout)

        self.Bind(wx.EVT_MENU, self.OnRefresh, self.projRefresh)
        self.Bind(wx.EVT_MENU, self.OnUpdates, self.projUpdates)
        self.Bind(wx.EVT_MENU, self.OnDownload, self.projDownload)
        self.Bind(wx.EVT_MENU, self.OnDetails, self.projDetails)        
        self.Bind(wx.EVT_MENU, self.OnSources, self.projSources)

        self.Bind(wx.EVT_BUTTON, self.OnDownload, self.downloadButton)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.refreshButton)
        self.Bind(wx.EVT_BUTTON, self.OnUpdates, self.updatesButton)
        self.Bind(wx.EVT_CLOSE, self.Closing)

    def __set_properties(self):
        self.SetSize((700, 500))
        self.statusbar.SetStatusWidths([-1])
        # statusbar fields
        statusbar_fields = [_("Ready")]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)

        attr = wx.TextAttr()
        attr.SetTabs([400])
        self.projectDetails.SetDefaultStyle(attr)

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons.Add(self.downloadButton, 0, wx.ALL, 3)
        sizer_buttons.Add(self.updatesButton, 0, wx.ALL, 3)
        sizer_buttons.Add(self.refreshButton, 0, wx.ALL, 3)
        #sizer_bottom.Add(sizer_buttons, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.buttonPanel.SetSizer(sizer_buttons)

        sizer_project = wx.BoxSizer(wx.VERTICAL)
        sizer_project.Add(self.projectDetails, 1, wx.EXPAND, 0)
        self.project_notebook_pane.SetSizer(sizer_project)
        self.notebook.InsertPage(0, self.project_notebook_pane, _("Project Details"), False, 0)
        sizer_bottom.Add(self.notebook, 1, wx.EXPAND, 0)
        self.panel.SetSizer(sizer_bottom)
        self.notebook.SetSelection(0)

        self.splitter.SplitHorizontally(self.list, self.panel)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND, 0)
        sizer.Add(self.splitter, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()

    def OnShowPopup(self, evt):
        pos = evt.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def Closing(self, event): # Cleanup cleanup, everybody do your share
        #self.thread.StopThreads()
        #self.thread.Destroy()
        log.info(_('Cleaning up plugins'))
        for name, instance, type, version in plugins.InterfacePluginList: instance.cleanup()
        log.info(_('Shutting down'))
        self.Destroy()

    def OnClose(self, event):
        self.list.DeleteAllItems()
        self.projectDetails.Clear()
        self.list.tabpage.SetPackage()
        start = startDialog(None, -1, '')
        success = start.ShowModal()
        start.Destroy()
        
        if success == wx.ID_CANCEL:
            self.Close()
        else:
            self.Refresh(project.projects[len(project.projects) - 1].GetData())

    def OnQuit(self, event):       self.Close()
    def OnHomepage(self, event):   lib.browserOpen(consts.urlHomepage)
    def OnHelpOnline(self, event): lib.browserOpen(consts.urlHelp)
    def OnTranslate(self, event):  lib.browserOpen(consts.urlTranslate)
    def OnReport(self, event):     lib.browserOpen(consts.urlBug)
    def OnDonate(self, event):     lib.browserOpen(consts.urlDonate)
    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        
        info.SetIcon(wx.Icon(consts.fileLogo, wx.BITMAP_TYPE_PNG))
        info.SetName(consts.appName)
        info.SetVersion(consts.appVersion)
        info.SetDescription(consts.description)
        info.SetCopyright(consts.copyright)
        info.SetWebSite(consts.urlHomepage)
        info.SetLicence(consts.license)
        info.AddDeveloper(consts.authors)
        info.AddDocWriter(consts.docwriters)
        info.AddArtist(consts.artists)
        info.AddTranslator(consts.translators)

        wx.AboutBox(info)
    
    def OnSources(self, event):
        proj = project.projects[len(project.projects) - 1]      
        name = proj.getSources() + _(' - Sources Editor')
        edit = FileEditor(name, proj.getSources())
        if edit.ShowModal() == wx.ID_OK:
            edit.txt.SaveFile(proj.getSources())
            if wx.MessageBox(_("Sources have changed. Would you like to reload the package list?"), _("Save Successful"), wx.YES_NO) == 2: #wx.ID_YES:
                self.OnRefresh(None)          
        edit.Destroy()

    def OnOptions(self, event):
        options = optionDialog(None, -1, '')
        if options.ShowModal() == wx.ID_OK:
            # Set settings
            consts.proxy_enabled = options.proxyCheckBox.GetValue()
            conf = open(consts.file_config, 'w')
            conf.write('LogDir=' + options.logCtrl.GetValue() + '\n' +
                        #'LocaleDir=' + options.localeCtrl.GetValue() + '\n' +
                        #'PackagesDir=' + options.packagesCtrl.GetValue() + '\n' +
                        'PluginsDir=' + options.pluginsCtrl.GetValue() + '\n' +
                        'ProjectsDir=' + options.projectsCtrl.GetValue() + '\n' +
                        'PixmapsDir=' + options.pixmapsCtrl.GetValue() + '\n' +
                        'ThemesDir=' + options.themesCtrl.GetValue() + '\n' +
                        'DefaultTheme=' + options.defaultThemeCtrl.GetValue() + '\n' +
                        'CurrentTheme=' + options.defaultThemeCtrl.GetValue() + '\n')
                        
            if options.proxyCheckBox.GetValue():
                consts.http_proxy = {'http': options.proxy_url.GetValue()}
                conf.write('HTTPProxy=' + options.proxy_url.GetValue() + '\n' +
                           'ProxyUsername=' + options.proxy_username.GetValue() + '\n' +
                           'ProxyPassword=' + options.proxy_password.GetValue() + '\n')
            conf.close()
            wx.MessageBox(_("If you changed a folder location, changes take affect after restarting Keryx."), _("Saved Changes"))
        options.Destroy()

    def OnDownload(self, event):
        # Downloads selected package and dependencies
        try:
            selected = self.list.GetSelectedItem()
            if selected: files = project.projects[len(project.projects) - 1].getDependencies(selected[1])
        except: return

        # Generate filename list, max 6 entries
        list = "\n\n"
        for i in range(len(files)): 
            if i <= 5: list += files[i][0] + "\n"
            else:
                list += "..."
                break 

        # Confirm downloads
        dlg = wx.MessageDialog(None, _("Do you wish to download the following") + " " + str(len(files)) + " " + _("files?") + list,
                          _("Confirm Downloads"), wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        
        # User doesn't want to download them
        if result == wx.ID_NO: 
            self.Refresh(project.projects[len(project.projects) -1].GetData())
            #self.downloadedLists()
            return 
        
        # Make sure packages directory exists
        dir = os.path.join(project.projects[len(project.projects) -1].dir, 'packages')
        if not os.path.exists(dir):
            os.mkdir(dir)
            
        #########################################################
        # FIXME: Return to the plugin for post download cleanup #
        #########################################################
        frame = download(self, None, files)
        #self.downloads.files = files
        #self.thread.start(self, self.downloads.start, None) #self.downloadedLsts) # Do nothing after the packages are downloaded
        #a.start(self, lists.start, None) # New thread

        # If it fails, reset the package lists, in other words, reload the list again.

        #self.download.downloads = files
        #self.download.start()

        #FIXME: If any package fails to download, set package installed version to blank 

    def OnUpdates(self, event):
        updates = []
        files = []
        for (key, value) in project.projects[len(project.projects) - 1].packages.iteritems():
            if value[0] == 1: updates.append(key)
        
        # Make sure we have updates
        if len(updates) == 0:
            return wx.MessageBox(_("No updates available. Your computer is up-to-date."),_("No updates"))

        # Got a list of package names, lets generate a list of filenames to download
        for item in updates:
            files += project.projects[len(project.projects) - 1].getDependencies(item)

        # Make sure packages directory exists
        dir = os.path.join(project.projects[len(project.projects) - 1].dir, 'packages')
        if not os.path.exists(dir):
            os.mkdir(dir)

        frame = download(self, None, files)
        
    def OnDetails(self, event):
        for i in range(self.notebook.GetPageCount()): # Find the details page and select it
            if self.notebook.GetPageText(i) == _("Package Details"): self.notebook.SetSelection(i)
        
#    def OnOpen(self, event):
#        dlg = wx.FileDialog(self, message=_("Choose a file"),
#            defaultDir=consts.dirProjects, 
#            defaultFile="",
#            wildcard=consts.wildcard,
#            style=wx.OPEN | wx.CHANGE_DIR)

#        # Show the dialog and retrieve the user response. If it is the OK response, 
#        # process the data
#        if dlg.ShowModal() == wx.ID_OK:
#            paths = dlg.GetPaths()
#            data = project.openKeryx(paths[0])
#            dlg.Destroy()
#            if data:
#                proj = project.project(data[0], data[1], data[2],  data[3], data[4], data[5], data[6], data[7])
#                project.projects[len(project.projects) -1] = proj # variable must be initialized
#                self.Refresh(project.projects[len(project.projects) -1].GetData())
            
#    def OnNew(self, event):
#        dlg = wx.TextEntryDialog(self, _("What would you like to name your new project?"),
#                _('New Project'), platform.node())
#        if dlg.ShowModal() == wx.ID_OK:
#            response = dlg.GetValue()
#            #print response
#        dlg.Destroy()

    def OnRefresh(self, event): self.Refresh(project.projects[len(project.projects) -1].GetData())
    def Refresh(self, data):
        self.SetTitle(data[0] + " - " + consts.appName + " v" + consts.appVersion)
        self.projectDetails.Clear()
        self.projectDetails.AppendText(data[0] + '\n')
        if data[2] != '': self.projectDetails.AppendText(_("Operating System:") + '\t' + data[2] + '\n')
        if data[3] != '': self.projectDetails.AppendText(_("Version:") + '\t' + data[3] + '\n')
        if data[4] != '': self.projectDetails.AppendText(_("Kernel:") + '\t' + data[5] + '\n')
        if data[5] != '': self.projectDetails.AppendText(_("Architecture:") + '\t' + data[4] + '\n')
        self.projectDetails.AppendText(_("Drive Free Space:") + '\t' + lib.driveFreeSpace() + '\n')
        #self.projectDetails.AppendText("%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s" % 
        #    (data[0], os, data[2], v, data[3], k, data[4], a, data[5], f, lib.driveFreeSpace()))
                    
        points = self.projectDetails.GetFont().GetPointSize()
        style = wx.Font(points, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.projectDetails.SetStyle(0, len(data[0]), wx.TextAttr("black", wx.NullColour, style))

        # Inquire whether latest package list should be downloaded
        dlg = wx.MessageDialog(None, _('Download the latest package list?'),
                          _("Download latest?"), wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()

        # Load package list
        self.SetStatusText(_("Loading packages") + "...", 0)
    
        if result == wx.ID_YES: frame = download(self, self.loadLocal, project.projects[len(project.projects) -1].getUrls(), True)
        else:                   self.loadLocal()

    def loadLocal(self, result=None):
        #TODO: Verify downloads?
        thread(self, project.projects[len(project.projects) - 1].loadLocal, self.loadPackages)

    def loadPackages(self, result=None):
        proj = project.projects[len(project.projects) - 1]
        #self.thread.Start(project.LocalPackagesThread(proj), None)
        self.list.SetMap(proj.packages)
        self.list.SortListItems(1, 1) # Sort column 1, ascending A->Z order

        self.SetStatusText(str(len(proj.packages.keys())) + " " + _("Packages"),0)

# end of class MainApp
