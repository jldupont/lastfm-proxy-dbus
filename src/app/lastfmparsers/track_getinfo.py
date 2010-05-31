'''
Created on May 13, 2010

@author: jldupont
'''
from base import BaseHandler, process   

__all__=["parse"]


def parse(xml, debug=False):
    handler=Handler(debug)
    process(xml, handler)
    return handler.props

            

class Handler(BaseHandler):
    """
    User.getRecentTracks response handler
    
    Extracts the "track" elements
    """
    
    def __init__(self, debug=False):
        BaseHandler.__init__(self, debug)
        self.currentTag={}
        self.sm= {
                   ("se", "lfm"):                    "do_skip"
                  ,("se", "track"):                  "do_begin_track"
                  ,("en", "track"):                  "do_end_track"
                  
                  ,("se", "id"):                     "do_noop"
                  ,("se", "id", "en", "id"):         "do_grab_data"
                  
                  ,("se", "name"):                   "do_noop"
                  ,("se", "name", "en", "name"):     "do_grab_data"

                  ,("se", "url"):                    "do_noop"
                  ,("se", "url", "en", "url"):       "do_grab_data"

                  ,("se", "playcount"):                     "do_noop"       
                  ,("se", "playcount", "en", "playcount"):  "do_grab_data"

                  ,("se", "userplaycount"):                     "do_noop"       
                  ,("se", "userplaycount", "en", "userplaycount"):  "do_grab_data"

                  ,("se", "userloved"):                     "do_noop"
                  ,("se", "userloved", "en", "userloved"):  "do_grab_data"

                  ,("se", "mbid"):                          "do_noop"
                  ,("se", "mbid", "en", "mbid"):            "do_grab_data"
            
            ## ARTIST      
                  ,("se", "artist"):                 "do_noop"
                  ,("se", "artist", "en", "artist"): "do_skip"
                  
                  ,("se", "artist", "se", "name"):                "do_noop"
                  ,("se", "artist", "se", "name", "en", "name"):  ("do_grab_artist_params", "artist.name")
                  
                  ,("se", "artist", "se", "mbid"):                "do_noop"  
                  ,("se", "artist", "se", "mbid", "en", "mbid"):  ("do_grab_artist_params", "artist.mbid")

                  ,("se", "artist", "se", "url"):                "do_noop"  
                  ,("se", "artist", "se", "url", "en", "url"):  ("do_grab_artist_params", "artist.url")

            ## ALBUM
                  ,("se", "album"):                "do_noop"
                  ,("se", "album", "en", "album"): "do_skip"

                  ,("se", "album", "se", "artist"):                "do_noop"
                  ,("se", "album", "se", "artist", "en", "artist"):  ("do_grab_album_params", "album.artist")

                  ,("se", "album", "se", "title"):                "do_noop"
                  ,("se", "album", "se", "title", "en", "title"):  ("do_grab_album_params", "album.title")
                  
                  ,("se", "album", "se", "mbid"):                "do_noop"  
                  ,("se", "album", "se", "mbid", "en", "mbid"):  ("do_grab_album_params", "album.mbid")

                  ,("se", "album", "se", "url"):                "do_noop"  
                  ,("se", "album", "se", "url", "en", "url"):  ("do_grab_album_params", "album.url")

            ## TAGS
                  ,("se", "toptags"):                "do_skip"
        
                  ,("se", "tag"):                    "do_commit_tag"
                  ,('se', u'tag', 'en', u'tag'):     "do_skip"
        
                  ,("se", "tag", "se", "name"):                "do_noop"  
                  ,("se", "tag", "se", "name", "en", "name"):  ("do_grab_tag_params", "tag.name")
        
                  ,("se", "tag", "se", "url"):                "do_noop"  
                  ,("se", "tag", "se", "url", "en", "url"):  ("do_grab_tag_params", "tag.url")

                  }

    def do_begin_track(self, event):
        if self.debug:
            print "!!! do_begin_track"
        self.props={}
        self.do_skip(event)
        
    def do_end_track(self, _event):
        if self.debug:
            print "do_end_track"
        pass
    

    def do_grab_artist_params(self, event, param):
        if self.debug:
            print "do_grab_artist_params: event: %s" % str(event)
        (_, data) = event
        self.props[param]=data
        self._pop(2)

    def do_grab_album_params(self, event, param):
        if self.debug:
            print "do_grab_album_params: event: %s" % str(event)
        (_, data) = event
        self.props[param]=data
        self._pop(2)

    def do_grab_tag_params(self, event, param):
        if self.debug:
            print "do_grab_tag_params: event: %s" % str(event)
        (_, data) = event
        self.currentTag[param] = data
        self._pop(2)

    def do_commit_tag(self, _event):
        self.tags=self.props.get("tags", [])
        if self.currentTag:
            self.tags.append(self.currentTag)
            self.props["tags"]=self.tags
            self.currentTag={}

## ================================================== Tests

if __name__=="__main__":

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


    r_test = """
<lfm status="ok">
<track>
    <id>12150</id>
    <name>Little 15</name>
    <mbid></mbid>
    <url>http://www.last.fm/music/Depeche+Mode/_/Little+15</url>
    <duration>255000</duration>
    <streamable fulltrack="0">0</streamable>    
    <listeners>98391</listeners>
    <playcount>400988</playcount>
    <userplaycount>9</userplaycount>    
    <userloved>0</userloved>
    <artist>
        <name>Depeche Mode</name>
        <mbid>8538e728-ca0b-4321-b7e5-cff6565dd4c0</mbid>
        <url>http://www.last.fm/music/Depeche+Mode</url>
    </artist>
    <album position="5">
        <artist>Depeche Mode</artist>
        <title>Music for the Masses</title>
        <mbid>8d059e75-d9bb-4d90-97a9-1cb6ed7472c6</mbid>
        <url>http://www.last.fm/music/Depeche+Mode/Music+for+the+Masses</url>        
        <image size="small">http://userserve-ak.last.fm/serve/64s/27272219.jpg</image>
        <image size="medium">http://userserve-ak.last.fm/serve/126/27272219.jpg</image>
        <image size="large">http://userserve-ak.last.fm/serve/174s/27272219.jpg</image>
        <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/27272219.jpg</image>
    </album>
    <toptags>
        <tag>
          <name>electronic</name>
          <url>http://www.last.fm/tag/electronic</url>
        </tag>
        <tag>
          <name>new wave</name>
          <url>http://www.last.fm/tag/new%20wave</url>
        </tag>
        <tag>
          <name>synthpop</name>
          <url>http://www.last.fm/tag/synthpop</url>
        </tag>
        <tag>
          <name>80s</name>
          <url>http://www.last.fm/tag/80s</url>
        </tag>
        <tag>
          <name>depeche mode</name>
          <url>http://www.last.fm/tag/depeche%20mode</url>
        </tag>
      </toptags>
    </track></lfm>
"""

    handler=Handler(debug=False)
    process(r_test, handler)
    print handler.props
