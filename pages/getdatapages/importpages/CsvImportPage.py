import wx, config, logging
import lib.gui_position_index as gui_position
import lib.meta_functions as meta

class CsvImportPage(wx.Panel):
    def __init__(self, parent):
        self.title = "Import .CSV Data"
        self.uid = config.CSV_IMPORT_PAGE_UNIQUE_ID
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1,
                             "Welcome to the CSV data import page page.\nYou can make your own import functions under the function tab.",
                             gui_position.CsvImportPage.text
                             )

        default_button_position = gui_position.CsvImportPage.default_button_position
        default_button_horizontal_position = default_button_position[0]
        default_button_vertical_position = default_button_position[1]
        default_dropdown_offset = gui_position.CsvImportPage.default_dropdown_offset
        default_dropdown_horizontal_offset = default_dropdown_offset[0]
        default_dropdown_vertical_offset = default_dropdown_offset[1]

        import_button = wx.Button(self, label="import .csv", pos=(default_button_horizontal_position, default_button_vertical_position), size=(-1,-1))
        import_button.Bind(wx.EVT_BUTTON, self.importCSV, import_button)

        self.csv_import_name_list = meta.return_csv_import_function_short_names()
        self.drop_down = wx.ComboBox(self, pos=(default_button_horizontal_position + default_dropdown_horizontal_offset, default_button_vertical_position + default_dropdown_vertical_offset), choices=self.csv_import_name_list)

        self.triple_list = meta.return_csv_import_function_triple()

        self.csv_import_name = None

    def importCSV(self, event):
        self.csv_import_name = self.drop_down.GetValue()

        # Identify the function mapped to screen name
        for triple in self.triple_list:
            if self.csv_import_name == triple.doc:
                csv_import_function = triple.function
            # in case doc string is too many characters...
            elif self.csv_import_name == triple.name:
                csv_import_function = triple.function

        if not csv_import_function:
            print line_number(), "Error, somthing went wrong locating the correct import function to use."

        # run ranking funtion on all stocks

        success = process_user_function.import_csv_via_user_created_function(self, csv_import_function)

        if not success:
            return

        if success == "fail":
            title_string = "Error"
            success_string = "This import has failed, please check make sure your function conforms to the import protocols."
            message_style = wx.ICON_ERROR
        elif success == "some":
            title_string = "Some Errors"
            success_string = "There were some errors with your import, please review your CSV file and make sure that your functions conform to the protocols, and that the ticker symbols in your csv files are the same format as wxStocks'."
            message_style = wx.ICON_EXCLAMATION
        elif success == "success":
            title_string = "Success"
            success_string = "Success! You're file has been successfully imported."
            message_style = wx.OK
        else:
            print line_number(), "Error in importCSV title and success strings"
            return

        print line_number(), "importCSV done"


        confirm = wx.MessageDialog(None,
                                   success_string,
                                   title_string,
                                   style = message_style
                                   )
        confirm.ShowModal()
