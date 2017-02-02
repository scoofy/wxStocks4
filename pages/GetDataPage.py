import wx, config, logging
import lib.gui_position_index as gui_position

from pages.getdatapages.TickerPage import TickerPage
from pages.getdatapages.YqlScrapePage import YqlScrapePage
from pages.getdatapages.SpreadsheetImportPage import SpreadsheetImportPage

class GetDataPage(wx.Panel):
    def __init__(self, parent):
        self.title = "Import Data"
        self.uid = config.GET_DATA_PAGE_UNIQUE_ID
        wx.Panel.__init__(self, parent)
        ####
        self.get_data_notebook = wx.Notebook(self)

        self.ticker_page = TickerPage(self.get_data_notebook)
        self.get_data_notebook.AddPage(self.ticker_page, self.ticker_page.title)

        self.yql_scrape_page = YqlScrapePage(self.get_data_notebook)
        self.get_data_notebook.AddPage(self.yql_scrape_page, self.yql_scrape_page.title)

        self.spreadsheet_import_page = SpreadsheetImportPage(self.get_data_notebook)
        self.get_data_notebook.AddPage(self.spreadsheet_import_page, self.spreadsheet_import_page.title)

        sizer2 = wx.BoxSizer()
        sizer2.Add(self.get_data_notebook, 1, wx.EXPAND, 0)
        self.SetSizer(sizer2)
        ####

