"""
    DBus Agent
    
    @author: jldupont
    @date: May 21, 2010
"""
import dbus.service
    
from app.system.tbase import AgentThreadedBase
from app.system.platform import isLinux
from app.system.db import UserTracksDb

__all__=[]


if isLinux():
    class SignalRx(dbus.service.Object):
        """
        DBus signals for the /Player path
        """
        PATH="/Records"
        
        def __init__(self):
            dbus.service.Object.__init__(self, dbus.SessionBus(), self.PATH)
            self.db=None
            
            dbus.Bus().add_signal_receiver(self.sQRecords,
                                           signal_name="qRecords",
                                           dbus_interface="com.jldupont.lastfm.proxy",
                                           bus_name=None,
                                           path="/Records"
                                           )            
    
        @dbus.service.signal(dbus_interface="com.jldupont.lastfm.proxy", signature="aa{sv}")
        def Records(self, list_dic):
            """
            Result 'output' signal
            
            A list of dictionaries i.e. array of array of {string:variant} entries
            """
    
 
        def sQRecords(self, ts_start, limit):
            """
            DBus signal handler - /Records/qRecords
            
            @todo: more user friendly error reporting...
            """
            try:     ts=int(ts_start)
            except:  
                print "** expecting integer 'ts_start'"
                return
            
            try:     l=int(limit)
            except:  
                print "** expecting integer 'limit'"
                return
            
            #print "sQRecords: ts_start: %s -- limit: %s" % (ts_start, limit)
            self.setup()
            try:    records=self.db.getRecords(ts, l)
            except: records=None
            
            rs=self.formatRecordSet(records)
            self.Records(rs)
            
        def formatRecordSet(self, records):
            rs=[]
            for r in records:
                id, created, updated, playcount, track_name, track_mbid, artist_name, artist_mbid, album_name, album_mbid=r
                entry={}
                entry["id"]=id
                entry["created"]=created
                entry["updated"]=updated
                entry["playcount"]=playcount
                entry["track_name"]=track_name
                entry["track_mbid"]=track_mbid
                entry["artist_name"]=artist_name
                entry["artist_mbid"]=artist_mbid
                entry["album_name"]=album_name
                entry["album_mbid"]=album_mbid
                rs.append(entry)
                
            return rs
    
        def setup(self):
            if self.db is not None:
                return
            
            try:    self.db=UserTracksDb()
            except: self.db=None
    
        def shutdown(self):
            try:    self.db.close()
            except: pass


    class DbusAgent(AgentThreadedBase):
        
        def __init__(self):
            """
            @param interval: interval in seconds
            """
            AgentThreadedBase.__init__(self)

            self.srx=SignalRx()
            
        def h_shutdown(self):
            print "ADBus - shutdown"


## Only on Linux unfortunately...
if isLinux():
    _=DbusAgent()
    _.start()
