"""
    Informer Agents
    
    Each Informer retrieves information related to a specific track
    using the "track.getinfo" method from the web service
    
    Messages In:
    ------------
    - "username"
    - "track_batch"
    
    
    Messages Out:
    ------------
    - "track_info"

    
    @author: jldupont
    @date: May 20, 2010
"""
from app.system.tbase import AgentThreadedBase
from app.lastfmparsers.track_getinfo import parse
import urllib
import urllib2

__all__=[]



class InformerAgent(AgentThreadedBase):
    
    TS=0
    CREATED=1
    UPDATED=2
    PLAYCOUT=3
    TRACK_NAME=4
    TRACK_MBID=5
    ARTIST=6
    ARTIST_MBID=7
    ALBUM=8
    ALBUM_MBID=9
    
    TIMEOUT = 10
    TRACK_GETINFO_URL="http://ws.audioscrobbler.com/2.0/?method=track.getinfo&artist=%s&track=%s&username=%s&api_key="
    API_KEY="50fa3794354dd9d42fc251416f523388"
    
    def __init__(self, even=True):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)
        self.even=even
        self.username=""
        self.url = self.TRACK_GETINFO_URL + self.API_KEY
        
    def h_shutdown(self):
        print "Informer - shutdown"        
        
    def h_username(self, username):
        self.username=username
        
    def h_track_batch(self, batch):
        #print "informer.h_track_batch: batch: %s" % str(batch)
        try:    count=len(batch)
        except: count=0
        
        if count==0:
            return

        #self.pub("log", "Informer - Fetching Info on %s tracks" % str(count))
        
        for item in batch:
            ts=int(item[self.TS])
            if self.isMine(ts):
                artist=item[self.ARTIST]
                track=item[self.TRACK_NAME]
                self.do_fetch(track, artist)
                
            
    def isMine(self, ts):
        """
        Pick which Informer gets this job
        """
        even=ts % 2
        if self.even and even==0:
            return True
        
        if not self.even and even==1:
            return True
        
        return False
            
    def genUrl(self, track, artist):
        try:    ua=urllib.quote_plus(self.username.encode("utf-8"))
        except: 
            ua=""
            self.pub("log", "warning", "Trouble URL encoding username: %s" % self.username)
        
        try:    et=urllib.quote_plus(track.encode("utf-8"))
        except Exception,_e:
            et=""
            self.pub("log", "warning", "Trouble URL encoding track: %s" % track)
            
        try:   ea=urllib.quote_plus(artist.encode("utf-8"))
        except Exception,_e:
            ea=""
            self.pub("log", "warning", "Trouble URL encoding artist: %s" % artist)            

            
        return self.url % (ea, et, ua)
        
    def do_fetch(self, track, artist):
        
        url=self.genUrl(track, artist)
        
        try:
            raw=urllib2.urlopen(url, None, self.TIMEOUT)
            resp=raw.read()
        except Exception,e:
            self.pub("errorFetchInfo", str(e))
            return
            
        try:
            rinfo=parse(resp)
        except Exception,e:
            self.pub("errorParsingInfo", str(e))
            return

        """
        {u'userloved': u'0', 
        u'name': u'Little 15', 
        'artist.name': u'Depeche Mode', 
        u'url': u'http://www.last.fm/music/Depeche+Mode/_/Little+15', 
        'artist.url': u'http://www.last.fm/music/Depeche+Mode', 
        'tags': [{'tag.name': u'electronic', 'tag.url': u'http://www.last.fm/tag/electronic'}, {'tag.name': u'new wave', 'tag.url': u'http://www.last.fm/tag/new%20wave'}, {'tag.name': u'synthpop', 'tag.url': u'http://www.last.fm/tag/synthpop'}, {'tag.name': u'80s', 'tag.url': u'http://www.last.fm/tag/80s'}], 
        u'id': u'12150', 
        'album.artist': u'Depeche Mode', 
        u'mbid': u'', 
        'album.url': u'http://www.last.fm/music/Depeche+Mode/Music+for+the+Masses', 
        'album.mbid': u'8d059e75-d9bb-4d90-97a9-1cb6ed7472c6', 
        'album.title': u'Music for the Masses', 
        'artist.mbid': u'8538e728-ca0b-4321-b7e5-cff6565dd4c0', 
        u'playcount': u'400988', 
        u'userplaycount': u'9'}
        """

        self.pub("track_info", rinfo)

## ============================================================================

_1=InformerAgent(True)
_1.start()

_2=InformerAgent(False)
_2.start()
