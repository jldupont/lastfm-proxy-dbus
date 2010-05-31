Linux Last.fm proxy service over DBus

DBus
====

The input signal is defined as:

* interface: 'com.jldupont.lastfm.proxy'
* path: Records
* signal name: qRecord
  * ts_start: (integer)  start timestamp
  * limit: (integer)  maximum number of records to retrieve
  
The resulting output signal is defined as:

* interface: 'com.jldupont.lastfm.proxy'
* path: Records
* signal name: Records
  * list of dict, signature: aa{sv}
 

Installation
============
There are 2 methods:

1. Use the Ubuntu Debian repository [jldupont](https://launchpad.net/~jldupont/+archive/phidgets)  with the package "rbsynclastfm"

2. Use the "Download Source" function of this git repo and use "sudo make install"

 
[Home](http://www.systemical.com/ "Home")