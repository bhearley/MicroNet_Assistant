#-----------------------------------------------------------------------------------------
#
#   UseModel.py
#
#   PURPOSE: Use a trained MicroNet Model to segment an image
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def UseModel(self,window):
    # Import Modules
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import os
    from PIL import Image, ImageTk
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import ttk
    import tkinter.font as tkfont

    # Import Functions
    from General.DeleteWidgets import DeleteLocal
    from General.DeleteWidgets import DeletePages
    from ModelCreator.SegmentationModels.MicroNet.SegmentMicroNet import SegmentMicroNet

    #Initialize list of attributes for each page
    self.att_list = []
    self.loc_att_list = []

    # Initialize Pass
    self.pass_in = False

    # Set the color Dictionary
    Clrs = {
            0:(0, 0, 255, 128),
            1:(255, 0, 0, 128),
            2:(0, 255, 0, 128),
            }

    # Function for Validation for Entry
    def only_numbers_and_decimal(char, current_value):
        # Check if the character is a digit or a decimal point
        if char.isdigit():
            return True
        elif char == '.' and current_value.count('.') == 1:  # Allow only one decimal point
            return True
        return False

    # Function to load a model
    def load_model(self):
        # Preallocate file path
        file_path = ''

        # Ask for the file name
        while '.tar' not in file_path:
            file_path = filedialog.askopenfilename(
                title="Open an image",
                filetypes=(("MicroNet Model", "*.tar"),)
            )

        # Save model path
        self.mod_path = file_path

        # Destory old title and label
        if hasattr(self,"mod_title"):
            self.mod_title.destroy()
            self.mod_label.destroy()
            self.class_label.destroy()
            self.entry_C.destroy()

        # Create title
        self.mod_title = ttk.Label(
                        window, 
                        text="Model Name:", 
                        style = "Modern2.TLabel",
                        anchor = 'w'
                        )
        self.mod_title.place(anchor = 'n', relx = 0.125, rely = 0.3)
        self.att_list.append('self.mod_title')

        # Create label
        self.mod_label = ttk.Label(
                        window, 
                        text= os.path.basename(self.mod_path), 
                        style = "Modern2.TLabel",
                        anchor = 'w'
                        )
        self.mod_label.place(anchor = 'n', relx = 0.125, rely = 0.335)
        self.att_list.append('self.mod_label')

        # Create classes label
        self.mod_label = ttk.Label(
                        window, 
                        text= 'Number of Classes:', 
                        style = "Modern2.TLabel",
                        anchor = 'w'
                        )
        self.mod_label.place(anchor = 'n', relx = 0.125, rely = 0.45)
        self.att_list.append('self.mod_label')

        # Register the validation function
        vcmd = (window.register(only_numbers_and_decimal), "%S", "%P")

        # Add the Entry Box for Scale
        self.entry_C = ttk.Entry(window, 
                            validate="key", 
                            validatecommand=vcmd, 
                            style="Custom.TEntry",
                            justify='center',
                            width = 10,
                            font = tkfont.Font(family="Segoe UI", size=14)
                            )
        self.entry_C.insert(0, "2")
        self.entry_C.place(anchor = 'n', relx = 0.125, rely = 0.485)
        self.att_list.append('self.entry_C')

    # Function to load an image
    def load_image(self):
        
        # Function to scale images
        def scale_img(self):
            # Get the scale
            scale = float(self.entry_S.get())

            # Scale the image
            self.image_inf = self.image_inf.resize((int(self.image_inf.width*scale), 
                                                        int(self.image_inf.height*scale)))

            # Reload the window
            self.pass_in = True
            load_image(self)
        

        # Check if image needs to be defined
        if self.pass_in == False:
            # Preallocate file path
            file_path = ''

            # Ask for the file name
            while '.' not in file_path:
                file_path = filedialog.askopenfilename(
                    title="Open an image",
                    filetypes=(("PNG Files", "*.png"),
                            ("JPEG Files", "*.jpg"),
                            ("TIFF Files", "*.tiff"),)
                )
            
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

            # Load the image
            self.img_inf_path = file_path
            self.image_inf = Image.open(file_path)

        else:
            self.pass_in = False

        # Create a Matplotlib figure
        if hasattr(self,"fig4") == False:
            scale_im = 0.8
            self.fig4, self.ax4 = plt.subplots(figsize=(8/scale_im, 6/scale_im))
            self.fig4.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig4, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(width=int(self.fig4.get_figwidth() * self.fig4.get_dpi()),
                                height=int(self.fig4.get_figheight() * self.fig4.get_dpi()))
        self.canvas_widget.place(anchor='n', relx = 0.5, rely = 0.2)
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax4.clear()  # Clear previous image
        self.ax4.imshow(self.image_inf)
        self.ax4.axis('off')  # Hide axes
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
        self.x_label.place(anchor = 'n', relx = 0.755, rely = 0.4)
        self.loc_att_list.append('self.x_label')

        # Create the y label
        self.y_label = ttk.Label(
                        window, 
                        text="Y:", 
                        style = "Modern2.TLabel"
                        )
        self.y_label.place(anchor = 'n', relx = 0.8275, rely = 0.4)
        self.loc_att_list.append('self.y_label')

        #Load an image using PIL
        self.image_path_scale = os.path.join(os.getcwd(),'GUI','Resize','scale.png')
        self.image_scale = Image.open(self.image_path_scale)
        scale = 0.06
        self.image_scale = self.image_scale.resize((int(self.image_scale.width*scale), int(self.image_scale.height*scale)))

        # Convert the image to a Tkinter-compatible format
        self.photo_scale = ImageTk.PhotoImage(self.image_scale)

        # Create a ttk.Label with the image
        self.label_scale = ttk.Label(window, 
                                    image=self.photo_scale,
                                    background="white")
        self.label_scale.place(anchor = 'n', relx = 0.9025, rely = 0.4)
        self.loc_att_list.append('self.label_scale')

        # Register the validation function
        vcmd = (window.register(only_numbers_and_decimal), "%S", "%P")

        # Add the Entry Box for X
        self.entry_X = ttk.Entry(window, 
                            validate="key", 
                            validatecommand=vcmd, 
                            style="Custom.TEntry",
                            justify='center',
                            width = 10,
                            font = tkfont.Font(family="Segoe UI", size=14)
                            )
        self.entry_X.insert(0, str(int(self.image_inf.width)))
        self.entry_X.place(anchor = 'n', relx = 0.7875, rely = 0.4)
        self.entry_X.config(state='disabled')
        self.loc_att_list.append('self.entry_X')

        # Add the Entry Box for Y
        self.entry_Y = ttk.Entry(window, 
                            validate="key", 
                            validatecommand=vcmd, 
                            style="Custom.TEntry",
                            justify='center',
                            width = 10,
                            font = tkfont.Font(family="Segoe UI", size=14)
                            )
        self.entry_Y.insert(0, str(int(self.image_inf.height)))
        self.entry_Y.place(anchor = 'n', relx = 0.86, rely = 0.4)
        self.entry_Y.config(state='disabled')
        self.loc_att_list.append('self.entry_Y')

        # Add the Entry Box for Scale
        self.entry_S = ttk.Entry(window, 
                            validate="key", 
                            validatecommand=vcmd, 
                            style="Custom.TEntry",
                            justify='center',
                            width = 10,
                            font = tkfont.Font(family="Segoe UI", size=14)
                            )
        self.entry_S.insert(0, "1")
        self.entry_S.place(anchor = 'n', relx = 0.94, rely = 0.4)
        self.loc_att_list.append('self.entry_S')

        # Create Scale Button
        self.btn_scale = ttk.Button(window, 
                                text = "Scale", 
                                command = lambda: scale_img(self), 
                                style = 'Modern2.TButton',
                                width = 10)
        self.btn_scale.place(anchor = 'n', relx = 0.86, rely = 0.5)
        self.loc_att_list.append('self.btn_scale')

    # Function to segment an image
    def segment_image(self):
        # Check if both an image and a model exist
        if hasattr(self,'mod_path') == False:
            messagebox.showerror(message='No model defined!')
            return
        
        if hasattr(self,'img_inf_path') == False:
            messagebox.showerror(message='No image defined!')
            return
        
        self.inf_pred = SegmentMicroNet(self.mod_path, self.img_inf_path, int(self.entry_C.get()))

        # Make a copy of the image
        self.image_inf_seg = self.image_inf.copy()

        # Get the pixels
        pixels = self.image_inf_seg.load()

        # Assign Values
        for i in range(self.inf_pred.shape[0]):
            for j in range(self.inf_pred.shape[1]):
                for k in range(self.inf_pred.shape[2]):
                    if self.inf_pred[i][j][k] == True:
                        pixels[i,j] = Clrs[k]
                    else:
                        pixels[i,j] = (255,255,255,0)

        # Combine Images
        self.combined_inf = Image.alpha_composite(self.image_inf, self.image_inf_seg)

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

        # Create a Matplotlib figure
        if hasattr(self,"fig4") == False:
            scale_im = 0.8
            self.fig4, self.ax4 = plt.subplots(figsize=(8/scale_im, 6/scale_im))
            self.fig4.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig4, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(width=int(self.fig4.get_figwidth() * self.fig4.get_dpi()),
                                height=int(self.fig4.get_figheight() * self.fig4.get_dpi()))
        self.canvas_widget.place(anchor='n', relx = 0.5, rely = 0.2)
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax4.clear()  # Clear previous image
        self.ax4.imshow(self.combined_inf)
        self.ax4.axis('off')  # Hide axes
        self.canvas.draw()

    # Function to continue to next page
    def next_page():
        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 9

        # Load the page
        self.load_page()

    # Function to go back to previous page
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
        img = Image.open(img_file).convert('RGBA')
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

    # Create Page Title
    self.label_title = ttk.Label(
                                window,
                                text='Segment Image',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(anchor = 'center', relx = 0.5, rely = 0.125)
    self.att_list.append('self.label_title')

    # Create button to load a model
    self.load_mod_btn = ttk.Button(
                                window, 
                                text = "Load Model", 
                                command = lambda:load_model(self), 
                                style = 'Modern.TButton',
                                width = 10
                                )
    self.load_mod_btn.place(anchor = 'n', relx = 0.125, rely = 0.2)
    self.att_list.append('self.load_mod_btn')
    
    # Create button to load an image
    self.load_btn = ttk.Button(
                                window, 
                                text = "Load Image", 
                                command = lambda:load_image(self), 
                                style = 'Modern.TButton',
                                width = 10
                                )
    self.load_btn.place(anchor = 'n', relx = 0.875, rely = 0.2)
    self.att_list.append('self.load_btn')

    # Create button to segment an image
    self.load_btn = ttk.Button(
                                window, 
                                text = "Segment Image", 
                                command = lambda:segment_image(self), 
                                style = 'Modern.TButton',
                                width = 15
                                )
    self.load_btn.place(anchor = 'n', relx = 0.5, rely = 0.85)
    self.att_list.append('self.load_btn')

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