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

    testing = True
    if not testing:
        # Password prompt
        import lib.password_functions as password_functions
        result = password_functions.return_password_verification()
        if result in [wx.ID_OK, wx.ID_APPLY]:
            result_index = [wx.ID_OK, wx.ID_APPLY].index(result)
            logging.debug(['wx.ID_OK', 'wx.ID_APPLY'][result_index])
            logging.debug(["Correct password", "New password accepted"][result_index])
            pass
        elif result in [wx.ID_CANCEL, wx.ID_REMOVE]:
            result_index = [wx.ID_CANCEL, wx.ID_REMOVE].index(result)
            logging.debug(['wx.ID_CANCEL', 'wx.ID_REMOVE'][result_index])
            sys.exit()
        else:
            logging.debug("wx.ID is unknown: " + str(result))
            sys.exit()

    # Launch wxStocks
    display_size = wx.DisplaySize()
    config.DISPLAY_SIZE = display_size
    import lib.gui as gui
    gui.MainFrame().Show()
    app.MainLoop()
main()

# end of line
