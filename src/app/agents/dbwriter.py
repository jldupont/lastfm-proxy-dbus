"""
    DbWriter

    Messages In:
    -------------
    - "track_to_update"
    - "tracks"
    - "unique_track"
    
    
    Messages Out:
    -------------
    - "track_details"

    @author: jldupont
    @date: May 20, 2010
"""
from app.system.tbase import AgentThreadedBase
from app.system.db import UserTracksDb

__all__=[]


class DbWriter(AgentThreadedBase):
    
    def __init__(self):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)
        self.db=None
        
    def _setup(self):
        try:     self.db=UserTracksDb()
        except:  self.db=None 
        
    def h_shutdown(self):
        try:    self.db.close()
        except: pass
        
        print "DbWriter - shutdown"
        
    def h_track_to_update(self, ts, track, artist, playcount):

        self._setup()
        if self.db is None:
            return
        
        try:
            count=self.db.updateOne(ts, track, artist, playcount)
        except Exception,e:
            self.pub("errorDbWriting", "DbWriter - "+str(e))
            return
        
        self.pub("updated", (artist, track, playcount, count))
        
    def h_unique_track(self, artist_name, track_name, record):
        #print "DbWriter: unique_track: %s - %s" % (artist_name, track_name)
        self._setup()
        if self.db is None:
            return
        
        try:
            new=self.db.UniqueTracks_InsertIfNotExists(*record)
            
            if new:
                self.pub("log", "Tracker - inserted artist(%s) track_name(%s)" % (artist_name, track_name))
        except:
            self.pub("log", "error", "Tracker - Error whilst inserting/updating unique track, artist_name: (%s) track_name: (%s)" % (artist_name, track_name))

        
    def h_tracks(self, page, tracks):
        """
        Handles 'recent tracks' received
        """
        self._setup()
        if self.db is None:
            return
        
        new_ts=[]
        
        for track in tracks:
            
            """
            ts, playcount, 
            track_name, track_mbid,
            artist_name, artist_mbid,
            album_name, album_mbid
            """
            try:    ts=track["date.attrs"]["uts"]
            except: ts=None
            
            if ts is None:
                continue
            
            track_name=track["name"]
            track_mbid=track["mbid"]
            artist_name=track["artist"]
            try:    artist_mbid=track["artist.attrs"]["mbid"]
            except: artist_mbid=""
            album_name=track["album"]
            try:    album_mbid=track["album.attrs"]["mbid"]
            except: album_mbid=""
            
            ## to help the bridge to Musicbrainz-proxy
            self.pub("track_details", artist_name, track_name, album_name)
            
            try:
                new=self.db.insertIfNotExist(ts, -1, 
                                     track_name, track_mbid, 
                                     artist_name, artist_mbid, 
                                     album_name, album_mbid)
                
                if new:
                    new_ts.append(ts)
            except Exception,e:
                self.pub("errorDbWriting", "DbWriter - " + str(e))
        
        total_tracks=self.db.getRowCount()
        
        ## Publish a list of new track timestamp
        ## that were inserted in the database.
        ## This should help compute what we are missing
        self.pub("new_ts", page, total_tracks, new_ts)

        
_f=DbWriter()
_f.start()

