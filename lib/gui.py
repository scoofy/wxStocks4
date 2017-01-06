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
from pages.TestPage import TestPage

class MainFrame(wx.Frame): # reorder tab postions here
    def __init__(self, parent=None, title="wxStocks", size = gui_position.MainFrame_size):
        wx.Frame.__init__(self, parent=parent, title=title, size = size)
        self.parent = parent
        self.SetSizeHints(gui_position.MainFrame_SetSizeHints[0],gui_position.MainFrame_SetSizeHints[1])
        self.title = "wxStocks"
        self.uid = config.MAIN_FRAME_UNIQUE_ID


        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Here we create a panel and a notebook on the panel
        main_frame = wx.Panel(self)
        self.notebook = wx.Notebook(main_frame)
        self.notebook.parent = main_frame


        # create the page windows as children of the notebook
        # add the pages to the notebook with the label to show on the tab
        self.test_page = TestPage(self.notebook)
        self.notebook.AddPage(self.test_page, self.test_page.title)

        sizer.Add(self.notebook, 1, wx.EXPAND)
        main_frame.SetSizer(sizer)



        logging.debug("done.\n\n------------------------- wxStocks startup complete -------------------------\n")


# end of line