#-----------------------------------------------------------------------------------------
#
#   TrainModel.py
#
#   PURPOSE: Define settings to train a micronet model
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def TrainModel(self,window):
    # Import Modules
    import os
    import pandas as pd
    from PIL import Image, ImageTk
    import shutil
    import sys
    import threading
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter.scrolledtext import ScrolledText
    import tksheet

    # Import Functions
    from General.DeleteWidgets import DeleteLocal
    from General.DeleteWidgets import DeletePages
    from ModelCreator.SegmentationModels.MicroNet.TrainMicroNetModel import TrainMicroNetModel

    #Initialize list of attributes for each page
    self.att_list = []
    self.loc_att_list = []

    # Get the list of available models
    mods = pd.read_csv(os.path.join(os.getcwd(),'ModelCreator','SegmentationModels','MicroNet','AvailableModels.csv'), header=None)
    self.architecture = []
    for i in range(mods.shape[1]):
        self.architecture.append(mods.values[0][i])    

    self.models = {}
    for i in range(1,mods.shape[0]):
        self.models[mods.values[i,0]] = []
        for j in range(1,mods.shape[1]):
            if pd.isna(mods.values[i,j]) == False:
                self.models[mods.values[i,0]].append(mods.values[i,j])


    # Function to create drop down for weights
    def create_weights_drop(event):
        # Destory previous
        if hasattr(self,"combo_7_03"):
            self.combo_7_03.destroy()

        # Get the current option
        values = self.models[self.combo_7_02.get()]

        self.combo_7_03 = ttk.Combobox(
                            self.box_frame_7_01,
                            values=values,
                            style="Modern.TCombobox",
                            state="readonly"
                            )
        self.combo_7_03.place(anchor='w', relx = 0.55, rely = 0.625)
        self.combo_7_03.set(values[0]) 
        self.loc_att_list.append('self.combo_7_03')

    # Function for cell select options
    def cell_select_opt(event,Rows):
        # Deterine locked columns
        sel_col = event.selected.column 
        sel_row = event.selected.row
        locked_cols = [0]
        lim = []
        for i in range(1,3):
            if Rows[sel_row][i] == None:
                locked_cols.append(i)
                lim.append(None)
            else:
                lim.append(Rows[sel_row][i])
            

        # Enable/Disable user ability to edit cells
        if event.selected.column != None:
            if event.selected.column in locked_cols:
                self.sheet_7_01.disable_bindings(("edit_cell"))
            else:
                self.sheet_7_01.enable_bindings(("edit_cell"))
                self.sheet_7_01.extra_bindings([("edit_cell", lambda event: num_val(event, Rows))])

    # Function for numeric validation
    def num_val(event, Rows):
        # Get the selected row and column
        c = event.selected.column
        r = event.selected.row

        # Set the number of division points
        try:
            float(self.sheet_7_01.data[r][c])
            # Try Limits
            if 0 <= float(self.sheet_7_01.data[r][c]) <= Rows[r][c]:
                return
            else:
                self.sheet_7_01.data[r][c] = 0
                self.sheet_7_01.redraw()
        except:
            self.sheet_7_01.data[r][c] = 0
            self.sheet_7_01.redraw()

    # Function for cell select options
    def cell_select_opt2(event,Rows):
        # Deterine locked columns
        locked_cols = [0]

        # Enable/Disable user ability to edit cells
        if event.selected.column != None:
            if event.selected.column in locked_cols:
                self.sheet_7_02.disable_bindings(("edit_cell"))
            else:
                self.sheet_7_02.enable_bindings(("edit_cell"))
                self.sheet_7_02.extra_bindings([("edit_cell", lambda event: num_val2(event, Rows))])

    # Function for numeric validation
    def num_val2(event, Rows):
        # Get the selected row and column
        c = event.selected.column
        r = event.selected.row

        # Set the number of division points
        try:
            if Rows[r][1] is None:
                float(self.sheet_7_02.data[r][c])
                self.sheet_7_02.data[r][c] = float(self.sheet_7_02.data[r][c])
                self.sheet_7_02.redraw()
        except:
            self.sheet_7_02.data[r][c] = ''
            self.sheet_7_02.redraw()

    # Function for cell select options
    def cell_select_opt3(event,Rows):
        # Deterine locked columns
        locked_cols = [0]

        # Enable/Disable user ability to edit cells
        if event.selected.column != None:
            if event.selected.column in locked_cols:
                self.sheet_7_03.disable_bindings(("edit_cell"))
            else:
                self.sheet_7_03.enable_bindings(("edit_cell"))
        
    # Function to begin training a model
    def begin_train(self):
        # Preallocate Settings
        self.Segment['ML']['Settings'] = {
                                        'Model':{
                                                'Architecture':None,
                                                'Encoder':None,
                                                'PreWeights':None
                                            },
                                        'Augmentation':{
                                                'Crop':None,
                                                'HorzFlip':None,
                                                'VertFlip':None,
                                                'RRot90':None,
                                                'RGaussNoise':None,
                                                'CLAHE':None,
                                                'RBrightness':[None, None],
                                                'RGamma':None,
                                                'Sharpen':None,
                                                'Blur':[None,None],
                                                'RContrast':[None,None],
                                                'HueSat':None
                                            },
                                        'Train':{
                                            'Epochs':None,
                                            'Patience':None,
                                            'LearnRate': None,
                                            'BatchSize':None,
                                            'ValBatchSize':None
                                            },
                                        'Classes':{    
                                            },
                                        'Settings':{
                                            'GPU':False,
                                            'ValViz':False,
                                            'TrainViz':False
                                            },
                                        'Paths':{
                                            'Train':os.path.join(os.getcwd(),'Temp','Train'),
                                            'Validation':os.path.join(os.getcwd(),'Temp','Validation'),
                                            'Test':os.path.join(os.getcwd(),'Temp','Test'),
                                            'TrainL':os.path.join(os.getcwd(),'Temp','Train Labelled'),
                                            'ValidationL':os.path.join(os.getcwd(),'Temp','Validation Labelled'),
                                            'TestL':os.path.join(os.getcwd(),'Temp','Test Labelled'),
                                        }
                                        }
        
        # Populate Settings
        # -- Model
        self.Segment['ML']['Settings']['Model']['Architecture'] = self.combo_7_01.get()
        self.Segment['ML']['Settings']['Model']['Encoder'] = self.combo_7_02.get()
        if self.combo_7_03.get() == 'Micronet':
            preweight = 'micronet'
        else:
            preweight = 'image-micronet'
        self.Segment['ML']['Settings']['Model']['PreWeights'] = preweight

        # -- Augmentation
        crop_w = int(self.combo_7_04.get().split('x')[0])
        self.Segment['ML']['Settings']['Augmentation']['Crop'] = crop_w
        keys = list(self.Segment['ML']['Settings']['Augmentation'].keys())
        for i in range(1,len(keys)):
            if self.Segment['ML']['Settings']['Augmentation'][keys[i]] is None:
                self.Segment['ML']['Settings']['Augmentation'][keys[i]] = float(self.sheet_7_01.data[i-1][1])
            else:
                self.Segment['ML']['Settings']['Augmentation'][keys[i]] = [float(self.sheet_7_01.data[i-1][1]),
                                                                           float(self.sheet_7_01.data[i-1][2])]
                
        # -- Train
        keys = list(self.Segment['ML']['Settings']['Train'].keys())
        for i in range(len(keys)):
            if self.sheet_7_02.data[i][1] != '':
                self.Segment['ML']['Settings']['Train'][keys[i]] = self.sheet_7_02.data[i][1]

        # -- Classes
        ColorDict = { # Use BGR for MicroNet
                    0:(255,0,0),
                    1:(0,0,255),
                    2:(0,255,0)} 
        for i in range(len(self.sheet_7_03.data)-1):
            if self.sheet_7_03.data[i][2] == True:
                self.Segment['ML']['Settings']['Classes'][self.sheet_7_03.data[i][1]] = ColorDict[i]
        if len(self.Segment['ML']['Settings']['Classes'].keys()) > 1:
            if self.sheet_7_03.data[-1][1] == True:
                self.Segment['ML']['Settings']['Classes'][self.sheet_7_03.data[-1][1]] = (0,0,0)

        # -- Settings
        if self.var_7_01.get() == 1:
            self.Segment['ML']['Settings']['Settings']['GPU'] = True

        if self.var_7_02.get() == 1:
            self.Segment['ML']['Settings']['Settings']['TrainViz'] = True

        if self.var_7_03.get() == 1:
            self.Segment['ML']['Settings']['Settings']['ValViz'] = True

        # -- Paths
        # Move all images to temp folder
        temp_dir = os.path.join(os.getcwd(),'Temp')
        dir_list = ['Train', 'Validation', 'Test', 'Train Labelled',  'Validation Labelled',  'Test Labelled']
        for dirs in dir_list:
            path = os.path.join(temp_dir,dirs)
            if os.path.exists(path):
                # Directory exists → delete all contents
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path) 
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  
            else:
                # Directory doesn't exist → create it
                os.makedirs(path)
                print(f"Directory '{path}' created.")

        # Get directory containing all images
        if hasattr(self,"save_path") == False:
            self.save_path = filedialog.askdirectory(
                title="Select Folder Containing Saved Images",)


        # -- Move Data to Temp Directory
        dirs_list = ['Train', 'Validation', 'Test']
        for dir_name in dirs_list:
            for img in self.Segment['ML']['Data']['Train']:
                # Get file base
                mask_file = img
                orig_file = img.split('_mask')[0] + '.' + img.split('.')[1]
                
                # Move the original file
                shutil.copy(os.path.join(self.save_path,orig_file), os.path.join(temp_dir, dir_name, orig_file))

                # Move the lablled file
                shutil.copy(os.path.join(self.save_path,mask_file), os.path.join(temp_dir, dir_name + ' Labelled',orig_file))
            
        # Create window to show terminal output
        class TextRedirector:
            def __init__(self2, widget):
                self2.widget = widget

            def write(self2, text):
                self2.widget.insert(tk.END, text)
                self2.widget.see(tk.END)  # auto-scroll

            def flush(self2):
                pass  # needed for compatibility (e.g., with print buffering)

        def training_simulation(stop_event):
            # Begin Training 
            TrainMicroNetModel(self.Segment['ML']['Settings'])

            # Create Message
            messagebox.showinfo(message = 'Model Saved!')
            

        def start_training():
            self.stop_event.clear()
            self.training_thread = threading.Thread(target=training_simulation, args=(self.stop_event,), daemon=True)
            self.training_thread.start()

        def on_closing():
            self.stop_event.set()  # Signal the thread to stop
            loading.destroy()    # Then close the window

        loading = tk.Toplevel(window)
        loading.title("Training Model")
        loading.geometry("600x400")
        loading.resizable(False, False)
        loading.configure(bg='white')
        loading.grab_set()
        loading.protocol("WM_DELETE_WINDOW", on_closing)

        output_text = ScrolledText(loading, width=80, height=20)
        output_text.pack(padx=10, pady=10)

        # Redirect stdout
        sys.stdout = TextRedirector(output_text)

        # Initialize Thread
        self.stop_event = threading.Event()
        self.training_thread = None

        start_training()

    # Function to continue to next page
    def next_page():
        # Delete the page
        DeleteLocal(self)
        DeletePages(self)

        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 8

        # Load the page
        self.load_page()

    # Function to go back to previous page
    def back_page():
        # Save the model
        self.save_model()

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 6

        # Load the page
        self.load_page()

    # Function for Help Window
    def helper():
        # Create the help window
        helpwindow = tk.Toplevel(window)
        helpwindow.title("Help")
        helpwindow.geometry("600x700")
        helpwindow.resizable(False, False)
        helpwindow.configure(bg='white')
        helpwindow.grab_set()  

        # Create the main canvas
        canvas = tk.Canvas(helpwindow, height=500, width=700, bg="white")
        scrollbar = tk.Scrollbar(helpwindow, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        frame = tk.Frame(canvas, bg="white")
        canvas_window = canvas.create_window((0, 0), window=frame, anchor="n")

        # Create the title
        label_title = ttk.Label(
                                frame,
                                text=' Export Images',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the Instructions
        instructions = ("The Export Images page allows the user to review the segmentations and " +
                        "export the images to a single folder." + 
                        "\n\n Button Functions:")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Set list of buttons and functions 
        image_list = ['save_btn.png', 'help_btn.png','back_btn.png','cont_btn.png']
        func_list = [f'Save the project', 
                     f'Load the Help Window',
                     f'Return to the Image Selection page',
                     f'Continue to Train Model page']

        # Add buttons and functions to frame
        for i in range(len(image_list)):
            # Load the image
            img_file = os.path.join(os.getcwd(),'GUI','Help',image_list[i])
            img = tk.PhotoImage(file=img_file)

            # Create a container for image + text
            row_frame = tk.Frame(frame, bg="white")
    
            # Image holder frame (fixed width)
            image_holder = tk.Frame(row_frame, width=140, height=40, bg="white")
            image_holder.pack_propagate(False)  # prevent shrinking
            image_holder.pack(side="left", padx=10, pady=5)
            image_label = tk.Label(image_holder, image=img, bg="white")
            image_label.image = img
            image_label.pack(anchor="center")

            # Text frame (fixed width, auto height)
            text_frame = tk.Frame(row_frame, width=400, bg="white")
            text_label = tk.Label(text_frame, text=func_list[i], anchor="nw", justify="left", bg="white", wraplength=250)
            text_label.pack(fill="both", expand=True)
            text_frame.pack(side="left", padx=10, pady=5)
            
            # Pack the row
            row_frame.pack(anchor="w")

        # Update scrollregion whenever the size of the frame changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Configure canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        # Bind Configurations
        frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        # Add more instructions
        instructions = ("Select an image from the lefthand list and select 'Load Image' to " +
                        "display the image on screen. To export the images for MicroNet, select " + 
                        "'Export Iamges' and select the directory to save the images to. For each " + 
                        "image, the original cropped image imagename.png and the segmented image " + 
                        "imagename_mask.png will be saved.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','exp_view.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

    # Create Page Title
    self.label_title = ttk.Label(
                                window,
                                text='MicroNet Model Definition',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(anchor = 'center', relx = 0.5, rely = 0.125)
    self.att_list.append('self.label_title')

    # Create the frame for model architecture/encoder
    self.box_frame_7_01 = tk.Frame(
                            window, 
                            bd=3, 
                            relief="ridge", 
                            width = 450,
                            height = 400,
                            bg="white"
                            )
    self.box_frame_7_01.place(anchor = 'n', relx=0.2, rely=0.175)
    self.att_list.append('self.box_frame_7_01')

    # Create a label for the model architecture
    self.label_7_01 = ttk.Label(
                            self.box_frame_7_01,
                            text='Model Definition',
                            style = "Modern3.TLabel",
                            )
    self.label_7_01.place(anchor='n', relx = 0.5, rely = 0.05)
    self.att_list.append('self.label_7_01')

    # Create label for architecture
    self.label_7_02 = ttk.Label(
                            self.box_frame_7_01,
                            text='Architecture: ',
                            style = "Modern2.TLabel",
                            anchor='w'
                            )
    self.label_7_02.place(anchor='w', relx = 0.075, rely = 0.225)
    self.att_list.append('self.label_7_02')

    # Create drop down for architecture
    self.combo_7_01 = ttk.Combobox(
                        self.box_frame_7_01,
                        values=self.architecture,
                        style="Modern.TCombobox",
                        state="readonly"
                        )
    self.combo_7_01.place(anchor='w', relx = 0.55, rely = 0.225)
    self.combo_7_01.set(self.architecture[0]) 
    self.loc_att_list.append('self.combo_7_01')

    if 'Model Information' in self.Segment.keys():
        self.combo_7_01.set(self.Segment['Model Information'][3])

    # Create label for Encoder
    self.label_7_03 = ttk.Label(
                            self.box_frame_7_01,
                            text='Encoder: ',
                            style = "Modern2.TLabel",
                            anchor='w'
                            )
    self.label_7_03.place(anchor='w', relx = 0.075, rely = 0.425)
    self.att_list.append('self.label_7_03')

    # Create drop down for encoder
    self.combo_7_02 = ttk.Combobox(
                            self.box_frame_7_01,
                            values=list(self.models.keys()),
                            style="Modern.TCombobox",
                            state="readonly"
                            )
    self.combo_7_02.bind("<<ComboboxSelected>>", create_weights_drop)
    self.combo_7_02.place(anchor='w', relx = 0.55, rely = 0.425)
    self.combo_7_02.set(list(self.models.keys())[0]) 
    self.loc_att_list.append('self.combo_7_02')

    if 'Model Information' in self.Segment.keys():
        self.combo_7_02.set(self.Segment['Model Information'][4])

    # Create label for Pretrained Weights
    self.label_7_04 = ttk.Label(
                            self.box_frame_7_01,
                            text='Pretrained Weights: ',
                            style = "Modern2.TLabel",
                            anchor='w'
                            )
    self.label_7_04.place(anchor='w', relx = 0.075, rely = 0.625)
    self.att_list.append('self.label_7_04')

    # Create the drop down for pretrained weights
    create_weights_drop(None)

    # Create GPU Checkbutton
    self.var_7_01 = tk.IntVar()
    self.checkbutton_7_01 = ttk.Checkbutton(
                                    self.box_frame_7_01, 
                                    text="Use GPU", 
                                    variable=self.var_7_01,
                                    style="TCheckbutton"
                                    )
    self.checkbutton_7_01.place(anchor = 'n', relx = 0.5, rely = 0.8)
    self.loc_att_list.append('self.checkbutton_7_01')

    # Create the frame for image augementation
    self.box_frame_7_02 = tk.Frame(
                            window, 
                            bd=3, 
                            relief="ridge", 
                            width = 550,
                            height = 700,
                            bg="white"
                            )
    self.box_frame_7_02.place(anchor = 'n', relx=0.5, rely=0.175)
    self.att_list.append('self.box_frame_7_02')

    # Create label for Image Augmentation
    self.label_7_05 = ttk.Label(
                            self.box_frame_7_02,
                            text='Image Augmentation',
                            style = "Modern3.TLabel",
                            )
    self.label_7_05.place(anchor='n', relx = 0.5, rely = 0.03)
    self.att_list.append('self.label_7_05')

    # Create Label for Window Size
    self.label_7_06 = ttk.Label(
                            self.box_frame_7_02,
                            text='Crop Window: ',
                            style = "Modern2.TLabel",
                            )
    self.label_7_06.place(anchor='n', relx = 0.5, rely = 0.15)
    self.att_list.append('self.label_7_06')

    # Get Crop Window Options
    min_size = 1e6
    for item in self.Segment['Final'].keys():
        if self.Segment['Final'][item].height < int(min_size):
            min_size = self.Segment['Final'][item].height

    size_opts = []
    size_ct = 32
    while size_ct <= min_size:
        size_opts.append(str(size_ct) + 'x' + str(size_ct))
        size_ct = size_ct + 32

    # Create drop down for size
    self.combo_7_04 = ttk.Combobox(
                            self.box_frame_7_02,
                            values=size_opts,
                            style="Modern.TCombobox",
                            state="readonly"
                            )
    self.combo_7_04.place(anchor='n', relx = 0.5, rely = 0.2)
    self.combo_7_04.set(size_opts[-1]) 
    self.loc_att_list.append('self.combo_7_04')

    if 'Model Information' in self.Segment.keys():
        self.combo_7_04.set(self.Segment['Model Information'][6])

    # Create the Image Augmentation Sheet
    Cols1 = ['Option','Probability','Limit']
    Rows1 = [
        ['Horizontal Flip', 1, None],
        ['Vertical Flip', 1, None],
        ['Random Rotate 90°', 1, None],
        ['Gaussian Noise', 1, None],
        ['CLAHE', 1, None],
        ['Random Brightness', 1, 1],
        ['Random Gamma', 1, None],
        ['Shapren', 1, None],
        ['Blur', 1, 10],
        ['Random Contrast', 1, 1],
        ['Hue Saturation', 1, None],
        ]
    self.sheet_7_01 = tksheet.Sheet(
                            self.box_frame_7_02, 
                            total_rows = len(Rows1), 
                            total_columns = len(Cols1), 
                            headers = Cols1,
                            width = 435, 
                            height = 375, 
                            show_x_scrollbar = False, 
                            show_y_scrollbar = False,
                            font = ('Segoe UI',12,"normal"),
                            header_font = ('Segoe UI',12,"bold")
                            )
    self.sheet_7_01.place(anchor = 'n', relx = 0.5, rely = 0.275)
    self.loc_att_list.append('self.sheet_7_01')

    # format sheet
    self.sheet_7_01.set_index_width(0)
    self.sheet_7_01.column_width(column = 0, width = 232, redraw = True)
    self.sheet_7_01.column_width(column = 1, width = 100, redraw = True)
    self.sheet_7_01.column_width(column = 2, width = 100, redraw = True)
    self.sheet_7_01.table_align(align = 'c',redraw=True)

    # Enable Bindings
    self.sheet_7_01.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
    self.sheet_7_01.extra_bindings([("cell_select", lambda event: cell_select_opt(event, Rows1))])
    # Set values
    for i in range(len(Rows1)):
        row = Rows1[i]
        self.sheet_7_01.set_cell_data(i,0,row[0])
        if row[1] != None:
            self.sheet_7_01.set_cell_data(i,1,0.5)
        if row[2] != None:
            self.sheet_7_01.set_cell_data(i,2,0)

    # Populate Existing Data
    if "Model Information" in self.Segment.keys():
        sheet_data = self.Segment['Model Information'][0]
        for i in range(len(sheet_data)):
            for j in range(len(sheet_data[0])):
                self.sheet_7_01.set_cell_data(i,j,sheet_data[i][j])

    self.sheet_7_01.redraw()

    # Create the frame for model architecture/encoder
    self.box_frame_7_03 = tk.Frame(
                            window, 
                            bd=3, 
                            relief="ridge", 
                            width = 400,
                            height = 500,
                            bg="white"
                            )
    self.box_frame_7_03.place(anchor = 'n', relx=0.8, rely=0.175)
    self.att_list.append('self.box_frame_7_03')

    # Create label for Image Augmentation
    self.label_7_07 = ttk.Label(
                            self.box_frame_7_03,
                            text='Training Settings',
                            style = "Modern3.TLabel",
                            )
    self.label_7_07.place(anchor='n', relx = 0.5, rely = 0.03)
    self.att_list.append('self.label_7_07')

    # Create the Image Augmentation Sheet
    Cols2 = ['Option','Value']
    Rows2 = [
        ['Epochs'],
        ['Patience'],
        ['Learning Rate'],
        ['Batch Size'],
        ['Validation Batch Size'],
        ]
    self.sheet_7_02 = tksheet.Sheet(
                            self.box_frame_7_03, 
                            total_rows = len(Rows2), 
                            total_columns = len(Cols2), 
                            headers = Cols2,
                            width = 335, 
                            height = 375, 
                            show_x_scrollbar = False, 
                            show_y_scrollbar = False,
                            font = ('Segoe UI',12,"normal"),
                            header_font = ('Segoe UI',12,"bold")
                            )
    self.sheet_7_02.place(anchor = 'n', relx = 0.5, rely = 0.2)
    self.loc_att_list.append('self.sheet_7_01')

    # format sheet
    self.sheet_7_02.set_index_width(0)
    self.sheet_7_02.column_width(column = 0, width = 232, redraw = True)
    self.sheet_7_02.column_width(column = 1, width = 100, redraw = True)
    self.sheet_7_02.table_align(align = 'c',redraw=True)

    # Enable Bindings
    self.sheet_7_02.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
    self.sheet_7_02.extra_bindings([("cell_select", lambda event: cell_select_opt2(event, Rows2))])
    # Set values
    for i in range(len(Rows2)):
        row = Rows2[i]
        self.sheet_7_02.set_cell_data(i,0,row[0])

    # Populate Existing Data
    if "Model Information" in self.Segment.keys():
        sheet_data = self.Segment['Model Information'][1]
        for i in range(len(sheet_data)):
            for j in range(len(sheet_data[0])):
                if i != 2 and j == 1:
                    try:
                        self.sheet_7_02.set_cell_data(i,j,int(sheet_data[i][j]))
                    except:
                        pass
                else:
                    self.sheet_7_02.set_cell_data(i,j,sheet_data[i][j])


    self.sheet_7_02.redraw()

    # Visualize Training Data
    self.var_7_02 = tk.IntVar()
    self.checkbutton_7_02 = ttk.Checkbutton(
                                    self.box_frame_7_03, 
                                    text="Visualize Training Data", 
                                    variable=self.var_7_02,
                                    style="TCheckbutton"
                                    )
    self.checkbutton_7_02.place(anchor = 'n', relx = 0.5, rely = 0.75)
    self.loc_att_list.append('self.checkbutton_7_02')

    # Visualize Validation Data
    self.var_7_03 = tk.IntVar()
    self.checkbutton_7_03 = ttk.Checkbutton(
                                    self.box_frame_7_03, 
                                    text="Visualize Validation Data", 
                                    variable=self.var_7_03,
                                    style="TCheckbutton"
                                    )
    self.checkbutton_7_03.place(anchor = 'n', relx = 0.5, rely = 0.85)
    self.loc_att_list.append('self.checkbutton_7_03')

    # Create the frame for model architecture/encoder
    self.box_frame_7_04 = tk.Frame(
                            window, 
                            bd=3, 
                            relief="ridge", 
                            width = 450,
                            height = 250,
                            bg="white"
                            )
    self.box_frame_7_04.place(anchor = 'n', relx=0.2, rely=0.5)
    self.att_list.append('self.box_frame_7_04')

    # Create label for Classification Labels
    self.label_7_08 = ttk.Label(
                            self.box_frame_7_04,
                            text='Labels',
                            style = "Modern3.TLabel",
                            )
    self.label_7_08.place(anchor='n', relx = 0.5, rely = 0.05)
    self.att_list.append('self.label_7_08')

    # Create the Image Augmentation Sheet
    Cols3 = ['Color','Label',' ']
    Rows3 = []
    Colors = {1:(0,0,255), 2:(255,0,0), 3:(0,255,0)}

    for item in self.Segment['Data'].keys():
        # Get colors in each image
        for i in range(1,4):
            if len(self.Segment['Data'][item]['Segments'][i]['Pixel List']) > 0:
                if Colors[i] not in Rows3:
                    Rows3.append(Colors[i])

    self.sheet_7_03 = tksheet.Sheet(
                            self.box_frame_7_04, 
                            total_rows = len(Rows3)+1, 
                            total_columns = len(Cols3), 
                            headers = Cols3,
                            width = 350, 
                            height = 155, 
                            show_x_scrollbar = False, 
                            show_y_scrollbar = False,
                            font = ('Segoe UI',12,"normal"),
                            header_font = ('Segoe UI',12,"bold")
                            )
    self.sheet_7_03.place(anchor = 'n', relx = 0.5, rely = 0.275)
    self.loc_att_list.append('self.sheet_7_03')

    # format sheet
    self.sheet_7_03.set_index_width(0)
    self.sheet_7_03.column_width(column = 0, width = 115, redraw = True)
    self.sheet_7_03.column_width(column = 1, width = 200, redraw = True)
    self.sheet_7_03.column_width(column = 2, width = 25, redraw = True)
    self.sheet_7_03.table_align(align = 'c',redraw=True)
    self.sheet_7_03.checkbox('C', checked=True)

    # Enable Bindings
    self.sheet_7_03.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
    self.sheet_7_03.extra_bindings([("cell_select", lambda event: cell_select_opt3(event, Rows3))])

    # Set values
    def rgb_to_hex(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    for i in range(len(Rows3)):
        hex_color = rgb_to_hex(Rows3[i][0], Rows3[i][1], Rows3[i][2])
        self.sheet_7_03.highlight_cells(i, 0, bg=hex_color, fg='black')
    self.sheet_7_03.set_cell_data(len(Rows3),0,'Other')

    # Populate Existing Data
    if "Model Information" in self.Segment.keys():
        sheet_data = self.Segment['Model Information'][2]
        for i in range(len(sheet_data)):
            for j in range(len(sheet_data[0])):
                self.sheet_7_03.set_cell_data(i,j,sheet_data[i][j])

    self.sheet_7_03.redraw()

    # Create Button to train
    self.train_btn = ttk.Button(
                               window, 
                               text = "Train Model", 
                               command = lambda:begin_train(self), 
                               style = 'Modern2.TButton',
                               width = 10
                               )
    self.train_btn.place(anchor = 'n', relx = 0.5, rely = 0.75)
    self.att_list.append('self.train_btn')
    
    # Create Continue Button
    self.btn_cont1 = ttk.Button(
                               window, 
                               text = "Continue", 
                               command = next_page, 
                               style = 'Modern2.TButton',
                               width = 10
                               )
    self.btn_cont1.place(anchor = 'e', relx = 0.997, rely = 0.975)
    self.att_list.append('self.btn_cont1')

    # Create Back Button
    self.btn_back1 = ttk.Button(window, 
                               text = "Back", 
                               command = back_page, 
                               style = 'Modern2.TButton',
                               width = 10)
    self.btn_back1.place(anchor = 'e', relx = 0.942, rely = 0.975)
    self.att_list.append('self.btn_back1')

    # Create Help Button
    # -- Load an image using PIL
    self.image_path_help = os.path.join(os.getcwd(),'GUI','General','help.png') 
    self.image_help = Image.open(self.image_path_help)
    scale = 0.05
    self.image_help = self.image_help.resize((int(self.image_help.width*scale), int(self.image_help.height*scale)))

    # -- Convert the image to a Tkinter-compatible format
    self.photo_help = ImageTk.PhotoImage(self.image_help)

    # -- Create the button
    self.btn_help = ttk.Button(
                                window, 
                                text = " Help",
                                image=self.photo_help,
                                compound='left',                                 
                                command = helper,
                                style = "Modern2.TButton",
                                width = 7
                                )
    self.btn_help.place(anchor = 'w', relx = 0.001, rely = 0.975)
    self.att_list.append('self.btn_help')