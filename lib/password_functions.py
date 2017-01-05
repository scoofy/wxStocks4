import wx, logging, sys, base64
import config
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import lib.db_functions as db

def return_password_verification(entry_type="Enter Password", error=None):
    db.load_encryption_strength()
    # check if password exists
    saved_hash = db.is_saved_password_hash()
    if saved_hash:
        if entry_type in ["Enter Password", "Incorrect Password"]:
            login_dialog = LoginDialog(title = entry_type, saved_hash = saved_hash)
            result = login_dialog.ShowModal()
            login_dialog.Destroy()
        if entry_type == "Reset Account":
            incorrect_text_entry = error == "bad reset"
            reset_dialog = FullResetDialog(incorrect_text_entry = incorrect_text_entry)
            result = reset_dialog.ShowModal()
            reset_dialog.Destroy()
    else:
        if entry_type == "passwords do not match":
            logging.debug('try again')
            create_password_dialog = CreateDialog(title = "Passwords did not match")
        else:
            logging.debug('creating password')
            create_password_dialog = CreateDialog()
        result = create_password_dialog.ShowModal()
        create_password_dialog.Destroy()
    return result

class LoginDialog(wx.Dialog):
    def __init__(self, title="Enter Password", saved_hash=None):
        """Constructor"""
        self.saved_hash = saved_hash

        wx.Dialog.__init__(self, None, title=title)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        incorrect_password = title == "Incorrect Password"
        if incorrect_password:
            incorrect_sizer = wx.BoxSizer(wx.HORIZONTAL)
            incorrect_label = wx.StaticText(self, label="The password you entered was incorrect, please try again:")
            incorrect_sizer.Add(incorrect_label, 0, wx.ALL|wx.CENTER, 5)
            main_sizer.Add(incorrect_sizer, 0, wx.ALL, 5)

        # pass info
        password_entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(self, label="Password:")
        password_entry_sizer.Add(password_label, 0, wx.ALL|wx.CENTER, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.password.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        password_entry_sizer.Add(self.password, 0, wx.ALL, 5)
        main_sizer.Add(password_entry_sizer, 0, wx.ALL, 5)

        button = wx.Button(self, label="Login")
        button.Bind(wx.EVT_BUTTON, self.onLogin)
        main_sizer.Add(button, 0, wx.ALL|wx.CENTER, 5)
        if incorrect_password:
            reset_button = wx.Button(self, label="Reset Account")
            reset_button.Bind(wx.EVT_BUTTON, self.resetAccount)
            main_sizer.Add(reset_button, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(main_sizer)

    def resetAccount(self, event):
        try_again = return_password_verification(entry_type = "Reset Account")
        if not try_again:
            try_again = wx.ID_CANCEL
        self.EndModal(try_again)


    def onLogin(self, event):
        """
        Check credentials and login
        """
        password = self.password.GetValue()

        if not db.valid_pw(password, self.saved_hash):
            try_again = return_password_verification(entry_type = "Incorrect Password")
            if not try_again:
                try_again = wx.ID_CANCEL
            self.EndModal(try_again)

        else:
            valid_salt = db.return_salt(self.saved_hash)
            kdf = PBKDF2HMAC(
                            algorithm=hashes.SHA256(),
                            length=32,
                            salt=valid_salt,
                            iterations=100000,
                            backend=default_backend()
                            )
            config.PASSWORD = base64.urlsafe_b64encode(kdf.derive(str(password)))
            self.EndModal(wx.ID_OK)


class FullResetDialog(wx.Dialog):
    def __init__(self, incorrect_text_entry=False):
        wx.Dialog.__init__(self, None, title="Full Account Reset")

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        if incorrect_text_entry:
            incorrect_sizer = wx.BoxSizer(wx.HORIZONTAL)
            incorrect_label = wx.StaticText(self, label='You did not enter the confirmation text correctly.')
            incorrect_sizer.Add(incorrect_label, 0, wx.ALL|wx.CENTER, 5)
            main_sizer.Add(incorrect_sizer, 0, wx.ALL, 5)


        reset_sizer = wx.BoxSizer(wx.HORIZONTAL)
        reset_label = wx.StaticText(self, label='To do a full reset type (without quotes): "delete all data"')
        reset_sizer.Add(reset_label, 0, wx.ALL|wx.CENTER, 5)
        main_sizer.Add(reset_sizer, 0, wx.ALL, 5)

        reset_entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.reset_text_entry = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        reset_entry_sizer.Add(self.reset_text_entry, 0, wx.ALL, 5)
        main_sizer.Add(reset_entry_sizer, 0, wx.ALL, 5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        reset_button = wx.Button(self, label="Delete all data and reset")
        reset_button.Bind(wx.EVT_BUTTON, self.fullReset)
        button_sizer.Add(reset_button, 0, wx.ALL|wx.CENTER, 5)
        cancel_button = wx.Button(self, label="Cancel")
        cancel_button.Bind(wx.EVT_BUTTON, self.cancelReset)
        button_sizer.Add(cancel_button, 0, wx.ALL|wx.CENTER, 5)

        main_sizer.Add(button_sizer, 0, wx.ALL|wx.CENTER, 5)

        self.SetSizer(main_sizer)

    def cancelReset(self, event):
        try_again = return_password_verification()
        if not try_again:
            try_again = wx.ID_CANCEL
        self.EndModal(try_again)

    def fullReset(self, event):
        confirm = self.reset_text_entry.GetValue()
        logging.debug(confirm)
        if confirm == u"delete all data":
            db.delete_all_secure_files()
            self.EndModal(wx.ID_REMOVE)
        else:
            try_again = return_password_verification(entry_type = "Reset Account", error="bad reset")
            if not try_again:
                try_again = wx.ID_CANCEL
            self.EndModal(try_again)



class CreateDialog(wx.Dialog):
    def __init__(self, title = "Create Password"):
        """Constructor"""
        wx.Dialog.__init__(self, None, title=title)

        # create password info
        password_entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(self, label="Type new password:")
        password_entry_sizer.Add(password_label, 0, wx.ALL|wx.CENTER, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        password_entry_sizer.Add(self.password, 0, wx.ALL, 5)

        verify_entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        verify_label = wx.StaticText(self, label="Confirm password:")
        verify_entry_sizer.Add(verify_label, 0, wx.ALL|wx.CENTER, 5)
        self.verify = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        verify_entry_sizer.Add(self.verify, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(password_entry_sizer, 0, wx.ALL, 5)
        main_sizer.Add(verify_entry_sizer, 0, wx.ALL, 5)

        button = wx.Button(self, label="Save Password")
        button.Bind(wx.EVT_BUTTON, self.onSubmit)
        main_sizer.Add(button, 0, wx.ALL|wx.CENTER, 5)

        self.SetSizer(main_sizer)

    def onSubmit(self, event):
        password = self.password.GetValue()
        verify = self.verify.GetValue()
        logging.debug("password: " + password)
        logging.debug(type(password))
        logging.debug("verify: " + verify)
        if password == verify:
            try:
                logging.debug('saving')
                db.save_password(password)
                valid_salt = db.return_salt(db.is_saved_password_hash())
                kdf = PBKDF2HMAC(
                                algorithm=hashes.SHA256(),
                                length=32,
                                salt=valid_salt,
                                iterations=100000,
                                backend=default_backend()
                                )
                config.PASSWORD = base64.urlsafe_b64encode(kdf.derive(str(password)))
                password, verify = None, None
                self.EndModal(wx.ID_APPLY)
            except Exception as e:
                logging.warning(e)
                sys.exit()
        else:
            try_again = return_password_verification(entry_type = "passwords do not match")
            logging.debug(str(try_again))
            if not try_again:
                try_again = wx.ID_CANCEL
            self.EndModal(try_again)
