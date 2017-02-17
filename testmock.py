import unittest, mock, __builtin__, logging
import wx
import lib, pages
import config
logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(lineno)d: %(message)s')

class TestMyFunctions(unittest.TestCase):
    @mock.patch("lib.password_functions.CreateDialog")
    @mock.patch("lib.password_functions.FullResetDialog")
    @mock.patch("lib.password_functions.LoginDialog")
    @mock.patch("lib.password_functions.db.is_saved_password_hash", return_value="boop")
    @mock.patch("lib.password_functions.db.load_encryption_strength", return_value=1)
    def test_return_password_verification_four_ways(self,
        mock_load_encrypt,
        mock_is_saved,
        mock_login_dialog,
        mock_full_reset,
        mock_create_dialog,):
        mock_load_encrypt.return_value = 1
        mock_is_saved.return_value = 'boop'
        mock_login_dialog().ShowModal.return_value = wx.ID_OK
        assert lib.password_functions.return_password_verification() == wx.ID_OK
        mock_login_dialog().ShowModal.return_value = wx.ID_CANCEL
        assert lib.password_functions.return_password_verification() == wx.ID_CANCEL
        mock_login_dialog().ShowModal.return_value = None


        mock_full_reset().ShowModal.return_value = wx.ID_OK
        assert lib.password_functions.return_password_verification(entry_type="Reset Account") == wx.ID_OK
        assert lib.password_functions.return_password_verification(entry_type="Reset Account", error="bad reset") == wx.ID_OK
        mock_full_reset().ShowModal.return_value = wx.ID_CANCEL
        assert lib.password_functions.return_password_verification(entry_type="Reset Account") == wx.ID_CANCEL
        assert lib.password_functions.return_password_verification(entry_type="Reset Account", error="bad reset") == wx.ID_CANCEL

        mock_is_saved.return_value = False

        mock_create_dialog().ShowModal.return_value = wx.ID_OK
        assert lib.password_functions.return_password_verification() == wx.ID_OK
        assert lib.password_functions.return_password_verification(entry_type="passwords do not match") == wx.ID_OK


class TestDBFunctions(unittest.TestCase):

    @mock.patch("lib.db_functions.load_SCREEN_NAME_AND_TIME_CREATED_TUPLE_LIST", return_value="boop")
    @mock.patch("lib.db_functions.load_GLOBAL_STOCK_SCREEN_DICT", return_value="boop")
    @mock.patch("lib.db_functions.load_all_portfolio_objects", return_value="boop")
    @mock.patch("lib.db_functions.load_GLOBAL_TICKER_LIST", return_value="boop")
    @mock.patch("lib.db_functions.load_GLOBAL_STOCK_DICT", return_value="boop")
    def test_load_all_data(self,
        mock_load_GLOBAL_STOCK_DICT,
        mock_load_GLOBAL_TICKER_LIST,
        mock_load_all_portfolio_objects,
        mock_load_GLOBAL_STOCK_SCREEN_DICT,
        mock_load_SCREEN_NAME_AND_TIME_CREATED_TUPLE_LIST,
        ):
        lib.db_functions.load_all_data()
        self.assertEqual(mock_load_GLOBAL_STOCK_DICT.call_count, 1)
        self.assertEqual(mock_load_GLOBAL_TICKER_LIST.call_count, 1)
        self.assertEqual(mock_load_all_portfolio_objects.call_count, 1)
        self.assertEqual(mock_load_GLOBAL_STOCK_SCREEN_DICT.call_count, 1)
        self.assertEqual(mock_load_SCREEN_NAME_AND_TIME_CREATED_TUPLE_LIST.call_count, 1)

    def test_load_GLOBAL_TICKER_LIST(self):
        pass

    def test_create_new_Stock_if_it_doesnt_exist(self):
        from lib.classes import Stock
        odd_strings = ["", "*", "/", "*", "/", "-P", "-", "^", " PR"]
        ticker = "GOOG"
        str_list = [(ticker + x) for x in odd_strings]
        for ticker_str in str_list:
            config.GLOBAL_STOCK_DICT = {}
            stock_obj = lib.db_functions.create_new_Stock_if_it_doesnt_exist(ticker_str)
            self.assertEqual(type(stock_obj), Stock)
            repeat_obj = lib.db_functions.create_new_Stock_if_it_doesnt_exist(stock_obj.ticker)
            self.assertEqual(repeat_obj, stock_obj)
            uni_stock_obj = lib.db_functions.create_new_Stock_if_it_doesnt_exist(unicode(ticker_str))
            self.assertEqual(type(uni_stock_obj), Stock)
    def test_set_Stock_attribute(self):
        from lib.classes import Stock
        test_obj = Stock("test")
        lib.db_functions.set_Stock_attribute(test_obj, "my_attribute", "test_var", "_sf")
        self.assertEqual(test_obj.my_attribute_sf, "test_var")


    @mock.patch("lib.db_functions.load_GLOBAL_ATTRIBUTE_SET", return_value="boop")
    @mock.patch("pickle.dumps", return_value="")
    @mock.patch("pickle.load", return_value={})
    @mock.patch("__builtin__.open", return_value="")
    def test_load_GLOBAL_STOCK_DICT(self,
        mock_open,
        mock_pickle_open,
        mock_pickle_dumps,
        mock_load_GLOBAL_ATTRIBUTE_SET,):
        lib.db_functions.load_GLOBAL_STOCK_DICT()
    #ugh





if __name__ == "__main__":
    unittest.main(exit=False)