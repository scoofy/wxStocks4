import unittest, mock, logging
import lib.password_functions
import lib.db_functions as db
import wx
logging.basicConfig(level=logging.DEBUG, format='%(filename)s %(lineno)d: %(message)s')

class TestMyFunctions(unittest.TestCase):
    @mock.patch("lib.password_functions.FullResetDialog")
    @mock.patch("lib.password_functions.LoginDialog")
    @mock.patch("lib.password_functions.db.is_saved_password_hash", return_value="boop")
    @mock.patch("lib.password_functions.db.load_encryption_strength", return_value=1)
    def test_return_password_verification(self,
                                          mock_load_encrypt,
                                          mock_is_saved,
                                          mock_login_dialog,
                                          mock_full_reset,
                                          ):
        #mock_load_encrypt.return_value = 1
        #mock_is_saved.return_value = 'boop'
        mock_login_dialog().ShowModal.return_value = wx.ID_OK
        assert lib.password_functions.return_password_verification() == wx.ID_OK
        mock_login_dialog().ShowModal.return_value = wx.ID_CANCEL
        assert lib.password_functions.return_password_verification() == wx.ID_CANCEL

        mock_full_reset().ShowModal.return_value = wx.ID_OK
        assert lib.password_functions.return_password_verification(entry_type="Reset Account") == wx.ID_OK
        assert lib.password_functions.return_password_verification(entry_type="Reset Account", error="bad reset") == wx.ID_OK
        mock_full_reset().ShowModal.return_value = wx.ID_CANCEL
        assert lib.password_functions.return_password_verification(entry_type="Reset Account") == wx.ID_CANCEL
        assert lib.password_functions.return_password_verification(entry_type="Reset Account", error="bad reset") == wx.ID_CANCEL















if __name__ == "__main__":
    unittest.main(exit=False)