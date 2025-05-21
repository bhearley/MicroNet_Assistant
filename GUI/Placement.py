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


    # Set to self
    self.Placement = Placement

    return