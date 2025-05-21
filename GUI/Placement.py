#-----------------------------------------------------------------------------------------
#
#   Placement.py
#
#   PURPOSE: Get the coordinates and size of each widget based on screen size
#
#   INPUTS:
#       self    structure containing all GUI information
#-----------------------------------------------------------------------------------------
def Placement(self, res):
    # Initialize Placement
    Placement = {
                    'MainPage':{
                                'Title':[],
                                'Logo':[],
                                'Frame1':[],
                                'Label1':[],
                                'Button1':[],
                                'Button2':[],
                                'Frame2':[],
                                'Label2':[],
                                'Button3':[],
                                'Button4':[],
                                'Help':[],
                                'Save':[]
                                },
                    'FileSelect':{
                                'LabelT':[],
                                'Canvas1':[],
                                'Toolbar1':[],
                                'ButtonLeftW':[],
                                'ButtonRightW':[],
                                'Scrollbar1':[],
                                'Label1':[],
                                'Listbox1':[],
                                'Scrollbar2':[],
                                'Label2':[],
                                'Listbox2':[],
                                'ButtonLeft':[],
                                'ButtonRight':[],
                                'ButtonAllLeft':[],
                                'ButtonAllRight':[],
                                'ButtonView':[],
                                'LabelTitle':[],
                                'ButtonFldr':[],
                                'ButtonCont':[],
                                'ButtonBack':[],
                                'Help':[]
                                },
                    'Resize':{
                                'Canvas1':[],
                                'Toolbar1':[],
                                'LabelX':[],
                                'LabelY':[],
                                'LabelS':[],
                                'EntryX':[],
                                'EntryY':[],
                                'EntryS':[],
                                'ButtonS':[],
                                'Check1':[],
                                'LabelTitle':[],
                                'ButtonLoad':[],
                                'Scrollbar1':[],
                                'Listbox1':[],
                                'ButtonCont':[],
                                'ButtonBack':[],
                                'Help':[]
                                },
                    'Crop':{
                                'Canvas1':[],
                                'Toolbar1':[],
                                'LabelCrop':[],
                                'EntryCrop':[],
                                'LabelCover':[],
                                'LabelTitle':[],
                                'Scrollbar1':[],
                                'Listbox1':[],
                                'Scrollbar2':[],
                                'Listbox2':[],
                                'ButtonLoad':[],
                                'ButtonView':[],
                                'ButtonDelete':[],
                                'ButtonCont':[],
                                'ButtonBack':[],
                                'Help':[]
                                },
                    'Segment':{
                                'Image1':[],
                                'Canvas1':[],
                                'Toolbar1':[],
                                'LabelTitle':[],
                                'ButtonAdd':[],
                                'ButtonRemove':[],
                                'Slider1':[],
                                'Combo1':[],
                                'Scrollbar1':[],
                                'Listbox1':[],
                                'Combo2':[],
                                'ButtonCont':[],
                                'ButtonBack':[],
                                'Help':[]
                                },
                    'Review':{
                                'Image1':[],
                                'LabelTitle':[],
                                'Scrollbar1':[],
                                'Listbox1':[],
                                'ButtonLoad':[],
                                'ButtonExport':[],
                                'ButtonCont':[],
                                'ButtonBack':[],
                                'Help':[]
                                },
    }
    
    # 2560 x 1440
    if res == "2560x1440":
        # -- Main Page
        Placement['MainPage']['Title'] = [0.5, 0.015, 1.75]
        Placement['MainPage']['Logo'] = [0.999, 0.045, 1]
        Placement['MainPage']['Frame1'] = [0.35, 0.5, 3, 400, 400]
        Placement['MainPage']['Label1'] = [0.5, 0.1]
        Placement['MainPage']['Button1'] = [0.5, 0.4, 18]
        Placement['MainPage']['Button2'] = [0.5, 0.75, 18]
        Placement['MainPage']['Frame2'] = [0.65, 0.5, 3, 400, 400]
        Placement['MainPage']['Label2'] = [0.5, 0.1]
        Placement['MainPage']['Button3'] = [0.5, 0.4, 18]
        Placement['MainPage']['Button4'] = [0.5, 0.75, 18]
        Placement['MainPage']['Help'] = [0.001, 0.975, 7, 0.05]
        Placement['MainPage']['Save'] = [0.05425, 0.975, 8]

        # -- CreateFileSelection
        Placement['FileSelect']['LabelT'] = [0.5, 0.0075]
        Placement['FileSelect']['Canvas1'] = [0.5, 0.1]
        Placement['FileSelect']['Toolbar1'] = [0.5, 0.82]
        Placement['FileSelect']['ButtonLeftW'] = [0.45, 0.9, 3]
        Placement['FileSelect']['ButtonRightW'] = [0.55, 0.9, 3]
        Placement['FileSelect']['Scrollbar1'] = [0.4, 0.29, 752]
        Placement['FileSelect']['Label1'] = [0.3, 0.25]
        Placement['FileSelect']['Listbox1'] = [0.3, 0.29, 34, 54]
        Placement['FileSelect']['Scrollbar2'] = [0.8, 0.29, 752]
        Placement['FileSelect']['Label2'] = [0.7, 0.25]
        Placement['FileSelect']['Listbox2'] = [0.7, 0.29, 34, 54]
        Placement['FileSelect']['ButtonRight'] = [0.5, 0.475, 3]
        Placement['FileSelect']['ButtonLeft'] = [0.5, 0.65, 3]
        Placement['FileSelect']['ButtonAllRight'] = [0.3, 0.85, 18]
        Placement['FileSelect']['ButtonAllLeft'] = [0.7, 0.85, 18]
        Placement['FileSelect']['ButtonView'] = [0.5, 0.85, 22]
        Placement['FileSelect']['LabelTitle'] = [0.5, 0.125]
        Placement['FileSelect']['ButtonFldr'] = [0.5, 0.18, 18]
        Placement['FileSelect']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['FileSelect']['ButtonBack'] = [0.942, 0.975, 10]
        Placement['FileSelect']['Help'] = [0.001, 0.975, 7, 0.05]

        # -- ResizeImage
        Placement['Resize']['Canvas1'] = [0.5, 0.2, 0.8]
        Placement['Resize']['Toolbar1'] = [0.5, 0.8]
        Placement['Resize']['LabelX'] = [0.755, 0.4]
        Placement['Resize']['LabelY'] = [0.8275, 0.4]
        Placement['Resize']['LabelS'] = [0.9025, 0.4]
        Placement['Resize']['EntryX'] = [0.7875, 0.4, 10]
        Placement['Resize']['EntryY'] = [0.86, 0.4, 10]
        Placement['Resize']['EntryS'] = [0.94, 0.4, 10]
        Placement['Resize']['ButtonS'] = [0.86, 0.5, 10]
        Placement['Resize']['Check1'] = [0.86, 0.57]
        Placement['Resize']['LabelTitle'] = [0.5, 0.125]
        Placement['Resize']['ButtonLoad'] = [0.125, 0.775, 10]
        Placement['Resize']['Scrollbar1'] = [0.225, 0.2, 752]
        Placement['Resize']['Listbox1'] = [0.125, 0.2, 34, 54]
        Placement['Resize']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['Resize']['ButtonBack'] = [0.942, 0.975, 10]
        Placement['Resize']['Help'] = [0.001, 0.975, 7, 0.05]

        # -- Crop
        Placement['Crop']['Canvas1'] = [0.5, 0.2, 0.8]
        Placement['Crop']['Toolbar1'] = [0.5, 0.8]
        Placement['Crop']['LabelCrop'] = [0.47, 0.86]
        Placement['Crop']['EntryCrop'] = [0.53, 0.86, 10]
        Placement['Crop']['LabelCover'] = [0.5, 0.86, 10]
        Placement['Crop']['LabelTitle'] = [0.5, 0.125]
        Placement['Crop']['Scrollbar1'] = [0.225, 0.2, 752]
        Placement['Crop']['Listbox1'] = [0.125, 0.2, 34, 54]
        Placement['Crop']['Scrollbar2'] = [0.9425, 0.2, 752]
        Placement['Crop']['Listbox2'] = [0.8425, 0.2, 34, 54]
        Placement['Crop']['ButtonLoad'] = [0.125, 0.775, 10]
        Placement['Crop']['ButtonView'] = [0.795, 0.775, 12]
        Placement['Crop']['ButtonDelete'] = [0.895, 0.775, 12]
        Placement['Crop']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['Crop']['ButtonBack'] = [0.942, 0.975, 10]
        Placement['Crop']['Help'] = [0.001, 0.975, 7, 0.05]

        # -- Segment
        Placement['Segment']['Image1'] = [0.845, 0.375, 0.3]
        Placement['Segment']['Canvas1'] = [0.5, 0.2, 0.8]
        Placement['Segment']['Toolbar1'] = [0.5, 0.875]
        Placement['Segment']['LabelTitle'] = [0.5, .125]
        Placement['Segment']['ButtonAdd'] = [0.805, 0.2, 5]
        Placement['Segment']['ButtonRemove'] = [0.885, 0.2, 5]
        Placement['Segment']['Slider1'] = [0.845, 0.265, 300]
        Placement['Segment']['Combo1'] = [0.845, 0.3]
        Placement['Segment']['Scrollbar1'] = [0.225, 0.2, 752]
        Placement['Segment']['Listbox1'] = [0.125, 0.2, 34, 54]
        Placement['Segment']['Combo2'] = [0.125, 0.765, 25]
        Placement['Segment']['ButtonLoad'] = [0.125, 0.8, 10]
        Placement['Segment']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['Segment']['ButtonBack'] = [0.942, 0.975, 10]
        Placement['Segment']['Help'] = [0.001, 0.975, 7, 0.05]

        # -- Review
        Placement['Review']['Image1'] = [0.5, 0.2, 1.2]
        Placement['Review']['LabelTitle'] = [0.5, 0.125]
        Placement['Review']['Scrollbar1'] = [0.225, 0.2, 752]
        Placement['Review']['Listbox1'] = [0.125, 0.2, 34, 54]
        Placement['Review']['ButtonLoad'] = [0.08, 0.775, 12]
        Placement['Review']['ButtonExport'] = [0.17, 0.775, 12]
        Placement['Review']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['Review']['ButtonBack'] = [0.942, 0.975, 10]
        Placement['Review']['Help'] = [0.001, 0.975, 7, 0.05]
        


    # 1536 x 960
    if res == "1536x960":
        # -- Main Page
        Placement['MainPage']['Title'] = [0.5, 0.005, 1.5]
        Placement['MainPage']['Logo'] = [0.999, 0.045, 0.8]
        Placement['MainPage']['Frame1'] = [0.35, 0.5, 3, 300, 300]
        Placement['MainPage']['Label1'] = [0.5, 0.1]
        Placement['MainPage']['Button1'] = [0.5, 0.4, 15]
        Placement['MainPage']['Button2'] = [0.5, 0.75, 15]
        Placement['MainPage']['Frame2'] = [0.65, 0.5, 3, 300, 300]
        Placement['MainPage']['Label2'] = [0.5, 0.1]
        Placement['MainPage']['Button3'] = [0.5, 0.4, 15]
        Placement['MainPage']['Button4'] = [0.5, 0.75, 15]
        Placement['MainPage']['Help'] = [0.001, 0.965, 7, 0.05]
        Placement['MainPage']['Save'] = [0.089, 0.965, 8]

        # -- CreateFileSelection
        Placement['FileSelect']['LabelT'] = [0.5, 0.0075]
        Placement['FileSelect']['Canvas1'] = [0.5, 0.08]
        Placement['FileSelect']['Toolbar1'] = [0.5, 0.82]
        Placement['FileSelect']['ButtonLeftW'] = [0.45, 0.9, 3]
        Placement['FileSelect']['ButtonRightW'] = [0.55, 0.9, 3]
        Placement['FileSelect']['Scrollbar1'] = [0.4, 0.325, 445]
        Placement['FileSelect']['Label1'] = [0.3, 0.285]
        Placement['FileSelect']['Listbox1'] = [0.3, 0.325, 20, 31]
        Placement['FileSelect']['Scrollbar2'] = [0.8, 0.325, 445]
        Placement['FileSelect']['Label2'] = [0.7, 0.285]
        Placement['FileSelect']['Listbox2'] = [0.7, 0.325, 20, 31]
        Placement['FileSelect']['ButtonRight'] = [0.5, 0.45, 3]
        Placement['FileSelect']['ButtonLeft'] = [0.5, 0.7, 3]
        Placement['FileSelect']['ButtonAllRight'] = [0.3, 0.85, 15]
        Placement['FileSelect']['ButtonAllLeft'] = [0.7, 0.85, 15]
        Placement['FileSelect']['ButtonView'] = [0.5, 0.85, 17]
        Placement['FileSelect']['LabelTitle'] = [0.5, 0.125]
        Placement['FileSelect']['ButtonFldr'] = [0.5, 0.225, 18]
        Placement['FileSelect']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['FileSelect']['ButtonBack'] = [0.909, 0.965, 10]
        Placement['FileSelect']['Help'] = [0.001, 0.965, 7, 0.05]

        # -- ResizeImage
        Placement['Resize']['Canvas1'] = [0.5, 0.15, 1.25]
        Placement['Resize']['Toolbar1'] = [0.5, 0.8]
        Placement['Resize']['LabelX'] = [0.7525, 0.399]
        Placement['Resize']['LabelY'] = [0.825, 0.399]
        Placement['Resize']['LabelS'] = [0.9, 0.399]
        Placement['Resize']['EntryX'] = [0.7875, 0.4, 6]
        Placement['Resize']['EntryY'] = [0.86, 0.4, 6]
        Placement['Resize']['EntryS'] = [0.94, 0.4, 6]
        Placement['Resize']['ButtonS'] = [0.86, 0.5, 10]
        Placement['Resize']['Check1'] = [0.86, 0.57]
        Placement['Resize']['LabelTitle'] = [0.5, 0.125]
        Placement['Resize']['ButtonLoad'] = [0.15, 0.775, 10]
        Placement['Resize']['Scrollbar1'] = [0.25, 0.2, 445]
        Placement['Resize']['Listbox1'] = [0.15, 0.2, 20, 31]
        Placement['Resize']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['Resize']['ButtonBack'] = [0.909, 0.965, 10]
        Placement['Resize']['Help'] = [0.001, 0.965, 7, 0.05]

        # -- Crop
        Placement['Crop']['Canvas1'] = [0.5, 0.175, 1.25]
        Placement['Crop']['Toolbar1'] = [0.5, 0.8]
        Placement['Crop']['LabelCrop'] = [0.45, 0.86]
        Placement['Crop']['EntryCrop'] = [0.55, 0.86, 10]
        Placement['Crop']['LabelCover'] = [0.5, 0.86, 10]
        Placement['Crop']['LabelTitle'] = [0.5, 0.125]
        Placement['Crop']['Scrollbar1'] = [0.25, 0.2, 445]
        Placement['Crop']['Listbox1'] = [0.15, 0.2, 20, 31]
        Placement['Crop']['Scrollbar2'] = [0.9425, 0.2, 445]
        Placement['Crop']['Listbox2'] = [0.8425, 0.2, 20, 31]
        Placement['Crop']['ButtonLoad'] = [0.15, 0.775, 10]
        Placement['Crop']['ButtonView'] = [0.795, 0.775, 12]
        Placement['Crop']['ButtonDelete'] = [0.9, 0.775, 12]
        Placement['Crop']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['Crop']['ButtonBack'] = [0.909, 0.965, 10]
        Placement['Crop']['Help'] = [0.001, 0.965, 7, 0.05]

        # -- Segment
        Placement['Segment']['Image1'] = [0.845, 0.5, 0.3]
        Placement['Segment']['Canvas1'] = [0.5, 0.2, 1.25]
        Placement['Segment']['Toolbar1'] = [0.5, 0.875]
        Placement['Segment']['LabelTitle'] = [0.5, .125]
        Placement['Segment']['ButtonAdd'] = [0.7775, 0.2, 5]
        Placement['Segment']['ButtonRemove'] = [0.91, 0.2, 5]
        Placement['Segment']['Slider1'] = [0.845, 0.275, 300]
        Placement['Segment']['Combo1'] = [0.845, 0.4]
        Placement['Segment']['Scrollbar1'] = [0.25, 0.2, 445]
        Placement['Segment']['Listbox1'] = [0.15, 0.2, 20, 31]
        Placement['Segment']['Combo2'] = [0.15, 0.74, 25]
        Placement['Segment']['ButtonLoad'] = [0.15, 0.79, 10]
        Placement['Segment']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['Segment']['ButtonBack'] = [0.909, 0.965, 10]
        Placement['Segment']['Help'] = [0.001, 0.965, 7, 0.05]

        # -- Review
        Placement['Review']['Image1'] = [0.5, 0.2, 0.8]
        Placement['Review']['LabelTitle'] = [0.5, 0.125]
        Placement['Review']['Scrollbar1'] = [0.25, 0.2, 445]
        Placement['Review']['Listbox1'] = [0.15, 0.2, 20, 31]
        Placement['Review']['ButtonLoad'] = [0.1025, 0.775, 12]
        Placement['Review']['ButtonExport'] = [0.2074, 0.775, 12]
        Placement['Review']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['Review']['ButtonBack'] = [0.909, 0.965, 10]
        Placement['Review']['Help'] = [0.001, 0.965, 7, 0.05]


    # Set to self
    self.Placement = Placement

    return