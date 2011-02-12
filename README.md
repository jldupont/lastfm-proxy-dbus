Linux Last.fm proxy service over DBus

DBus
====

The input signals are defined as:

* interface: 'com.jldupont.lastfm.proxy'
* path: Records
* signal name: qRecords
  * ts_start: (integer)  start timestamp
  * limit: (integer)  maximum number of records to retrieve

* interface: 'com.jldupont.lastfm.proxy'
* path: Records
* signal name: qRecordsLatest
  * ts_start: (integer)  start timestamp
  * limit: (integer)  maximum number of records to retrieve
  
The resulting output signal are defined as:

* interface: 'com.jldupont.lastfm.proxy'
* path: Records
* signal name: Records
  * list of dict with 'entries', signature: aa{sv}

* interface: 'com.jldupont.lastfm.proxy'
* path: Records
* signal name: RecordsLatest
  * list of dict with 'entries', signature: aa{sv}
 

Entry
-----

The following fields are available:

 - "id"
 - "created"
 - "updated"
 - "playcount"
 - "track_name"
 - "track_mbid"
 - "artist_name"
 - "artist_mbid"
 - "album_name"
 - "album_mbid"



Installation
============
There are 2 methods:

1. Use the Ubuntu Debian repository [jldupont](https://launchpad.net/~jldupont/+archive/phidgets)  with the package "rbsynclastfm"

2. Use the "Download Source" function of this git repo and use "sudo make install"

 
History
=======

 - v1.1: added signal to Musicbrainz-proxy-dbus 
 - v1.2: added signal "qRecordsLatest" and output result "RecordsLatest"
 - v1.3: fixed bug with "qRecordsLatest" processing
 - v1.4: new created records are set with "updated=now()"
 - v1.5: enhanced reporting of "unique tracks" with associated "playcount"
 - v1.6: enhanced scanning for tracks in need of update
 - v1.61: corrected debian packaging to include needed "python-tk" package
 - v1.70: significant speed-up: message switch with priority & burst limiting
 - v1.71: additional speed-up: tweaked GUI main message loop
 - v1.72: fixed shutdown process
 - v1.73: minor fix in AgentThreadedBase
 - v1.74: fixed issue with missing "userplaycount" field during update phase
 - v1.76: fixed issue with "userplaycount==0" field
 - v1.80: added help button and tray icon
 - v2.01: changed location of sqlite database to ~/
 
[Home](http://www.systemical.com/ "Home")