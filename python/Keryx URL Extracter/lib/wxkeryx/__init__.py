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

import wx
from lib import consts, log, project
from main import MainApp
from startDialog import startDialog

class wxKeryx(wx.App):
    def OnInit(self):
        log.info(_('wxWidgets interface loaded'))
        wx.InitAllImageHandlers()
        main = MainApp(None, -1, consts.appName + " v" + consts.appVersion)
        self.SetTopWindow(main)
        main.Show()
        main.SetFocus()
        
        start = startDialog(None, -1, '')
        success = start.ShowModal()
        start.Destroy()
        
        if success == wx.ID_CANCEL: main.Close()
        else:
            main.Refresh(project.projects[len(project.projects) - 1].GetData())
            self.MainLoop()
        return 1

# end of class wxKeryx

def Start():
#    import gettext
#    gettext.install(consts.appNameShort)
    keryx = wxKeryx(0)
