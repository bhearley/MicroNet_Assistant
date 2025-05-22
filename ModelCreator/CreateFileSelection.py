#-----------------------------------------------------------------------------------------
#
#   CreateFileSelection.py
#
#   PURPOSE: Allow user to select folder and images for the labelling.
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def CreateFileSelection(self,window):
    #Import Modules
    import imghdr
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import os
    from PIL import Image, ImageTk
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import ttk

    # Import Functions
    from General.DeleteWidgets import DeleteLocal
    from General.DeleteWidgets import DeletePages

    #Initialize list of attributes for each page
    self.att_list = []
    self.loc_att_list = []

    # Function to set image directory
    def set_path():

        # Delete Local Attributes
        DeleteLocal(self)

        # Get the Image Directory
        self.file_path = filedialog.askdirectory(
            title="Select Folder Containing Images",)

        if self.file_path == '':
            self.proj_file = None
            return
    
        # Get all image files
        files = os.listdir(self.file_path)
        if files is not None:
            img_files = []
            for file in files:
                if not os.path.isfile(os.path.join(self.file_path,file)):
                    continue
                else:
                    image_type = imghdr.what(os.path.join(self.file_path,file))
                    if image_type is not None:
                        img_files.append(file)

        # Save to data structure
        self.Segment['Files'] = {
                                'Path': self.file_path,
                                'All Files': img_files,
                                'Project Files':[],
                                'Resized Images':{},
                                'Segment Files' : []
                                }

        # Display images
        show_images(self)
    
    # Function to display images
    def show_images(self):

        # Function to move items right
        def move_right():
        
            # Get selected values
            values = [self.listbox_all.get(idx) for idx in self.listbox_all.curselection()]

            # Get all options in both list boxes
            list1 = list(self.listbox_all.get(0, tk.END))
            list2 = list(self.listbox_man.get(0, tk.END))

            # Update Lists
            for item in values:
                list1.remove(item)
            list1.sort()
            list2 = list2 + values
            list2.sort()

            # Update Listboxes
            self.listbox_all.delete(0, tk.END)  
            for item in list1:
                self.listbox_all.insert(tk.END, item)

            self.listbox_man.delete(0, tk.END)  
            for item in list2:
                self.listbox_man.insert(tk.END, item)

            # Update Data Structures
            self.Segment['Files']['All Files'] = list1
            self.Segment['Files']['Segment Files'] = list2

        # Function to move items left
        def move_left():
        
            # Get selected values
            values = [self.listbox_man.get(idx) for idx in self.listbox_man.curselection()]

            # Get all options in both list boxes
            list1 = list(self.listbox_all.get(0, tk.END))
            list2 = list(self.listbox_man.get(0, tk.END))

            # Update Lists
            for item in values:
                list2.remove(item)
            list2.sort()
            list1 = list1 + values
            list1.sort()

            # Update Listboxes
            self.listbox_all.delete(0, tk.END)  
            for item in list1:
                self.listbox_all.insert(tk.END, item)

            self.listbox_man.delete(0, tk.END)  
            for item in list2:
                self.listbox_man.insert(tk.END, item)

            # Update Data Structures
            self.Segment['Files']['All Files'] = list1
            self.Segment['Files']['Segment Files'] = list2

        # Function to move all items right
        def move_all_right():
        
            # Get all options in both list boxes
            list1 = list(self.listbox_all.get(0, tk.END))
            list2 = list(self.listbox_man.get(0, tk.END))

            # Update Lists
            list2 = list2 + list1
            while len(list1) > 0:
                list1.remove(list1[0])
            list1.sort()
            list2.sort()

            # Update Listboxes
            self.listbox_all.delete(0, tk.END)  
            for item in list1:
                self.listbox_all.insert(tk.END, item)

            self.listbox_man.delete(0, tk.END)  
            for item in list2:
                self.listbox_man.insert(tk.END, item)

            # Update Data Structures
            self.Segment['Files']['All Files'] = list1
            self.Segment['Files']['Segment Files'] = list2

        # Function to move all items left
        def move_all_left():
        
            # Get all options in both list boxes
            list1 = list(self.listbox_all.get(0, tk.END))
            list2 = list(self.listbox_man.get(0, tk.END))

            # Update Lists
            list1 = list2 + list1
            while len(list2) > 0:
                list2.remove(list2[0])
            list1.sort()
            list2.sort()

            # Update Listboxes
            self.listbox_all.delete(0, tk.END)  
            for item in list1:
                self.listbox_all.insert(tk.END, item)

            self.listbox_man.delete(0, tk.END)  
            for item in list2:
                self.listbox_man.insert(tk.END, item)

            # Update Data Strucutres
            self.Segment['Files']['All Files'] = list1
            self.Segment['Files']['Segment Files'] = list2

        # Function to view selected images
        def view_selected():
        
            # Function to display image
            def show_image(tag):
        
                # Delete existing image
                for widget in view_window.winfo_children():
                    if isinstance(widget, tk.Canvas):
                        widget.delete("all")

                # Delete existing image title
                try:
                    self.label_title_v.destroy()
                except:
                    pass

                # Get the new image
                if tag == 'r':
                    self.ct = self.ct + 1
                if tag == 'l':
                    self.ct = self.ct - 1
                if self.ct == len(self.all_files_v):
                    self.ct = 0
                if self.ct == -1:
                    self.ct = len(self.all_files_v)-1

                # Create the title
                self.label_title_v = ttk.Label(
                                            view_window,
                                            text=self.all_files_v[self.ct],
                                            style = "ModernT.TLabel"
                                            )
                self.label_title_v.place(
                                        anchor="n", 
                                        relx = self.Placement['FileSelect']['LabelT'][0], 
                                        rely = self.Placement['FileSelect']['LabelT'][1]
                                        )

                # Show the image
                self.img_view = Image.open(os.path.join(self.file_path, self.all_files_v[self.ct])).convert('RGBA')

                # Create the Matplotlib Figure
                # -- Get the image dimensions in pixels
                img_width = self.img_view.width
                img_height = self.img_view.height

                # -- Get the DPI
                dpi = window.winfo_fpixels('1i')  # pixels per inch
                
                # -- Convert max size to pixels
                max_width_px = int(self.Placement['FileSelect']['Canvas1'][2] * dpi)
                max_height_px = int(self.Placement['FileSelect']['Canvas1'][3] * dpi)

                # -- Get the scale
                scale = min(max_width_px / img_width, max_height_px / img_height)

                # -- Get the figure size
                new_width = int(img_width * scale)/dpi
                new_height = int(img_height * scale)/dpi

                # -- Create the figure
                self.figv, self.axv = plt.subplots(figsize=(new_width, new_height))
                self.figv.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

                # Embed the Matplotlib figure in Tkinter
                self.canvas_v = FigureCanvasTkAgg(self.figv, master=view_window)
                self.canvas_widget_v = self.canvas_v.get_tk_widget()
                self.canvas_widget_v.config(
                                        width=int(self.figv.get_figwidth() * self.figv.get_dpi()),
                                        height=int(self.figv.get_figheight() * self.figv.get_dpi())
                                        )
                self.canvas_widget_v.place(
                                        anchor='n', 
                                        relx = self.Placement['FileSelect']['Canvas1'][0], 
                                        rely = self.Placement['FileSelect']['Canvas1'][1]
                                        )

                # Display the image
                self.axv.clear()  
                self.axv.imshow(self.img_view)
                self.axv.axis('off')  
                self.canvas_v.draw()

                # Add the Matplotlib navigation toolbar
                self.toolbar = NavigationToolbar2Tk(self.canvas_v, view_window)
                self.toolbar.update()
                self.toolbar.place(
                                anchor='n', 
                                relx = self.Placement['FileSelect']['Toolbar1'][0], 
                                rely = self.Placement['FileSelect']['Toolbar1'][1]
                                )
                self.loc_att_list.append('self.toolbar')

            # Get All Selected Files
            self.all_files_v = []

            # Get selected values
            values1 = [self.listbox_all.get(idx) for idx in self.listbox_all.curselection()]
            values2 = [self.listbox_man.get(idx) for idx in self.listbox_man.curselection()]

            for value in values1:
                self.all_files_v.append(value)
            for value in values2:
                self.all_files_v.append(value)

            # Check if files have been selected
            if len(self.all_files_v) > 0:

                # Create a window to view the images
                view_window = tk.Toplevel(window)
                view_window.title("View Images")
                view_window.geometry("800x700")
                view_window.resizable(False, False)
                view_window.configure(bg='white')
                view_window.grab_set()

                # Create button to scroll left
                btn_left_v = ttk.Button(
                                        view_window, 
                                        text = "\u2190", 
                                        command = lambda:show_image('l'), 
                                        style = "Modern4.TButton",
                                        width = self.Placement['FileSelect']['ButtonLeftW'][2]
                                        )
                btn_left_v.place(
                                anchor = 'n', 
                                relx = self.Placement['FileSelect']['ButtonLeftW'][0], 
                                rely = self.Placement['FileSelect']['ButtonLeftW'][1]
                                )

                # Create button to scroll right
                btn_right_v = ttk.Button(
                                        view_window, 
                                        text = "\u2192", 
                                        command = lambda:show_image('r'),
                                        style = "Modern4.TButton",
                                        width = self.Placement['FileSelect']['ButtonRightW'][2]
                                        )
                btn_right_v.place(
                                anchor = 'n', 
                                relx = self.Placement['FileSelect']['ButtonRightW'][0], 
                                rely = self.Placement['FileSelect']['ButtonRightW'][1]
                                )

                # Initialize
                self.ct = -1
                show_image('r')
            
            else:
                messagebox.showerror(message="No files selected!")

        # Delete Local Attributes
        DeleteLocal(self)

        # Get File List
        self.file_path = self.Segment['Files']['Path']
        
        # Create a vertical scrollbar for all images
        self.scrollbar_all= ttk.Scrollbar(
                                        window, 
                                        orient= 'vertical', 
                                        style = "Vertical.TScrollbar"
                                        )
        self.scrollbar_all.place(
                                anchor='n', 
                                relx = self.Placement['FileSelect']['Scrollbar1'][0], 
                                rely = self.Placement['FileSelect']['Scrollbar1'][1], 
                                height = self.Placement['FileSelect']['Scrollbar1'][2]
                                )
        self.loc_att_list.append('self.scrollbar_all')

        # Create a label for all images
        self.label_all = ttk.Label(
                                window,
                                text='All Images',
                                style = "Modern3.TLabel"
                                )
        self.label_all.place(
                            anchor='n', 
                            relx = self.Placement['FileSelect']['Label1'][0], 
                            rely = self.Placement['FileSelect']['Label1'][1]
                            )
        self.loc_att_list.append('self.label_all')

        # Get list of all files
        all_images = self.Segment['Files']['All Files']
        all_images.sort()

        # Create a list box for all files
        items = tk.StringVar(value=all_images)
        self.listbox_all = tk.Listbox(
                                    window, 
                                    listvariable=items,
                                    selectmode='multiple',
                                    height = self.Placement['FileSelect']['Listbox1'][2],
                                    width = self.Placement['FileSelect']['Listbox1'][3],
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
                            relx = self.Placement['FileSelect']['Listbox1'][0], 
                            rely = self.Placement['FileSelect']['Listbox1'][1]
                            )
        self.listbox_all.config(yscrollcommand= self.scrollbar_all.set)
        self.loc_att_list.append('self.listbox_all')

        # Configure the scrollbar for all images
        self.scrollbar_all.config(command= self.listbox_all.yview)

        # Create a vertical scrollbar for project images
        self.scrollbar_man= ttk.Scrollbar(
                                        window, 
                                        orient= 'vertical', 
                                        style = "Vertical.TScrollbar"
                                        )
        self.scrollbar_man.place(
                                anchor='n', 
                                relx = self.Placement['FileSelect']['Scrollbar2'][0], 
                                rely = self.Placement['FileSelect']['Scrollbar2'][1], 
                                height = self.Placement['FileSelect']['Scrollbar2'][2]
                                )
        self.loc_att_list.append('self.scrollbar_man')

        # Create the label for project images
        self.label_man = ttk.Label(
                                window,
                                text='Manual Segmentation Images',
                                style = "Modern3.TLabel"
                                )
        self.label_man.place(
                            anchor='n', 
                            relx = self.Placement['FileSelect']['Label2'][0], 
                            rely = self.Placement['FileSelect']['Label2'][1]
                            )
        self.loc_att_list.append('self.label_man')

        # Get list of project images
        seg_images = self.Segment['Files']['Segment Files']
        seg_images.sort()

         # Create the list box for project images
        items2 = tk.StringVar(value=seg_images)
        self.listbox_man = tk.Listbox(
                                    window, 
                                    listvariable=items2,
                                    selectmode='multiple',
                                    height = self.Placement['FileSelect']['Listbox2'][2],
                                    width = self.Placement['FileSelect']['Listbox2'][3],
                                    bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                    fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                    font=self.style_man['ListBox']['ListBox1']['font'],    
                                    selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                    selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                    highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                    bd=self.style_man['ListBox']['ListBox1']['bd']
                                    )
        self.listbox_man.place(
                            anchor='n', 
                            relx = self.Placement['FileSelect']['Listbox2'][0], 
                            rely = self.Placement['FileSelect']['Listbox2'][1]
                            )
        self.listbox_man.config(yscrollcommand= self.scrollbar_man.set)
        self.loc_att_list.append('self.listbox_man')

        # Configure the scrollbar for project images
        self.scrollbar_man.config(command= self.listbox_man.yview)

        # Create button to move items right
        self.btn_right = ttk.Button(
                                window, 
                                text = "\u2192", 
                                command = move_right, 
                                style = "Modern4.TButton",
                                width = self.Placement['FileSelect']['ButtonRight'][2]
                                )
        self.btn_right.place(
                            anchor = 'c', 
                            relx = self.Placement['FileSelect']['ButtonRight'][0], 
                            rely = self.Placement['FileSelect']['ButtonRight'][1]
                            )
        self.loc_att_list.append('self.btn_right')

        # Create button to move items left
        self.btn_left = ttk.Button(
                                window, 
                                text = "\u2190", 
                                command = move_left, 
                                style = "Modern4.TButton",
                                width = self.Placement['FileSelect']['ButtonLeft'][2]
                                )
        self.btn_left.place(
                            anchor = 'c', 
                            relx = self.Placement['FileSelect']['ButtonLeft'][0], 
                            rely = self.Placement['FileSelect']['ButtonLeft'][1]
                            )
        self.loc_att_list.append('self.btn_left')

        # Create button to move all items right
        self.btn_right_all = ttk.Button(
                                       window, 
                                       text = "Add All Images", 
                                       command = move_all_right, 
                                       style = "Modern3.TButton",
                                       width = self.Placement['FileSelect']['ButtonAllRight'][2]
                                        )
        self.btn_right_all.place(
                                anchor = 'n', 
                                relx = self.Placement['FileSelect']['ButtonAllRight'][0], 
                                rely = self.Placement['FileSelect']['ButtonAllRight'][1]
                                )
        self.loc_att_list.append('self.btn_right_all')

        # Create button to move all items left
        self.btn_left_all = ttk.Button(
                                    window, 
                                    text = "Remove All Images", 
                                    command = move_all_left, 
                                    style = "Modern3.TButton",
                                    width = self.Placement['FileSelect']['ButtonAllLeft'][2]
                                    )
        self.btn_left_all.place(
                                anchor = 'n', 
                                relx = self.Placement['FileSelect']['ButtonAllLeft'][0], 
                                rely = self.Placement['FileSelect']['ButtonAllLeft'][1]
                                )
        self.loc_att_list.append('self.btn_left_all')

        # Create button to view an image
        self.btn_view = ttk.Button(
                                window, 
                                text = "View Selected Images", 
                                command = view_selected, 
                                style = "Modern3.TButton",
                                width = self.Placement['FileSelect']['ButtonView'][0]
                                )
        self.btn_view.place(
                            anchor = 'n', 
                            relx = self.Placement['FileSelect']['ButtonView'][0], 
                            rely = self.Placement['FileSelect']['ButtonView'][1]
                            )
        self.loc_att_list.append('self.btn_view')

    # Function to continue to next page
    def next_page():

        # Check if the image directory has been set
        if hasattr(self,"listbox_man") == False:

            # Show error if there are no segementation files
            messagebox.showerror(message = 'No Image Directory Set.')
            return
        
        # Get the list of project images
        list2 = list(self.listbox_man.get(0, tk.END))

        # Check for project images
        if len(list2) == 0:

            # Show error if there are no segementation files
            messagebox.showerror(message = 'No files added for manual labelling.')
            return

        # Save the segmentation files
        self.Segment['Files']['Project Files'] = list2

        # Save a copy of each image
        for item in list2:
            self.Segment['Files']['Resized Images'][item] = Image.open(os.path.join(self.Segment['Files']['Path'], item)).convert('RGBA')

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 2

        # Load the page
        self.load_page()

    # Function to go back to the previous page
    def back_page():

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 0

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
                                text=' Image Selection',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the Instructions
        instructions = ("The Image Selection page allows selection of the folder containing the " +
                       "images to segment and select which files to include in the project. \n\n" +
                       "Button Functions:")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Set list of buttons and functions
        image_list = ['save_btn.png', 'help_btn.png','back_btn.png','cont_btn.png','set_img.png']
        func_list = [f'Save the project', 
                     f'Load the Help Window',
                     f'Return to the Main Menu',
                     f'Continue to the Resize Images page', 
                     f'Set the directory that contains the images used to train the MicroNet model']

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
        instructions = ("After setting the directory, two list boxes will be displayed to add images to the project. " + 
                        "Only images in the lefthand list box will be used for training the MicroNet model.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','sel_imgs.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Individual images can be added to the project by selecting the file name on the "+
                        "lefthand box and pressing the '\u2192' button. Images can be removed from the project by " + 
                        "selecting the filename on the right hand box and pressing the '\u2190' button. Additionally, "+
                        "all images can be added to the project by pressing the 'Add All Images' button, and all "+""
                        "image can be removed from the project by pressing the 'Remove All Images' button.")

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
                                text='Image Selection',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(
                        anchor = 'center', 
                        relx = self.Placement['FileSelect']['LabelTitle'][0], 
                        rely = self.Placement['FileSelect']['LabelTitle'][1]
                        )
    self.att_list.append('self.label_title')

    # Create Folder Selection Button
    self.btn_dir = ttk.Button(
                            window, 
                            text = "Set Image Directory", 
                            command = set_path, 
                            style = 'Modern.TButton',
                            width = self.Placement['FileSelect']['ButtonFldr'][2]
                            )
    self.btn_dir.place(
                    anchor = 'center', 
                    relx = self.Placement['FileSelect']['ButtonFldr'][0], 
                    rely = self.Placement['FileSelect']['ButtonFldr'][1]
                    )
    self.att_list.append('self.btn_dir')
    
    # Create Continue Button
    self.btn_cont = ttk.Button(
                            window, 
                            text = "Continue", 
                            command = next_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['FileSelect']['ButtonCont'][2]
                            )
    self.btn_cont.place(
                        anchor = 'e', 
                        relx = self.Placement['FileSelect']['ButtonCont'][0], 
                        rely = self.Placement['FileSelect']['ButtonCont'][1]
                        )
    self.att_list.append('self.btn_cont')
    
    # Create Back Button
    self.btn_back = ttk.Button(
                            window, 
                            text = "Back", 
                            command = back_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['FileSelect']['ButtonBack'][2]
                            )
    self.btn_back.place(
                        anchor = 'e', 
                        relx = self.Placement['FileSelect']['ButtonBack'][0], 
                        rely = self.Placement['FileSelect']['ButtonBack'][1]
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
                            width = self.Placement['FileSelect']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['FileSelect']['Help'][0], 
                        rely = self.Placement['FileSelect']['Help'][1]
                        )
    self.att_list.append('self.btn_help')

    # Load Files
    if 'Files' in self.Segment.keys():
        show_images(self)