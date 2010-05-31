'''
Created on May 13, 2010

@author: jldupont
'''
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import StringIO
    
__all__=["process", "BaseHandler"]

def process(data, handler):
    """
    Processes a response from Last.fm API
    
    @param data: XML string
    
    @return: dict 
    """
    bus=HandlerBus()
    bus.add(handler)
    
    par=make_parser()
    par.setContentHandler(bus)
    sio=StringIO.StringIO(data)
    
    par.parse(sio)
    

class HandlerBus(ContentHandler):
    """
    Distributes the XML parsing events 
    to the registered objects
    
    An instance of this class would be
    passed to the XML parser
    """
    def __init__(self):
        self._regs=[]
        
    def add(self, reg):
        self._regs.append(reg)
        
    def startElement(self, name, attrs):
        for r in self._regs:
            r.startElement(name, attrs)
    
    def characters(self, ch):
        for r in self._regs:
            r.characters(ch)
                
    def endElement(self, name):
        for r in self._regs:
            r.endElement(name)
            


class BaseHandler(object):
    """
    """
    def __init__(self, debug=False):
        self.debug=debug
        self._acc=""
        self.current={}
        self.props={}
        self.state=[]
        self.topass=False
        self.default="do_topass"
        
    ## ================================== Event callbacks
    
    def startElement(self, tag, attrs):
        self.state.extend(["se", tag])
        self._exec((tag, attrs))
    
    def characters(self, ch):
        self._acc+=ch
                
    def endElement(self, tag):
        self.state.extend(["en", tag])
        self._exec((tag, self._acc.strip()))
        self.state=self.state[:-2]
        self._acc=""
    
    ## =================================== Support Methods
    def _missingState(self, event, *_p):
        self.do_noop(event)
        if self.debug:
            print "Missing state for event: " + str(event)
    
    def _exec(self, event):
        t=tuple(self.state)
        if self.debug:
            print "\n  _exec: state: %s" % str(t)        
            print "  _exec: event: %s" % str(event)

        if self.topass:
            self.topass=False
            self.do_pop2(None)
            if self.debug:
                print "* passing *"
            return
        
        try:        
            (method, params) = self.sm.get(t, self.default)
            getattr(self, method, self._missingState)(event, params)
            #print "** 1.method: %s" % method
        except Exception,_e:
            #print "Exception: %s" % str(e)
            method= self.sm.get(t, self.default)
            getattr(self, method, self._missingState)(event)
            #print "** 2.method: %s" % method
        
    ## =================================== State related handlers
    def do_grab_attrs(self, event):
        (tag, attrs) = event
        self.props["%s.attrs" % tag]=attrs
        if self.debug:
            print "do_grab_attrs: event: %s" % str(event)
        
    def do_grab_data(self, event):
        (tag, data) = event
        self.props[tag]=data
        if self.debug:
            print "do_grab_data: event: %s" % str(event)
        self.do_skip(event)

    def do_grab_el_attrs(self, event, param):
        (_, attrs) = event
        self.current["%s.attrs" % param]=attrs
        if self.debug:
            print "do_grab_el_attrs: event: %s" % str(event)
        
    def do_grab_el_data(self, event, param):
        (_, data) = event
        self.current[param]=data
        if self.debug:
            print "do_grab_el_data: event: %s" % str(event)
        self.do_skip(event)

    def do_skip(self, event):
        if self.debug:
            print "do_skip: %s" % str(event)
            print "do_skip: state: %s" % str(self.state)
        self.state=[]

    def do_noop(self, event):
        if self.debug:
            print "do_noop: %s" % str(event)
            print "do_noop: state: %s" % str(self.state)

    def do_topass(self, event):
        self.topass=True
        if self.debug:
            print "do_topass: %s" % str(event)
            print "do_topass: state: %s" % str(self.state)

    def do_pop2(self, _):
        if self.debug:
            print "  do_pop2()"
        self._pop(2)

    ## =================================== Helpers
    def _pop(self, n):
        self.state=self.state[:-n]
    