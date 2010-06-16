"""
    @author: jldupont
    @date: May 19, 2010
"""
import os
import sqlite3
import time
from app.system.platform import isOSX

__all__=["getDbPath", "UserTracksDb"]


def getDbPath():
    if isOSX():
        path="~/Library/Preferences/lastfm-proxy-dbus.sqlite"
    else:
        path="~/.config/lastfm-proxy-dbus.sqlite"

    return os.path.expanduser(path)


class UserTracksDb(object):
    """
    Fields:
    
    - timestamp
    - updated
    - playcount
    - track name
    - track mbid
    - artist name
    - artist mbid
    - album name
    - album mbid
    """
    def __init__(self):
        
        path=getDbPath()
        self.conn=sqlite3.connect(path)
        self.c = self.conn.cursor()

        self.c.execute("""create table if not exists tracks (ts integer primary key,
                            created integer,
                            updated integer,
                            playcount integer,
                            track_name text, track_mbid text,
                            artist_name text, artist_mbid text,
                            album_name text, album_mbid text)
                        """)
        
        ## If change to this structure, dont' forget to update
        ## agent ADbus
        
        self.c.execute("""create table if not exists utracks (id integer primary key,
                            created integer,
                            updated integer,
                            playcount integer,
                            track_name text, track_mbid text,
                            artist_name text, artist_mbid text,
                            album_name text, album_mbid text)
                        """)


    def close(self):
        try:    self.conn.close()
        except: pass

    def UniqueTracks_InsertIfNotExists(self, playcount,
                         track_name, track_mbid,
                         artist_name, artist_mbid,
                         album_name, album_mbid):
        """
        Inserts or Updates a specific record in
        the "unique tracks" (i.e. 'utracks') table
        """
        new=False
        now=time.time()        

        self.c.execute("""UPDATE utracks SET playcount=?, updated=?
                            WHERE track_name=? AND 
                                artist_name=?""", 
                        (playcount, now,
                         track_name, artist_name ))
        
        ## v1.4: updated=now
        if self.c.rowcount != 1:
            self.c.execute("""INSERT INTO utracks (created, updated, playcount, 
                            track_name, track_mbid,
                            artist_name, artist_mbid,
                            album_name, album_mbid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (now, now, playcount, track_name, track_mbid,
                            artist_name, artist_mbid,
                            album_name, album_mbid) )
            new=True
                            
        self.conn.commit()
        return new


    def insertIfNotExist(self, ts, playcount,
                         track_name, track_mbid,
                         artist_name, artist_mbid,
                         album_name, album_mbid):
        """
        Inserts a record 
        if it does not exist already
        
        @return: True if the record is new
        """
        new=False
        now=time.time()        

        self.c.execute("""UPDATE tracks SET track_name=?, track_mbid=?,
                        artist_name=?, artist_mbid=?,
                        album_name=?, album_mbid=?, playcount=?, updated=? WHERE ts=?""", 
                        (track_name, track_mbid,
                        artist_name, artist_mbid,
                        album_name, album_mbid, playcount, now,
                        ts))
        
        
        if self.c.rowcount != 1:
            self.c.execute("""INSERT INTO tracks (ts, created, updated, playcount, 
                            track_name, track_mbid,
                            artist_name, artist_mbid,
                            album_name, album_mbid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (ts, now, 0, playcount, track_name, track_mbid,
                            artist_name, artist_mbid,
                            album_name, album_mbid) )
            new=True
            
        self.conn.commit()

        return new

    def updateOne(self, ts, track, artist, playcount):
        self.c.execute("""UPDATE tracks SET updated=?, playcount=? WHERE track_name=? AND artist_name=?""", 
                       (ts, playcount, track, artist))
        rowcount=self.c.rowcount
        self.conn.commit()
        return rowcount
    
    def insertBatchIfNotExist(self, batch):
        for el in batch:
            self.insertIfNotExist(*el)
            
    
    def markUpdated(self, ts):
        """
        Marks a specific entry as 'updated'
        i.e. 'updated=1'
        """
        try:
            self.c.execute("""UPDATE tracks SET updated=? where ts=?""", (1, ts))
            self.conn.commit()
        except:
            pass
    
    
    def getPage(self, timestamp, limit, _updated=0):
        """
        Returns a 'range' of entries
        beginning at 'timestamp' (going up i.e.
        later) and 'limit' number of entries
        """
        self.c.execute("""SELECT * FROM tracks ORDER BY ts DESC LIMIT ? WHERE ts>= ?""", (limit, timestamp))
       
    def getLowestTs(self):
        """
        Finds the lowest timestamp
        """ 
        try:
            self.c.execute("""SELECT * FROM tracks ORDER BY ts ASC LIMIT 1""")    
            ts=self.c.fetchone()[0]
        except:
            ts=0
            
        return ts

    def getHighestTs(self):
        """
        Finds the highest timestamp
        """ 
        try:    
            self.c.execute("""SELECT * FROM tracks ORDER BY ts DESC LIMIT 1""")
            ts=self.c.fetchone()[0]
        except: ts=0
            
        return ts
    
    def getRowCount(self):
        """
        Returns the total row count
        """
        try:
            self.c.execute("""SELECT Count(*) FROM tracks""")    
            count=self.c.fetchone()[0]
        except: count=0
        
        return count

    def UniqueTracks_getRowCount(self):
        """
        Returns the total row count
        """
        try:
            self.c.execute("""SELECT Count(*) FROM utracks""")    
            count=self.c.fetchone()[0]
        except: count=0
        
        return count


    def getToUpdateCount(self):
        """
        Returns the total row count of entries to update
        """
        try:
            self.c.execute("""SELECT Count(*) FROM tracks WHERE updated=0""")    
            count=self.c.fetchone()[0]
        except: count=0
        
        return count

        
    def findNextToUpdate(self, limit=20):
        """
        Find the next record to update
        """
        try:
            self.c.execute("""SELECT * FROM tracks WHERE updated=0 LIMIT ?""", (limit,))
            item=self.c.fetchall()
        except Exception,_e:
            item=None
            
        return item
    
    def getRecords(self, ts_start, limit=100):
        """
        Returns a 'range' of entries
        beginning at 'ts_start' (going up i.e.
        later) and 'limit' number of entries
        """
        if limit < 0:
            limit = 10
        
        limit=min(limit, 100)
        
        try:
            self.c.execute("""SELECT * FROM utracks WHERE (updated>=?) ORDER BY updated ASC LIMIT ?""", (ts_start, limit))
            items=self.c.fetchall()
        except Exception, _e:
            items=None
             
        return items   

    def getRecordsLatest(self, ts_start, limit=100):
        if limit < 0:
            limit = 10
        
        limit=min(limit, 100)
        
        try:
            self.c.execute("""SELECT * FROM utracks WHERE (updated<=?) ORDER BY updated DESC LIMIT ?""", (ts_start, limit))
            items=self.c.fetchall()
        except Exception, _e:
            items=None
             
        return items   
        

    
if __name__=="__main__":
    d=UserTracksDb()
    #d.insertIfNotExist(0, -1, "track0", "t0", "artist", "a0", "album", "al0")
    
    #print d.getRowCount()
    #print d.getLowestTs()
    #print d.getHighestTs()
    #print d.findNextToUpdate()
    
    records=d.getRecords(1274460562, 100)
    print len(records)
    
    