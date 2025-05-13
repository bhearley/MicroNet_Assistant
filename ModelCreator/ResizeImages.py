#-----------------------------------------------------------------------------------------
#
#   ResizeImages.py
#
#   PURPOSE: Resize the images for MicroNet
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def ResizeImages(self,window):
    # Import Modules
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import os
    from PIL import Image, ImageTk
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk    

    # Import Functions
    from General.DeleteWidgets import DeleteLocal
    from General.DeleteWidgets import DeletePages

    #Initialize list of attributes for each page
    self.att_list = []
    self.loc_att_list = []

    # Initialize pass
    self.pass_in = False

    # Function to show the image
    def load_image(self):
        # Function for Validation for Entry
        def only_numbers_and_decimal(char, current_value):
            # Check if the character is a digit or a decimal point
            if char.isdigit():
                return True
            elif char == '.' and current_value.count('.') == 1:  # Allow only one decimal point
                return True
            return False
        
        # Function to scale images
        def scale_img(self):
            # Get the scale
            scale = float(self.entry_S.get())

            # Scale all images
            if self.var.get() == 1:
                keys = list(self.Segment['Files']['Resized Images'].keys())

            # Scale current image only
            else:
                keys = [self.img_full_name]

            # Scale Images
            for key in keys:
                # Get the image
                self.img_to_scale = self.Segment['Files']['Resized Images'][key]

                # Scale the image
                self.img_to_scale = self.img_to_scale.resize((int(self.img_to_scale.width*scale), 
                                                            int(self.img_to_scale.height*scale)))

                # Save the resized image
                self.Segment['Files']['Resized Images'][key] = self.img_to_scale

            # Reload the window
            self.pass_in = True
            load_image(self)
        
        # Delete Existing Items
        for widget in self.loc_att_list:
            try:
                eval(widget).destroy()
            except:
                pass
        try:
            del self.canvas
        except:
            pass

        # Get the image name
        if self.pass_in == False:
            if len([self.listbox_01.get(idx) for idx in self.listbox_01.curselection()]) > 0:
                self.img_full_name = [self.listbox_01.get(idx) for idx in self.listbox_01.curselection()][0]
            else:
                messagebox.showerror(message = 'No image selected!')
                return
        else:
            self.pass_in = False

            # Load the image
        self.image_full = self.Segment['Files']['Resized Images'][self.img_full_name]

        # Create a Matplotlib figure
        if hasattr(self,"fig1") == False:
            self.fig1, self.ax1 = plt.subplots(figsize=(8/1.15, 6/1.15))
            self.fig1.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig1, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(width=int(self.fig1.get_figwidth() * self.fig1.get_dpi()),
                                height=int(self.fig1.get_figheight() * self.fig1.get_dpi()))
        self.canvas_widget.place(anchor='n', relx = 0.5, rely = 0.15)
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax1.clear()  # Clear previous image
        self.ax1.imshow(self.image_full)
        self.ax1.axis('off')  # Hide axes
        self.canvas.draw()

        # Add the Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, window)
        self.toolbar.update()
        self.toolbar.place(anchor='n', relx = 0.5, rely = 0.8)
        self.loc_att_list.append('self.toolbar')

        # Create the x label
        self.x_label = ttk.Label(
                        window, 
                        text="X:", 
                        style = "Modern2.TLabel"
                        )
        self.x_label.place(anchor = 'n', relx = 0.7525, rely = 0.199)
        self.loc_att_list.append('self.x_label')

        # Create the y label
        self.y_label = ttk.Label(
                        window, 
                        text="Y:", 
                        style = "Modern2.TLabel"
                        )
        self.y_label.place(anchor = 'n', relx = 0.825, rely = 0.199)
        self.loc_att_list.append('self.y_label')

        #Load an image using PIL
        self.image_path_scale = os.path.join(os.getcwd(),'GUI','Resize','scale.png')
        self.image_scale = Image.open(self.image_path_scale)
        scale = 0.05
        self.image_scale = self.image_scale.resize((int(self.image_scale.width*scale), int(self.image_scale.height*scale)))

        # Convert the image to a Tkinter-compatible format
        self.photo_scale = ImageTk.PhotoImage(self.image_scale)

        # Create a ttk.Label with the image
        self.label_scale = ttk.Label(window, 
                                    image=self.photo_scale,
                                    background="white")
        self.label_scale.place(anchor = 'n', relx = 0.9, rely = 0.199)
        self.loc_att_list.append('self.label_scale')

        # Register the validation function
        vcmd = (window.register(only_numbers_and_decimal), "%S", "%P")

        # Add the Entry Box for X
        self.entry_X = ttk.Entry(window, 
                            validate="key", 
                            validatecommand=vcmd, 
                            style="Custom.TEntry",
                            justify='center',
                            width = 10
                            )
        self.entry_X.insert(0, str(int(self.image_full.width)))
        self.entry_X.place(anchor = 'n', relx = 0.7875, rely = 0.2)
        self.entry_X.config(state='disabled')
        self.loc_att_list.append('self.entry_X')

        # Add the Entry Box for Y
        self.entry_Y = ttk.Entry(window, 
                            validate="key", 
                            validatecommand=vcmd, 
                            style="Custom.TEntry",
                            justify='center',
                            width = 10
                            )
        self.entry_Y.insert(0, str(int(self.image_full.height)))
        self.entry_Y.place(anchor = 'n', relx = 0.86, rely = 0.2)
        self.entry_Y.config(state='disabled')
        self.loc_att_list.append('self.entry_Y')

        # Add the Entry Box for Scale
        self.entry_S = ttk.Entry(window, 
                            validate="key", 
                            validatecommand=vcmd, 
                            style="Custom.TEntry",
                            justify='center',
                            width = 10
                            )
        self.entry_S.insert(0, "1")
        self.entry_S.place(anchor = 'n', relx = 0.94, rely = 0.2)
        self.loc_att_list.append('self.entry_S')

        # Create Scale Button
        self.btn_scale = ttk.Button(window, 
                                text = "Scale", 
                                command = lambda: scale_img(self), 
                                style = 'Modern2.TButton',
                                width = 10)
        self.btn_scale.place(anchor = 'n', relx = 0.86, rely = 0.3)
        self.loc_att_list.append('self.btn_scale')

        # Create a ttk.Checkbutton widget (used as the toggle)
        self.var = tk.IntVar()
        self.checkbutton = ttk.Checkbutton(
                                    window, 
                                    text="Scale All Images", 
                                    variable=self.var,
                                    style="TCheckbutton"
                                    )
        self.checkbutton.place(anchor = 'n', relx = 0.86, rely = 0.37)
        self.loc_att_list.append('self.checkbutton')

    # Function to continue to next page
    def next_page():
        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 3

        # Load the page
        self.load_page()

    # Function to go back to previous page
    def back_page():
        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 1

        # Load the page
        self.load_page()

    # Funtion for Help Window
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
                                text=' Resize Images',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the Instructions
        instructions = ("The Resize Images page allows users to scale the images for segmentation. " + 
                        "MicroNet performs best when the maximum pixel size for an image is between "+
                        "1000 and 2000 pixels. \n\n Button Functions:")

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
                     f'Continue to the Crop Images page']

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
                        "display the image on screen. The X and Y dimensions in pixels are " +
                        "shown to the right of the image.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','sel_image_scale.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Edit the scale using the entry box to the right of the dimensions." +
                        " To edit just the selected image, uncheck the 'Scale All Images' box." +
                        " To scale all images in the project file, check the 'Scale All Images' box." +
                        " Press the 'Scale' button to scale the image(s)")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','scale.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

    # Create Page Title
    self.label_title = ttk.Label(
                                window,
                                text='Resize Images',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(anchor = 'center', relx = 0.5, rely = 0.125)
    self.att_list.append('self.label_title')
    
    # Create button to load an image
    self.load_btn = ttk.Button(
                                window, 
                                text = "Load Image", 
                                command = lambda:load_image(self), 
                                style = 'Modern2.TButton',
                                width = 10
                                )
    self.load_btn.place(anchor = 'n', relx = 0.15, rely = 0.775)
    self.att_list.append('self.load_btn')

    # Create scrollbar for list of images
    self.scrollbar_01= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_01.place(anchor='n', relx = 0.25, rely = 0.2, height = 452)
    self.att_list.append('self.scrollbar_01')
    
    # Get list of all images
    all_images = list(self.Segment['Files']['Resized Images'].keys())
    all_images.sort()

    # Create the list box of images
    items = tk.StringVar(value=all_images)
    self.listbox_01 = tk.Listbox(
                                window, 
                                listvariable=items,
                                selectmode='single',
                                height = 28,
                                width = 48,
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd']
                                )
    self.listbox_01.place(anchor='n', relx = 0.15, rely = 0.2)
    self.att_list.append('self.listbox_01')
    self.listbox_01.config(yscrollcommand= self.scrollbar_01.set)

    # Configure the scrollbar for list of all images
    self.scrollbar_01.config(command= self.listbox_01.yview)

    # Create Continue Button
    self.btn_cont1 = ttk.Button(
                               window, 
                               text = "Continue", 
                               command = next_page, 
                               style = 'Modern2.TButton',
                               width = 10
                               )
    self.btn_cont1.place(anchor = 'e', relx = 0.999, rely = 0.965)
    self.att_list.append('self.btn_cont1')
    
    # Create Back Button
    self.btn_back1 = ttk.Button(
                               window, 
                               text = "Back", 
                               command = back_page, 
                               style = 'Modern2.TButton',
                               width = 10
                               )
    self.btn_back1.place(anchor = 'e', relx = 0.915, rely = 0.965)
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
    self.btn_help.place(anchor = 'w', relx = 0.001, rely = 0.965)
    self.att_list.append('self.btn_help')