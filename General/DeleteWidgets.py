#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# DeleteWidgets.py
#
# PURPOSE: Delete tkinter widgets from the page
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Delete Page Information
def DeletePages(self):
    #--------------------------------------------------------------------------
    #
    #   PURPOSE: Delete widgets from a page.
    #
    #--------------------------------------------------------------------------

    for widget in self.att_list:
        try:
            eval(widget).destroy()
            del widget
        except:
            del widget

# Delete Local Attributes
def DeleteLocal(self):
    #--------------------------------------------------------------------------
    #
    #   PURPOSE: Delete widgets from a tab on the General Page.
    #
    #--------------------------------------------------------------------------

    for widget in self.loc_att_list:
        try:
            eval(widget).destroy()
            del widget
        except:
            del widget

# Delete Tab Attributes
def DeleteTab(self):
    #--------------------------------------------------------------------------
    #
    #   PURPOSE: Delete temporary attributes from a tab on the General Page.
    #
    #--------------------------------------------------------------------------

    for widget in self.tab_att_list:
        try:
            eval(widget).destroy()
            del widget
        except:
            del widget