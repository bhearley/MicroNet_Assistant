#-----------------------------------------------------------------------------------------
#
#   DataDefinition.py
#
#   PURPOSE: Split Image Into Training/Validation/Test
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def DataDefinition(self,window):
    # Import Modules
    import glob
    import os
    from PIL import Image, ImageTk
    import tkinter as tk
    from tkinter import ttk

    # Import Functions
    from General.DeleteWidgets import DeleteLocal
    from General.DeleteWidgets import DeletePages

    #Initialize list of attributes for each page
    self.att_list = []
    self.loc_att_list = []

    # Preallocate image lists
    if "ML" not in self.Segment.keys():

        # Get the Working Directory
        dir_name = os.path.dirname(self.proj_file)
        
        # Define the Temp folder path
        save_path = os.path.join(dir_name, 'Temp')

        # Create the data structure
        self.Segment['ML'] = {
                            'Data':{
                                    'Unused':[],
                                    'Train':[],
                                    'Valid':[],
                                    'Test':[]
                                    },
                            'Settings':{},
                            'TempDir':save_path
                            }
        
        # Add all files to structure
        files = glob.glob(os.path.join(self.Segment['ML']['TempDir'],'Annotated','*.png'))
        for file in files:
            self.Segment['ML']['Data']['Unused'].append(os.path.basename(file))

    # Function to add items to a list
    def add_to_list(self, tag):

        # Set Out Tag
        tag_o = tag

        # Get All Selected Images
        values = [self.listbox_all.get(idx) for idx in self.listbox_all.curselection()]
        if len(values) > 0:
            val_o = values
            tag_o = 'self.listbox_all'
        values = [self.listbox_train.get(idx) for idx in self.listbox_train.curselection()]
        if len(values) > 0:
            val_o = values
            tag_o = 'self.listbox_train'
        values = [self.listbox_val.get(idx) for idx in self.listbox_val.curselection()]
        if len(values) > 0:
            val_o = values
            tag_o = 'self.listbox_val'
        values = [self.listbox_test.get(idx) for idx in self.listbox_test.curselection()]
        if len(values) > 0:
            val_o = values
            tag_o = 'self.listbox_test'

        # Check tags aren't equal
        if tag != tag_o:

            # Get all options in both list boxes
            list1 = list(eval(tag_o).get(0, tk.END))
            list2 = list(eval(tag).get(0, tk.END))

            # Update Lists
            for item in val_o:
                list1.remove(item)
            list1.sort()
            list2 = list2 + val_o
            list2.sort()

            # Update Listboxes
            eval(tag_o).delete(0, tk.END)  
            for item in list1:
                eval(tag_o).insert(tk.END, item)

            eval(tag).delete(0, tk.END)  
            for item in list2:
                eval(tag).insert(tk.END, item)

            # Update Structure
            self.Segment['ML']['Data']['Unused'] = list(self.listbox_all.get(0, tk.END))
            self.Segment['ML']['Data']['Train'] = list(self.listbox_train.get(0, tk.END))
            self.Segment['ML']['Data']['Valid'] = list(self.listbox_val.get(0, tk.END))
            self.Segment['ML']['Data']['Test'] = list(self.listbox_test.get(0, tk.END))

    # Function to continue to next page
    def next_page():

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)

        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 7

        # Load the page
        self.load_page()

    # Function to go back to previous page
    def back_page():

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 5

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
                                text='Data Definition',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(
                            anchor = 'center', 
                            relx = self.Placement['DataDef']['LabelTitle'][0], 
                            rely = self.Placement['DataDef']['LabelTitle'][1]
                            )
    self.att_list.append('self.label_title')

    # Create a vertical scrollbar for All images
    self.scrollbar_all= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_all.place(
                            anchor='n', 
                            relx = self.Placement['DataDef']['Scrollbar1'][0], 
                            rely = self.Placement['DataDef']['Scrollbar1'][1], 
                            height = self.Placement['DataDef']['Scrollbar1'][2]
                            )
    self.loc_att_list.append('self.scrollbar_all')

    # Create the label for All Images
    self.label_all = ttk.Label(
                            window,
                            text='All Images',
                            style = "Modern3.TLabel"
                            )
    self.label_all.place(
                        anchor='n', 
                        relx = self.Placement['DataDef']['Label1'][0], 
                        rely = self.Placement['DataDef']['Label1'][1]
                        )
    self.loc_att_list.append('self.label_all')

    # Create All Images List Box
    items1 = tk.StringVar(value=self.Segment['ML']['Data']['Unused'])
    self.listbox_all = tk.Listbox(
                                window, 
                                listvariable=items1,
                                selectmode='multiple',
                                height = self.Placement['DataDef']['Listbox1'][2],
                                width = self.Placement['DataDef']['Listbox1'][3],
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd']
                                )
    self.listbox_all.place(
                        anchor='n', 
                        relx = self.Placement['DataDef']['Listbox1'][0], 
                        rely = self.Placement['DataDef']['Listbox1'][1]
                        )
    self.listbox_all.config(yscrollcommand= self.scrollbar_all.set)
    self.loc_att_list.append('self.listbox_all')

    # Create button to move items right
    self.btn_all = ttk.Button(
                            window, 
                            text = "Add to Unused", 
                            command = lambda : add_to_list(self,'self.listbox_all'), 
                            style = "Modern3.TButton",
                            width = self.Placement['DataDef']['Button1'][0]
                            )
    self.btn_all.place(
                    anchor = 'c', 
                    relx = self.Placement['DataDef']['Button1'][0], 
                    rely = self.Placement['DataDef']['Button1'][1]
                    )
    self.loc_att_list.append('self.btn_all')

    # Create a vertical scrollbar for Training Data
    self.scrollbar_train= ttk.Scrollbar(
                                        window, 
                                        orient= 'vertical', 
                                        style = "Vertical.TScrollbar"
                                        )
    self.scrollbar_train.place(
                            anchor='n', 
                            relx = self.Placement['DataDef']['Scrollbar2'][0], 
                            rely = self.Placement['DataDef']['Scrollbar2'][1], 
                            height = self.Placement['DataDef']['Scrollbar2'][2]
                            )
    self.loc_att_list.append('self.scrollbar_train')

    # Create the label for Training Data
    self.label_train = ttk.Label(
                                window,
                                text='Training Data',
                                style = "Modern3.TLabel"
                                )
    self.label_train.place(
                        anchor='n', 
                        relx = self.Placement['DataDef']['Label2'][0], 
                        rely = self.Placement['DataDef']['Label2'][1]
                        )
    self.loc_att_list.append('self.label_train')

    # Create Training Data List Box
    items2 = tk.StringVar(value=self.Segment['ML']['Data']['Train'])
    self.listbox_train = tk.Listbox(
                                    window, 
                                    listvariable=items2,
                                    selectmode='multiple',
                                    height = self.Placement['DataDef']['Listbox2'][2],
                                    width = self.Placement['DataDef']['Listbox2'][3],
                                    bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                    fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                    font=self.style_man['ListBox']['ListBox1']['font'],    
                                    selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                    selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                    highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                    bd=self.style_man['ListBox']['ListBox1']['bd']
                                    )
    self.listbox_train.place(
                            anchor='n', 
                            relx = self.Placement['DataDef']['Listbox2'][0], 
                            rely = self.Placement['DataDef']['Listbox2'][1]
                            )
    self.listbox_train.config(yscrollcommand= self.scrollbar_train.set)
    self.loc_att_list.append('self.listbox_train')

    # Create button to move items to train
    self.btn_train = ttk.Button(
                                window, 
                                text = "Add to Training", 
                                command = lambda : add_to_list(self,'self.listbox_train'), 
                                style = "Modern3.TButton",
                                width = self.Placement['DataDef']['Button2'][2]
                                )
    self.btn_train.place(
                        anchor = 'c', 
                        relx = self.Placement['DataDef']['Button2'][0], 
                        rely = self.Placement['DataDef']['Button2'][1]
                        )
    self.loc_att_list.append('self.btn_train')

    # Create a vertical scrollbar for Validation Data
    self.scrollbar_val= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_val.place(
                            anchor='n', 
                            relx = self.Placement['DataDef']['Scrollbar3'][0], 
                            rely = self.Placement['DataDef']['Scrollbar3'][1], 
                            height = self.Placement['DataDef']['Scrollbar3'][2]
                            )
    self.loc_att_list.append('self.scrollbar_val')

    # Create the label for Validation Data
    self.label_val = ttk.Label(
                            window,
                            text='Validation Data',
                            style = "Modern3.TLabel"
                            )
    self.label_val.place(
                        anchor='n', 
                        relx = self.Placement['DataDef']['Label3'][0], 
                        rely = self.Placement['DataDef']['Label3'][1]
                        )
    self.loc_att_list.append('self.label_val')

    # Create Validation Data List Box
    items3 = tk.StringVar(value=self.Segment['ML']['Data']['Valid'])
    self.listbox_val = tk.Listbox(
                                window, 
                                listvariable=items3,
                                selectmode='multiple',
                                height = self.Placement['DataDef']['Listbox3'][2],
                                width = self.Placement['DataDef']['Listbox3'][3],
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd']
                                )
    self.listbox_val.place(
                        anchor='n', 
                        relx = self.Placement['DataDef']['Listbox3'][0], 
                        rely = self.Placement['DataDef']['Listbox3'][1]
                        )
    self.listbox_val.config(yscrollcommand= self.scrollbar_val.set)
    self.loc_att_list.append('self.listbox_val')

    # Create button to move items to validation
    self.btn_val = ttk.Button(
                            window, 
                            text = "Add to Valdiation", 
                            command = lambda : add_to_list(self,'self.listbox_val'), 
                            style = "Modern3.TButton",
                            width = self.Placement['DataDef']['Button3'][2]
                            )
    self.btn_val.place(
                    anchor = 'c', 
                    relx = self.Placement['DataDef']['Button3'][0], 
                    rely = self.Placement['DataDef']['Button3'][1]
                    )
    self.loc_att_list.append('self.btn_val')

    # Create a vertical scrollbar for Test Data
    self.scrollbar_test= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_test.place(
                            anchor='n', 
                            relx = self.Placement['DataDef']['Scrollbar4'][0], 
                            rely = self.Placement['DataDef']['Scrollbar4'][1], 
                            height = self.Placement['DataDef']['Scrollbar4'][2]
                            )
    self.loc_att_list.append('self.scrollbar_test')

    # Create the label for All Images
    self.label_test = ttk.Label(
                                window,
                                text='Test Data',
                                style = "Modern3.TLabel"
                                )
    self.label_test.place(
                        anchor='n', 
                        relx = self.Placement['DataDef']['Label4'][0], 
                        rely = self.Placement['DataDef']['Label4'][1]
                        )
    self.loc_att_list.append('self.label_test')

    # Create All Images List Box
    items4 = tk.StringVar(value=self.Segment['ML']['Data']['Test'])
    self.listbox_test = tk.Listbox(
                                window, 
                                listvariable=items4,
                                selectmode='multiple',
                                height = self.Placement['DataDef']['Listbox4'][2],
                                width = self.Placement['DataDef']['Listbox4'][3],
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd']
                                )
    self.listbox_test.place(
                            anchor='n', 
                            relx = self.Placement['DataDef']['Listbox4'][0], 
                            rely = self.Placement['DataDef']['Listbox4'][1]
                            )
    self.listbox_test.config(yscrollcommand= self.scrollbar_test.set)
    self.loc_att_list.append('self.listbox_test')

    # Create button to move items to test
    self.btn_test = ttk.Button(
                            window, 
                            text = "Add to Test", 
                            command = lambda : add_to_list(self,'self.listbox_test'), 
                            style = "Modern3.TButton",
                            width = self.Placement['DataDef']['Button4'][2]
                            )
    self.btn_test.place(
                        anchor = 'c', 
                        relx = self.Placement['DataDef']['Button4'][0], 
                        rely = self.Placement['DataDef']['Button4'][1]
                        )
    self.loc_att_list.append('self.btn_test')

    # Create Continue Button
    self.btn_cont = ttk.Button(
                            window, 
                            text = "Continue", 
                            command = next_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['DataDef']['ButtonCont'][2]
                            )
    self.btn_cont.place(
                        anchor = 'e', 
                        relx = self.Placement['DataDef']['ButtonCont'][0], 
                        rely = self.Placement['DataDef']['ButtonCont'][1]
                        )
    self.att_list.append('self.btn_cont')
    
    # Create Back Button
    self.btn_back = ttk.Button(
                            window, 
                            text = "Back", 
                            command = back_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['DataDef']['ButtonBack'][2]
                            )
    self.btn_back.place(
                        anchor = 'e', 
                        relx = self.Placement['DataDef']['ButtonBack'][0], 
                        rely = self.Placement['DataDef']['ButtonBack'][1]
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
                            width = self.Placement['DataDef']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['DataDef']['Help'][0], 
                        rely = self.Placement['DataDef']['Help'][1]
                        )
    self.att_list.append('self.btn_help')