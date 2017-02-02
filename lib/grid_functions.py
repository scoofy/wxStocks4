import wx, logging
import pandas as pd
import numpy as np
import wx.grid as gridlib
import lib.utilities as utils

GRID_LINE_COLOUR = '#CCCCCC'
EVEN_ROW_COLOUR = '#CCE6FF'

def create_df_grid(wxPanel, dataframe, autosize=False):
    try:
        wxPanel.sizer.Hide(wxPanel.grid)
        wxPanel.sizer.Remove(wxPanel.grid)
    except:
        pass
    wxPanel.grid = create_grid(wxPanel, dataframe, autosize)
    wxPanel.grid_sizer = wx.BoxSizer(wx.HORIZONTAL)
    wxPanel.grid_sizer.Add(wxPanel.grid, 1, wx.ALL|wx.EXPAND)
    wxPanel.sizer.Add(wxPanel.grid_sizer, 1, wx.ALL|wx.EXPAND)
    wxPanel.SetSizerAndFit(wxPanel.sizer)
    utils.reset_layout(wxPanel.grid)

def create_grid(panel, data, autosize):
    table = DataTable(data)
    logging.debug("DataTable created")
    grid = DataGrid(panel)
    grid.CreateGrid(len(data), len(data.columns))
    logging.debug("Grid created")
    grid.SetTable(table)
    logging.debug("Table Set")
    if autosize:
        logging.debug("Autosizing grid")
        grid.AutoSize()
        logging.debug("Grid autosized")
    #grid.AutoSizeColumns(autosize)
    #logging.debug("Columns autosized")

    return grid

class DataTable(gridlib.PyGridTableBase):
    def __init__(self, data=None):
        gridlib.PyGridTableBase.__init__(self)
        self.headerRows = 0
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data.columns) + 1

    def GetValue(self, row, col):
        if col == 0:
            return self.data.index[row]
        return self.data.ix[row, col-1]

    def SetValue(self, row, col, value):
        pass

    def GetColLabelValue(self, col):
        if col == 0:
            return 'Index' if self.data.index.name is None else self.data.index.name
        return self.data.columns[col-1]

    def GetTypeName(self, row, col):
        return gridlib.GRID_VALUE_STRING

    def GetAttr(self, row, col, prop):
        attr = gridlib.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr

class DataGrid(gridlib.Grid):
    def __init__(self, parent):
        self.parent = parent
        gridlib.Grid.__init__(self, self.parent, -1)
        self.SetGridLineColour(GRID_LINE_COLOUR)
        self.table = DataTable()

