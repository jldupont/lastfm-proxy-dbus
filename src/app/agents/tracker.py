"""
    Tracker
    
    Maintains the 'unique tracks' table

    Messages In:
    ------------
    - "tick"
    - "track_info"
    
    Messages Out:
    ------------
    - "unique_track"
    - "uniqueTracksCount"
    

    @author: jldupont
    @date: May 21, 2010
"""
from app.system.tbase import AgentThreadedBase
from app.system.db    import UserTracksDb

__all__=[]


class TrackerAgent(AgentThreadedBase):
    
    INTERVAL = 4*5 ##seconds
    
    def __init__(self):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)
        self.db=None
        self.count = 0
        self.rowCount=0

    def h_shutdown(self):
        print "Tracker - shutdown"

    def h_tick(self, *_):
        self.count += 1

        if self.count > self.INTERVAL:
            self.count = 0
            rowCount=self.getCount()
            
            if rowCount is not None:
                self.pub("uniqueTracksCount", rowCount)

            if rowCount != self.rowCount:
                self.rowCount=rowCount
                self.pub("log", "Tracker - Unique Tracks count(%s)" % str(rowCount))
            
            
    def getCount(self):
        try: self.db=UserTracksDb()
        except: self.db=None
        
        if self.db is not None:
            count = self.db.UniqueTracks_getRowCount()
        else:
            count = None
            
        return count
            

    def h_track_info(self, track_info):
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
        ti=track_info

        try:    track_name=ti["name"]
        except: track_name=""
                
        try:    artist_name=ti["artist.name"]
        except: artist_name=""
        
        try:    mbid=ti["mbid"]
        except: mbid=""
        
        try:    album=ti["album.title"]
        except: album= ""

        try:    album_mbid=ti["album.mbid"]
        except: album_mbid= ""

        try:    artist_mbid=ti["artist.mbid"]
        except: artist_mbid= ""
            
        try:    userplaycount=ti["userplaycount"]
        except: userplaycount=0
        
        if track_name=="" or artist_name=="":
            self.pub("log", "warning", "Tracker - detected bad track_info")
            return
        
        record=[userplaycount,
                track_name, mbid,
                artist_name, artist_mbid,
                album, album_mbid, 
                ]
            
        self.pub("unique_track", artist_name, track_name, record)


_=TrackerAgent()
_.start()
