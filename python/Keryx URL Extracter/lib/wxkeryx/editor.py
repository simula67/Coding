import platform, wx
from lib import consts, project

class FileEditor(wx.Dialog):
    def __init__(self, window_name, filename):
        wx.Dialog.__init__(self, None, -1, window_name)#, size=(300, 300))
        self.SetIcon(wx.Icon(consts.fileIco, wx.BITMAP_TYPE_ICO))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)
        self.txt.LoadFile(filename)
        sizer.Add(self.txt, 1, wx.EXPAND|wx.ALL, 3)
        
        # Add buttons
        btnsizer = wx.StdDialogButtonSizer()
        btnSave = wx.Button(self, wx.ID_OK, 'Save')
        btnSave.SetDefault()
        btnsizer.AddButton(btnSave) 
        btnCancel = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btnCancel)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5)

        self.SetSizer(sizer)
        
        if platform.system() != 'Windows':
            self.Bind(wx.EVT_TEXT, self.comment, self.txt)
            self.comment(None)

    def comment(self, event):
        location = 0
        for line in self.txt.GetValue().split('\n'):
            if line.find('#') != -1: # line contains a comment
                self.txt.SetStyle(location + line.index('#'), len(line)+location, wx.TextAttr("RED"))
            location += len(line) + 1
        