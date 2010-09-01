"""
    Last.fm utilities
        
    Created on 2010-09-01
    @author: jldupont
"""
import hashlib

class Request(object):
    
    API_KEY="50fa3794354dd9d42fc251416f523388"
    API_SECRET="50fa3794354dd9d42fc251416f523388"
    API_END_POINT="http://ws.audioscrobbler.com/2.0/?"
    
    PARAMS_TO_EXCLUDE_FROM_SIGNATURE=["format", "callback"]
    PARAMS_TO_EXCLUDE_FROM_UTF8_ENCODING=["api_key", "api_sig", "method", "format"]
    
    MMAP={
          "auth.getToken":{"api_key_required": True, "signature_required": True}
          }
    
    def __init__(self, method, **kargs):
        self.method=method
        if kargs:
            self.kargs={}
        else:
            self.kargs=kargs
        self.signature_string=None
        
    def __str__(self):
        """
        Returns the URL representation for the method
        """
        self._buildSignatureString()
        
        url=self.API_END_POINT
        for key, value in self.kargs.iteritems():
            url = url + ("&%s=%s" % (key, value))
        
        return url
        
    ## ===================================================
    def _buildSignatureString(self):
        """
        Builds the string used for signing the request
        """
        self.params=self.kargs
        
        try:    method_details=self.MMAP[self.method]
        except: 
            raise RuntimeError("unsupported method")
        
        api_key_required=method_details["api_key_required"]
        if api_key_required:
            self.params.update({"api_key": self.API_KEY, "method":self.method})
            
        signature_required=method_details["signature_required"]
        if not signature_required:
            self.signature_string=""
            return
            
        sorted_keys=self.params.keys().sort()
        
        str=""
        try:
            for key in sorted_keys:
                if key not in self.PARAMS_TO_EXCLUDE_FROM_SIGNATURE:
                    
                    ## assume the parameter's value is valid
                    try:    
                        if key not in self.PARAMS_TO_EXCLUDE_FROM_UTF8_ENCODING:
                            value=self.params[key].encode("utf-8")
                        else:
                            value=self.params[key]
                    except: value=self.params[key]
                    str="%s%s" % (key, value)
        except:
            pass
        
        str += self.API_SECRET
        m=hashlib.md5()
        m.update(str)
        self.signature_string=m.hexdigest()
        
        self.kargs.update({"api_sig": self.signature_string})
        
        
if __name__=="__main__":
    r=Request("auth.getToken")
    print r
    
    """
    <?xml version="1.0" encoding="utf-8"?> 
        <lfm status="ok"> 
            <token>5fe344e65fd7fb2e9535ca52804c8659</token>
        </lfm> 
    """
