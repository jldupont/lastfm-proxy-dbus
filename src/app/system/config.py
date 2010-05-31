"""
    @author: jldupont
    @date: May 18, 2010
"""
import os
import gconf
import ConfigParser

## OS X support
try:   
    from Foundation import *
except:
    pass


__all__=["findUsername"]


def findUsername():
    """
    Attempts to find the user's Last.fm username
    
    1) Rhythmbox 'audioscrobbler' plugin
    2) Last.fm Desktop 
    """
    return osxLastFm() or _lastfmDkUsername() or _rbUsername()

        
def _lastfmDkUsername():    
    try:
        path=os.path.expanduser("~/.config/Last.fm/Last.fm.conf")
        p=ConfigParser.ConfigParser()
        p.read([path])
        username=p.get("Users", "CurrentUser")
    except:
        username=None
        
    return username
    
        
def _rbUsername():
    try:
        RB_PATH="/apps/rhythmbox/audioscrobbler/%s"
        client=gconf.client_get_default()
        username=client.get_string(RB_PATH % "username")
    except:
        username=None
    
    return username


def osxLastFm():
    try:
        path=os.path.expanduser("~/Library/Preferences/fm.last.Last.fm.plist")
        plist, _format, _error = NSPropertyListSerialization.propertyListFromData_mutabilityOptions_format_errorDescription_(NSData.dataWithContentsOfMappedFile_(path), NSPropertyListImmutable, None, None) #@UndefinedVariable
        username=plist["Users.CurrentUser"]
    except:
        username=None
        
    return username
    


## ======================================================================= 
## ======================================================================= Tests
## ======================================================================= 

if __name__=="__main__":

    print findUsername()
    