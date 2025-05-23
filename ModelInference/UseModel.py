#-----------------------------------------------------------------------------------------
#
#   UseModel.py
#
#   PURPOSE: Use a trained MicroNet Model to segment an image.
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
    import threading
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
    ClrsF = {
            0:(0, 0, 255, 255),
            1:(255, 0, 0, 255),
            2:(0, 255, 0, 255),
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
    def load_model(self, tag):

        if tag == 'New':
            # Preallocate file path
            file_path = ''

            # Ask for the file name
            file_path = filedialog.askopenfilename(
                title="Open an image",
                filetypes=(("MicroNet Model", "*.tar"),)
            )
        else:
            file_path = self.mod_path

        # Get model
        if ".tar" in file_path:
            # Save model path
            self.mod_path = file_path

            # Destory old title and label
            if hasattr(self,"mod_title"):
                self.mod_title.destroy()
                self.mod_label.destroy()
                self.class_label.destroy()
                self.entry_C.destroy()

            # Create model title
            self.mod_title = ttk.Label(
                                    window, 
                                    text="Model Name:", 
                                    style = "Modern2.TLabel",
                                    anchor = 'w'
                                    )
            self.mod_title.place(
                                anchor = 'n', 
                                relx = self.Placement['UseMod']['LabelMT'][0], 
                                rely = self.Placement['UseMod']['LabelMT'][1]
                                )
            self.att_list.append('self.mod_title')

            # Create model label
            self.mod_label = ttk.Label(
                                    window, 
                                    text= os.path.basename(self.mod_path), 
                                    style = "Modern2.TLabel",
                                    anchor = 'w'
                                    )
            self.mod_label.place(
                                anchor = 'n', 
                                relx = self.Placement['UseMod']['LabelM'][0], 
                                rely = self.Placement['UseMod']['LabelM'][1]
                                )
            self.att_list.append('self.mod_label')

            # Create classes label
            self.class_label = ttk.Label(
                                        window, 
                                        text= 'Number of Classes:', 
                                        style = "Modern2.TLabel",
                                        anchor = 'w'
                                        )
            self.class_label.place(
                                anchor = 'n', 
                                relx = self.Placement['UseMod']['LabelC'][0], 
                                rely = self.Placement['UseMod']['LabelC'][1]
                                )
            self.att_list.append('self.class_label')

            # Register the validation function
            vcmd = (window.register(only_numbers_and_decimal), "%S", "%P")

            # Add the Entry Box for Number of Classes
            self.entry_C = ttk.Entry(
                                    window, 
                                    validate="key", 
                                    validatecommand=vcmd, 
                                    style="Custom.TEntry",
                                    justify='center',
                                    width = self.Placement['UseMod']['EntryC'][2],
                                    font = tkfont.Font(family="Segoe UI", size=14)
                                    )
            self.entry_C.insert(0, "2")
            self.entry_C.place(
                            anchor = 'n', 
                            relx = self.Placement['UseMod']['EntryC'][0], 
                            rely = self.Placement['UseMod']['EntryC'][1]
                            )
            self.att_list.append('self.entry_C')

    # Function to load an image
    def load_image(self):
        
        # Function to scale images
        def scale_img(self):

            # Get the scale
            scale = float(self.entry_S.get())

            # Scale the image
            self.image_inf = self.image_inf.resize((int(self.image_inf.width*scale), int(self.image_inf.height*scale)))

            # Delete the scale widgets
            self.label_x.destroy()
            self.label_y.destroy()
            self.label_scale.destroy()
            self.entry_X.destroy()
            self.entry_Y.destroy()
            self.entry_S.destroy()
            self.btn_scale.destroy()

            # Reload the window
            self.pass_in = True
            load_image(self)
        
        # Check if image needs to be defined
        if self.pass_in == False:

            # Preallocate file path
            file_path = ''

            # Ask for the file name
            file_path = filedialog.askopenfilename(
                title="Open an image",
                filetypes=(("PNG Files", "*.png"),
                        ("JPEG Files", "*.jpg"),
                        ("TIFF Files", "*.tiff"),)
                )
            
            # Delete existing widgets
            try:
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
                self.image_inf = Image.open(file_path).convert('RGBA')

            except:
                return

        else:
            self.pass_in = False

        # Create a Matplotlib figure
        # -- Get the image dimensions in pixels
        img_width = self.image_inf.width
        img_height = self.image_inf.height

        # -- Get the DPI
        dpi = window.winfo_fpixels('1i')  # pixels per inch

        # -- Convert max size to pixels
        max_width_px = int(self.Placement['UseMod']['Canvas1'][2] * dpi)
        max_height_px = int(self.Placement['UseMod']['Canvas1'][3] * dpi)

        # -- Get the scale
        scale = min(max_width_px / img_width, max_height_px / img_height)

        # -- Get the figure size
        new_width = int(img_width * scale)/dpi
        new_height = int(img_height * scale)/dpi

        # -- Create the figure
        self.fig_use, self.ax_use = plt.subplots(figsize=(new_width, new_height))
        self.fig_use.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_use, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(
                                width=int(self.fig_use.get_figwidth() * self.fig_use.get_dpi()),
                                height=int(self.fig_use.get_figheight() * self.fig_use.get_dpi())
                                )
        self.canvas_widget.place(
                                anchor='n', 
                                relx = self.Placement['UseMod']['Canvas1'][0], 
                                rely = self.Placement['UseMod']['Canvas1'][1]
                                )
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax_use.clear()  # Clear previous image
        self.ax_use.imshow(self.image_inf)
        self.ax_use.axis('off')  # Hide axes
        self.canvas.draw()

        # Add the Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, window)
        self.toolbar.update()
        self.toolbar.place(
                        anchor='n', 
                        relx = self.Placement['UseMod']['Toolbar1'][0], 
                        rely = self.Placement['UseMod']['Toolbar1'][1]
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
                        relx = self.Placement['UseMod']['LabelX'][0], 
                        rely = self.Placement['UseMod']['LabelX'][1]
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
                        relx = self.Placement['UseMod']['LabelY'][0], 
                        rely = self.Placement['UseMod']['LabelY'][1]
                        )
        self.loc_att_list.append('self.label_y')

        # Load an image using PIL
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
                            relx = self.Placement['UseMod']['LabelS'][0], 
                            rely = self.Placement['UseMod']['LabelS'][1]
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
                                width = self.Placement['UseMod']['EntryX'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_X.insert(0, str(int(self.image_inf.width)))
        self.entry_X.place(
                        anchor = 'n', 
                        relx = self.Placement['UseMod']['EntryX'][0], 
                        rely = self.Placement['UseMod']['EntryX'][1]
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
                                width = self.Placement['UseMod']['EntryY'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_Y.insert(0, str(int(self.image_inf.height)))
        self.entry_Y.place(
                        anchor = 'n', 
                        relx = self.Placement['UseMod']['EntryY'][0], 
                        rely = self.Placement['UseMod']['EntryY'][1]
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
                                width = self.Placement['UseMod']['EntryS'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_S.insert(0, "1")
        self.entry_S.place(
                        anchor = 'n', 
                        relx = self.Placement['UseMod']['EntryS'][0], 
                        rely = self.Placement['UseMod']['EntryS'][1]
                        )
        self.loc_att_list.append('self.entry_S')

        # Create Scale Button
        self.btn_scale = ttk.Button(
                                    window, 
                                    text = "Scale", 
                                    command = lambda: scale_img(self), 
                                    style = 'Modern2.TButton',
                                    width = self.Placement['UseMod']['ButtonS'][2]
                                    )
        self.btn_scale.place(
                            anchor = 'n', 
                            relx = self.Placement['UseMod']['ButtonS'][0], 
                            rely = self.Placement['UseMod']['ButtonS'][1]
                            )
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
        
        # Function to save the data
        def seg_img(callback):

            # Segment the image
            self.inf_pred = SegmentMicroNet(self.mod_path, self.img_inf_path, int(self.entry_C.get()))

            # Notify when done
            callback()

        # Function to display progress bar while saving
        def show_loading_window():

            # Create the window
            loading = tk.Toplevel(window)
            loading.title("Segmenting")
            loading.geometry("250x100")
            loading.resizable(False, False)
            loading.configure(bg='white')
            loading.grab_set()  

            # Function for progress bar Exit Protocol
            def on_closing_saving(self):
                # Don't allow exit while saving
                return
            
            # Create the window exit protocal
            loading.protocol("WM_DELETE_WINDOW", lambda:on_closing_saving(self))

            # Create the loading label
            ttk.Label(loading, 
                        text="Segmenting Image - Please Wait.", 
                        style = "Modern1.TLabel").pack(pady=10)

            # Create the progress bar
            pb = ttk.Progressbar(loading, mode='indeterminate',style = "Modern.Horizontal.TProgressbar")
            pb.pack(fill='x', padx=20, pady=10)
            pb.start(10)

            # Function to close window when task is completed
            def on_task_done():

                # Stop the progress bar
                pb.stop()

                # Destroy the window
                loading.destroy()

            # Begin segmentation on background thread
            threading.Thread(target=seg_img, args=(on_task_done,), daemon=True).start()

            # Wait until loading window is closed
            window.wait_window(loading)

        # Start Segmentation
        show_loading_window()
        
        # Make a copy of the image
        self.image_inf_seg = self.image_inf.copy()

        # Get the pixels
        pixels = self.image_inf_seg.load()

        # Assign Values
        for i in range(self.inf_pred.shape[0]):
            for j in range(self.inf_pred.shape[1]):
                for k in range(self.inf_pred.shape[2]):
                    if self.inf_pred[i][j][k] == True:
                        pixels[j,i] = Clrs[k]
                    else:
                        pixels[j,i] = (255,255,255,0)

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
        self.btn_load_img.destroy()
        self.btn_load_mod.destroy()
        self.btn_seg.destroy()
        self.mod_title.destroy()
        self.mod_label.destroy()
        self.class_label.destroy()
        self.entry_C.destroy()

        # Create a Matplotlib figure
        # -- Get the image dimensions in pixels
        img_width = self.combined_inf.width
        img_height = self.combined_inf.height

        # -- Get the DPI
        dpi = window.winfo_fpixels('1i')  # pixels per inch

        # -- Convert max size to pixels
        max_width_px = int(self.Placement['UseMod']['Canvas1'][2] * dpi)
        max_height_px = int(self.Placement['UseMod']['Canvas1'][3] * dpi)

        # -- Get the scale
        scale = min(max_width_px / img_width, max_height_px / img_height)

        # -- Get the figure size
        new_width = int(img_width * scale)/dpi
        new_height = int(img_height * scale)/dpi

        # -- Create the figure
        self.fig_use, self.ax_use = plt.subplots(figsize=(new_width, new_height))
        self.fig_use.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_use, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(
                                width=int(self.fig_use.get_figwidth() * self.fig_use.get_dpi()),
                                height=int(self.fig_use.get_figheight() * self.fig_use.get_dpi())
                                )
        self.canvas_widget.place(
                                anchor='n', 
                                relx = self.Placement['UseMod']['Canvas1'][0], 
                                rely = self.Placement['UseMod']['Canvas1'][1]
                                )
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax_use.clear()  # Clear previous image
        self.ax_use.imshow(self.combined_inf)
        self.ax_use.axis('off')  # Hide axes
        self.canvas.draw()

        # Create button to save image
        self.btn_save = ttk.Button(
                                window, 
                                text = "Save Image", 
                                command = lambda:save_seg(self, 'Save'), 
                                style = 'Modern.TButton',
                                width = self.Placement['UseMod']['ButtonSave'][2]
                                )
        self.btn_save.place(
                            anchor = 'n', 
                            relx = self.Placement['UseMod']['ButtonSave'][0], 
                            rely = self.Placement['UseMod']['ButtonSave'][1]
                            )
        self.loc_att_list.append('self.btn_save')

        # Create button to save image
        self.btn_disc = ttk.Button(
                                window, 
                                text = "Discard Image", 
                                command = lambda:save_seg(self, 'Discard'), 
                                style = 'Modern.TButton',
                                width = self.Placement['UseMod']['ButtonDisc'][2]
                                )
        self.btn_disc.place(
                            anchor = 'n', 
                            relx = self.Placement['UseMod']['ButtonDisc'][0], 
                            rely = self.Placement['UseMod']['ButtonDisc'][1]
                            )
        self.loc_att_list.append('self.btn_disc')

    # Function to save/discard an image
    def save_seg(self, tag):

        # Save Image
        if tag == 'Save':

            # Get save name
            file_path = ''
            file_path = filedialog.asksaveasfilename(title="Save the image")

            if file_path != '':
                if '.' not in file_path:
                    file_path = file_path + '.' + self.img_inf_path.split('.')[-1]

            # Make a copy of the image
            self.image_inf_seg = self.image_inf.copy()

            # Get the pixels
            pixels = self.image_inf_seg.load()

            # Assign Values
            for i in range(self.inf_pred.shape[0]):
                for j in range(self.inf_pred.shape[1]):
                    for k in range(self.inf_pred.shape[2]):
                        if self.inf_pred[i][j][k] == True:
                            pixels[i,j] = ClrsF[k]
                        else:
                            pixels[i,j] = (255,255,255,0)

            # Combine Images
            self.combined_inf = Image.alpha_composite(self.image_inf, self.image_inf_seg)

            # Save the image
            self.combined_inf.save(file_path)

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)

        # Reload the page
        UseModel(self, window)
        ReloadUseModel(self)

    # Function to reload the page after save/discard
    def ReloadUseModel(self):

        # Reload the model
        load_model(self,'Reload')

        # Reload the image
        self.pass_in = True
        load_image(self)

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
    def home():

        # Delete all items
        for widget in window.winfo_children():
            widget.delete("all")
                
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
    self.label_title.place(
                        anchor = 'center', 
                        relx = self.Placement['UseMod']['LabelTitle'][0], 
                        rely = self.Placement['UseMod']['LabelTitle'][1]
                        )
    self.att_list.append('self.label_title')

    # Create button to load a model
    self.btn_load_mod = ttk.Button(
                                window, 
                                text = "Load Model", 
                                command = lambda:load_model(self, 'New'), 
                                style = 'Modern.TButton',
                                width = self.Placement['UseMod']['ButtonLoadM'][2]
                                )
    self.btn_load_mod.place(
                            anchor = 'n', 
                            relx = self.Placement['UseMod']['ButtonLoadM'][0], 
                            rely = self.Placement['UseMod']['ButtonLoadM'][1]
                            )
    self.att_list.append('self.btn_load_mod')
    
    # Create button to load an image
    self.btn_load_img = ttk.Button(
                                window, 
                                text = "Load Image", 
                                command = lambda:load_image(self), 
                                style = 'Modern.TButton',
                                width = self.Placement['UseMod']['ButtonLoadI'][2]
                                )
    self.btn_load_img.place(
                            anchor = 'n', 
                            relx = self.Placement['UseMod']['ButtonLoadI'][0], 
                            rely = self.Placement['UseMod']['ButtonLoadI'][1]
                            )
    self.att_list.append('self.btn_load_img')

    # Create button to segment an image
    self.btn_seg = ttk.Button(
                            window, 
                            text = "Segment Image", 
                            command = lambda:segment_image(self), 
                            style = 'Modern.TButton',
                            width = self.Placement['UseMod']['ButtonSeg'][2]
                            )
    self.btn_seg.place(
                    anchor = 'n', 
                    relx = self.Placement['UseMod']['ButtonSeg'][0], 
                    rely = self.Placement['UseMod']['ButtonSeg'][1]
                    )
    self.att_list.append('self.btn_seg')

    # Create Continue Button
    self.btn_cont = ttk.Button(
                            window, 
                            text = "Continue", 
                            command = next_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['UseMod']['ButtonCont'][2]
                            )
    self.btn_cont.place(
                        anchor = 'e', 
                        relx = self.Placement['UseMod']['ButtonCont'][0], 
                        rely = self.Placement['UseMod']['ButtonCont'][1]
                        )
    self.att_list.append('self.btn_cont')

    # Create Home Button
    # -- Load an image using PIL
    self.image_path_home = os.path.join(os.getcwd(),'GUI','General','home.png') 
    self.image_home = Image.open(self.image_path_home)
    scale = self.Placement['UseMod']['ButtonHome'][3]
    self.image_home = self.image_home.resize((int(self.image_help.width*scale), int(self.image_help.height*scale)))

    # -- Convert the image to a Tkinter-compatible format
    self.photo_home = ImageTk.PhotoImage(self.image_home)

    # -- Create the button
    self.btn_home = ttk.Button(
                            window, 
                            text = " Home",
                            image=self.photo_home,
                            compound='left',                                 
                            command = home,
                            style = "Modern2.TButton",
                            width = self.Placement['UseMod']['ButtonHome'][2]
                            )
    self.btn_home.place(
                        anchor = 'e', 
                        relx = self.Placement['UseMod']['ButtonHome'][0], 
                        rely = self.Placement['UseMod']['ButtonHome'][1]
                        )
    self.att_list.append('self.btn_home')

    # Create Help Button
    # -- Load an image using PIL
    self.image_path_help = os.path.join(os.getcwd(),'GUI','General','help.png') 
    self.image_help = Image.open(self.image_path_help)
    scale = self.Placement['FileSelect']['Help'][3]
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
                            width = self.Placement['UseMod']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['UseMod']['Help'][0], 
                        rely = self.Placement['UseMod']['Help'][1]
                        )
    self.att_list.append('self.btn_help')