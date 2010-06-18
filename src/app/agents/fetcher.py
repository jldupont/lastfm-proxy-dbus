"""
    Fetcher Agent
    
    Messages In:
    ------------
    - "username"
    - "tick"
    - "page?"
    
    
    Messages Out:
    ------------
    - "page_details"
    - "tracks"
    
    
    @author: Jean-Lou Dupont
    @date: 17 May 2010
"""
import time
import urllib2
import urllib
from app.system.tbase import AgentThreadedBase
from app.lastfmparsers.user_getrecenttracks import parse

__all__=[]

## 100ms / tick
INTERVAL_TICKS=4*60*5


class FetcherAgent(AgentThreadedBase):
    """
    User.RecentTracks
    """
    TIMEOUT = 4
    USER_RECENTTRACKS_URL="http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&page=%s&limit=200&api_key="
    API_KEY="50fa3794354dd9d42fc251416f523388"
    
    def __init__(self, interval):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)

        self.username=None
        self.interval = interval
        self.lastFetch=0
        self.lastSuccessfulFetch=0
        self.count = 0
        self.url=self.USER_RECENTTRACKS_URL + self.API_KEY        
                
    def h_shutdown(self):
        print "Fetcher - shutdown"
                
    def h_username(self, username):
        self.username=username
                
    def h_tick(self, _count):
        self.count += 1
        if self.count == self.interval or self.lastFetch==0:
            self.count = 0
            self.do_fetch()
            
    def do_fetch(self):
        if self.username is None:
            return

        self.lastFetch=time.time()
        
        ## always fetch the first page
        ##  and we'll be asked for more specific
        ##  ones if needed
        self.fetch_page(1)

    def hq_page(self, page):
        """
        'page?' question handler
        """
        self.fetch_page(page)


    def fetch_page(self, page):
        """
        Fetches a specific page from 'user.recenttracks'
        """
        ua=urllib.quote_plus(self.username.encode("utf-8"))
        url=self.url % (ua, page)
                
        #print "fetching page: "+str(page)

        try:
            raw=urllib2.urlopen(url, None, self.TIMEOUT)
            resp=raw.read()
            
            self.lastSuccessfulFetch=time.time()
        except Exception,e:
            self.pub("errorFetch", str(e))
            return
            
        try:
            rtracks=parse(resp)
        except Exception,e:
            self.pub("errorParsing", str(e))
            return
        
        try:
            rattrs=rtracks["recenttracks.attrs"]
            tracks=rtracks["tracks"]

            page=rattrs["page"]
            perPage=rattrs["perPage"]
            totalPages=rattrs["totalPages"]
        except:
            self.pub("errorResponseFormat", 
                     "Error whilst retrieving fields from 'user.recenttracks' response")
            return

        lowest, highest, count = self.process_tracks(tracks)
        self.pub("page_details", {"page": page, "perPage":perPage,
                                  "totalPages": totalPages,
                                  "lowest_ts": lowest, "highest_ts": highest,
                                  "count": count
                                  })

        self.pub("tracks", page, tracks)
        

    def process_tracks(self, tracks):
        """
        Computes the 'lowest' and 'highest'
        timestamps of the 'recent tracks page' fetched
        """
        lowest=0
        highest=0
        count = 0
        for track in tracks:
            try:    
                ts=track["date.attrs"]["uts"]
                if lowest == 0:
                    lowest = ts
                if highest == 0:
                    highest = ts
                    
                if ts < lowest:
                    lowest = ts
                if ts > highest:
                    highest = ts
                    
                count += 1
            ## The record on the first page can be the 
            ## currently playing track and hence without
            ## a timestamp
            except: 
                pass
            
        return (lowest, highest, count)
            
        
        

_f=FetcherAgent(INTERVAL_TICKS)
_f.start()

