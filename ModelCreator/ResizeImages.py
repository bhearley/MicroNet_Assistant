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
    import tkinter.font as tkfont
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

        # Function for Validation of Entry - only float values
        def only_numbers_and_decimal(char, current_value):

            # Check if the character is a digit or a decimal point
            if char.isdigit():
                return True
            elif char == '.' and current_value.count('.') == 1:
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
            if len([self.listbox_load.get(idx) for idx in self.listbox_load.curselection()]) > 0:
                self.img_full_name = [self.listbox_load.get(idx) for idx in self.listbox_load.curselection()][0]
            else:
                messagebox.showerror(message = 'No image selected!')
                return
        else:
            self.pass_in = False

        # Load the image
        self.image_full = self.Segment['Files']['Resized Images'][self.img_full_name]

        # Create a Matplotlib figure
        # -- Get the image dimensions in pixels
        img_width = self.image_full.width
        img_height = self.image_full.height

        # -- Get the DPI
        dpi = window.winfo_fpixels('1i')  # pixels per inch
        
        # -- Convert max size to pixels
        max_width_px = int(self.Placement['Resize']['Canvas1'][2] * dpi)
        max_height_px = int(self.Placement['Resize']['Canvas1'][3] * dpi)

        # -- Get the scale
        scale = min(max_width_px / img_width, max_height_px / img_height)

        # -- Get the figure size
        new_width = int(img_width * scale)/dpi
        new_height = int(img_height * scale)/dpi

        # -- Create the figure
        self.fig_resize, self.ax_resize = plt.subplots(figsize=(new_width, new_height))
        self.fig_resize.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_resize, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(
                                width=int(self.fig_resize.get_figwidth() * self.fig_resize.get_dpi()),
                                height=int(self.fig_resize.get_figheight() * self.fig_resize.get_dpi())
                                )
        self.canvas_widget.place(
                                anchor='n', 
                                relx = self.Placement['Resize']['Canvas1'][0], 
                                rely = self.Placement['Resize']['Canvas1'][1]
                                )
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax_resize.clear()  
        self.ax_resize.imshow(self.image_full)
        self.ax_resize.axis('off')  
        self.canvas.draw()

        # Add the Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, window)
        self.toolbar.update()
        self.toolbar.place(
                        anchor='n', 
                        relx = self.Placement['Resize']['Toolbar1'][0], 
                        rely = self.Placement['Resize']['Toolbar1'][1]
                        )
        self.loc_att_list.append('self.toolbar')

        # Create the x label
        self.label_x = ttk.Label(
                                window, 
                                text="X:", 
                                style = "Modern2.TLabel"
                                )
        self.label_x.place(
                        anchor = 'n', 
                        relx = self.Placement['Resize']['LabelX'][0], 
                        rely = self.Placement['Resize']['LabelX'][1]
                        )
        self.loc_att_list.append('self.label_x')

        # Create the y label
        self.label_y = ttk.Label(
                                window, 
                                text="Y:", 
                                style = "Modern2.TLabel"
                                )
        self.label_y.place(
                        anchor = 'n', 
                        relx = self.Placement['Resize']['LabelY'][0], 
                        rely = self.Placement['Resize']['LabelY'][1]
                        )
        self.loc_att_list.append('self.label_y')

        # Load the scale image for the scale button
        self.image_path_scale = os.path.join(os.getcwd(),'GUI','Resize','scale.png')
        self.image_scale = Image.open(self.image_path_scale)
        scale = 0.06
        self.image_scale = self.image_scale.resize((int(self.image_scale.width*scale), int(self.image_scale.height*scale)))

        # Convert the image to a Tkinter-compatible format
        self.photo_scale = ImageTk.PhotoImage(self.image_scale)

        # Create a ttk.Label with the image
        self.label_scale = ttk.Label(
                                    window, 
                                    image=self.photo_scale,
                                    background="white"
                                    )
        self.label_scale.place(
                            anchor = 'n', 
                            relx = self.Placement['Resize']['LabelS'][0], 
                            rely = self.Placement['Resize']['LabelS'][1]
                            )
        self.loc_att_list.append('self.label_scale')

        # Register the validation function
        vcmd = (window.register(only_numbers_and_decimal), "%S", "%P")

        # Add the Entry Box for X
        self.entry_X = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['Resize']['EntryX'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_X.insert(0, str(int(self.image_full.width)))
        self.entry_X.place(
                        anchor = 'n',
                        relx = self.Placement['Resize']['EntryX'][0], 
                        rely = self.Placement['Resize']['EntryX'][1]
                        )
        self.entry_X.config(state='disabled')
        self.loc_att_list.append('self.entry_X')

        # Add the Entry Box for Y
        self.entry_Y = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['Resize']['EntryY'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_Y.insert(0, str(int(self.image_full.height)))
        self.entry_Y.place(
                        anchor = 'n', 
                        relx = self.Placement['Resize']['EntryY'][0], 
                        rely = self.Placement['Resize']['EntryY'][1]
                        )
        self.entry_Y.config(state='disabled')
        self.loc_att_list.append('self.entry_Y')

        # Add the Entry Box for Scale
        self.entry_S = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['Resize']['EntryS'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_S.insert(0, "1")
        self.entry_S.place(
                        anchor = 'n',
                        relx = self.Placement['Resize']['EntryS'][0], 
                        rely = self.Placement['Resize']['EntryS'][1]
                        )
        self.loc_att_list.append('self.entry_S')

        # Create Scale Button
        self.btn_scale = ttk.Button(
                                    window, 
                                    text = "Scale", 
                                    command = lambda: scale_img(self), 
                                    style = 'Modern2.TButton',
                                    width = self.Placement['Resize']['ButtonS'][2]
                                    )
        self.btn_scale.place(
                            anchor = 'n',
                            relx = self.Placement['Resize']['ButtonS'][0], 
                            rely = self.Placement['Resize']['ButtonS'][1]
                            )
        self.loc_att_list.append('self.btn_scale')

        # Create a ttk.Checkbutton widget (used as the toggle)
        self.var = tk.IntVar()
        self.check_scale = ttk.Checkbutton(
                                        window, 
                                        text="Scale All Images", 
                                        variable=self.var,
                                        style="TCheckbutton"
                                        )
        self.check_scale.place(
                            anchor = 'n',
                            relx = self.Placement['Resize']['Check1'][0], 
                            rely = self.Placement['Resize']['Check1'][1]
                            )
        self.loc_att_list.append('self.check_scale')

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
    self.label_title.place(
                        anchor = 'center', 
                        relx = self.Placement['Resize']['LabelTitle'][0], 
                        rely = self.Placement['Resize']['LabelTitle'][1]
                        )
    self.att_list.append('self.label_title')
    
    # Create button to load an image
    self.btn_load = ttk.Button(
                            window, 
                            text = "Load Image", 
                            command = lambda:load_image(self), 
                            style = 'Modern.TButton',
                            width = self.Placement['Resize']['ButtonLoad'][2]
                            )
    self.btn_load.place(
                        anchor = 'n', 
                        relx = self.Placement['Resize']['ButtonLoad'][0], 
                        rely = self.Placement['Resize']['ButtonLoad'][1]
                        )
    self.att_list.append('self.btn_load')

    # Create scrollbar for list of images
    self.scrollbar_load= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_load.place(
                            anchor='n', 
                            relx = self.Placement['Resize']['Scrollbar1'][0], 
                            rely = self.Placement['Resize']['Scrollbar1'][1], 
                            height = self.Placement['Resize']['Scrollbar1'][2]
                            )
    self.att_list.append('self.scrollbar_load')
    
    # Get list of all images
    all_images = list(self.Segment['Files']['Resized Images'].keys())
    all_images.sort()

    # Create the list box of images
    items = tk.StringVar(value=all_images)
    self.listbox_load = tk.Listbox(
                                window, 
                                listvariable=items,
                                selectmode='single',
                                height = self.Placement['Resize']['Listbox1'][2],
                                width = self.Placement['Resize']['Listbox1'][3],
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd']
                                )
    self.listbox_load.place(
                            anchor='n', 
                            relx = self.Placement['Resize']['Listbox1'][0], 
                            rely = self.Placement['Resize']['Listbox1'][1]
                            )
    self.att_list.append('self.listbox_load')
    self.listbox_load.config(yscrollcommand= self.scrollbar_load.set)

    # Configure the scrollbar for list of all images
    self.scrollbar_load.config(command= self.listbox_load.yview)

   # Create Continue Button
    self.btn_cont = ttk.Button(
                            window, 
                            text = "Continue", 
                            command = next_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Resize']['ButtonCont'][2]
                            )
    self.btn_cont.place(
                        anchor = 'e', 
                        relx = self.Placement['Resize']['ButtonCont'][0], 
                        rely = self.Placement['Resize']['ButtonCont'][1]
                        )
    self.att_list.append('self.btn_cont')
    
    # Create Back Button
    self.btn_back = ttk.Button(
                            window, 
                            text = "Back", 
                            command = back_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Resize']['ButtonBack'][2]
                            )
    self.btn_back.place(
                        anchor = 'e', 
                        relx = self.Placement['Resize']['ButtonBack'][0], 
                        rely = self.Placement['Resize']['ButtonBack'][1]
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
                            width = self.Placement['Resize']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['Resize']['Help'][0], 
                        rely = self.Placement['Resize']['Help'][1]
                        )
    self.att_list.append('self.btn_help')