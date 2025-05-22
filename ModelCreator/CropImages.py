#-----------------------------------------------------------------------------------------
#
#   CropImages.py
#
#   PURPOSE: Crop Images and save as png
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def CropImages(self,window):
    # Import Modules
    import copy
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import matplotlib.patches as patches
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

    # Function to load an image to crop
    def load_image(self):

        # Function for Validation for Entry
        def only_numbers(char):

            # Check if the character is a digit or a decimal point
            return char.isdigit()
        
        # Function for Creating Hovering Cursor Rectangle
        def on_mouse_move(self, event):
            if self.allow_motion == True:

                # Remove previous crop area
                for patch in self.ax_crop.patches:  
                    patch.remove()

                # Don't show hover point while zooming
                if self.toolbar.mode == 'zoom rect':
                    return  

                # Ignore if outside axes
                if event.inaxes != self.ax_crop:
                    return  

                # Plot a rectangle using a patch for pixel-perfect control
                self.hover_rect = patches.Rectangle(
                                                    (int(event.xdata - self.crop_window/2), 
                                                    int(event.ydata - self.crop_window/2)), 
                                                    self.crop_window, 
                                                    self.crop_window, 
                                                    linewidth=2, 
                                                    linestyle='--',
                                                    edgecolor='red', 
                                                    facecolor='none'
                                                    )
                self.ax_crop.add_patch(self.hover_rect)
                self.canvas.draw_idle()

        # Function to Lock Hovering Cursor Rectangle
        def mouse_click(self, event):

            # Check if event is in axes
            if event.inaxes == self.ax_crop:

                # Check if full square is in the image
                if 0 <= event.xdata - self.crop_window/2 and  self.image_full.width >= event.xdata + self.crop_window/2 and 0 <= event.ydata - self.crop_window/2 and  self.image_full.height >= event.ydata + self.crop_window/2:
                    
                    # Check that zoom is off
                    if self.toolbar.mode != 'zoom rect':
    
                        # Function to Confirm Crop Window
                        def save_image(self, event):

                            # Get the box 
                            x = self.ax_crop.patches[0].get_x()
                            y = self.ax_crop.patches[0].get_y()
                            width = self.ax_crop.patches[0].get_width()
                            height = self.ax_crop.patches[0].get_height()

                            # Get the image
                            self.image_crop = copy.deepcopy(self.image_full)
                            self.image_crop = self.image_full.crop((x, y, x + width, y + height))

                            # Get List of all images in project
                            all_images = list(self.Segment['Data'].keys())
                            ct = 0
                            base_name = self.img_full_name.split('.')[0]

                            # Get the new image name
                            while base_name +'_' + str(ct) + '.png' in all_images:
                                ct = ct + 1

                            # Save new image to data structure
                            self.Segment['Data'][base_name +'_' + str(ct)+ '.png'] = {
                                                                                    'Original Image':self.image_crop,
                                                                                    'Pixel List All':set(),
                                                                                    'Predictor':None,
                                                                                    'Segmented Image':None,
                                                                                    'Segments':{}
                                                                                    }
                            
                            # Preallocate segmentations
                            for i in range(3):
                                self.Segment['Data'][base_name +'_' + str(ct)+ '.png']['Segments'][i+1] = {
                                                                                                        'Pixel List':set()
                                                                                                        }
                            # Update List Box
                            update_listbox(self)

                            # Remove the rectangle
                            for patch in self.ax_crop.patches: 
                                patch.remove()
                            self.canvas.draw_idle()

                            # Unbind Buttons
                            window.unbind("<Return>")
                            window.unbind("<Escape>")

                            # Rebind Enter for Entry
                            self.entry_C.bind("<Return>", lambda event : get_window(self, event))

                            # Enable Motion
                            self.allow_motion = True

                        # Function to discard image
                        def no_save_image(self, event):

                            # Remove the rectangle
                            for patch in self.ax_crop.patches:
                                patch.remove()
                            self.canvas.draw_idle()

                            # Unbind Buttons
                            window.unbind("<Return>")
                            window.unbind("<Escape>")

                            # Rebind Enter for Entry
                            self.entry_C.bind("<Return>", lambda event: get_window(self, event))

                            # Enable Motion
                            self.allow_motion = True

                        # Fix Rectange
                        self.allow_motion = False

                        # Change to solid lines
                        self.ax_crop.patches[0].set_linestyle('-')
                        self.canvas.draw_idle()

                        # Unbind crop window entry
                        self.entry_C.unbind("<Return>")

                        # Bind Buttons
                        window.bind("<Return>", lambda event: save_image(self, event))
                        window.bind("<Escape>", lambda event: no_save_image(self, event))

        # Function to Remove Hovering Cursor Rectangle         
        def on_mouse_leave(self, event):

            # Check if motion is allowed
            if self.allow_motion == True:
                try:
                    # Remove previous point if it exists
                    for patch in self.ax_crop.patches:  
                        patch.remove()
                except:
                    pass
                self.canvas.draw_idle()

        # Function to Set Crop Window
        def get_window(self, event):
            self.crop_window = int(self.entry_C.get())
        
        # Check if image is selected
        if len([self.listbox_orig.get(idx) for idx in self.listbox_orig.curselection()]) < 1:
            messagebox.showerror(message = 'No image selected!')
            return
        
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

        # Get the image
        self.img_full_name = [self.listbox_orig.get(idx) for idx in self.listbox_orig.curselection()][0]
        self.image_full = self.Segment['Files']['Resized Images'][self.img_full_name]

        # Create a Matplotlib figure
        # -- Get the image dimensions in pixels
        img_width = self.image_full.width
        img_height = self.image_full.height

        # -- Get the DPI
        dpi = window.winfo_fpixels('1i')  # pixels per inch
        
        # -- Convert max size to pixels
        max_width_px = int(self.Placement['Crop']['Canvas1'][2] * dpi)
        max_height_px = int(self.Placement['Crop']['Canvas1'][3] * dpi)

        # -- Get the scale
        scale = min(max_width_px / img_width, max_height_px / img_height)

        # -- Get the figure size
        new_width = int(img_width * scale)/dpi
        new_height = int(img_height * scale)/dpi

        # -- Create the figure
        self.fig_crop, self.ax_crop = plt.subplots(figsize=(new_width, new_height))
        self.fig_crop.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_crop, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(
                                width=int(self.fig_crop.get_figwidth() * self.fig_crop.get_dpi()),
                                height=int(self.fig_crop.get_figheight() * self.fig_crop.get_dpi())
                                )
        self.canvas_widget.place(
                                anchor='n', 
                                relx = self.Placement['Crop']['Canvas1'][0], 
                                rely = self.Placement['Crop']['Canvas1'][1]
                                )
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax_crop.clear()
        self.ax_crop.imshow(self.image_full)
        self.ax_crop.axis('off')
        self.canvas.draw()

        # Add the Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, window)
        self.toolbar.update()
        self.toolbar.place(
                        anchor='n', 
                        relx = self.Placement['Crop']['Toolbar1'][0], 
                        rely = self.Placement['Crop']['Toolbar1'][1]
                        )
        self.loc_att_list.append('self.toolbar')

        # Create the crop window label
        self.label_crop = ttk.Label(
                                    window, 
                                    text='Crop Window:',
                                    background="white",
                                    style = "Modern2.TLabel"
                                    )
        self.label_crop.place(
                            anchor = 'n', 
                            relx = self.Placement['Crop']['LabelCrop'][0], 
                            rely = self.Placement['Crop']['LabelCrop'][1]
                            )
        self.loc_att_list.append('self.label_crop')

        # Register the validation function
        vcmd = (window.register(only_numbers), "%S")

        # Add the Entry Box for Crop Window Size
        self.entry_C = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['Crop']['EntryCrop'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_C.insert(0, "700")
        self.entry_C.place(
                        anchor = 'n', 
                        relx = self.Placement['Crop']['EntryCrop'][0], 
                        rely = self.Placement['Crop']['EntryCrop'][1]
                        )
        self.loc_att_list.append('self.entry_C')
        self.crop_window = int(self.entry_C.get())

        # Bind Crop Window Entry
        self.entry_C.bind("<Return>", lambda event: get_window(self, event))

        # Bind Movement
        self.allow_motion = True
        self.c1 = self.canvas.mpl_connect("motion_notify_event", lambda event : on_mouse_move(self, event))
        self.c2 = self.canvas.mpl_connect("button_press_event", lambda event: mouse_click(self, event))
        self.c3 = self.canvas.mpl_connect('figure_leave_event', lambda event: on_mouse_leave(self, event))

    # Function to update cropped image listbox
    def update_listbox(self):

        # Get list of images
        crop_images = list(self.Segment['Data'].keys())

        # Update the listbox
        self.listbox_crop.delete(0, tk.END)  
        for item in crop_images:
            self.listbox_crop.insert(tk.END, item)

    # Function to view a cropped image
    def view_image(self):

        # Check for selected image
        if len([self.listbox_crop.get(idx) for idx in self.listbox_crop.curselection()]) < 1:
            messagebox.showerror(message = 'No Cropped Image Selected!')
            return

        # Unbind canvas MPL
        try:
            # Unbind buttons
            self.canvas.mpl_disconnect(self.c1)
            self.canvas.mpl_disconnect(self.c2)
            self.canvas.mpl_disconnect(self.c3)
        except:
            pass

        # Destroy the canvas
        try:
            self.toolbar.destroy()
            self.canvas_widget.destroy()
            del self.canvas
        except:
            pass

        # Get the image
        self.img_view_name = [self.listbox_crop.get(idx) for idx in self.listbox_crop.curselection()][0]
        self.image_view = self.Segment['Data'][self.img_view_name]['Original Image']

        # Create a Matplotlib figure
        # -- Get the image dimensions in pixels
        img_width = self.image_view.width
        img_height = self.image_view.height

        # -- Get the DPI
        dpi = window.winfo_fpixels('1i')  # pixels per inch
        
        # -- Convert max size to pixels
        max_width_px = int(self.Placement['Crop']['Canvas1'][2] * dpi)
        max_height_px = int(self.Placement['Crop']['Canvas1'][3] * dpi)

        # -- Get the scale
        scale = min(max_width_px / img_width, max_height_px / img_height)

        # -- Get the figure size
        new_width = int(img_width * scale)/dpi
        new_height = int(img_height * scale)/dpi

        # -- Create the figure
        self.fig_crop_v, self.ax_crop_v = plt.subplots(figsize=(new_width, new_height))
        self.fig_crop_v.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_crop_v, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(
                                width=int(self.fig_crop_v.get_figwidth() * self.fig_crop_v.get_dpi()),
                                height=int(self.fig_crop_v.get_figheight() * self.fig_crop_v.get_dpi())
                                )
        self.canvas_widget.place(
                                anchor='n', 
                                relx = self.Placement['Crop']['Canvas1'][0], 
                                rely = self.Placement['Crop']['Canvas1'][1]
                                )
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax_crop_v.clear()
        self.ax_crop_v.imshow(self.image_view)
        self.ax_crop_v.axis('off')
        self.canvas.draw()

        # Add the Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, window)
        self.toolbar.update()
        self.toolbar.place(
                        anchor='n', 
                        relx = self.Placement['Crop']['Toolbar1'][0], 
                        rely = self.Placement['Crop']['Toolbar1'][1]
                        )
        self.loc_att_list.append('self.toolbar')

        # Cover the crop window
        self.label_cover = ttk.Label(
                                    window,
                                    text = "                                                                                                    ",
                                    background='white',
                                    padding = self.Placement['Crop']['LabelCover'][2],
                                    )
        self.label_cover.place(
                            anchor = 'n', 
                            relx = self.Placement['Crop']['LabelCover'][0], 
                            rely = self.Placement['Crop']['LabelCover'][1]
                            )
        self.loc_att_list.append('self.label_cover')

    # Function to delete a cropped image
    def del_images(self):

        # Check for selected image
        if len([self.listbox_crop.get(idx) for idx in self.listbox_crop.curselection()]) < 1:
            messagebox.showerror('No Cropped Image Selected!')
            return
        
        # Get the image
        self.img_del = [self.listbox_crop.get(idx) for idx in self.listbox_crop.curselection()][0]

        # Confirm Delete
        if messagebox.askyesno("Delete Image", "Do you want to delete "+ self.img_del + "?"):
            try:
                # Try Deleting
                try:
                    del self.Segment['Data'][self.img_del]
                except:
                    pass

                # Get list of images
                crop_images = list(self.Segment['Data'].keys())

                # Update the listbox
                self.listbox_crop.delete(0, tk.END)  
                for item in crop_images:
                    self.listbox_crop.insert(tk.END, item)

                # Show message
                messagebox.showinfo(message = self.img_del + ' was successfully deleted!')
            except:
                # Show message
                messagebox.showinfo(message = self.img_del + ' was not deleted.')
                pass

    # Function to continue to next page
    def next_page():

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 4

        # Load the page
        self.load_page()

    # Function to go back to previous page
    def back_page():

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 2

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
                                text=' Crop Images',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the Instructions
        instructions = ("The Crop Images page allows cropping full images into square regions for MicroNet Training. "+
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
                        "display the image on screen.")

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
        instructions = ("Set the size of the crop window using the entry box below the image. Press 'Enter' to " +
                        "set the new window size.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','crop_window.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Hover over the image to display the crop window in red.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','crop_edit.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Press 'Enter' to lock the current crop window.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','crop_conf.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("To add the cropped image to the project, press 'Enter'. The cropped image name" + 
                        "is automatically generated and saved in the right hand list box. To discard the " + 
                        "cropped image, press 'Escape'.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("Cropped images can be viewed by selecting an image from the righ hand "+
                        "list box and pressing the 'View Image' button. Cropped images can be deleted " +
                        "by pressing the 'Delete Image' button. Only the cropped image will be deleted - the "+
                        "original image will remain in the left hand list box.")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern1.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','crop_view.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

    # Create Page Title
    self.label_title = ttk.Label(
                                window,
                                text='Crop Images',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(anchor = 'center', 
                           relx = self.Placement['Crop']['LabelTitle'][0], 
                           rely = self.Placement['Crop']['LabelTitle'][1])
    self.att_list.append('self.label_title')

    # Create scrollbar for list of all images
    self.scrollbar_orig= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_orig.place(
                            anchor='n', 
                            relx = self.Placement['Crop']['Scrollbar1'][0], 
                            rely = self.Placement['Crop']['Scrollbar1'][1], 
                            height = self.Placement['Crop']['Scrollbar1'][2]
                            )
    self.att_list.append('self.scrollbar_orig')
    
    # Get list of all images
    all_images = list(self.Segment['Files']['Resized Images'].keys())
    all_images.sort()

    # Create the list box of images
    items = tk.StringVar(value=all_images)
    self.listbox_orig = tk.Listbox(
                                window, 
                                listvariable=items,
                                selectmode='single',
                                height = self.Placement['Crop']['Listbox1'][2],
                                width = self.Placement['Crop']['Listbox1'][3],
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd']
                                )
    self.listbox_orig.place(
                            anchor='n', 
                            relx = self.Placement['Crop']['Listbox1'][0], 
                            rely = self.Placement['Crop']['Listbox1'][1]
                            )
    self.att_list.append('self.listbox_orig')
    self.listbox_orig.config(yscrollcommand= self.scrollbar_orig.set)

    # Configure the scrollbar
    self.scrollbar_orig.config(command= self.listbox_orig.yview)

    # Create the scrollbar for cropped images
    self.scrollbar_crop= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_crop.place(
                            anchor='n', 
                            relx = self.Placement['Crop']['Scrollbar2'][0], 
                            rely = self.Placement['Crop']['Scrollbar2'][1], 
                            height = self.Placement['Crop']['Scrollbar2'][2]
                            )
    self.att_list.append('self.scrollbar_crop')
    
    # Get List of cropped images
    if "Data" in self.Segment.keys():
        crop_images = list(self.Segment['Data'].keys())
    else:
        self.Segment['Data'] = {}
        crop_images = []
    crop_images.sort()

    # Create listbox for cropped images
    items2 = tk.StringVar(value=crop_images)
    self.listbox_crop = tk.Listbox(
                                window, 
                                listvariable=items2,
                                selectmode='single',
                                height = self.Placement['Crop']['Listbox2'][2],
                                width = self.Placement['Crop']['Listbox2'][3],
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd']
                                )
    self.listbox_crop.place(
                            anchor='n',
                            relx = self.Placement['Crop']['Listbox2'][0], 
                            rely = self.Placement['Crop']['Listbox2'][1]
                            )
    self.att_list.append('self.listbox_crop')
    self.listbox_crop.config(yscrollcommand= self.scrollbar_crop.set)

    # Configure the scrollbar for cropped images
    self.scrollbar_crop.config(command= self.listbox_crop.yview)

    # Create button to load an image
    self.btn_load = ttk.Button(
                            window, 
                            text = "Load Image", 
                            command = lambda:load_image(self), 
                            style = 'Modern2.TButton',
                            width = self.Placement['Crop']['ButtonLoad'][2]
                            )
    self.btn_load.place(
                        anchor = 'n', 
                        relx = self.Placement['Crop']['ButtonLoad'][0], 
                        rely = self.Placement['Crop']['ButtonLoad'][1]
                        )
    self.att_list.append('self.btn_load')

    # Create button to view a cropped image
    self.btn_view = ttk.Button(
                            window, 
                            text = "View Image", 
                            command = lambda:view_image(self), 
                            style = 'Modern2.TButton',
                            width = self.Placement['Crop']['ButtonView'][2]
                            )
    self.btn_view.place(
                        anchor = 'n',
                        relx = self.Placement['Crop']['ButtonView'][0], 
                        rely = self.Placement['Crop']['ButtonView'][1]
                        )
    self.att_list.append('self.btn_view')

    # Create button to delete a cropped image
    self.btn_del = ttk.Button(
                            window, 
                            text = "Delete Image", 
                            command = lambda:del_images(self), 
                            style = 'Modern2.TButton',
                            width = self.Placement['Crop']['ButtonDelete'][2]
                            )
    self.btn_del.place(
                    anchor = 'n',
                    relx = self.Placement['Crop']['ButtonDelete'][0], 
                    rely = self.Placement['Crop']['ButtonDelete'][1]
                    )
    self.att_list.append('self.btn_del')

    # Create Continue Button
    self.btn_cont = ttk.Button(
                            window, 
                            text = "Continue", 
                            command = next_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Crop']['ButtonCont'][2]
                            )
    self.btn_cont.place(
                        anchor = 'e', 
                        relx = self.Placement['Crop']['ButtonCont'][0], 
                        rely = self.Placement['Crop']['ButtonCont'][1]
                        )
    self.att_list.append('self.btn_cont')
    
    # Create Back Button
    self.btn_back = ttk.Button(
                            window, 
                            text = "Back", 
                            command = back_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Crop']['ButtonBack'][2]
                            )
    self.btn_back.place(
                        anchor = 'e', 
                        relx = self.Placement['Crop']['ButtonBack'][0], 
                        rely = self.Placement['Crop']['ButtonBack'][1]
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
                            width = self.Placement['Crop']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['Crop']['Help'][0], 
                        rely = self.Placement['Crop']['Help'][1]
                        )
    self.att_list.append('self.btn_help')