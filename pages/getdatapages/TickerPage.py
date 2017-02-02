import wx, config, logging
import lib.gui_position_index as gui_position
import lib.scrapers as scrape
import lib.db_functions as db
import threading

class TickerPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.title = "Download Ticker Data"
        self.uid = config.TICKER_PAGE_UNIQUE_ID

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.download_button = wx.Button(self, label="Download Tickers")
        self.download_button.Bind(wx.EVT_BUTTON, self.confirmDownloadTickers, self.download_button)
        self.button_sizer.Add(self.download_button, 0, wx.EXPAND)


        self.refresh_button = wx.Button(self, label="Refresh")
        self.refresh_button.Bind(wx.EVT_BUTTON, self.refreshTickers, self.refresh_button)
        self.button_sizer.Add(self.refresh_button, 0, wx.EXPAND)

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

        self.more_text = wx.StaticText(self, -1,
                             "Currently downloads tickers from {}. To add or remove exchanges, edit the config file.".format(exchanges),
                             )
        self.button_sizer.Add(self.more_text, 0, wx.EXPAND)


        self.sizer.Add(self.button_sizer, 0, wx.EXPAND)
        self.showAllTickers()
        self.SetSizer(self.sizer)
        logging.debug("TickerPage loaded")

    def confirmDownloadTickers(self, event):
        confirm = wx.MessageDialog(None,
                                   "You are about to make a request from Nasdaq.com. If you do this too often they may temporarily block your IP address.",
                                   'Confirm Download',
                                   style = wx.YES_NO
                                   )
        confirm.SetYesNoLabels(("&Download"), ("&Cancel"))
        yesNoAnswer = confirm.ShowModal()
        #try:
        #   confirm.SetYesNoLabels(("&Scrape"), ("&Cancel"))
        #except AttributeError:
        #   pass
        confirm.Destroy()
        self.file_display.Hide()

        if yesNoAnswer == wx.ID_YES:
            download_tickers = threading.Thread(name="download tickers", target=self.downloadTickers)
            download_tickers.start()

    def downloadTickers(self):
        logging.debug("Begin ticker download...")
        ticker_list_without_prices = scrape.nasdaq_full_ticker_list_downloader()
        uppercase_exchange_list = [x.upper() for x in config.STOCK_EXCHANGE_LIST]
        for data in ticker_list_without_prices:
            #print data
            # The following line does:
            # data[2] is exchange
            if data[2].upper() in uppercase_exchange_list:
                stock = db.create_new_Stock_if_it_doesnt_exist(data[0])
                stock.firm_name = data[1]
                stock.Exchange_na = data[2]
                stock.etf_na = data[3]

        logging.debug("Begin price data download...")
        ticker_data = scrape.convert_nasdaq_csv_to_stock_objects()
        db.save_GLOBAL_STOCK_DICT()

        self.showAllTickers()
        # Update scrape page
        scrape_page = config.GLOBAL_PAGES_DICT.get(config.YQL_SCRAPE_PAGE_UNIQUE_ID).obj
        scrape_page.calculate_scrape_times()
        # Update view all stocks
        view_all_stocks_page = config.GLOBAL_PAGES_DICT.get(config.ALL_STOCKS_PAGE_UNIQUE_ID).obj
        view_all_stocks_page.spreadSheetFillAllStocks("event")

    # no longer used
    def saveTickerDataAsStocks(self, ticker_data_from_download):
        # first check for stocks that have fallen off the stock exchanges
        ticker_list = []
        dead_tickers = []

        # create a list of tickers
        for ticker_data_sublist in ticker_data_from_download:
            logging.debug(ticker_data_sublist[0] + ":", ticker_data_sublist[1])

            ticker_symbol_upper = utils.strip_string_whitespace(ticker_data_sublist[0]).upper()
            ticker_list.append(ticker_symbol_upper)

        # check all stocks against that list
        for ticker in config.GLOBAL_STOCK_DICT:
            if ticker in ticker_list:
                if config.GLOBAL_STOCK_DICT[ticker].ticker_relevant == False:
                    config.GLOBAL_STOCK_DICT[ticker].ticker_relevant = True
                logging.debug(ticker, "appears to be fine")
            else:
                # ticker may have been removed from exchange
                logging.debug(ticker + " appears to be dead")
                dead_tickers.append(ticker)

        # check for errors, and if not, mark stocks as no longer on exchanges:
        if len(dead_tickers) > config.NUMBER_OF_DEAD_TICKERS_THAT_SIGNALS_AN_ERROR:
            logging.error("Something went wrong with ticker download, probably a dead link")
        else:
            for dead_ticker_symbol in dead_tickers:
                logging.debug(dead_ticker_symbol)
                dead_stock = utils.return_stock_by_symbol(dead_ticker_symbol)
                dead_stock.ticker_relevant = False

        # save stocks if new
        for ticker_data_sublist in ticker_data_from_download:
            ticker_symbol = utils.strip_string_whitespace(ticker_data_sublist[0])
            firm_name = ticker_data_sublist[1]

            if "$" in ticker_symbol:
                logging.debug('Ticker {} with "$" symbol found, not sure if ligitimate, so not saving it.'.format(ticker_symbol))
                continue

            stock = db.create_new_Stock_if_it_doesnt_exist(ticker_symbol)
            stock.firm_name = firm_name
            logging.debug("Saving:", stock.ticker, stock.firm_name)
        db.save_GLOBAL_STOCK_DICT()
    # end no longer used

    def refreshTickers(self, event):
        self.showAllTickers()

    def showAllTickers(self):
        logging.debug("Loading Tickers")
        ticker_list = [ticker for ticker in config.GLOBAL_STOCK_DICT]
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

        #print line_number()
        #pp.pprint(config.GLOBAL_STOCK_DICT)
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
