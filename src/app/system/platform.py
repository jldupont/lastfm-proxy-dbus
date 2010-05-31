"""
    @author: jldupont
    @date: May 19, 2010
"""

import os

__all__=["isOSX", "isLinux"]


platform, _, _, _, _ = os.uname()

def isOSX():
    return platform == "Darwin"

def isLinux():
    return platform == "Linux"


if __name__=="__main__":
    print "is OSX? " + str( isOSX() )
    print "is Linux? " + str( isLinux() )
    