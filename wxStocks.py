# Requirements that must be installed
import wx #, numpy

# Standard Libraries
import sys, inspect, hashlib, threading, base64

# Stop using print!
import logging
logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(lineno)d: %(message)s')
logging.debug('This is a log message.')

# True globals are in config
import config

################################################################################################
# This is due to a serious error in wxPython that exists right now.
# There should be a popup that prompts this password AFTER the mainloop begins, in the init section.
# That does not appear to be functioning, as it freezes all dropdowns and causes other bits of havoc.
# This is a work around to prevent needing to constantly be entering your password.
# It's not the most secure solution, but for all intents and purposes here, it should be fine.

#db.load_encryption_strength()
import getpass

################################################################################################
# Load data
config.TIMER_THREAD_ON = True

config.TIMER_THREAD()
#db.load_all_data()

config.TIMER_THREAD_ON = False



### START ###################################################################
def main():
    app = wx.App()
    import lib.password_functions as password_functions
    result = password_functions.return_password_verification()
    if result == wx.ID_OK:
        logging.debug('wx.ID_OK')
        logging.debug("Correct password")
        pass
    elif result == wx.ID_APPLY:
        logging.debug('wx.ID_APPLY')
        logging.debug("New password accepted")
        pass
    elif result == wx.ID_CANCEL:
        logging.debug('wx.ID_CANCEL')
        sys.exit()
    elif result == wx.ID_REMOVE:
        logging.debug('wx.ID_REMOVE')
        logging.debug("Data Deleted")
        sys.exit()
    else:
        logging.debug(str(result))
        sys.exit()

    display_size = wx.DisplaySize()
    config.DISPLAY_SIZE = display_size
    import lib.gui as gui
    gui.MainFrame().Show()
    app.MainLoop()
main()

# end of line
