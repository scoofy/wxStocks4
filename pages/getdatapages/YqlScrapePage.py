import wx, config, logging
import lib.utilities as utils
import lib.gui_position_index as gui_position

class YqlScrapePage(wx.Panel):
    def __init__(self, parent):
        self.title = "Scrape YQL"
        self.uid = config.YQL_SCRAPE_PAGE_UNIQUE_ID
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1,
                             "Welcome to the scrape page",
                             gui_position.YqlScrapePage.text
                             )
        self.scrape_button = wx.Button(self, label="Scrape YQL", pos=gui_position.YqlScrapePage.scrape_button, size=(-1,-1))
        self.scrape_button.Bind(wx.EVT_BUTTON, self.confirmScrape, self.scrape_button)

        self.abort_scrape_button = wx.Button(self, label="Cancel Scrape", pos=gui_position.YqlScrapePage.abort_scrape_button, size=(-1,-1))
        self.abort_scrape_button.Bind(wx.EVT_BUTTON, self.abortScrape, self.abort_scrape_button)
        self.abort_scrape_button.Hide()
        self.abort_scrape = False

        self.progress_bar = wx.Gauge(self, -1, 100, size=gui_position.YqlScrapePage.progress_bar_size, pos = gui_position.YqlScrapePage.progress_bar)
        self.progress_bar.Hide()

        self.numScrapedStocks = 0
        self.number_of_tickers_to_scrape = 0
        self.total_relevant_tickers = 0
        self.tickers_to_scrape = 0
        self.scrape_time_text = 0
        self.number_of_unscraped_stocks = 0


        self.total_relevant_tickers = wx.StaticText(self, -1,
                             label = "Total number of tickers = {}".format(self.numScrapedStocks + self.number_of_tickers_to_scrape),
                             pos = gui_position.YqlScrapePage.total_relevant_tickers
                             )
        self.tickers_to_scrape = wx.StaticText(self, -1,
                             label = "Tickers that need to be scraped = {}".format(self.number_of_tickers_to_scrape),
                             pos = gui_position.YqlScrapePage.tickers_to_scrape
                             )
        sleep_time = config.SCRAPE_SLEEP_TIME
        scrape_time_secs = (self.number_of_tickers_to_scrape/config.SCRAPE_CHUNK_LENGTH) * sleep_time * 2
        scrape_time = utils.time_from_epoch(scrape_time_secs)
        self.scrape_time_text = wx.StaticText(self, -1,
                     label = "Time = {}".format(scrape_time),
                     pos = gui_position.YqlScrapePage.scrape_time_text
                     )


        self.calculate_scrape_times()

        logging.debug("YqlScrapePage loaded")

    def calculate_scrape_times(self):
        logging.debug("Calculating scrape times...")
        sleep_time = config.SCRAPE_SLEEP_TIME

        # calculate number of stocks and stuff to scrape
        self.numScrapedStocks = 0
        self.number_of_tickers_to_scrape = 0
        for stock in config.GLOBAL_STOCK_DICT:
            if config.GLOBAL_STOCK_DICT[stock].ticker_relevant:
                self.number_of_tickers_to_scrape += 1
                current_time = float(time.time())
                time_since_update = current_time - config.GLOBAL_STOCK_DICT[stock].last_yql_basic_scrape_update
                if (int(time_since_update) < int(config.TIME_ALLOWED_FOR_BEFORE_RECENT_UPDATE_IS_STALE) ):
                    self.numScrapedStocks += 1

        self.number_of_unscraped_stocks = self.number_of_tickers_to_scrape - self.numScrapedStocks
        total_ticker_len = len(config.GLOBAL_STOCK_DICT)
        scrape_time_secs = (self.number_of_unscraped_stocks/config.SCRAPE_CHUNK_LENGTH) * sleep_time * 2
        scrape_time = utils.time_from_epoch(scrape_time_secs)

        self.total_relevant_tickers.SetLabel("Total number of tickers = {}".format(self.number_of_tickers_to_scrape))

        self.tickers_to_scrape.SetLabel("Tickers that need to be scraped = {}".format(self.number_of_unscraped_stocks))

        self.scrape_time_text.SetLabel("Time = {}".format(scrape_time))

        logging.debug("Calculation done")

    def confirmScrape(self, event):
        confirm = wx.MessageDialog(None,
                                   "You are about to scrape of Yahoo's YQL database. If you do this too often Yahoo may temporarily block your IP address.",
                                   'Scrape stock data?',
                                   style = wx.YES_NO
                                   )
        confirm.SetYesNoLabels(("&Scrape"), ("&Cancel"))
        yesNoAnswer = confirm.ShowModal()
        #try:
        #   confirm.SetYesNoLabels(("&Scrape"), ("&Cancel"))
        #except AttributeError:
        #   pass
        confirm.Destroy()

        if yesNoAnswer == wx.ID_YES:
            self.scrapeYQL()

    def scrapeYQL(self):
        chunk_list_and_percent_of_full_scrape_done_and_number_of_tickers_to_scrape = scrape.prepareYqlScrape()

        chunk_list = chunk_list_and_percent_of_full_scrape_done_and_number_of_tickers_to_scrape[0]
        percent_of_full_scrape_done = chunk_list_and_percent_of_full_scrape_done_and_number_of_tickers_to_scrape[1]
        self.number_of_tickers_to_scrape = chunk_list_and_percent_of_full_scrape_done_and_number_of_tickers_to_scrape[2]


        self.progress_bar.SetValue(percent_of_full_scrape_done)
        self.progress_bar.Show()
        self.scrape_button.Hide()
        self.abort_scrape_button.Show()

        # Process the scrape while updating a progress bar
        timer = threading.Timer(0, self.executeScrapePartOne, [chunk_list, 0])
        timer.start()

        #scrape_thread = threading.Thread(target=self.executeOneScrape, args = (ticker_chunk,))
        #scrape_thread.daemon = True
        #scrape_thread.start()
        #while scrape_thread.isAlive():

        #   # Every two sleep times execute a new scrape
        #   full_scrape_sleep = float(sleep_time * 2)
        #   scrape_thread.join(full_scrape_sleep)
        #   cont, skip = progress_dialog.Update(self.numScrapedStocks)
        #   if not cont:
        #       progress_dialog.Destroy()
        #       return

    def executeScrapePartOne(self, ticker_chunk_list, position_of_this_chunk):
        if self.abort_scrape == True:
            self.abort_scrape = False
            self.progress_bar.Hide()
            logging.debug("Scrape canceled.")
            return

        data = scrape.executeYqlScrapePartOne(ticker_chunk_list, position_of_this_chunk)

        sleep_time = config.SCRAPE_SLEEP_TIME
        timer = threading.Timer(sleep_time, self.executeScrapePartTwo, [ticker_chunk_list, position_of_this_chunk, data])
        timer.start()



    def executeScrapePartTwo(self, ticker_chunk_list, position_of_this_chunk, successful_pyql_data):
        if self.abort_scrape == True:
            self.abort_scrape = False
            self.progress_bar.Hide()
            logging.debug("Scrape canceled.")
            return

        scrape.executeYqlScrapePartTwo(ticker_chunk_list, position_of_this_chunk, successful_pyql_data)

        sleep_time = config.SCRAPE_SLEEP_TIME
        logging.warning("Sleeping for {} seconds before the next task".format(sleep_time))
        #time.sleep(sleep_time)

        #self.numScrapedStocks += number_of_stocks_in_this_scrape
        #cont, skip = self.progress_dialog.Update(self.numScrapedStocks)
        #if not cont:
        #   self.progress_dialog.Destroy()
        #   return


        number_of_tickers_in_chunk_list = 0
        for chunk in ticker_chunk_list:
            for ticker in chunk:
                number_of_tickers_in_chunk_list += 1
        number_of_tickers_previously_updated = self.number_of_tickers_to_scrape - number_of_tickers_in_chunk_list
        number_of_tickers_done_in_this_scrape = 0
        for i in range(len(ticker_chunk_list)):
            if i > position_of_this_chunk:
                continue
            for ticker in ticker_chunk_list[i]:
                number_of_tickers_done_in_this_scrape += 1
        total_number_of_tickers_done = number_of_tickers_previously_updated + number_of_tickers_done_in_this_scrape
        percent_of_full_scrape_done = round( 100 * float(total_number_of_tickers_done) / float(self.number_of_tickers_to_scrape))

        position_of_this_chunk += 1
        percent_done = round( 100 * float(position_of_this_chunk) / float(len(ticker_chunk_list)) )
        logging.debug("{}%".format(percent_done) + " done this scrape execution.")
        logging.debug("{}%".format(percent_of_full_scrape_done) + " done of all tickers.")
        self.progress_bar.SetValue(percent_of_full_scrape_done)
        self.calculate_scrape_times()
        if position_of_this_chunk >= len(ticker_chunk_list):
            # finished
            self.abort_scrape_button.Hide()
            self.scrape_button.Show()
            self.progress_bar.SetValue(100)
            return
        else:
            logging.debug("ready to loop again")
            timer = threading.Timer(sleep_time, self.executeScrapePartOne, [ticker_chunk_list, position_of_this_chunk])
            timer.start()

    def abortScrape(self, event):
        logging.debug("Canceling scrape... this may take up to {} seconds.".format(config.SCRAPE_SLEEP_TIME))
        if self.abort_scrape == False:
            self.abort_scrape = True
            self.abort_scrape_button.Hide()
            self.scrape_button.Show()
            self.calculate_scrape_times()
