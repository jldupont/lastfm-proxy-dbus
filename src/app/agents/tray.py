"""
    Tray Icon Agent
        
    Created on 2010-08-16
    @author: jldupont
"""
__all__=["TrayAgent"]

import os
import gtk #@UnusedImport
import gtk.gdk
import app.system.mswitch as mswitch
from app.system.tbase import AgentThreadedBase

class AppPopupMenu:
    def __init__(self, app):
        self.item_exit = gtk.MenuItem( "exit", True)
        self.item_show = gtk.MenuItem( "show", True)
        self.item_exit.connect( 'activate', app.exit)
        self.item_show.connect( 'activate', app.show)

        self.menu = gtk.Menu()
        self.menu.append( self.item_show)
        self.menu.append( self.item_exit)        
        self.menu.show_all()

    def show_menu(self, button, time):
        self.menu.popup( None, None, None, button, time)
        

class AppIcon(object):
    
    def __init__(self, icon_path, icon_file):
        self.icon_path=icon_path
        self.icon_file=icon_file
        self.curdir=os.path.abspath( os.path.dirname(__file__) )
        self.twodirup=os.path.abspath( os.path.join(self.curdir, "..", "..") )
    
    def getIconPixBuf(self): 
        try:
            ipath=self.icon_path+"/"+self.icon_file
            pixbuf = gtk.gdk.pixbuf_new_from_file( ipath )
        except:
            ipath=os.path.join(self.twodirup, self.icon_file)
            pixbuf = gtk.gdk.pixbuf_new_from_file( ipath )
                      
        return pixbuf.scale_simple(24,24,gtk.gdk.INTERP_BILINEAR)




class TrayObject(object):
    def __init__(self, app_name, icon_path, icon_file, icon_file_warning):
        
        self.app_name=app_name
        self.popup_menu=AppPopupMenu(self)
        
        self.tray=gtk.StatusIcon()
        self.tray.set_visible(True)
        self.tray.set_tooltip(self.app_name)
        #self.tray.connect('activate', self.do_popup_menu_activate)
        self.tray.connect('popup-menu', self.do_popup_menu)
        
        self.icon_scaled_buf = AppIcon(icon_path, icon_file).getIconPixBuf()
        self.icon_warning_scaled_buf = AppIcon(icon_path, icon_file_warning).getIconPixBuf()
        
    def set_app_normal(self):
        """
        When the application is in 'normal' condition
        """
        self.tray.set_from_pixbuf( self.icon_scaled_buf )
        
    def set_app_warning(self):
        """
        When the application experiences a 'warning' condition
        """
        self.tray.set_from_pixbuf( self.icon_warning_scaled_buf )
        
        
    def do_popup_menu_activate(self, statusIcon):
        timestamp=gtk.get_current_event_time()
        print timestamp
        self.popup_menu.show_menu(None, int(timestamp))
        
    def do_popup_menu(self, status, button, time):
        self.popup_menu.show_menu(button, time)

    def show(self, *_):
        mswitch.publish(self, "app_show")

    def exit(self, *p):
        mswitch.publish(self, "__quit__")


class TrayAgent(AgentThreadedBase):
    def __init__(self, app_name, icon_path, icon_file, icon_file_warning):
        AgentThreadedBase.__init__(self)

        self.tray=TrayObject(app_name, icon_path, icon_file, icon_file_warning)
        
        self.state="normal"        
        self.h_app_normal()
                
    def h_app_normal(self, *_):
        """
        When the application is in 'normal' condition
        """
        self.state="normal"
        self.tray.set_app_normal()
        
    def h_app_warning(self, *_):
        """
        When the application experiences a 'warning' condition
        """
        self.state="warning"
        self.tray.set_app_warning()
        
    def h_app_state_toggle(self, *_):
        #print "toggle: state: %s" % self.state
        if self.state=="normal":
            self.h_app_warning()
        else:
            self.h_app_normal()

