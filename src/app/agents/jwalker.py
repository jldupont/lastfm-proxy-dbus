"""
    Journal Walker
    
    Goes through the user's Last.fm 
    'user.recenttracks' journal
    
    The process is kickstarted by the Fetcher agent by
    the action of fetching a 'recent tracks' history page.
    As a result, 'page_details' and 'tracks' message are generated.
    
    Messages In:
    ------------
    - "new_ts"
    - "page_details"
    
    Messages Out:
    -------------
    - "page?"
    - "totalDbTracks"
    - "numPages"
    
    
    @author: jldupont
    @date: May 20, 2010
"""
import random
from app.system.tbase import AgentThreadedBase

__all__=[]



class JwalkerAgent(AgentThreadedBase):
    
    def __init__(self):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)

        self.perPage = 0
        self.lastPage = -1
        self.currentTotal = 0
        self.recentPages=[]
        self.totalDbCount=0
        self.range=[]
        self.complete=False
       
    def h_shutdown(self):
        print "Jwalker - shutdown"
       
    def h_new_ts(self, page, total_db_tracks, ts_list):
        """
        List of track timestamp corresponding
        to tracks just inserted in the db
        """
        if self.totalDbCount != total_db_tracks:
            self.pub("totalDbTracks", total_db_tracks)
            self.totalDbCount=total_db_tracks
            self.pub("log", "Journal - total tracks: %s" % str(total_db_tracks))
        
        if page == self.lastPage:
            return 

        ## we are up-to-date (approx at least)... hooray!
        if total_db_tracks > self.currentTotal:
            self.pub("log", "Up-to-date (total_db_tracks > lastfm_recenttracks)")
            return

        ## we were lucky here... try the next one
        if len(ts_list) > 0:
            next_page=int(page)+1
            self.pub("page?", next_page)
            self.pub("log", "Journal - Continue sequence, page: %s" % str(next_page))         
            return

        ## We didn't want to exit just before this point
        ##  in case we missed some update page at the front
        if self.complete:
            return
        
        ## Try our luck on a new sequence
        next_page=self._pickPage()
        self.pub("page?", next_page)
        self.pub("log", "Journal - Trying new sequence, from page: %s" % str(next_page))
        
    def h_page_details(self, details):
        """
            Grab 'page_details' and ask
            for the 'last page' if we don't
            already have it.
        """
        page=int(details["page"])
        lastPage=int(details["totalPages"])
        self.perPage=int(details["perPage"])
        
        if lastPage != self.lastPage:
            self.pub("numPages", lastPage)
            self.range = range(2, lastPage+1)
            self.pub("log", "Journal - Pages in Recent Tracks: %s" % str(lastPage))
            
        self.lastPage=int(lastPage)
        
        self.currentTotal=(self.lastPage-1)*self.perPage

        self.pub("lastfmRecentTracksCount", self.currentTotal)
        
        ## Keep a recent list of pages
        ##  So that we don't visit them more then necessary
        try:
            self.recentPages.index(page)
        except:
            self.recentPages.append(page)
            try:    self.range.remove(page)
            except: pass
        
        if self.complete:
            return
        
        if len(self.range)==0:
            self.complete=True
            self.pub("log", "Completed -- User Recent Tracks journal walking")

        
    def _pickPage(self):
        """
        Pick a page at random whilst moderately
        ensuring we haven't pick the same page
        recently enough 
        """
        tries=0
        page=2
        while True:
            page=random.randint(2, self.lastPage)
            if page not in self.recentPages:
                #print "jwalker._pickPage: random: "+str(page)
                break
            tries += 1
            if tries > 10:
                try:    page=self.range.pop()
                except: page=self.lastPage
                #print "jwalker._pickPage: from range: "+str(page)
                break

        return page
                
            
            
_=JwalkerAgent()
_.start()
