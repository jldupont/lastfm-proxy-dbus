"""
    @date: May 14, 2010
    @author: jldupont
"""
APP_NAME="lastfm-proxy-dbus"
APP_ICON = "lastfm-proxy-dbus"
ICON_PATH="/usr/share/icons/"
ICON_FILE=APP_NAME+".png"
ICON_FILE_WARNING=APP_NAME+"-warning.png"
LOG_PATH="~/"+APP_NAME+".log"
#DB_PATH ="~/"+APP_NAME+".sqlite"
HELP_URL="http://www.systemical.com/doc/opensource/"+APP_NAME
#TIME_BASE=250  ##milliseconds
#TICKS_SECOND=1000/TIME_BASE


import os
import sys
import time
import gobject
import dbus.glib
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

gobject.threads_init()
dbus.glib.init_threads()

## For development environment
ppkg=os.path.abspath( os.getcwd() +"/app")
if os.path.exists(ppkg):
    sys.path.insert(0, ppkg)


from Tkinter import * #@UnusedWildImport
from Queue import Queue, Empty
import webbrowser
        
from   app.system.tbase import mdispatch
import app.system.mswitch as mswitch

        
class App(Frame): 
    
    UMSG_TIMEOUT=90
    
    def __init__(self):
        Frame.__init__(self, None) 
        
        self.loop=None
        self.quitting=False
        
        self.iq=Queue()
        self.isq=Queue()
        self.count=0
        
        self.grid()
        
        self.luser=Label(self, text="Username:")
        self.euser=Label(self, text="", width=20, relief=GROOVE, borderwidth=2)
        
        self.luser.grid(row=0, column=0)
        self.euser.grid(row=0, column=1)
        
        #self.master.grid_columnconfigure(0, weight=1)
        #self.master.grid_columnconfigure(1, weight=1)
        #self.master.grid_columnconfigure(2, weight=1)
     
        #self.master.grid_rowconfigure(0,    weight=1)
        #self.master.grid_rowconfigure(1,    weight=1)
        #self.master.grid_rowconfigure(2,    weight=1)
        
        self.dbCountLabel=Label(self, text="Db Recent Tracks:")
        self.dbCountEntry=Label(self, text="", width=20, relief=GROOVE, borderwidth=2)

        self.dbCountLabel.grid(row=2, column=0)
        self.dbCountEntry.grid(row=2, column=1)

        self.rtCountLabel=Label(self, text="Last.fm Recent Tracks:")
        self.rtCountEntry=Label(self, text="", width=20, relief=GROOVE, borderwidth=2)

        self.rtCountLabel.grid(row=3, column=0)
        self.rtCountEntry.grid(row=3, column=1)

        self.toUpdateLabel=Label(self, text="Tracks to update:")
        self.toUpdateEntry=Label(self, text="", width=20, relief=GROOVE, borderwidth=2)

        self.toUpdateLabel.grid(row=4, column=0)
        self.toUpdateEntry.grid(row=4, column=1)

        self.uniqueTracksCountLabel=Label(self, text="Db Unique Tracks:")
        self.uniqueTracksCountEntry=Label(self, text="", width=20, relief=GROOVE, borderwidth=2)

        self.uniqueTracksCountLabel.grid(row=5, column=0)
        self.uniqueTracksCountEntry.grid(row=5, column=1)

        self.mbox=Message(self, borderwidth=2, relief=GROOVE, aspect=350)#, width=250)
        self.mbox.grid(row=6, column=0, sticky=E+W, columnspan=2)
        #self.mbox.pack()
        
        #self.mbox.config(text="")
        
        self.hbutton=Button(self, text="Help", command=self.do_help)
        self.hbutton.grid(row=7, column=0, columnspan=2)

        #self.hAuthorize=Button(self, text="Authorize", command=self.do_authorize)
        #self.hAuthorize.grid(row=7, column=1)

        
        self.master.title("Last.fm Proxy DBus")
        
        self.master.protocol("WM_DELETE_WINDOW", self.OnHide)
        
        self.userMsgTimeout=0
        
    ## --------------------------------------------------------------
    def do_authorize(self):
        print "Authorize!"
    
    def setLoop(self, loop):
        self.loop=loop
    
    def do_help(self):
        webbrowser.open(HELP_URL)
    
    def OnHide(self):
        self.winfo_toplevel().withdraw()
        
    def setUserMessage(self, str):
        """
        Sets the message in the User Message box
        """
        self.userMsgTimeout=self.UMSG_TIMEOUT
        self.mbox.config(text=str)
             
    def _manageUserMessage(self):
        if self.userMsgTimeout is None:
            return
            
        if self.userMsgTimeout == 0:
            self.setUserMessage("")
            self.userMsgTimeout=None
        else:
            self.userMsgTimeout -= 1
             
    ## ==============================================================
    def h_app_show(self, *_):
        self.winfo_toplevel().deiconify()
        
    def on_destroy(self):
        mswitch.publish(None, "__quit__", None)
        self.quitting=True
        
    def h_default(self, msg, *p, **k):
        ##print "h_default: msg: %s" % str(msg)
        pass
        
    def h_errorDbWriting(self, errorMessage):
        self.setUserMessage("Error writing to database: " + errorMessage)
        
    def h_errorFetch(self, errorMessage):
        self.setUserMessage("Error fetching user's recent tracks: " + errorMessage)
           
    def errorParsing(self, errorMessage):
        self.setUserMessage("Error parsing user's recent tracks: " + errorMessage)
           
    def h_username(self, username):
        self.euser.config(text=username)
           
    def h_errorFetchInfo(self, errorMessage):
        self.setUserMessage("Error fetching track.getInfo: " + errorMessage)
             
    def h_errorParsingInfo(self, errorMessage):
        self.setUserMessage("Error parsing track.getInfo: " + errorMessage)
        
    ## ==============================================================
    def tick(self):
        #print "tick (%s)" % time.time()
        self._manageUserMessage()
        
        while True:
            try:
                envelope=self.isq.get(block=False)
                quit, mtype, handled=mdispatch(self, "__main__", envelope)
                if handled==False:
                    mswitch.publish(self.__class__, "__interest__", (mtype, False, self.isq)) 
                if quit:
                    self.on_destroy()
            except Empty:
                break
            
        burst=5
        while True:
            try:
                envelope=self.iq.get(block=False)
                quit, mtype, handled=mdispatch(self, "__main__", envelope)
                if handled==False:
                    mswitch.publish(self.__class__, "__interest__", (mtype, False, self.iq))
                if quit:
                    self.on_destroy()                    
                burst -= 1
                if burst==0:
                    break
            except Empty:
                break

        self.count += 1
        mswitch.publish("__main__", "tick", self.count)
        
        if self.quitting:
            self.quit()
            self.loop.quit()
        
              
    def h_numPages(self, numPages):
        pass
    
    def h_lastfmRecentTracksCount(self, count):
        self.rtCountEntry.config(text=count)
    
    def h_totalDbTracks(self, count):
        self.dbCountEntry.config(text=count)
              
    def h_toUpdateCount(self, count):
        self.toUpdateEntry.config(text=count)
              
    def h_uniqueTracksCount(self, count):
        self.uniqueTracksCountEntry.config(text=count)
              
    def main(self):
        """
        Run main application window
        """ 
        mswitch.subscribe(self.iq, self.isq)
        
        self.tick()
        #self.mainloop()
        

## -------------------------------------------------------------------

from app.agents.tray import TrayAgent
_ta=TrayAgent(APP_NAME, ICON_PATH, ICON_FILE, ICON_FILE_WARNING)
_ta.start()

from app.agents.logger import LoggerAgent
_la=LoggerAgent(APP_NAME, LOG_PATH)
_la.start()
        
import app.agents.fetcher   #@UnusedImport
import app.agents.user      #@UnusedImport
import app.agents.dbwriter  #@UnusedImport
import app.agents.jwalker   #@UnusedImport
import app.agents.updater   #@UnusedImport
import app.agents.informer  #@UnusedImport
import app.agents.tracker   #@UnusedImport
import app.agents.adbus     #@UnusedImport
import app.agents.tester    #@UnusedImport

app=App()
app.main()
    
def refreshTkinter():
    app.tick()
    app.update()
    return True
    
gobject.timeout_add(100, refreshTkinter)
loop = gobject.MainLoop()

app.setLoop(loop)
loop.run()
