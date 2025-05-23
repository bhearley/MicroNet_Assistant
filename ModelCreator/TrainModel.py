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

    # Organize models into structure
    self.models = {}
    for i in range(1,mods.shape[0]):
        self.models[mods.values[i,0]] = []
        for j in range(1,mods.shape[1]):
            if pd.isna(mods.values[i,j]) == False:
                self.models[mods.values[i,0]].append(mods.values[i,j])


    # Function to create drop down for weights
    def create_weights_drop(event):

        # Destory previous drow down
        if hasattr(self,"combo_prew"):
            self.combo_prew.destroy()

        # Get the current option
        values = self.models[self.combo_enc.get()]

        # Create the drop down for weights
        self.combo_prew = ttk.Combobox(
                                            self.frame_model,
                                            values=values,
                                            style="Modern.TCombobox",
                                            state="readonly"
                                            )
        self.combo_prew.place(
                                anchor='w', 
                                relx = self.Placement['Train']['Combo3'][0], 
                                rely = self.Placement['Train']['Combo3'][1]
                                )
        self.combo_prew.set(values[0]) 
        self.loc_att_list.append('self.combo_prew')

    # Function for cell select options
    def cell_select_opt(event,Rows):

        # Determine locked items
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
                self.sheet_aug.disable_bindings(("edit_cell"))
            else:
                self.sheet_aug.enable_bindings(("edit_cell"))
                self.sheet_aug.extra_bindings([("edit_cell", lambda event: num_val(event, Rows))])

    # Function for numeric validation
    def num_val(event, Rows):

        # Get the selected row and column
        c = event.selected.column
        r = event.selected.row

        try:
            float(self.sheet_aug.data[r][c])
            # Try Limits
            if 0 <= float(self.sheet_aug.data[r][c]) <= Rows[r][c]:
                return
            else:
                self.sheet_aug.data[r][c] = 0
                self.sheet_aug.redraw()
        except:
            self.sheet_aug.data[r][c] = 0
            self.sheet_aug.redraw()

    # Function for cell select options
    def cell_select_opt2(event,Rows):

        # Set locked columns
        locked_cols = [0]

        # Enable/Disable user ability to edit cells
        if event.selected.column != None:
            if event.selected.column in locked_cols:
                self.sheet_set.disable_bindings(("edit_cell"))
            else:
                self.sheet_set.enable_bindings(("edit_cell"))
                self.sheet_set.extra_bindings([("edit_cell", lambda event: num_val2(event, Rows))])

    # Function for numeric validation
    def num_val2(event, Rows):

        # Get the selected row and column
        c = event.selected.column
        r = event.selected.row

        try:
            if r != 2:
                int(self.sheet_set.data[r][c])
                self.sheet_set.data[r][c] = int(self.sheet_set.data[r][c])
                self.sheet_set.redraw()
            else:
                float(self.sheet_set.data[r][c])
                self.sheet_set.data[r][c] = float(self.sheet_set.data[r][c])
                self.sheet_set.redraw()
        except:
            self.sheet_set.data[r][c] = ''
            self.sheet_set.redraw()

    # Function for cell select options
    def cell_select_opt3(event):

        # Set locked columns
        locked_cols = [0]

        # Enable/Disable user ability to edit cells
        if event.selected.column != None:
            if event.selected.column in locked_cols:
                self.sheet_labels.disable_bindings(("edit_cell"))
            else:
                self.sheet_labels.enable_bindings(("edit_cell"))
        
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
        self.Segment['ML']['Settings']['Model']['Architecture'] = self.combo_arch.get()
        self.Segment['ML']['Settings']['Model']['Encoder'] = self.combo_enc.get()
        if self.combo_prew.get() == 'Micronet':
            preweight = 'micronet'
        else:
            preweight = 'image-micronet'
        self.Segment['ML']['Settings']['Model']['PreWeights'] = preweight

        # -- Augmentation
        crop_w = int(self.combo_window.get().split('x')[0])
        self.Segment['ML']['Settings']['Augmentation']['Crop'] = crop_w
        keys = list(self.Segment['ML']['Settings']['Augmentation'].keys())
        for i in range(1,len(keys)):
            if self.Segment['ML']['Settings']['Augmentation'][keys[i]] is None:
                self.Segment['ML']['Settings']['Augmentation'][keys[i]] = float(self.sheet_aug.data[i-1][1])
            else:
                self.Segment['ML']['Settings']['Augmentation'][keys[i]] = [float(self.sheet_aug.data[i-1][1]),
                                                                           float(self.sheet_aug.data[i-1][2])]
                
        # -- Train
        keys = list(self.Segment['ML']['Settings']['Train'].keys())
        for i in range(len(keys)):
            if self.sheet_set.data[i][1] != '':
                self.Segment['ML']['Settings']['Train'][keys[i]] = self.sheet_set.data[i][1]

        # -- Classes
        ColorDict = { # Use BGR for MicroNet
                    0:(255,0,0),
                    1:(0,0,255),
                    2:(0,255,0)} 
        for i in range(len(self.sheet_labels.data)-1):
            if self.sheet_labels.data[i][2] == True:
                self.Segment['ML']['Settings']['Classes'][self.sheet_labels.data[i][1]] = ColorDict[i]
        if len(self.Segment['ML']['Settings']['Classes'].keys()) > 1:
            if self.sheet_labels.data[-1][1] == True:
                self.Segment['ML']['Settings']['Classes'][self.sheet_labels.data[-1][1]] = (0,0,0)

        # -- Settings
        if self.var_GPU.get() == 1:
            self.Segment['ML']['Settings']['Settings']['GPU'] = True

        if self.var_vizTD.get() == 1:
            self.Segment['ML']['Settings']['Settings']['TrainViz'] = True

        if self.var_vizVD.get() == 1:
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

        # Function to train a model
        def training_simulation(stop_event):

            # Begin Training 
            TrainMicroNetModel(self.Segment['ML']['Settings'])

            # Create Message
            messagebox.showinfo(message = 'Model Saved!')
            
        # Function to start training on thread
        def start_training():
            self.stop_event.clear()
            self.training_thread = threading.Thread(target=training_simulation, args=(self.stop_event,), daemon=True)
            self.training_thread.start()

        # Function for exit protocol
        def on_closing():
            self.stop_event.set()  # Signal the thread to stop
            loading.destroy()    # Then close the window

        # Create training window
        loading = tk.Toplevel(window)
        loading.title("Training Model")
        loading.geometry("600x400")
        loading.resizable(False, False)
        loading.configure(bg='white')
        loading.grab_set()
        loading.protocol("WM_DELETE_WINDOW", on_closing)

        # Set output text
        output_text = ScrolledText(loading, width=80, height=20)
        output_text.pack(padx=10, pady=10)

        # Redirect stdout
        sys.stdout = TextRedirector(output_text)

        # Initialize Thread
        self.stop_event = threading.Event()
        self.training_thread = None

        # Begin training
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
                                text=' MicroNet Model Definition',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the Instructions
        instructions = ("The MicroNet Model Definition page allows users to define " + 
                        "the settings for the MicroNet model and train a model. " + 
                        "\n\n Button Functions:")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Set list of buttons and functions 
        image_list = [ 'help_btn.png', 'save_btn.png', 'back_btn.png','cont_btn.png', 'train_mod.png']
        func_list = [f'Load the Help Window', 
                     f'Save the MicroNet Segmentation Model project',
                     f'Return to the Data Definition Page',
                     f'Continue to the Segment Image page',
                     f'Being Training the model'
                     ]

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

        # Add subtitle
        subtitle = ("Model Definition")

        label_sub1 = ttk.Label(
                            frame,
                            text=subtitle,
                            style = "Modern4.TLabel",
                            wraplength=750
                            )
        label_sub1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("The Model Definition section allows users to define the model " + 
                        "architecture, encoder, and pretrained weights for the model. " + 
                        "Further detail comparing the different model architectures and " + 
                        "encoders is given at " + 
                        "https://github.com/nasa/pretrained-microscopy-models/tree/main. " + 
                        "Additionally, a checkbox option is given to use GPU for training. " + 
                        "If selected and a GPU is found on the machine, GPU will be used; " + 
                        "otherwise, CPU will be used for training.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','mod_def.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add subtitle
        subtitle = ("Labels")

        label_sub1 = ttk.Label(
                            frame,
                            text=subtitle,
                            style = "Modern4.TLabel",
                            wraplength=750
                            )
        label_sub1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("The Labels section displays to the user the classes found " + 
                        "in the labeled images. Users can name a class using the " + 
                        "“Label” column of the table. Additionally, each column can " + 
                        "be selected/unselected to be included in the training. If a " + 
                        "class is unselected, it will be treated as the background class.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','labels.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add subtitle
        subtitle = ("Image Augmentation")

        label_sub1 = ttk.Label(
                            frame,
                            text=subtitle,
                            style = "Modern4.TLabel",
                            wraplength=750
                            )
        label_sub1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("The Image Augmentation section allows the user to define the " + 
                        "settings for random augmentations applied to each image in the " + 
                        "training set. A drop down menu provides the options for the crop " + 
                        "window that will be randomly selected for each image in the training " + 
                        "set. All test and validation images will have the same window size " + 
                        "but cropped in the center of the image. Entered probabilities for " + 
                        "each row must be between 0 and 1. Additionally, Random Brightness, " + 
                        "Random Contrast, and Blur have a specified limit input. Both the " + 
                        "Random Brightness and Random Contrast limit must be between 0 and 1. " + 
                        "Blur limit must be greater than 0.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','image_aug.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add subtitle
        subtitle = ("Training Settings")

        label_sub1 = ttk.Label(
                            frame,
                            text=subtitle,
                            style = "Modern4.TLabel",
                            wraplength=750
                            )
        label_sub1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("The Training Settings section allows users to define the " + 
                        "settings regarding training the model. In the table, either " + 
                        "the Epochs or Patience must be defined. Setting a value for " + 
                        "the Epochs row will train the model for a set number of " + 
                        "epochs regardless of performance. Setting a value for the " + 
                        "Patience will train the model until no change in performance " + 
                        "is seen for the number of epochs set in that row. If both " + 
                        "values are set, only the Epochs value will be passed to the " + 
                        "training function. Additionally, two checkboxes enable " + 
                        "visualizing the Training Data and Validation Data. " + 
                        "Checking either box will display each image with its " + 
                        "corresponding labels in a new window.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','train_set.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add subtitle
        subtitle = ("Training the Model")

        label_sub1 = ttk.Label(
                            frame,
                            text=subtitle,
                            style = "Modern4.TLabel",
                            wraplength=750
                            )
        label_sub1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("To begin training the model, press the “Train Model” button. " + 
                        "The user will be prompted to select the folder that the " + 
                        "images were exported to (both original cropped and labeled " + 
                        "images). The MicroNet output will be displayed in a separate " + 
                        "window to monitor progress.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','train_prog.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("When either the number of epochs or patience criteria is met, " + 
                        "the training and validation learning curves will be presented " + 
                        "to the user.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','learn_curves.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("The program will then ask the user if they want to continue " + 
                        "training. If “Yes” is selected, the model will continue " + 
                        "training. \n" +
                        "\u2022 If the number of epochs was set, the model will " + 
                        "train for the same number of additional epochs. \n" + 
                        "\u2022 If the patience was set, the learning rate will " + 
                        "be reduced by a factor of 0.1 and training will continue " + 
                        "until the same patience is met. \n\n"  + 
                        "Once no more training is desired, the user will be prompted to save the model.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

    # Create Page Title
    self.label_title = ttk.Label(
                                window,
                                text='MicroNet Model Definition',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(
                        anchor = 'center', 
                        relx = self.Placement['Train']['LabelTitle'][0], 
                        rely = self.Placement['Train']['LabelTitle'][1]
                        )
    self.att_list.append('self.label_title')

    # Create the frame for model architecture/encoder
    self.frame_model = tk.Frame(
                                window, 
                                bd=self.Placement['Train']['Frame1'][2], 
                                relief="ridge", 
                                width = self.Placement['Train']['Frame1'][3],
                                height = self.Placement['Train']['Frame1'][4],
                                bg="white"
                                )
    self.frame_model.place(
                        anchor = 'n', 
                        relx=self.Placement['Train']['Frame1'][0], 
                        rely=self.Placement['Train']['Frame1'][1]
                        )
    self.att_list.append('self.frame_model')

    # Create a label for the model architecture
    self.label_model = ttk.Label(
                                self.frame_model,
                                text='Model Definition',
                                style = "Modern3.TLabel",
                                )
    self.label_model.place(
                        anchor='n', 
                        relx = self.Placement['Train']['Label1'][0], 
                        rely = self.Placement['Train']['Label1'][1]
                        )
    self.att_list.append('self.label_model')

    # Create label for architecture
    self.label_arch = ttk.Label(
                                self.frame_model,
                                text='Architecture: ',
                                style = "Modern2.TLabel",
                                anchor='w'
                                )
    self.label_arch.place(
                        anchor='w', 
                        relx = self.Placement['Train']['Label2'][0], 
                        rely = self.Placement['Train']['Label2'][1]
                        )
    self.att_list.append('self.label_arch')

    # Create drop down for architecture
    self.combo_arch = ttk.Combobox(
                                self.frame_model,
                                values=self.architecture,
                                style="Modern.TCombobox",
                                state="readonly"
                                )
    self.combo_arch.place(
                        anchor='w', 
                        relx = self.Placement['Train']['Combo1'][0], 
                        rely = self.Placement['Train']['Combo1'][1]
                        )
    self.combo_arch.set(self.architecture[0]) 
    self.loc_att_list.append('self.combo_arch')

    # -- Set existing model architecture value
    if 'Model Information' in self.Segment.keys():
        self.combo_arch.set(self.Segment['Model Information'][3])

    # Create label for Encoder
    self.label_enc = ttk.Label(
                            self.frame_model,
                            text='Encoder: ',
                            style = "Modern2.TLabel",
                            anchor='w'
                            )
    self.label_enc.place(
                        anchor='w', 
                        relx = self.Placement['Train']['Label3'][0], 
                        rely = self.Placement['Train']['Label3'][1]
                        )
    self.att_list.append('self.label_enc')

    # Create drop down for encoder
    self.combo_enc = ttk.Combobox(
                                self.frame_model,
                                values=list(self.models.keys()),
                                style="Modern.TCombobox",
                                state="readonly"
                                )
    self.combo_enc.bind("<<ComboboxSelected>>", create_weights_drop)
    self.combo_enc.place(
                        anchor='w', 
                        relx = self.Placement['Train']['Combo2'][0], 
                        rely = self.Placement['Train']['Combo2'][1]
                        )
    self.combo_enc.set(list(self.models.keys())[0]) 
    self.loc_att_list.append('self.combo_enc')

    # -- Set existing model encoder value
    if 'Model Information' in self.Segment.keys():
        self.combo_enc.set(self.Segment['Model Information'][4])

    # Create label for Pretrained Weights
    self.label_prew = ttk.Label(
                                self.frame_model,
                                text='Pretrained Weights: ',
                                style = "Modern2.TLabel",
                                anchor='w'
                                )
    self.label_prew.place(
                        anchor='w', 
                        relx = self.Placement['Train']['Label4'][0], 
                        rely = self.Placement['Train']['Label4'][1]
                        )
    self.att_list.append('self.label_prew')

    # Create the drop down for pretrained weights
    create_weights_drop(None)

    # Create GPU Checkbutton
    self.var_GPU = tk.IntVar()
    self.check_GPU = ttk.Checkbutton(
                                    self.frame_model, 
                                    text="Use GPU", 
                                    variable=self.var_GPU,
                                    style="TCheckbutton"
                                    )
    self.check_GPU.place(
                        anchor = 'n', 
                        relx = self.Placement['Train']['Check1'][0], 
                        rely = self.Placement['Train']['Check1'][1]
                        )
    self.loc_att_list.append('self.check_GPU')

    # Create the frame for image augementation
    self.frame_aug = tk.Frame(
                            window, 
                            bd=self.Placement['Train']['Frame2'][2], 
                            relief="ridge", 
                            width = self.Placement['Train']['Frame2'][3],
                            height = self.Placement['Train']['Frame2'][4],
                            bg="white"
                            )
    self.frame_aug.place(
                        anchor = 'n', 
                        relx=self.Placement['Train']['Frame2'][0], 
                        rely=self.Placement['Train']['Frame2'][1]
                        )
    self.att_list.append('self.frame_aug')

    # Create label for Image Augmentation
    self.label_aug = ttk.Label(
                                self.frame_aug,
                                text='Image Augmentation',
                                style = "Modern3.TLabel",
                                )
    self.label_aug.place(
                        anchor='n', 
                        relx = self.Placement['Train']['Label5'][0], 
                        rely = self.Placement['Train']['Label5'][1]
                        )
    self.att_list.append('self.label_aug')

    # Create Label for Window Size
    self.label_window = ttk.Label(
                                self.frame_aug,
                                text='Crop Window: ',
                                style = "Modern2.TLabel",
                                )
    self.label_window.place(
                            anchor='n', 
                            relx = self.Placement['Train']['Label6'][0], 
                            rely = self.Placement['Train']['Label6'][1]
                            )
    self.att_list.append('self.label_window')

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
    self.combo_window = ttk.Combobox(
                                    self.frame_aug,
                                    values=size_opts,
                                    style="Modern.TCombobox",
                                    state="readonly"
                                    )
    self.combo_window.place(
                            anchor='n', 
                            relx = self.Placement['Train']['Combo4'][0], 
                            rely = self.Placement['Train']['Combo4'][1]
                            )
    self.combo_window.set(size_opts[-1]) 
    self.loc_att_list.append('self.combo_window')

    # -- Set existing model window value
    if 'Model Information' in self.Segment.keys():
        self.combo_window.set(self.Segment['Model Information'][6])

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
    self.sheet_aug = tksheet.Sheet(
                                self.frame_aug, 
                                total_rows = len(Rows1), 
                                total_columns = len(Cols1), 
                                headers = Cols1,
                                width = self.Placement['Train']['Sheet1'][2], 
                                height = self.Placement['Train']['Sheet1'][3], 
                                show_x_scrollbar = False, 
                                show_y_scrollbar = False,
                                font = ('Segoe UI',12,"normal"),
                                header_font = ('Segoe UI',12,"bold")
                                )
    self.sheet_aug.place(
                        anchor = 'n', 
                        relx = self.Placement['Train']['Sheet1'][0], 
                        rely = self.Placement['Train']['Sheet1'][1]
                        )
    self.loc_att_list.append('self.sheet_aug')

    # Format sheet
    self.sheet_aug.set_index_width(0)
    self.sheet_aug.column_width(column = 0, width = self.Placement['Train']['Sheet1'][4], redraw = True)
    self.sheet_aug.column_width(column = 1, width = self.Placement['Train']['Sheet1'][5], redraw = True)
    self.sheet_aug.column_width(column = 2, width = self.Placement['Train']['Sheet1'][6], redraw = True)
    self.sheet_aug.table_align(align = 'c',redraw=True)

    # Enable Bindings
    self.sheet_aug.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
    self.sheet_aug.extra_bindings([("cell_select", lambda event: cell_select_opt(event, Rows1))])

    # Set values
    for i in range(len(Rows1)):
        row = Rows1[i]
        self.sheet_aug.set_cell_data(i,0,row[0])
        if row[1] != None:
            self.sheet_aug.set_cell_data(i,1,0.5)
        if row[2] != None:
            self.sheet_aug.set_cell_data(i,2,0)

    # Populate Existing Data
    if "Model Information" in self.Segment.keys():
        sheet_data = self.Segment['Model Information'][0]
        for i in range(len(sheet_data)):
            for j in range(len(sheet_data[0])):
                self.sheet_aug.set_cell_data(i,j,sheet_data[i][j])

    # Redraw sheet
    self.sheet_aug.redraw()

    # Create the frame for training settings
    self.frame_set = tk.Frame(
                            window, 
                            bd=self.Placement['Train']['Frame3'][2], 
                            relief="ridge", 
                            width = self.Placement['Train']['Frame3'][3],
                            height = self.Placement['Train']['Frame3'][4],
                            bg="white"
                            )
    self.frame_set.place(
                        anchor = 'n', 
                        relx=self.Placement['Train']['Frame3'][0], 
                        rely=self.Placement['Train']['Frame3'][1]
                        )
    self.att_list.append('self.frame_set')

    # Create label for Training Settings
    self.label_set = ttk.Label(
                            self.frame_set,
                            text='Training Settings',
                            style = "Modern3.TLabel",
                            )
    self.label_set.place(
                        anchor='n', 
                        relx = self.Placement['Train']['Label7'][0], 
                        rely = self.Placement['Train']['Label7'][1]
                        )
    self.att_list.append('self.label_set')

    # Create the Training Settings Sheet
    Cols2 = ['Option','Value']
    Rows2 = [
        ['Epochs'],
        ['Patience'],
        ['Learning Rate'],
        ['Batch Size'],
        ['Validation Batch Size'],
        ]
    self.sheet_set = tksheet.Sheet(
                                self.frame_set, 
                                total_rows = len(Rows2), 
                                total_columns = len(Cols2), 
                                headers = Cols2,
                                width = self.Placement['Train']['Sheet2'][2], 
                                height = self.Placement['Train']['Sheet2'][3], 
                                show_x_scrollbar = False, 
                                show_y_scrollbar = False,
                                font = ('Segoe UI',12,"normal"),
                                header_font = ('Segoe UI',12,"bold")
                                )
    self.sheet_set.place(
                        anchor = 'n', 
                        relx = self.Placement['Train']['Sheet2'][0], 
                        rely = self.Placement['Train']['Sheet2'][1]
                        )
    self.loc_att_list.append('self.sheet_aug')

    # Format sheet
    self.sheet_set.set_index_width(0)
    self.sheet_set.column_width(column = 0, width = self.Placement['Train']['Sheet2'][4], redraw = True)
    self.sheet_set.column_width(column = 1, width = self.Placement['Train']['Sheet2'][5], redraw = True)
    self.sheet_set.table_align(align = 'c',redraw=True)

    # Enable Bindings
    self.sheet_set.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
    self.sheet_set.extra_bindings([("cell_select", lambda event: cell_select_opt2(event, Rows2))])

    # Set values
    for i in range(len(Rows2)):
        row = Rows2[i]
        self.sheet_set.set_cell_data(i,0,row[0])

    # Populate Existing Data
    if "Model Information" in self.Segment.keys():
        sheet_data = self.Segment['Model Information'][1]
        for i in range(len(sheet_data)):
            for j in range(len(sheet_data[0])):
                if i != 2 and j == 1:
                    try:
                        self.sheet_set.set_cell_data(i,j,int(sheet_data[i][j]))
                    except:
                        pass
                else:
                    self.sheet_set.set_cell_data(i,j,sheet_data[i][j])

    # Redraw sheet
    self.sheet_set.redraw()

    # Visualize Training Data
    self.var_vizTD = tk.IntVar()
    self.check_vizTD = ttk.Checkbutton(
                                    self.frame_set, 
                                    text="Visualize Training Data", 
                                    variable=self.var_vizTD,
                                    style="TCheckbutton"
                                    )
    self.check_vizTD.place(
                        anchor = 'n', 
                        relx = self.Placement['Train']['Check2'][0], 
                        rely = self.Placement['Train']['Check2'][1]
                        )
    self.loc_att_list.append('self.check_vizTD')

    # Visualize Validation Data
    self.var_vizVD = tk.IntVar()
    self.check_vizVD = ttk.Checkbutton(
                                    self.frame_set, 
                                    text="Visualize Validation Data", 
                                    variable=self.var_vizVD,
                                    style="TCheckbutton"
                                    )
    self.check_vizVD.place(
                            anchor = 'n', 
                            relx = self.Placement['Train']['Check3'][0], 
                            rely = self.Placement['Train']['Check3'][1]
                            )
    self.loc_att_list.append('self.check_vizVD')

    # Create the frame for labels
    self.frame_labels = tk.Frame(
                                window, 
                                bd=self.Placement['Train']['Frame4'][2], 
                                relief="ridge", 
                                width = self.Placement['Train']['Frame4'][3],
                                height = self.Placement['Train']['Frame4'][4],
                                bg="white"
                                )
    self.frame_labels.place(
                            anchor = 'n', 
                            relx=self.Placement['Train']['Frame4'][0], 
                            rely=self.Placement['Train']['Frame4'][1]
                            )
    self.att_list.append('self.frame_labels')

    # Create label for Classification Labels
    self.label_labels = ttk.Label(
                                self.frame_labels,
                                text='Labels',
                                style = "Modern3.TLabel",
                                )
    self.label_labels.place(
                            anchor='n', 
                            relx = self.Placement['Train']['Label8'][0], 
                            rely = self.Placement['Train']['Label8'][1]
                            )
    self.att_list.append('self.label_labels')

    # Create the Image Augmentation Sheet
    Cols3 = ['Color','Label',' ']
    Rows3 = []
    Colors = {1:(0,0,255), 2:(255,0,0), 3:(0,255,0)}

    # Get colors in each image
    for item in self.Segment['Data'].keys():
        for i in range(1,4):
            if len(self.Segment['Data'][item]['Segments'][i]['Pixel List']) > 0:
                if Colors[i] not in Rows3:
                    Rows3.append(Colors[i])

    # Create labels sheet
    self.sheet_labels = tksheet.Sheet(
                                    self.frame_labels, 
                                    total_rows = len(Rows3)+1, 
                                    total_columns = len(Cols3), 
                                    headers = Cols3,
                                    width = self.Placement['Train']['Sheet3'][2], 
                                    height = self.Placement['Train']['Sheet3'][3], 
                                    show_x_scrollbar = False, 
                                    show_y_scrollbar = False,
                                    font = ('Segoe UI',12,"normal"),
                                    header_font = ('Segoe UI',12,"bold")
                                    )
    self.sheet_labels.place(
                            anchor = 'n', 
                            relx = self.Placement['Train']['Sheet3'][0], 
                            rely = self.Placement['Train']['Sheet3'][1]
                            )
    self.loc_att_list.append('self.sheet_labels')

    # Format sheet
    self.sheet_labels.set_index_width(0)
    self.sheet_labels.column_width(column = 0, width = self.Placement['Train']['Sheet3'][4], redraw = True)
    self.sheet_labels.column_width(column = 1, width = self.Placement['Train']['Sheet3'][5], redraw = True)
    self.sheet_labels.column_width(column = 2, width = self.Placement['Train']['Sheet3'][6], redraw = True)
    self.sheet_labels.table_align(align = 'c',redraw=True)
    self.sheet_labels.checkbox('C', checked=True)

    # Enable Bindings
    self.sheet_labels.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
    self.sheet_labels.extra_bindings([("cell_select", lambda event: cell_select_opt3(event))])

    # Set values
    def rgb_to_hex(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    for i in range(len(Rows3)):
        hex_color = rgb_to_hex(Rows3[i][0], Rows3[i][1], Rows3[i][2])
        self.sheet_labels.highlight_cells(i, 0, bg=hex_color, fg='black')
    self.sheet_labels.set_cell_data(len(Rows3),0,'Other')

    # Populate Existing Data
    if "Model Information" in self.Segment.keys():
        sheet_data = self.Segment['Model Information'][2]
        for i in range(len(sheet_data)):
            for j in range(len(sheet_data[0])):
                self.sheet_labels.set_cell_data(i,j,sheet_data[i][j])

    # Redraw sheet
    self.sheet_labels.redraw()

    # Create Button to train
    self.btn_train = ttk.Button(
                               window, 
                               text = "Train Model", 
                               command = lambda:begin_train(self), 
                               style = 'Modern2.TButton',
                               width = self.Placement['Train']['ButtonTrain'][2]
                               )
    self.btn_train.place(
                        anchor = 'n', 
                        relx = self.Placement['Train']['ButtonTrain'][0], 
                        rely = self.Placement['Train']['ButtonTrain'][1]
                        )
    self.att_list.append('self.btn_train')
    
    # Create Continue Button
    self.btn_cont = ttk.Button(
                            window, 
                            text = "Continue", 
                            command = next_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Train']['ButtonCont'][2]
                            )
    self.btn_cont.place(
                        anchor = 'e', 
                        relx = self.Placement['Train']['ButtonCont'][0], 
                        rely = self.Placement['Train']['ButtonCont'][1]
                        )
    self.att_list.append('self.btn_cont')
    
    # Create Back Button
    self.btn_back = ttk.Button(
                            window, 
                            text = "Back", 
                            command = back_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Train']['ButtonBack'][2]
                            )
    self.btn_back.place(
                        anchor = 'e', 
                        relx = self.Placement['Train']['ButtonBack'][0], 
                        rely = self.Placement['Train']['ButtonBack'][1]
                        )
    self.att_list.append('self.btn_back')

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
                            width = self.Placement['Train']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['Train']['Help'][0], 
                        rely = self.Placement['Train']['Help'][1]
                        )
    self.att_list.append('self.btn_help')