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
        self.current={}
        self.sm= {
                   ("se", "lfm"):                    "do_skip"
        
                  ,("se", "recenttracks"):           "do_recenttracks"
                  ,("en", "recenttracks"):           "do_skip"
                  
                  ,("se", "track"):                  "do_begin_track"
                  ,("en", "track"):                  "do_end_track"
                  
                  ,("se", "artist"):                 ("do_grab_el_attrs","artist")
                  ,("se", "artist", "en", "artist"): ("do_grab_el_data", "artist")
                  
                  ,("se", "album"):                  ("do_grab_el_attrs", "album")
                  ,("se", "album", "en", "album"):   ("do_grab_el_data", "album")

                  ,("se", "name"):                   ("do_grab_el_attrs", "name")
                  ,("se", "name", "en", "name"):     ("do_grab_el_data", "name")

                  ,("se", "mbid"):                   "do_noop"
                  ,("se", "mbid", "en", "mbid"):     ("do_grab_el_data", "mbid")

                  ,("se", "url"):                    "do_noop"
                  ,("se", "url", "en", "url"):       ("do_grab_el_data", "url")

                  ,("se", "date"):                   ("do_grab_el_attrs", "date")
                  ,("se", "date", "en", "date"):     ("do_grab_el_data", "date")
                  
                  }

    def do_recenttracks(self, event):
        self.do_grab_attrs(event)
        self.do_skip(event)
        
    def do_begin_track(self, event):
        self.current={}
        self.do_skip(event)

    def do_end_track(self, _event):
        self.tracks=self.props.get("tracks", [])
        self.tracks.append(self.current)
        self.props["tracks"]=self.tracks
        self.current={}

## ================================================== Tests

if __name__=="__main__":

    """
    {u'recenttracks.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2ce4c>, 
    'tracks': [
        {'album': u'Crossroads', 
            'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2cf4c>, 
            'name': u'Fear', 
            'artist': u'Mind.In.A.Box', 
            'url': u'http://www.last.fm/music/Mind.In.A.Box/_/Fear', 
            'mbid': u'', 
            'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2ceec>, 
            'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2ce8c>}, 
        {'album': u'Breathing Avenue', 
            'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2ceac>, 
            'name': u'reMind', 
            'artist': u'Minerve', 
            'url': u'http://www.last.fm/music/Minerve/_/reMind', 
            'mbid': u'', 
            'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2cf6c>, 
            'date': u'13 May 2010, 02:14', 
            'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2cf8c>, 
            'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2cfec>}, 
        {'album': u'Host', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2cfcc>, 'name': u'Ordinary Days', 'artist': u'Paradise Lost', 'url': u'http://www.last.fm/music/Paradise+Lost/_/Ordinary+Days', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3308c>, 'date': u'13 May 2010, 02:10', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3304c>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a2cfac>}, {'album': u'The Art Of Revenge', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3314c>, 'name': u'Your Nature', 'artist': u'XP8', 'url': u'http://www.last.fm/music/XP8/_/Your+Nature', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3306c>, 'date': u'13 May 2010, 00:29', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3302c>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3312c>}, {'album': u'', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3310c>, 'name': u'Torn (Covenant remix)', 'artist': u'Seabound', 'url': u'http://www.last.fm/music/Seabound/_/Torn+%28Covenant+remix%29', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3318c>, 'date': u'13 May 2010, 00:21', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a330cc>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a331ac>}, {'album': u'', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3324c>, 'name': u'8 Bits (club.Edit)', 'artist': u'Mind.In.A.Box', 'url': u'http://www.last.fm/music/Mind.In.A.Box/_/8+Bits+%28club.Edit%29', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a330ec>, 'date': u'13 May 2010, 00:17', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3320c>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a331ec>}, {'album': u'', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a332cc>, 'name': u'Never Surrender - Citadel (Clan Of Xymox Remix)', 'artist': u'The Cruxshadows', 'url': u'http://www.last.fm/music/The+Cr%C3%BCxshadows/_/Never+Surrender+-+Citadel+%28Clan+Of+Xymox+Remix%29', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3316c>, 'date': u'13 May 2010, 00:12', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3328c>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a330ac>}, {'album': u'', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3334c>, 'name': u'7 Deadly Sins', 'artist': u'Simple Minds', 'url': u'http://www.last.fm/music/Simple+Minds/_/7+Deadly+Sins', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a331cc>, 'date': u'13 May 2010, 00:06', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3330c>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3322c>}, {'album': u'Serve or Suffer', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a333cc>, 'name': u'Serve Or Suffer', 'artist': u'Absurd Minds', 'url': u'http://www.last.fm/music/Absurd+Minds/_/Serve+Or+Suffer', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3326c>, 'date': u'13 May 2010, 00:02', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3338c>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a332ac>}, {'album': u'Debris', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3344c>, 'name': u'Beta Complex', 'artist': u'Ayria', 'url': u'http://www.last.fm/music/Ayria/_/Beta+Complex', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a333ac>, 'date': u'12 May 2010, 19:27', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a333ec>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3342c>}, {'album': u'Expansion', 'album.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a334ec>, 'name': u'Memories (club remix)', 'artist': u'NamNamBulu', 'url': u'http://www.last.fm/music/NamNamBulu/_/Memories+%28club+remix%29', 'mbid': u'', 'date.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3346c>, 'date': u'12 May 2010, 19:21', 'name.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a3348c>, 'artist.attrs': <xml.sax.xmlreader.AttributesImpl instance at 0x8a334cc>}]}    """
 
    r_test = u"""
<lfm status="ok"> 
<recenttracks user="jldupont" page="1" perPage="10" totalPages="3153"> 
<track nowplaying="true"> 
    <artist mbid="6fe25812-9155-43a1-b5af-8371f90a4f59">Mind.In.A.Box</artist> 
    <name>Fear</name> 
    <streamable>1</streamable> 
    <mbid></mbid> 
    <album mbid="d3d18cbe-e0ae-4ddf-82f1-aa9207047561">Crossroads</album> 
    <url>http://www.last.fm/music/Mind.In.A.Box/_/Fear</url> 
    <image size="small">http://userserve-ak.last.fm/serve/34s/9964547.jpg</image> 
    <image size="medium">http://userserve-ak.last.fm/serve/64s/9964547.jpg</image> 
    <image size="large">http://userserve-ak.last.fm/serve/126/9964547.jpg</image> 
    <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/9964547.jpg</image> 
</track> 
<track> 
        <artist mbid="b93145c8-3734-4c19-91c4-8b4b6b34f2d9">Minerve</artist> 
<name>reMind</name> 
<streamable>1</streamable> 
<mbid></mbid> 
<album mbid="c903c11f-8a0f-4ddf-8a9a-724fc1c1b55f">Breathing Avenue</album> 
<url>http://www.last.fm/music/Minerve/_/reMind</url> 
    <image size="small">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
    <image size="medium">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
    <image size="large">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
    <image size="extralarge">http://images.amazon.com/images/P/B0001XPUYC.03.MZZZZZZZ.jpg</image> 
        <date uts="1273716861">13 May 2010, 02:14</date> 
</track> 
<track> 
        <artist mbid="10bf95b6-30e3-44f1-817f-45762cdc0de0">Paradise Lost</artist> 
<name>Ordinary Days</name> 
<streamable>1</streamable> 
<mbid></mbid> 
<album mbid="e38567b4-a80c-4301-922b-0768ff249826">Host</album> 
<url>http://www.last.fm/music/Paradise+Lost/_/Ordinary+Days</url> 
    <image size="small">http://userserve-ak.last.fm/serve/34s/34568145.jpg</image> 
    <image size="medium">http://userserve-ak.last.fm/serve/64s/34568145.jpg</image> 
    <image size="large">http://userserve-ak.last.fm/serve/126/34568145.jpg</image> 
    <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/34568145.jpg</image> 
        <date uts="1273716652">13 May 2010, 02:10</date> 
</track> 
<track> 
        <artist mbid="2d66fa4c-5ae6-4aae-89b9-2a3ac8421b72">XP8</artist> 
<name>Your Nature</name> 
<streamable>1</streamable> 
<mbid></mbid> 
<album mbid="9e021a83-4886-422a-a5ff-51e95d7a1e6e">The Art Of Revenge</album> 
<url>http://www.last.fm/music/XP8/_/Your+Nature</url> 
    <image size="small">http://userserve-ak.last.fm/serve/34s/24517437.jpg</image> 
    <image size="medium">http://userserve-ak.last.fm/serve/64s/24517437.jpg</image> 
    <image size="large">http://userserve-ak.last.fm/serve/126/24517437.jpg</image> 
    <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/24517437.jpg</image> 
        <date uts="1273710547">13 May 2010, 00:29</date> 
</track> 
<track> 
        <artist mbid="816ba2e2-31da-4cb7-ace0-99546f6bd657">Seabound</artist> 
<name>Torn (Covenant remix)</name> 
<streamable>0</streamable> 
<mbid></mbid> 
<album mbid=""></album> 
<url>http://www.last.fm/music/Seabound/_/Torn+%28Covenant+remix%29</url> 
    <image size="small"></image> 
    <image size="medium"></image> 
    <image size="large"></image> 
    <image size="extralarge"></image> 
        <date uts="1273710102">13 May 2010, 00:21</date> 
</track> 
<track> 
        <artist mbid="6fe25812-9155-43a1-b5af-8371f90a4f59">Mind.In.A.Box</artist> 
<name>8 Bits (club.Edit)</name> 
<streamable>0</streamable> 
<mbid></mbid> 
<album mbid=""></album> 
<url>http://www.last.fm/music/Mind.In.A.Box/_/8+Bits+%28club.Edit%29</url> 
    <image size="small"></image> 
    <image size="medium"></image> 
    <image size="large"></image> 
    <image size="extralarge"></image> 
        <date uts="1273709860">13 May 2010, 00:17</date> 
</track> 
<track> 
        <artist mbid="3d8d3d22-5a0e-4b23-ae56-78abcc2c3f8f">The Cruxshadows</artist> 
<name>Never Surrender - Citadel (Clan Of Xymox Remix)</name> 
<streamable>0</streamable> 
<mbid></mbid> 
<album mbid=""></album> 
<url>http://www.last.fm/music/The+Cr%C3%BCxshadows/_/Never+Surrender+-+Citadel+%28Clan+Of+Xymox+Remix%29</url> 
    <image size="small"></image> 
    <image size="medium"></image> 
    <image size="large"></image> 
    <image size="extralarge"></image> 
        <date uts="1273709530">13 May 2010, 00:12</date> 
</track> 
<track> 
        <artist mbid="f41490ce-fe39-435d-86c0-ab5ce098b423">Simple Minds</artist> 
<name>7 Deadly Sins</name> 
<streamable>1</streamable> 
<mbid></mbid> 
<album mbid=""></album> 
<url>http://www.last.fm/music/Simple+Minds/_/7+Deadly+Sins</url> 
    <image size="small"></image> 
    <image size="medium"></image> 
    <image size="large"></image> 
    <image size="extralarge"></image> 
        <date uts="1273709217">13 May 2010, 00:06</date> 
</track> 
<track> 
        <artist mbid="979ce33b-4d8e-4e44-8c7e-f9d3054f4386">Absurd Minds</artist> 
<name>Serve Or Suffer</name> 
<streamable>1</streamable> 
<mbid></mbid> 
<album mbid="">Serve or Suffer</album> 
<url>http://www.last.fm/music/Absurd+Minds/_/Serve+Or+Suffer</url> 
    <image size="small">http://userserve-ak.last.fm/serve/34s/43021379.jpg</image> 
    <image size="medium">http://userserve-ak.last.fm/serve/64s/43021379.jpg</image> 
    <image size="large">http://userserve-ak.last.fm/serve/126/43021379.jpg</image> 
    <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/43021379.jpg</image> 
        <date uts="1273708946">13 May 2010, 00:02</date> 
</track> 
<track> 
        <artist mbid="d7762352-8894-4fb2-9165-5fa7a2fbac42">Ayria</artist> 
<name>Beta Complex</name> 
<streamable>1</streamable> 
<mbid></mbid> 
<album mbid="94ad5c65-bd40-4627-90d7-592bc72817b3">Debris</album> 
<url>http://www.last.fm/music/Ayria/_/Beta+Complex</url> 
    <image size="small">http://userserve-ak.last.fm/serve/34s/33128449.jpg</image> 
    <image size="medium">http://userserve-ak.last.fm/serve/64s/33128449.jpg</image> 
    <image size="large">http://userserve-ak.last.fm/serve/126/33128449.jpg</image> 
    <image size="extralarge">http://userserve-ak.last.fm/serve/300x300/33128449.jpg</image> 
        <date uts="1273692462">12 May 2010, 19:27</date> 
</track> 
<track> 
        <artist mbid="aff48c86-899b-490f-b5e4-39e80d43465c">NamNamBulu</artist> 
<name>Memories (club remix)</name> 
<streamable>0</streamable> 
<mbid></mbid> 
<album mbid="75303b60-5ec4-425a-9716-c135c9966f3f">Expansion</album> 
<url>http://www.last.fm/music/NamNamBulu/_/Memories+%28club+remix%29</url> 
    <image size="small">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
    <image size="medium">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
    <image size="large">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
    <image size="extralarge">http://images.amazon.com/images/P/B00024DORU.01.MZZZZZZZ.jpg</image> 
        <date uts="1273692103">12 May 2010, 19:21</date> 
</track> 
</recenttracks></lfm> 
"""
    handler=Handler(debug=True)
    process(r_test, handler)
    print handler.props
