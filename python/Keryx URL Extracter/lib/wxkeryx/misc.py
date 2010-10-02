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

import lib, os.path, urllib, wx
import wx.lib.delayedresult as delayedresult
import wx.lib.mixins.listctrl  as  listmix
from lib import consts, log

class VirtualList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, tabpage, data = {}):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_SINGLE_SEL|wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
        self.tabpage = tabpage
        # Add some art
        self.il = wx.ImageList(16, 16)
        self.sm_up = self.il.Add(wx.Bitmap(consts.icon_arrow_up))
        self.sm_dn = self.il.Add(wx.Bitmap(consts.icon_arrow_down))
        self.uptodate = self.il.Add(wx.Bitmap(consts.icon_uptodate))
        self.update = self.il.Add(wx.Bitmap(consts.icon_update))
        self.error = self.il.Add(wx.Bitmap(consts.icon_error))
        self.downloaded = self.il.Add(wx.Bitmap(consts.icon_downloaded))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        # Add some attributes (colourful background for each item rows)
        self.attrUpdate = wx.ListItemAttr()
        self.attrUpdate.SetBackgroundColour("light blue") # blue
        self.attrUptodate = wx.ListItemAttr()
        self.attrUptodate.SetBackgroundColour(wx.Color(150, 235, 140)) # green
        self.attrError = wx.ListItemAttr()
        self.attrError.SetBackgroundColour(wx.Color(255, 118, 106)) # red
        self.attrDownloaded = wx.ListItemAttr()
        self.attrDownloaded.SetBackgroundColour(wx.Color(255, 215, 100)) # yellow

        # Build the columns
        count = 0
        for title, width in consts.columns:
            self.InsertColumn(count, title)
            self.SetColumnWidth(count, width)
            count += 1
        #self.InsertColumn(0, _("S"))
        #self.InsertColumn(1, _("Package Name"))
        #self.InsertColumn(2, _("Installed Version"))
        #self.InsertColumn(3, _("Latest Version"))
        #self.InsertColumn(4, _("Description"))
        
        #self.SetColumnWidth(0, 50)
        #self.SetColumnWidth(1, 200)
        #self.SetColumnWidth(2, 200)
        #self.SetColumnWidth(3, 200)
        #self.SetColumnWidth(4, 200)

        #These two should probably be passed to init more cleanly
        #setting the numbers of items = number of elements in the dictionary
        self.SetMap(data)
        self.currentItem = None

        #mixins
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, 3)

        #sort by genre (column 2), A->Z ascending order (1)
        #self.SortListItems(0, 1)
       
        #events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)

    def SetMap(self, dataMap):
        self.itemDataMap = dataMap
        self.itemIndexMap = dataMap.keys()
        self.SetItemCount(len(dataMap))
        self.tabpage.SetPackage()
        self.Refresh()
        
    def OnColClick(self,event): event.Skip()

    def GetSelectedItem(self): return self.itemDataMap[self.itemIndexMap[self.currentItem]]
    
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        index=self.itemIndexMap[self.currentItem]
        self.tabpage.SetPackage(self.itemDataMap[index])

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        #print 'item activated'

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemDeselected(self, evt):
        pass

    def OnGetItemText(self, item, col):
        index=self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s

    def OnGetItemImage(self, item):
        index=self.itemIndexMap[item]
        icon=self.itemDataMap[index][0]

        if icon==0:
            return self.uptodate
        elif icon==1:
            return self.update
        elif icon==2:
            return self.error
        elif icon==3:
            return self.downloaded
        else:
            return -1

    def OnGetItemAttr(self, item):
        index=self.itemIndexMap[item]
        update=self.itemDataMap[index][0]

        if update==0:
            return self.attrUptodate
        elif update==1:
            return self.attrUpdate
        elif update==2:
            return self.attrError
        elif update==3:
            return self.attrDownloaded
        else:
            return None

    def SortItems(self,sorter=cmp):
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items
        
        # redraw the list
        self.Refresh()

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self): return self

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self): return (self.sm_dn, self.sm_up)
    
# end of class VirtualList
        
class detailsTab():
    def __init__(self, notebook):
        self.notebook = notebook
        self.pane = wx.Panel(self.notebook, -1, style=wx.TAB_TRAVERSAL)
        index = self.notebook.GetImageList().Add(wx.Bitmap(consts.icon_package))
        self.details = wx.TextCtrl(self.pane, style = wx.TE_MULTILINE | wx.TE_RICH | wx.TE_READONLY)

        attr = wx.TextAttr()
        attr.SetTabs([400])
        self.details.SetDefaultStyle(attr)

        sizer = wx.BoxSizer()
        sizer.Add(self.details, 1, wx.EXPAND, 0)
        self.pane.SetSizer(sizer)
        self.notebook.AddPage(self.pane, _("Package Details"), False, index)

    def SetPackage(self, stats = ['','','','','','','',0]):
        self.details.Clear()
        if stats[1] == '': return

        update = stats[0]
        name = stats[1]
        inst = stats[2]
        latest = stats[3]
        descrip = stats[4]
        depends = stats[5]
        filename = stats[6]
        size = lib.convert_file_size(stats[7])
        
        if not name == '': self.details.AppendText(name + '\n')
        if not descrip == '': self.details.AppendText(_("Description:\t") + descrip + '\n')
        if not inst == '': self.details.AppendText(_("Installed Version:\t") + inst + '\n')
        if not latest == '': self.details.AppendText(_("Latest Version:\t") + latest + '\n')
        if not depends =='': self.details.AppendText(_("Dependencies:\t") + depends + '\n')
        if not size == '': self.details.AppendText(_("Size:\t") + size + '\n')
        if not filename == '': self.details.AppendText(_("Filename:\t") + filename + '\n')
        #self.details.AppendText("%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s" % 
        #    (name, d, descrip, i, inst, l, latest, dep, depends, s, size, f, filename))

        # Fixes scrolling issue
        self.details.ScrollLines(-15)

        points = self.details.GetFont().GetPointSize()
        style = wx.Font(points, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.details.SetStyle(0, len(name), wx.TextAttr("black", wx.NullColour, style))
        
# end of class detailsTab

class ProportionalSplitter(wx.SplitterWindow):
        def __init__(self,parent, id = -1, proportion=0.60, size = wx.DefaultSize, **kwargs):
                wx.SplitterWindow.__init__(self,parent,id,wx.Point(0, 0),size, **kwargs)
                self.SetMinimumPaneSize(50) #the minimum size of a pane.
                self.proportion = proportion
                if not 0 < self.proportion < 1:
                        raise ValueError, "proportion value for ProportionalSplitter must be between 0 and 1."
                self.ResetSash()
                self.Bind(wx.EVT_SIZE, self.OnReSize)
                self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged, id=id)
                ##hack to set sizes on first paint event
                self.Bind(wx.EVT_PAINT, self.OnPaint)
                self.firstpaint = True

        def SplitHorizontally(self, win1, win2):
                if self.GetParent() is None: return False
                return wx.SplitterWindow.SplitHorizontally(self, win1, win2,
                        int(round(self.GetParent().GetSize().GetHeight() * self.proportion)))

        def SplitVertically(self, win1, win2):
                if self.GetParent() is None: return False
                return wx.SplitterWindow.SplitVertically(self, win1, win2,
                        int(round(self.GetParent().GetSize().GetWidth() * self.proportion)))

        def GetExpectedSashPosition(self):
                if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
                else:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
                return int(round(tot * self.proportion))

        def ResetSash(self):
                self.SetSashPosition(self.GetExpectedSashPosition())

        def OnReSize(self, event):
                "Window has been resized, so we need to adjust the sash based on self.proportion."
                self.ResetSash()
                event.Skip()

        def OnSashChanged(self, event):
                "We'll change self.proportion now based on where user dragged the sash."
                pos = float(self.GetSashPosition())
                if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().height)
                else:
                        tot = max(self.GetMinimumPaneSize(),self.GetParent().GetClientSize().width)
                self.proportion = pos / tot
                event.Skip()

        def OnPaint(self,event):
                if self.firstpaint:
                        if self.GetSashPosition() != self.GetExpectedSashPosition():
                                self.ResetSash()
                        self.firstpaint = False
                event.Skip()
                
# end of class ProportionalSplitter

