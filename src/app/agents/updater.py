"""
    Updater Agent
    
    Messages In:
    ------------
    - "tick"
    - "track_info"
    
    Messages Out:
    ------------
    - "track_to_update"
    - "track_batch"
    - "toUpdateCount"
    
    @author: jldupont
    @date: May 20, 2010
"""
import time
from app.system.tbase import AgentThreadedBase
from app.system.db    import UserTracksDb

__all__=[]



class UpdaterAgent(AgentThreadedBase):
    
    INTERVAL=10*15
    
    def __init__(self):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)
        self.count=0
        self.db=None

    def h_shutdown(self):
        print "Updater - shutdown"

    def h_tick(self, _count):
        self.count += 1
    
        if self.count > self.INTERVAL:
            self.do_update()
            self.count=0
            
    def _setupDb(self):
        if self.db is None:
            try:    self.db=UserTracksDb()
            except: self.db=None
        
            
    def do_update(self):
        self._setupDb()
        if self.db is None:
            return
            
        batch=self.db.findNextToUpdate()
        self.pub("track_batch", batch)
        
        total=self.db.getToUpdateCount()
        self.pub("toUpdateCount", total)
        
        if total > 0:
            self.pub("log", "Updater - # tracks to update: %s" % str(total))
        
    def h_track_info(self, track_info):
        track=track_info["name"]
        artist=track_info["artist.name"]        
        
        #print "updater.track_info: artist(%s) track(%s)" % (artist, track)
        try:
            playcount=int(track_info["userplaycount"])
        except Exception,e:
            self.pub("log", "warning", "Updater - track_info with missing field(%s), artist(%s) track(%s)" % (e, artist, track))
            playcount=0
            
        ts=int(time.time())
        self.pub("track_to_update", ts, track, artist, playcount)


_=UpdaterAgent()
_.start()
