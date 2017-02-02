import wx, config, logging
import lib.gui_position_index as gui_position
from pages.getdatapages.importpages.XlsImportPage import XlsImportPage
from pages.getdatapages.importpages.CsvImportPage import CsvImportPage

class SpreadsheetImportPage(wx.Panel):
    def __init__(self, parent):
        self.title = "Import Data Spreadsheets"
        self.uid = config.SPREADSHEET_IMPORT_PAGE_UNIQUE_ID
        wx.Panel.__init__(self, parent)
        ####
        spreadsheet_page_panel = wx.Panel(self, -1, pos=(0,5), size=( wx.EXPAND, wx.EXPAND))
        spreadsheet_notebook = wx.Notebook(spreadsheet_page_panel)

        self.xls_import_page = XlsImportPage(spreadsheet_notebook)
        spreadsheet_notebook.AddPage(self.xls_import_page, self.xls_import_page.title)

        self.csv_import_page = CsvImportPage(spreadsheet_notebook)
        spreadsheet_notebook.AddPage(self.csv_import_page, self.csv_import_page.title)

        sizer2 = wx.BoxSizer()
        sizer2.Add(spreadsheet_notebook, 1, wx.EXPAND)
        self.SetSizer(sizer2)
        ####
