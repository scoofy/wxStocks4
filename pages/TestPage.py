import wx, config, logging, string
import lib.gui_position_index as gui_position
import lib.grid_functions as create_grid

class TestPage(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self.title = "Test Page Farts"
        self.uid = config.TICKER_PAGE_UNIQUE_ID
        wx.Panel.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddSpacer(gui_position.TickerPage.AddSpacer) # vertical offset
        self.SetSizer(self.sizer)

        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1,
                             "Welcome to the farts page.",
                             gui_position.TickerPage.text
                             )
        header_sizer.Add(text, 0, wx.ALL|wx.CENTER, 5)

        download_button = wx.Button(self, label="Download Farts", pos=gui_position.TickerPage.download_button)
        download_button.Bind(wx.EVT_BUTTON, self.createGridInPlaceOfTickers, download_button)
        header_sizer.Add(download_button, 0, wx.ALL|wx.CENTER, 5)

        refresh_button = wx.Button(self, label="Refresh Farts", pos=gui_position.TickerPage.refresh_button)
        refresh_button.Bind(wx.EVT_BUTTON, self.refreshTickers, refresh_button)
        header_sizer.Add(refresh_button, 0, wx.ALL|wx.CENTER, 5)


        exchanges = ""
        for exchange_name in config.STOCK_EXCHANGE_LIST:
            if exchange_name is config.STOCK_EXCHANGE_LIST[0]:
                exchanges = exchange_name.upper()
            elif exchange_name is config.STOCK_EXCHANGE_LIST[-1]:
                if len(config.STOCK_EXCHANGE_LIST) == 2:
                    exchanges = exchanges + " and " + exchange_name.upper()
                else:
                    exchanges = exchanges + ", and " + exchange_name.upper()
            else:
                exchanges = exchanges + ", " + exchange_name.upper()

        more_text = wx.StaticText(self, -1,
                             "Currently downloads tickers from %s. To add or remove exchanges, edit the config file." % exchanges,
                             gui_position.TickerPage.more_text
                             )

        self.showAllTickers()
        logging.debug("TickerPage loaded")

    def createDFGrid(self, event):
        import pandas as pd
        import numpy as np
        df_dict = {}
        df_list = []
        count = 0
        rows = range(np.random.randint(26,100))
        cols = range(np.random.randint(26, 100))
        for j in rows:
            for i in cols:
                col_char = chr(i%26 + 97) * (((i/26)+1) + (len(rows)/26)*count)
                df_dict[col_char] = np.array([x*i for x in rows])
                df_list.append((col_char, i*j))
            count+=1

        logging.debug(df_list)
        df = pd.DataFrame(df_dict)
        return create_grid.create_df_grid(self, df,)# autosize=True)

    def downloadTickers(self):
        pass

    # no longer used
    def saveTickerDataAsStocks(self, ticker_data_from_download):
        pass

    def refreshTickers(self, event):
        pass

    def createGridInPlaceOfTickers(self, event):
        logging.debug(self.sizer.GetChildren())
        self.sizer.Hide(self.file_display)
        self.sizer.Remove(self.file_display)
        self.grid = self.createDFGrid("event")

    def showAllTickers(self):
        logging.debug("Loading Tickers")
        ticker_list = []
        for ticker in config.GLOBAL_STOCK_DICT:
            if config.GLOBAL_STOCK_DICT[ticker].ticker_relevant:
                ticker_list.append(ticker)
        ticker_list.sort()
        self.displayTickers(ticker_list)
        self.sizer.Add(self.file_display, 1, wx.ALL|wx.EXPAND)
        self.file_display.Show()
        logging.debug("Done")

    def displayTickers(self, ticker_list):
        ticker_list.sort()
        ticker_list_massive_str = ""
        for ticker in ticker_list:
            ticker_list_massive_str += ticker
            ticker_list_massive_str += ", "

        display_tickers_position_vertical_offset = gui_position.TickerPage.display_tickers_position_vertical_offset
        size = gui_position.TickerPage.display_tickers_size_if_resize_errors
        try:
            width, height = gui_position.main_frame_size()
            size = ( width -  display_tickers_size_horizontal_adjustment , height - display_tickers_position_vertical_offset) # find the difference between the Frame and the grid size
        except:
            pass

        try:
            self.file_display.Destroy()
        except:
            pass
        self.file_display = wx.TextCtrl(self, -1,
                                    ticker_list_massive_str,
                                    (2, display_tickers_position_vertical_offset),
                                    size = size,
                                    style = wx.TE_READONLY | wx.TE_MULTILINE ,
                                    )