import wx, config, logging
import lib.gui_position_index as gui_position
import lib.utilities as utils

class WelcomePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.title = "Welcome"
        self.uid = config.WELCOME_PAGE_UNIQUE_ID
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.instructions_text = '''
    Instructions:   this program is essentially a work-flow following the tabs above.
    ---------------------------------------------------------------------------------------------------------------------------------

    Welcome:\t\t\t\t\t\tGeneral insturction and password reset.

    Import Data:
    \tDownload Tickers:\t\t\tThis page is where you download ticker .CSV files to create a list of tickers to scrape.
    \tScrape YQL:\t\t\t\t\tThis page takes all tickers, and then scrapes current stock data using them.
    \tImport Data Spreadsheets:\t\tThis page allows you to import your own spreadsheets. You must first create functions in it's Edit Functions tab.

    Portfolios:\t\t\t\t\t\tThis page allows you to load your portfolios from which you plan on making trades.
    \t\t\t\t\t\t\t\tIf you have more than one portfolio you plan on working from, you may add more.

    View Data:
    \tView All Stocks:\t\t\t\tThis page generates a list of all stocks that have been scraped and presents all the data about them.
    \t\t\t\t\t\t\t\t-  Use this page to double check your data to make sure it's accurate and up to date.
    \tView One Stock:\t\t\t\tThis page allows you to look at all the data associated with one stock.
    \t\t\t\t\t\t\t\t-  Here you will find the attributes you may use in programming your own functions involving individual stocks.

    Analyse Data:
    \tScreen:\t\t\t\t\t\tThis page allows you to screen for stocks that fit your criteria, and save them for later.
    \tSaved Screens:\t\t\t\tThis page allows you to recall old screens you've saved.
    \tRank:\t\t\t\t\t\tThis page allows you to rank stocks along certain criteria.
    \tCustom Analysis:\t\t\t\tThis page allows you to execute your own custom analysis.
    \t\t\t\t\t\t\t\t-  You can learn about programming and interfacing with wxStocks to do your own analysis in the Edit Functions section.

    Research:\t\t\t\t\t\tDo your homework! This page allows you to easily access data for stocks you intend to buy or sell.
    \t\t\t\t\t\t\t\tYou can add different buttons in the config page if you have other sources your prefer.

    Sale Prep:\t\t\t\t\t\tThis page allows you to estimate the amount of funds generated from a potential stock sale.

    Trade:\t\t\t\t\t\t\tThis page (currently not functional) takes the stocks you plan to sell, estimates the amount of money generated,
    \t\t\t\t\t\t\t\tand lets you estimate the volume of stocks to buy to satisfy your diversification requirements.

    Edit Functions:\t\t\t\t\tHere you many view/edit/restore user created functions. You may also edit them in your own text editor.

    '''

        self.instructions = wx.TextCtrl(self,
                                        id = -1,
                                        value = self.instructions_text,
                                        style = wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_READONLY,
                                        )
        self.instructions.Refresh()
        self.text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_sizer.Add(self.instructions, 1, wx.EXPAND)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.reset_password_button = wx.Button(self, label="Reset Password")
        self.reset_password_button.Bind(wx.EVT_BUTTON, self.toggleResetSizer, self.reset_password_button)
        self.button_sizer.Add(self.reset_password_button, 0, flag = wx.ALIGN_RIGHT)

        current_password_text = "Current Password:"
        self.current_password_static_text = wx.StaticText(self, id = -1, label = current_password_text)
        self.current_password_field = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)

        new_password_text = "New Password:"
        self.new_password_static_text = wx.StaticText(self, id = -1, label = new_password_text)
        self.new_password_field = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD ) #| wx.TE_PROCESS_ENTER)

        confirm_password_text = "Confirm New Password:"
        self.confirm_password_static_text = wx.StaticText(self, id = -1, label = confirm_password_text)
        self.confirm_new_password_field = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD ) #| wx.TE_PROCESS_ENTER)



        encryption_hardness_text = "Encryption Strength (1-24) (optional):"
        self.encryption_hardness_static_text = wx.StaticText(self, id = -1, label = encryption_hardness_text)
        self.encryption_hardness_field = wx.TextCtrl(self, -1, "")
        self.encryption_hardness_field.SetHint("default = 8")

        self.reset_password_submit_button = wx.Button(self, label="Submit")
        self.reset_password_submit_button.Bind(wx.EVT_BUTTON, self.resetPassword, self.reset_password_submit_button)

        self.password_reset_status_static_text = wx.StaticText(self, id = -1, label = "")

        self.delete_all_stock_data = wx.Button(self, label="Delete All Stock Data")
        self.delete_all_stock_data.Bind(wx.EVT_BUTTON,
                                        self.deleteAllStockData,
                                        self.delete_all_stock_data)
        self.button_sizer.Add(self.delete_all_stock_data, 0, flag = wx.ALIGN_RIGHT)

        self.reset_sizer = wx.FlexGridSizer(rows = 2, cols=5)
        self.reset_sizer_is_shown = True
        self.reset_sizer.Add(self.current_password_static_text, 0, wx.ALIGN_RIGHT)
        self.reset_sizer.Add(self.current_password_field, 0)
        self.reset_sizer.Add(self.new_password_static_text, 0, wx.ALIGN_RIGHT)
        self.reset_sizer.Add(self.new_password_field, 0)
        self.reset_sizer.Add(self.password_reset_status_static_text, 0, wx.ALIGN_RIGHT)

        self.reset_sizer.Add(self.encryption_hardness_static_text, 0, wx.ALIGN_RIGHT)
        self.reset_sizer.Add(self.encryption_hardness_field, 0)
        self.reset_sizer.Add(self.confirm_password_static_text, 0, wx.ALIGN_RIGHT)
        self.reset_sizer.Add(self.confirm_new_password_field, 0)
        self.reset_sizer.Add(self.reset_password_submit_button, 0, wx.ALIGN_RIGHT)



        self.sizer.Add(self.text_sizer, 1, wx.CENTER|wx.EXPAND, 10)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.button_sizer, 0, wx.ALIGN_RIGHT, 10)
        self.sizer.Add(self.reset_sizer, 0, wx.ALIGN_RIGHT, 10)

        self.toggleResetSizer('event')

        self.SetSizer(self.sizer)
        logging.debug("WelcomePage loaded")

        #self.toggleResetSizer('event') command executes in gui

    def toggleResetSizer(self, event):
        self.reset_sizer_is_shown = not self.reset_sizer_is_shown
        if not self.reset_sizer_is_shown:
            self.current_password_field.Clear()
            self.new_password_field.Clear()
            self.confirm_new_password_field.Clear()
            self.encryption_hardness_field.Clear()
        self.reset_sizer.ShowItems(show = self.reset_sizer_is_shown)
        self.Layout()

    def testFunction(self, event):
        try:
            self.function_to_test()
        except Exception as e:
            logging.debug(e)

    def resetPassword(self, event):
        old_password = self.current_password_field.GetValue()
        new_password = self.new_password_field.GetValue()
        confirm_password = self.confirm_new_password_field.GetValue()
        encryption_strength = self.encryption_hardness_field.GetValue()
        if encryption_strength:
            try:
                encryption_strength = int(encryption_strength)
            except:
                self.password_reset_status_static_text.SetLabel("Encryption strength must be an integer or blank.")
                self.current_password_field.Clear()
                self.new_password_field.Clear()
                self.confirm_new_password_field.Clear()
                self.encryption_hardness_field.Clear()
                return

        saved_hash = db.is_saved_password_hash()

        if new_password != confirm_password:
            self.password_reset_status_static_text.SetLabel("Your confirmation did not match your new password.")
            self.current_password_field.Clear()
            self.new_password_field.Clear()
            self.confirm_new_password_field.Clear()
            self.encryption_hardness_field.Clear()
            return

        if not db.valid_pw(old_password, saved_hash):
            self.password_reset_status_static_text.SetLabel("The password you submitted is incorrect.")
            self.current_password_field.Clear()
            self.new_password_field.Clear()
            self.confirm_new_password_field.Clear()
            self.encryption_hardness_field.Clear()
            return

        # Success!
        # reset password and all relevant files
        db.reset_all_encrypted_files_with_new_password(old_password, new_password, encryption_strength)
        self.password_reset_status_static_text.SetLabel("You have successfully change your password.")
        self.closePasswordResetFields()


    def closePasswordResetFields(self):
        self.reset_password_submit_button.Hide()

        self.current_password_field.Clear()
        self.new_password_field.Clear()
        self.confirm_new_password_field.Clear()
        self.encryption_hardness_field.Clear()

        self.current_password_static_text.Hide()
        self.current_password_field.Hide()
        self.new_password_static_text.Hide()
        self.new_password_field.Hide()
        self.confirm_password_static_text.Hide()
        self.confirm_new_password_field.Hide()
        self.encryption_hardness_static_text.Hide()
        self.encryption_hardness_field.Hide()

        self.reset_password_button.Show()

    def deleteAllStockData(self, event):
        confirm = wx.MessageDialog(None,
                                 "Caution! You are about to delete all saved stock data. Your portfolio and screen data will remain, but all stock data will be deleted. To avoid errors, the program will then update basic stock data, and shut down.",
                                 'Delete All Stock Data?',
                                 style = wx.YES_NO
                                 )
        confirm.SetYesNoLabels(("&Cancel"), ("&Yes, Delete All Stock Data and Restart"))
        yesNoAnswer = confirm.ShowModal()
        confirm.Destroy()
        if yesNoAnswer == wx.ID_NO:
            self.deleteAllStockDataConfirm()

    def deleteAllStockDataConfirm(self):
        config.GLOBAL_TICKER_LIST = []
        db.save_GLOBAL_TICKER_LIST()

        config.GLOBAL_STOCK_DICT = {}
        config.GLOBAL_ATTRIBUTE_SET = set([])
        db.save_GLOBAL_STOCK_DICT()

        print line_number(), "Data deleted."

        ticker_page = config.GLOBAL_PAGES_DICT.get(config.TICKER_PAGE_UNIQUE_ID).obj
        ticker_page.downloadTickers()

        sys.exit()
