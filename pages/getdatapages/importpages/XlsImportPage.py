import wx, config, logging
import lib.gui_position_index as gui_position
import lib.meta_functions as meta

class XlsImportPage(wx.Panel):
    def __init__(self, parent):
        self.title = "Import .XLS Data"
        self.uid = config.XLS_IMPORT_PAGE_UNIQUE_ID
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1,
                             "Welcome to the XLS data import page page.\nYou can make your own import functions under the function tab.",
                             (10,10)
                             )

        default_button_position = gui_position.XlsImportPage.default_button_position
        default_button_horizontal_position = default_button_position[0]
        default_button_vertical_position = default_button_position[1]
        default_dropdown_offset = gui_position.XlsImportPage.default_dropdown_offset
        default_dropdown_horizontal_offset = default_dropdown_offset[0]
        default_dropdown_vertical_offset = default_dropdown_offset[1]
        aaii_offset = gui_position.XlsImportPage.aaii_offset # if aaii files in aaii import folder, this button will appear below the import dropdown

        import_button = wx.Button(self, label="import .xls", pos=(default_button_horizontal_position, default_button_vertical_position), size=(-1,-1))
        import_button.Bind(wx.EVT_BUTTON, self.importXLS, import_button)

        import_all_aaii_files_button = wx.Button(self, label="import aaii files from folder", pos=(default_button_horizontal_position, default_button_vertical_position + aaii_offset), size=(-1,-1))
        import_all_aaii_files_button.Bind(wx.EVT_BUTTON, self.import_AAII_files, import_all_aaii_files_button)

        self.xls_import_name_list = meta.return_xls_import_function_short_names()
        self.drop_down = wx.ComboBox(self, pos=(default_button_horizontal_position + default_dropdown_horizontal_offset, default_button_vertical_position + default_dropdown_vertical_offset), choices=self.xls_import_name_list)

        self.triple_list = meta.return_xls_import_function_triple()

        self.xls_import_name = None

    def importXLS(self, event):
        self.xls_import_name = self.drop_down.GetValue()

        # Identify the function mapped to screen name
        for triple in self.triple_list:
            if self.xls_import_name == triple.doc:
                xls_import_function = triple.function
            # in case doc string is too many characters...
            elif self.xls_import_name == triple.name:
                xls_import_function = triple.function

        if not xls_import_function:
            print line_number(), "Error, somthing went wrong locating the correct import function to use."

        # run ranking funtion on all stocks

        success = process_user_function.import_xls_via_user_created_function(self, xls_import_function)

        if not success:
            return

        if success == "fail":
            title_string = "Error"
            success_string = "This import has failed, please check make sure your function conforms to the import protocols."
            message_style = wx.ICON_ERROR
        elif success == "some":
            title_string = "Some Errors"
            success_string = "There were some errors with your import, please review your XLS file and make sure that your functions conform to the protocols, and that the ticker symbols in your xls files are the same format as wxStocks'."
            message_style = wx.ICON_EXCLAMATION
        elif success == "success":
            title_string = "Success"
            success_string = "Success! You're file has been successfully imported."
            message_style = wx.OK
        else:
            print line_number(), "Error in importXLS title and success strings"
            return

        print line_number(), "importXLS done"


        confirm = wx.MessageDialog(None,
                                   success_string,
                                   title_string,
                                   style = message_style
                                   )
        confirm.ShowModal()

    def import_AAII_files(self, event):
        print line_number(), "Remove argument below this line after debugging"
        path = None
        aaii_data_folder_dialogue = wx.DirDialog(self, "Choose a directory:")
        if aaii_data_folder_dialogue.ShowModal() == wx.ID_OK:
            path = aaii_data_folder_dialogue.GetPath()
            print line_number(), path
        aaii_data_folder_dialogue.Destroy()
        if path:
            aaii.import_aaii_files_from_data_folder(path=path)
