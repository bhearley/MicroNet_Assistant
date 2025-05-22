#-----------------------------------------------------------------------------------------
#
#   Placements.py
#
#   PURPOSE: Get the coordinates and size of each widget based on screen size
#
#   INPUTS:
#       self    structure containing all GUI information
#-----------------------------------------------------------------------------------------
def Placements(self, res):
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
                    'DataDef':{
                                'LabelTitle':[],
                                'Scrollbar1':[],
                                'Label1':[],
                                'Listbox1':[],
                                'Button1':[],
                                'Scrollbar2':[],
                                'Label2':[],
                                'Listbox2':[],
                                'Button2':[],
                                'Scrollbar3':[],
                                'Label3':[],
                                'Listbox3':[],
                                'Button3':[],
                                'Scrollbar4':[],
                                'Label4':[],
                                'Listbox4':[],
                                'Button4':[],
                                'ButtonCont':[],
                                'ButtonBack':[],
                                'Help':[]
                                },
                    'Train':{
                                'Combo3':[],
                                'LabelTitle':[],
                                'Frame1':[],
                                'Label1':[],
                                'Label2':[],
                                'Combo1':[],
                                'Label3':[],
                                'Combo2':[],
                                'Label4':[],
                                'Check1':[],
                                'Frame2':[],
                                'Label5':[],
                                'Label6':[],
                                'Combo4':[],
                                'Sheet1':[],
                                'Label4':[],
                                'Frame3':[],
                                'Label7':[],
                                'Sheet2':[],
                                'Check2':[],
                                'Check3':[],
                                'Frame4':[],
                                'Label8':[],
                                'Sheet3':[],
                                'ButtonTrain':[],
                                'ButtonCont':[],
                                'ButtonBack':[],
                                'Help':[]
                                },
                    'UseMod':{
                                'LabelMT':[],
                                'LabelM':[],
                                'LabelC':[],
                                'EntryC':[],
                                'Canvas1':[],
                                'Toolbar1':[],
                                'LabelX':[],
                                'LabelY':[],
                                'LabelS':[],
                                'EntryX':[],
                                'EntryY':[],
                                'EntryS':[],
                                'ButtonS':[],
                                'ButtonSave':[],
                                'ButtonDisc':[],
                                'LabelTitle':[],
                                'ButtonLoadM':[],
                                'ButtonLoadI':[],
                                'ButtonSeg':[],
                                'ButtonCont':[],
                                'ButtonHome':[],
                                'Help':[]
                                },
                    'RUC':{
                                'LabelCol':[],
                                'LabelCol2':[],
                                'SheetCol':[],
                                'Canvas2':[],
                                'Toolbar2':[],
                                'SliderX':[],
                                'SliderY':[],
                                'LabelExp':[],
                                'ComboExp':[],
                                'LabelConv':[],
                                'LabelConvX':[],
                                'EntryConvX':[],
                                'LabelConvY':[],
                                'EntryConvY':[],
                                'ButtonExp':[],
                                'LabelSeg':[],
                                'Canvas1':[],
                                'LabelRUC':[],
                                'LabelSubX':[],
                                'EntryXL':[],
                                'EntryXU':[],
                                'EntryXV':[],
                                'LabelSubY':[],
                                'EntryYL':[],
                                'EntryYU':[],
                                'EntryYV':[],
                                'ButtonRUC':[],
                                'ButtonExp':[],
                                'LabelTitle':[],
                                'ButtonFile':[],
                                'ButtonHome':[],
                                'Help':[]
                                }
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

        # -- Data Definition
        Placement['DataDef']['LabelTitle'] = [0.5, 0.125]
        Placement['DataDef']['Scrollbar1'] = [0.25, 0.2, 752]
        Placement['DataDef']['Label1'] = [0.15, 0.16]
        Placement['DataDef']['Listbox1'] = [0.15, 0.2, 34, 54]
        Placement['DataDef']['Button1'] = [0.15, 0.775, 15]
        Placement['DataDef']['Scrollbar2'] = [0.483, 0.2, 752]
        Placement['DataDef']['Label2'] = [0.383, 0.16]
        Placement['DataDef']['Listbox2'] = [0.383, 0.2, 34, 54]
        Placement['DataDef']['Button2'] = [0.383, 0.775, 15]
        Placement['DataDef']['Scrollbar3'] = [0.716, 0.2, 752]
        Placement['DataDef']['Label3'] = [0.616, 0.16]
        Placement['DataDef']['Listbox3'] = [0.616, 0.2, 34, 54]
        Placement['DataDef']['Button3'] = [0.616, 0.775, 15]
        Placement['DataDef']['Scrollbar4'] = [0.95, 0.2, 752]
        Placement['DataDef']['Label4'] = [0.85, 0.16]
        Placement['DataDef']['Listbox4'] = [0.85, 0.2, 34 ,54]
        Placement['DataDef']['Button4'] = [0.85, 0.775, 15]
        Placement['DataDef']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['DataDef']['ButtonBack'] = [0.942, 0.975, 10]
        Placement['DataDef']['Help'] = [0.001, 0.975, 7, 0.05]

        # -- Train
        Placement['Train']['Combo3'] = [0.55, 0.625]
        Placement['Train']['LabelTitle'] = [0.5, 0.125]
        Placement['Train']['Frame1'] = [0.2, 0.175, 3, 450, 400]
        Placement['Train']['Label1'] = [0.5, 0.05]
        Placement['Train']['Label2'] = [0.075, 0.225]
        Placement['Train']['Combo1'] = [0.55, 0.225]
        Placement['Train']['Label3'] = [0.075, 0.425]
        Placement['Train']['Combo2'] = [0.55, 0.425]
        Placement['Train']['Label4'] = [0.075, 0.625]
        Placement['Train']['Check1'] = [0.5, 0.8]
        Placement['Train']['Frame2'] = [0.5, 0.175, 3, 550, 700]
        Placement['Train']['Label5'] = [0.5, 0.03]
        Placement['Train']['Label6'] = [0.5, 0.15]
        Placement['Train']['Combo4'] = [0.5, 0.2]
        Placement['Train']['Sheet1'] = [0.5, 0.275, 435, 375, 232, 100, 100]
        Placement['Train']['Frame3'] = [0.8, 0.175, 3, 400, 500]
        Placement['Train']['Label7'] = [0.5, 0.03]
        Placement['Train']['Sheet2'] = [0.5, 0.2, 335, 375, 232, 100]
        Placement['Train']['Check2'] = [0.5, 0.75]
        Placement['Train']['Check3'] = [0.5, 0.85]
        Placement['Train']['Frame4'] = [0.2, 0.5, 3, 450, 250]
        Placement['Train']['Label8'] = [0.5, 0.05]
        Placement['Train']['Sheet3'] = [0.5, 0.275, 350, 155, 115, 200, 25]
        Placement['Train']['ButtonTrain'] = [0.5, 0.75, 10]
        Placement['Train']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['Train']['ButtonBack'] = [0.942, 0.975, 10]
        Placement['Train']['Help'] = [0.001, 0.975, 7, 0.05]

        # -- Use Model
        Placement['UseMod']['LabelMT'] = [0.125, 0.3]
        Placement['UseMod']['LabelM'] = [0.125, 0.335]
        Placement['UseMod']['LabelC'] = [0.125, 0.45]
        Placement['UseMod']['EntryC'] = [0.125, 0.485, 10]
        Placement['UseMod']['Canvas1'] = [0.5, 0.3, 0.8]
        Placement['UseMod']['Toolbar1'] = [0.5, 0.875]
        Placement['UseMod']['LabelX'] = [0.77, 0.4]
        Placement['UseMod']['LabelY'] = [0.8425, 0.4]
        Placement['UseMod']['LabelS'] = [0.9175, 0.4]
        Placement['UseMod']['EntryX'] = [0.8025, 0.4, 10]
        Placement['UseMod']['EntryY'] = [0.875, 0.4, 10]
        Placement['UseMod']['EntryS'] = [0.955, 0.4, 10]
        Placement['UseMod']['ButtonS'] = [0.875, 0.5, 10]
        Placement['UseMod']['ButtonSave'] = [0.44, 0.2, 12]
        Placement['UseMod']['ButtonDisc'] = [0.56, 0.2, 12]
        Placement['UseMod']['LabelTitle'] = [0.5, 0.125]
        Placement['UseMod']['ButtonLoadM'] = [0.125, 0.2, 10]
        Placement['UseMod']['ButtonLoadI'] = [0.875, 0.2, 10]
        Placement['UseMod']['ButtonSeg'] = [0.5, 0.2, 15]
        Placement['UseMod']['ButtonCont'] = [0.997, 0.975, 10]
        Placement['UseMod']['ButtonHome'] = [0.942, 0.975, 7, 1]
        Placement['UseMod']['Help'] = [0.001, 0.975, 7, 0.05]

        # -- Build RUC
        Placement['RUC']['LabelCol'] = [0.175, 0.8, 10]
        Placement['RUC']['LabelCol2'] = [0.175, 0.825, 10]
        Placement['RUC']['SheetCol'] = [0.505, 0.675, 220, 250, 100, 100]
        Placement['RUC']['Canvas2'] = [0.825, 0.25, 0.9]
        Placement['RUC']['Toolbar2'] = [0.825, 0.85]
        Placement['RUC']['SliderX'] = [0.5, 0.335, 200]
        Placement['RUC']['SliderY'] = [0.5, 0.485, 200]
        Placement['RUC']['LabelExp'] = [0.5, 0.1]
        Placement['RUC']['ComboExp'] = [0.5, 0.2]
        Placement['RUC']['LabelConv'] = [0.5, 0.4]
        Placement['RUC']['LabelConvX'] = [0.2, 0.5]
        Placement['RUC']['EntryConvX'] = [0.5, 0.5, 10]
        Placement['RUC']['LabelConvY'] = [0.2, 0.65]
        Placement['RUC']['EntryConvY'] = [0.5, 0.65, 10]
        Placement['RUC']['ButtonExpW'] = [0.5, 0.8, 12]
        Placement['RUC']['LabelSeg'] = [0.175, 0.175,]
        Placement['RUC']['Canvas1'] = [0.175, 0.25, 0.9]
        Placement['RUC']['LabelRUC'] = [0.825, .175]
        Placement['RUC']['LabelSubX'] = [0.5, 0.2]
        Placement['RUC']['EntryXL'] = [0.425, 0.329, 10]
        Placement['RUC']['EntryXU'] = [0.575, 0.329, 10]
        Placement['RUC']['EntryXV'] = [0.5, 0.2925, 10]
        Placement['RUC']['LabelSubY'] = [0.5, 0.4]
        Placement['RUC']['EntryYL'] = [0.425, 0.479, 10]
        Placement['RUC']['EntryYU'] = [0.575, 0.479, 10]
        Placement['RUC']['EntryYV'] = [0.5, 0.4425, 10]
        Placement['RUC']['ButtonRUC'] = [0.5, 0.595, 12]
        Placement['RUC']['ButtonExp'] = [0.5, 0.525, 10]
        Placement['RUC']['LabelTitle'] = [0.5, 0.125]
        Placement['RUC']['ButtonFile'] = [0.5, 0.15, 12]
        Placement['RUC']['ButtonHome'] = [0.997, 0.975, 7, 1]
        Placement['RUC']['Help'] = [0.001, 0.975, 7, 0.05]
        


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

        # -- Data Definition
        Placement['DataDef']['LabelTitle'] = [0.5, 0.125]
        Placement['DataDef']['Scrollbar1'] = [0.25, 0.2, 445]
        Placement['DataDef']['Label1'] = [0.15, 0.16]
        Placement['DataDef']['Listbox1'] = [0.15, 0.2, 20, 31]
        Placement['DataDef']['Button1'] = [0.15, 0.75, 15]
        Placement['DataDef']['Scrollbar2'] = [0.483, 0.2, 445]
        Placement['DataDef']['Label2'] = [0.383, 0.16]
        Placement['DataDef']['Listbox2'] = [0.383, 0.2, 20, 31]
        Placement['DataDef']['Button2'] = [0.383, 0.75, 15]
        Placement['DataDef']['Scrollbar3'] = [0.716, 0.2, 445]
        Placement['DataDef']['Label3'] = [0.616, 0.16]
        Placement['DataDef']['Listbox3'] = [0.616, 0.2, 20, 31]
        Placement['DataDef']['Button3'] = [0.616, 0.75, 15]
        Placement['DataDef']['Scrollbar4'] = [0.95, 0.2, 445]
        Placement['DataDef']['Label4'] = [0.85, 0.16]
        Placement['DataDef']['Listbox4'] = [0.85, 0.2, 20, 31]
        Placement['DataDef']['Button4'] = [0.85, 0.75, 15]
        Placement['DataDef']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['DataDef']['ButtonBack'] = [0.909, 0.965, 10]
        Placement['DataDef']['Help'] = [0.001, 0.965, 7, 0.05]

        # -- Train
        Placement['Train']['Combo3'] = [0.55, 0.625]
        Placement['Train']['LabelTitle'] = [0.5, 0.125]
        Placement['Train']['Frame1'] = [0.15, 0.175, 3, 375, 325]
        Placement['Train']['Label1'] = [0.5, 0.05]
        Placement['Train']['Label2'] = [0.05, 0.225]
        Placement['Train']['Combo1'] = [0.55, 0.225]
        Placement['Train']['Label3'] = [0.05, 0.425]
        Placement['Train']['Combo2'] = [0.55, 0.425]
        Placement['Train']['Label4'] = [0.05, 0.625]
        Placement['Train']['Check1'] = [0.5, 0.8]
        Placement['Train']['Frame2'] = [0.5, 0.175, 3, 450, 560]
        Placement['Train']['Label5'] = [0.5, 0.03]
        Placement['Train']['Label6'] = [0.5, 0.16]
        Placement['Train']['Combo4'] = [0.5, 0.225]
        Placement['Train']['Sheet1'] = [0.5, 0.325, 435, 375, 232, 100, 100]
        Placement['Train']['Frame3'] = [0.85, 0.175, 3, 375, 500]
        Placement['Train']['Label7'] = [0.5, 0.03]
        Placement['Train']['Sheet2'] = [0.5, 0.2, 335, 375, 232, 100]
        Placement['Train']['Check2'] = [0.5, 0.75]
        Placement['Train']['Check3'] = [0.5, 0.85]
        Placement['Train']['Frame4'] = [0.15, 0.55, 3, 375, 225]
        Placement['Train']['Label8'] = [0.5, 0.05]
        Placement['Train']['Sheet3'] = [0.5, 0.225, 350, 155, 115, 200, 25]
        Placement['Train']['ButtonTrain'] = [0.5, 0.825, 10]
        Placement['Train']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['Train']['ButtonBack'] = [0.909, 0.965, 10]
        Placement['Train']['Help'] = [0.001, 0.965, 7, 0.05]

        # -- Use Model
        Placement['UseMod']['LabelMT'] = [0.125, 0.3]
        Placement['UseMod']['LabelM'] = [0.125, 0.335]
        Placement['UseMod']['LabelC'] = [0.125, 0.45]
        Placement['UseMod']['EntryC'] = [0.125, 0.485, 10]
        Placement['UseMod']['Canvas1'] = [0.5, 0.3, 1.25]
        Placement['UseMod']['Toolbar1'] = [0.5, 0.825]
        Placement['UseMod']['LabelX'] = [0.77, 0.4]
        Placement['UseMod']['LabelY'] = [0.8425, 0.4]
        Placement['UseMod']['LabelS'] = [0.9175, 0.4]
        Placement['UseMod']['EntryX'] = [0.8025, 0.4, 6]
        Placement['UseMod']['EntryY'] = [0.875, 0.4, 6]
        Placement['UseMod']['EntryS'] = [0.955, 0.4, 6]
        Placement['UseMod']['ButtonS'] = [0.875, 0.5, 10]
        Placement['UseMod']['ButtonSave'] = [0.425, 0.2, 12]
        Placement['UseMod']['ButtonDisc'] = [0.575, 0.2, 12]
        Placement['UseMod']['LabelTitle'] = [0.5, 0.125]
        Placement['UseMod']['ButtonLoadM'] = [0.125, 0.2, 10]
        Placement['UseMod']['ButtonLoadI'] = [0.875, 0.2, 10]
        Placement['UseMod']['ButtonSeg'] = [0.5, 0.2, 15]
        Placement['UseMod']['ButtonCont'] = [0.999, 0.965, 10]
        Placement['UseMod']['ButtonHome'] = [0.909, 0.965, 7]
        Placement['UseMod']['Help'] = [0.001, 0.965, 7, 0.05]

        # -- Build RUC
        Placement['RUC']['LabelCol'] = [0.175, 0.8, 10]
        Placement['RUC']['LabelCol2'] = [0.175, 0.825, 10]
        Placement['RUC']['SheetCol'] = [0.505, 0.675, 220, 250, 100, 100]
        Placement['RUC']['Canvas2'] = [0.825, 0.25, 1.5]
        Placement['RUC']['Toolbar2'] = [0.825, 0.825]
        Placement['RUC']['SliderX'] = [0.5, 0.335, 150]
        Placement['RUC']['SliderY'] = [0.5, 0.485, 150]
        Placement['RUC']['LabelExp'] = [0.5, 0.1]
        Placement['RUC']['ComboExp'] = [0.5, 0.2]
        Placement['RUC']['LabelConv'] = [0.5, 0.4]
        Placement['RUC']['LabelConvX'] = [0.2, 0.5]
        Placement['RUC']['EntryConvX'] = [0.5, 0.5, 10]
        Placement['RUC']['LabelConvY'] = [0.2, 0.65]
        Placement['RUC']['EntryConvY'] = [0.5, 0.65, 10]
        Placement['RUC']['ButtonExpW'] = [0.5, 0.8, 10]
        Placement['RUC']['LabelSeg'] = [0.175, 0.175]
        Placement['RUC']['Canvas1'] = [0.175, 0.25, 1.5]
        Placement['RUC']['LabelRUC'] = [0.825, .175]
        Placement['RUC']['LabelSubX'] = [0.5, 0.25]
        Placement['RUC']['EntryXL'] = [0.425, 0.329, 6]
        Placement['RUC']['EntryXU'] = [0.575, 0.329, 6]
        Placement['RUC']['EntryXV'] = [0.5, 0.2925, 6]
        Placement['RUC']['LabelSubY'] = [0.5, 0.4]
        Placement['RUC']['EntryYL'] = [0.425, 0.479, 6]
        Placement['RUC']['EntryYU'] = [0.575, 0.479, 6]
        Placement['RUC']['EntryYV'] = [0.5, 0.4425, 6]
        Placement['RUC']['ButtonRUC'] = [0.5, 0.595, 10]
        Placement['RUC']['ButtonExp'] = [0.5, 0.525, 10]
        Placement['RUC']['LabelTitle'] = [0.5, 0.125]
        Placement['RUC']['ButtonFile'] = [0.5, 0.15, 12]
        Placement['RUC']['ButtonHome'] = [0.999, 0.965, 7, 1]
        Placement['RUC']['Help'] = [0.001, 0.965, 7, 0.05]

    else:
        Placements(self, "1536x960")


    # Set to self
    self.Placement = Placement

    return