"""
    Tester Agent
        
    Created on 2010-08-31
    @author: jldupont
"""
from app.system.tbase import AgentThreadedBase

__all__=[]


class TesterAgent(AgentThreadedBase):
    
    INTERVAL=10*10
    
    def __init__(self):
        """
        @param interval: interval in seconds
        """
        AgentThreadedBase.__init__(self)

    def h_tick(self, count):

        if (count % self.INTERVAL)==0:
            self.pub("app_state_toggle", None)
        
        

_=TesterAgent()
_.start()
