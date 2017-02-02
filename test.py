import unittest, mock
import wxStocks
import wx
import lib

class TestExample(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.password = lib.password_functions.LoginDialog()
        self.main = lib.gui.MainFrame()

    def tearDown(self):
        self.main.Destroy()

    def testPassword(self):
        wx.CallAfter(self.onLogin, "I don't appear until after OnRun exits")
        for attribute in dir(self.app):
            if not attribute.startswith("__"):
                print attribute

    def testWelcomePage(self):
        self.assertEqual("Welcome", self.main.welcome_page.title)

def suite():
    suite = unittest.makeSuite(TestExample, 'test')
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')


# import modelExample
# import wx

# class TestExample(unittest.TestCase):

#     def setUp(self):
#         self.app = wx.PySimpleApp()
#         self.frame = modelExample.ModelExample(parent=None, id=-1)

#     def tearDown(self):
#         self.frame.Destroy()

#     def testModel(self):
#         self.frame.OnBarney(None)
#         self.assertEqual("Barney", self.frame.model.first,
#                 msg="First is wrong")
#         self.assertEqual("Rubble", self.frame.model.last)

# def suite():
#     suite = unittest.makeSuite(TestExample, 'test')
#     return suite

# if __name__ == '__main__':
#     unittest.main(defaultTest='suite')

