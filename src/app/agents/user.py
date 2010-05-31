"""
    User Agent

    Responsible of keeping up-to-date with 
    the user's Last.fm username
    
    @author: jldupont
    @date: May 19, 2010
"""
from app.system.tbase  import AgentThreadedBase
from app.system.config import findUsername

__all__=[]

## seconds
INTERVAL_TICKS=30 

class UserAgent(AgentThreadedBase):
    
    def __init__(self, interval):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)

        self.username=None

        self.interval = interval
        self.count = 0        
        
    def h_shutdown(self):
        print "User - shutdown"
        
    def hq_username(self):
        """
        'username?' message handler
        """
        self.do_refresh()
                
    def h_tick(self, _count):
        
        self.count += 1
        if self.count == self.interval or self.count==1:
            self.do_refresh()
            
    def do_refresh(self):
        username=findUsername()
        if username != self.username:
            self.pub("log", "Found Last.fm username: %s" % username)
        self.username=username
        self.pub("username", self.username)
        

_f=UserAgent(INTERVAL_TICKS)
_f.start()

