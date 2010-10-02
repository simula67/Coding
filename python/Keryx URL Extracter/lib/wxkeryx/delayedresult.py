import lib, os.path, wx
import wx.lib.delayedresult as delayedresult
from lib import consts, log

class thread(wx.Frame):
    """This demos simplistic use of delayedresult module."""
    def __init__(self, parent, func, endfunc):
        wx.Frame.__init__(self, None, title=_("Loading..."))
        self.parent = parent
        self.function = func
        self.endfunction = endfunc

        self.SetIcon(wx.Icon(consts.fileIco, wx.BITMAP_TYPE_ICO))
        panel = wx.Panel(self)
        loading = wx.StaticText(panel, -1, _("This may take a while. Please be patient."))
        self.gauge = wx.Gauge(panel)
        #cancelBtn  = wx.Button(panel, -1, "Cancel")
        
        #self.cur = wx.StaticText(panel, -1, "Current Transfer:")
        #self.cur.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        #self.current = wx.StaticText(panel)
        #self.download_gauge = wx.Gauge(panel)
        #self.status = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        
        #status = wx.BoxSizer()
        #status.Add(self.cur, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        #status.Add(self.current, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(loading, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        main.Add(self.gauge, 0, wx.EXPAND|wx.ALL, 5)
        #main.Add(status)
        #main.Add(self.download_gauge, 0, wx.EXPAND|wx.ALL, 5)
        #main.Add(self.status, 1, wx.EXPAND|wx.ALL, 5)
        #main.Add(cancelBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        panel.SetSizer(main)
        self.SetSize(wx.Size(300,100))
        self.Center()
        self.Show()

        self.jobID = 0
        self.abortEvent = delayedresult.AbortEvent()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #self.Bind(wx.EVT_BUTTON, self.handleAbort, cancelBtn)
        self.Bind(wx.EVT_TIMER, self.TimerHandler)

        self.timer = wx.Timer(self)
        self.timer.Start(100)
        
        self.parent.Enable(False)
        self.handleGet(None)

    def TimerHandler(self, event): self.gauge.Pulse()
        
    def OnClose(self, event):
        """Only needed because in demo, closing the window does not kill the 
        app, so worker thread continues and sends result to dead frame; normally
        your app would exit so this would not happen."""
        #if self.buttonAbort.IsEnabled():
            #self.log( "Exiting: Aborting job %s" % self.jobID )
            #self.handleAbort(None)
        self.Show()
            
    def handleGet(self, event): 
        """Compute result in separate thread, doesn't affect GUI response."""
        #self.buttonGet.Enable(False)
        #self.buttonAbort.Enable(True)
        self.abortEvent.clear()
        self.jobID += 1
        
        #log.info( "Starting job %s in producer thread: GUI remains responsive"
        #          % self.jobID )
        delayedresult.startWorker(self._resultConsumer, self.function, 
                                  wargs=(self.jobID,self.abortEvent), jobID=self.jobID)

                                                
    def _resultProducer(self, jobID, abortEvent):
        """Downloads the files in self.files"""
        
        msg = "Downloading %i file(s)\n" % len(self.files)
        wx.CallAfter(self.LogMessage, msg)

        success = True
        for data in self.files:
            if abortEvent(): return [1, self.files]

            url = data[0]
            file = data[1]
            end = url.split('/')
            protocol = end[0] + '//'
            site = end[2]
            end = end[len(end) - 1]

            msg = "%s%s    %s" % (protocol, site, end)
            wx.CallAfter(self.SetFile, msg)

            try: # Attempt to download the file
                urllib.urlretrieve(url, file, self.progress)
                #TODO: Generate md5hashes for these files
                
                msg = "Success: %s\nSaved to: %s\n" % (url, file)
                wx.CallAfter(self.LogMessage, msg)
    
            except IOError, e: # Failed downloading
                success = False
                msg = "Failed: %s\nReason: %s\n" % (url, str(e))
                wx.CallAfter(self.LogMessage, msg)

        if success == True: 
            wx.CallAfter(self.DisplayMessage,_("All downloads have been completed successfully."), _("Download Complete"))
            result = [0,self.files]
        else:
            wx.CallAfter(self.DisplayMessage, _("Some downloads failed to complete.") + "\n" +_("Please check") + " " + os.path.join(consts.dirLog, "log") + " " + _("for more details."), _("Download Failed"))
            result = [1,self.files]
        return result

    def progress(self, blocks, size, total):
        if blocks*size > total: fraction = float(total)/float(total)
        else:                   fraction = float(blocks*size)/float(total)
        
        wx.CallAfter(self.SetGauge, int(round(fraction*100,2)))

    def LogMessage(self, msg):
        log.info(msg)
        self.status.AppendText(msg)
    def DisplayMessage(self, msg, caption): wx.MessageBox(msg, caption)
    def SetGauge(self, val): self.download_gauge.SetValue(val)
    def SetFile(self, val): self.current.SetLabel(val)

    def handleAbort(self, event): 
        """Abort the result computation."""
        log.info( "Aborting result for job %s" % self.jobID )
        #self.buttonGet.Enable(True)
        #self.buttonAbort.Enable(False)
        self.abortEvent.set()

        
    def _resultConsumer(self, delayedResult):
        jobID = delayedResult.getJobID()
        assert jobID == self.jobID
        try:
            result = delayedResult.get()
        except Exception, exc:
            log.info( "Result for job %s raised exception: %s" % (jobID, exc) )
            return
        
        # output result
        #log.info( "Got result for job %s: %s" % (jobID, result) )
        self.parent.Enable()
        self.Destroy()
        if self.endfunction: self.endfunction()
