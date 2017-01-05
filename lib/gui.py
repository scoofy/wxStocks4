#################################################################
#   Most of the wxPython in wxStocks is located here.           #
#   Table of Contents:                                          #
#       1: Imports and line_number function                     #
#       2: Main Frame, where tab order is placed.               #
#       3: Tabs                                                 #
#       4: Grid objects                                         #
#################################################################
import wx
import logging
import config
import lib.gui_position_index as gui_position

class MainFrame(wx.Frame): # reorder tab postions here
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="wxStocks", pos = wx.DefaultPosition, size = gui_position.MainFrame_size)
        self.SetSizeHints(gui_position.MainFrame_SetSizeHints[0],gui_position.MainFrame_SetSizeHints[1])
        self.title = "wxStocks"
        self.uid = config.MAIN_FRAME_UNIQUE_ID

        # Here we create a panel and a notebook on the panel
        main_frame = wx.Panel(self)

        logging.debug("done.\n\n------------------------- wxStocks startup complete -------------------------\n")


# end of line