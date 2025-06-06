#-----------------------------------------------------------------------------------------
#
#   SegmentImages.py
#
#   PURPOSE: Manually Segment Images
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def SegmentImages(self,window):
    # Import Modules
    import glob
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.patches import Ellipse
    import numpy as np
    import os
    from PIL import Image, ImageTk
    import shutil
    import threading
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import ttk
    
    # Import Segmentation Functions
    from ModelCreator.SegmentationModels.SAM.Utility import LoadModel, SetImage, GetMask

    # Import Functions
    from General.DeleteWidgets import DeleteLocal
    from General.DeleteWidgets import DeletePages

    #Initialize list of attributes for each page
    self.att_list = []
    self.loc_att_list = []

    # Initialize flags
    self.prev_img = None
    self.pass_init = False

    # Set the color Dictionary
    Clrs = {
            1:{
                'Edit':(30, 60, 255, 128),
                'Final':(0, 0, 255, 128),
                },
            2:{
                'Edit':(255, 60, 30, 128),
                'Final':(255, 0, 0, 128),
                },
            3:{
                'Edit':(0, 255, 90, 128),
                'Final':(0, 255, 0, 128),
                },
            }
    
    # Create the Temp folder if it doesn't exist
    curr_dir = os.getcwd()
    temp_dir = os.path.join(curr_dir,'Temp')
    try:
        os.mkdir(temp_dir)
    except:
        pass

    # Save PNG of each image in Temp folder
    png_files = glob.glob(os.path.join(temp_dir, "*.png"))
    for file_path in png_files:
        os.remove(file_path)
    for key in self.Segment['Data'].keys():
        self.Segment['Data'][key]['Original Image'].save(os.path.join(temp_dir,key), format = "PNG")

    # Function to get brush for display
    def GetEllipse():

        # Get Brush Size
        self.brush_size = int(self.slider_brush.get())*2

        # Convert image pixels to data units in x/y
        xlim = self.ax_seg.get_xlim()
        ylim = self.ax_seg.get_ylim()

        # Axes size in pixels
        bbox = self.ax_seg.get_window_extent()
        ax_width_px = bbox.width
        ax_height_px = bbox.height

        xdata_per_pixel = abs(xlim[1] - xlim[0]) / ax_width_px
        ydata_per_pixel = abs(ylim[1] - ylim[0]) / ax_height_px

        # Set Radius
        self.pixel_radius_x = 2 * xdata_per_pixel
        self.pixel_radius_y = 2 * ydata_per_pixel

    # Function to load an image    
    def load_image(self):

        # Function for a mouse click event on the canvas
        def mouse_click(self, event):
            # Check if zoom is on
            if self.toolbar.mode != '':
                    return
            
            # Manaully adding/removing points is off
            if self.add_selected == False and self.rem_selected == False:

                # Check for mouse click only
                if event.button == 1 or event.button == 3:

                    # Check for event in axes
                    if event.inaxes == self.ax_seg:

                        # Get the selected point
                        x, y = int(event.xdata), int(event.ydata)

                        # Check that point is inside the image bounds
                        if 0 <= x < self.image.width and 0 <= y < self.image.height:

                            # Get Segment Anythin Mask
                            if self.seg_mod == 'Segment Anything (SAM)':

                                # Preallocate the prompts
                                if hasattr(self, "mask_in") == False:
                                    self.mask_in = []
                                    self.mask_type = []

                                # Append the new prompt
                                self.mask_in.append([x, y])
                                if event.button == 1:
                                    self.mask_type.append(1)
                                else:
                                    self.mask_type.append(0)

                                # Get the mask
                                mask, score, logit = GetMask(self.predictor, self.mask_in, self.mask_type)

                                # Initialize new image
                                self.mask_image = Image.open(self.image_path)
                                pixels = self.mask_image.load()
                                for i in range(mask.shape[0]):
                                    for j in range(mask.shape[1]):
                                        pixels[i, j] = (255, 255, 255, 0)

                                # Get pixel data
                                pixels = self.mask_image.load()

                                # Apply color to pixels in mask
                                for i in range(mask.shape[0]):
                                    for j in range(mask.shape[1]):
                                        if mask[i,j] == True:
                                            pixels[j,i] = Clrs[self.seg_num]['Edit']

                                # Composite pictures together
                                self.combined = Image.alpha_composite(self.combined_all, self.mask_image)

                                # Get the limits
                                xlim = self.ax_seg.get_xlim()
                                ylim = self.ax_seg.get_ylim()

                                # Display the image
                                self.ax_seg.clear()
                                self.ax_seg.imshow(self.combined)
                                self.ax_seg.axis('off')  # Hide axes
                                
                                # Remove Previous Selection Points
                                while len(self.ax_seg.lines) > 0:
                                    self.ax_seg.lines[len(self.ax_seg.lines)-1].remove()

                                # Plot Points
                                for i in range(len(self.mask_in)):
                                    pt = self.mask_in[i]
                                    if self.mask_type[i] == 1:
                                        color = 'go'
                                    else:
                                        color = 'ro'
                                    self.ax_seg.plot(pt[0], pt[1], color)

                                # Set the axes limits
                                self.ax_seg.set_xlim(xlim)
                                self.ax_seg.set_ylim(ylim)

                                # Redraw the canvas
                                self.canvas.draw()

                                # Bind Buttons
                                window.bind("<Return>", lambda event : save_mask(self, mask, 'save', event))
                                window.bind("<Escape>", lambda event : save_mask(self, mask, 'undo', event))

            # If manaully adding/removing points is off
            elif self.add_selected == True or self.rem_selected == True:

                # Check for left mouse click and event in axes
                if event.button == 1 and event.inaxes == self.ax_seg:

                    # Turn on drawing and save the points
                    self.drawing = True

        # Function to save or discard a mask
        def save_mask(self, mask, tag, event):

            # Check if "Enter" was pressed to save
            if tag == 'save':

                # Get pixel data
                pixels = self.mask_image_f.load()

                # Set empty image
                for i in range(self.mask_image_f.width):
                    for j in range(self.mask_image_f.height):
                        pixels[i, j] = (255, 255, 255, 0)

                # Apply new mask
                for i in range(mask.shape[0]):
                    for j in range(mask.shape[1]):
                        if mask[i,j] == True:
                            if (j,i) not in self.Segment['Data'][self.img_name]['Pixel List All']:
                                pixels[j, i] = Clrs[self.seg_num]['Final']
                                self.Segment['Data'][self.img_name]['Pixel List All'].add((j,i))
                                self.Segment['Data'][self.img_name]['Segments'][self.seg_num]['Pixel List'].add((j,i))

                # Composite pictures together
                self.combined_all = Image.alpha_composite(self.combined_all, self.mask_image_f)

            # Get the limits
            xlim = self.ax_seg.get_xlim()
            ylim = self.ax_seg.get_ylim()

            # Display the image
            self.ax_seg.clear()
            self.ax_seg.imshow(self.combined_all)
            self.ax_seg.axis('off')
            
            # Set the axes limits
            self.ax_seg.set_xlim(xlim)
            self.ax_seg.set_ylim(ylim)

            # Draw the canvas
            self.canvas.draw()

            # Reset the mask inputs
            self.mask_in = []
            self.mask_type = []

            # Unbind buttons
            window.unbind("<Return>")
            window.unbind("<Escape>")

        # Function to turn on addings points manually
        def add_pixels(self):

            # Remove Hover Point
            try:
                # Remove the brush
                for patch in self.ax_seg.patches: 
                    patch.remove()
                self.canvas.draw_idle()
            except:
                pass

            # Change Button Status
            if self.add_selected is False:
                self.add_selected = True
                self.rem_selected = True
                rem_pixels(self)
            else:
                self.add_selected = False

            # Change Button Display
            if self.add_selected:
                self.btn_add_pts.config(style="Modern5Selected.TButton")
                
            else:
                self.btn_add_pts.config(style="Modern5.TButton")
            
        # Function to turn on removing points manually
        def rem_pixels(self):

            # Remove Hover Point
            try:
                # Remove the brush
                for patch in self.ax_seg.patches: 
                    patch.remove()
                self.canvas.draw_idle()
            except:
                pass

            # Change Button Status
            if self.rem_selected is False:
                self.rem_selected = True
                self.add_selected = True
                add_pixels(self)
            else:
                self.rem_selected = False

            # Change Button Display
            if self.rem_selected:
                self.btn_rem_pts.config(style="Modern5Selected.TButton")
                
            else:
                self.btn_rem_pts.config(style="Modern5.TButton")

        # Function for changing the combobox for segmentation selection
        def change_combo(event):

            # Get the selected value
            value = self.combo_color.get()
            self.seg_num = int(value.strip(' ')[-1])

            # Change the color
            if hasattr(self,"img_color"):
                self.img_color.destroy()
            if self.seg_num == 1:
                self.img_c = os.path.join(os.getcwd(),'GUI', 'Segment', "blue.png")
            if self.seg_num == 2:
                self.img_c = os.path.join(os.getcwd(),'GUI', 'Segment', "red.png")
            if self.seg_num == 3:
                self.img_c = os.path.join(os.getcwd(),'GUI', 'Segment', "green.png")

            # Display the image
            self.img_c = Image.open(self.img_c)
            scale = self.Placement['Segment']['Image1'][2]
            self.img_c = self.img_c.resize((int(self.img_c.width*scale), int(self.img_c.height*scale)))
            self.imgtk_c = ImageTk.PhotoImage(self.img_c)
            self.img_color = tk.Label(window, image = self.imgtk_c, bg = 'white')
            self.img_color.place(
                                anchor = 'n', 
                                relx = self.Placement['Segment']['Image1'][0], 
                                rely = self.Placement['Segment']['Image1'][1]
                                )
            self.loc_att_list.append('self.img_color')

        # Create Hovering Cursor
        def on_mouse_move(self, event):

            # Check if manually adding/removing points is on
            if self.add_selected == True or self.rem_selected == True:

                # Check if drawing is disabled
                if self.drawing == False:

                    # Remove previous point if it exists
                    if hasattr(self,"hover_dot"):
                        try:
                            self.hover_dot.remove()
                        except:
                            pass

                    # Check that zoom is off
                    if self.toolbar.mode != '':
                        return  

                    # Check that point is on canvas
                    if event.inaxes != self.ax_seg:
                        try:
                            # Remove the brush
                            for patch in self.ax_seg.patches: 
                                patch.remove()
                            self.canvas.draw_idle()
                            self.canvas.draw_idle()
                        except:
                            pass
                        return  

                    # Get Brush Information
                    GetEllipse()

                    # Get the limits
                    xlim = self.ax_seg.get_xlim()
                    ylim = self.ax_seg.get_ylim()

                    # Plot a circle using a patch for pixel-perfect control
                    self.hover_dot = Ellipse((event.xdata, event.ydata),
                                        width=self.brush_size * self.pixel_radius_x, height=self.brush_size * self.pixel_radius_y,
                                        edgecolor='white', facecolor='none', linewidth=1.5)
                    self.ax_seg.add_patch(self.hover_dot)
                    self.canvas.draw_idle()

                    # Set the axes limits
                    self.ax_seg.set_xlim(xlim)
                    self.ax_seg.set_ylim(ylim)
                
                # If drawing is enabled and the event is in the axes
                else:
                    if self.drawing and event.inaxes == self.ax_seg:

                        # Draw new point
                        new_point = Ellipse(
                                        (event.xdata, event.ydata),
                                        width=self.brush_size * self.pixel_radius_x, 
                                        height=self.brush_size * self.pixel_radius_y,
                                        edgecolor='white', 
                                        facecolor='white', 
                                        linewidth=1.5
                                        )
                        self.ax_seg.add_patch(new_point)

                        # Redraw the canvas
                        self.canvas.draw_idle()

            # If manually adding/removing points is off
            else:
                try:
                    self.hover_dot.remove()
                except:
                    pass

        # Create Brush
        def on_mouse_release(self, event):

            # Check if toolbar mode is zoom
            if self.toolbar.mode == 'zoom':
                self.toolbar._zoom_mode = None
                self.toolbar.zoom()  
                self.toolbar.mode = ''
                return
            
            # Check if toolbar mode is zoom rect
            elif self.toolbar.mode == 'zoom rect':
                self.toolbar._zoom_mode = None
                self.toolbar.zoom()  
                self.toolbar.mode = ''
                return
            
            # Check if toolbar mode is pan
            elif self.toolbar.mode == 'pan':
                self.toolbar.pan()   
                return

            # Check if manually add/remove points is on
            if self.add_selected == True or self.rem_selected == True:

                # Check if drawing is on and the left mouse click is used
                if self.drawing and event.button == 1:

                    # Reset Drawing
                    self.drawing = False

                    # Get image dimensions
                    h, w = self.mask_image_f.width, self.mask_image_f.height

                    # Build grid of pixel coordinates
                    y, x = np.ogrid[:h, :w]

                    # Initialize an empty mask
                    mask = np.zeros((h, w), dtype=bool)

                    # Loop through patches
                    for patch in self.ax_seg.patches:

                        # Get Ellipse parameters
                        cx, cy = patch.center
                        width = patch.width
                        height = patch.height

                        # Set Ellipse mask
                        ellipse_mask = ((x - cx) / (width / 2))**2 + ((y - cy) / (height / 2))**2 <= 1
                        mask |= ellipse_mask

                    # Get Original Pixel Colors
                    pixels_orig = self.image.load()
                    
                    # Change the color of effected pixels
                    pixels = self.mask_image_f.load()

                    # Set empty
                    for i in range(self.mask_image_f.width):
                        for j in range(self.mask_image_f.height):
                            pixels[i, j] = (255, 255, 255, 0)

                    # Set Pixel Colors for Adding
                    if self.add_selected == True:
                        for i in range(self.mask_image_f.width):
                            for j in range(self.mask_image_f.height):
                                if mask[i,j] == True:
                                    if (j, i) not in self.Segment['Data'][self.img_name]['Pixel List All']:
                                        pixels[j,i] = Clrs[self.seg_num]['Final']
                                        self.Segment['Data'][self.img_name]['Pixel List All'].add((j,i))
                                        self.Segment['Data'][self.img_name]['Segments'][self.seg_num]['Pixel List'].add((j,i))

                    # Set Pixel Colors for Removing
                    if self.rem_selected == True:
                        for i in range(self.mask_image_f.width):
                            for j in range(self.mask_image_f.height):
                                if mask[i,j] == True:
                                    if (j, i) in self.Segment['Data'][self.img_name]['Segments'][self.seg_num]['Pixel List']:
                                        pixels[j, i] = pixels_orig[j, i]
                                        self.Segment['Data'][self.img_name]['Pixel List All'].remove((j,i))
                                        self.Segment['Data'][self.img_name]['Segments'][self.seg_num]['Pixel List'].remove((j,i))

                    # Composite pictures together
                    self.combined_all = Image.alpha_composite(self.combined_all, self.mask_image_f)

                    # Get the limits
                    xlim = self.ax_seg.get_xlim()
                    ylim = self.ax_seg.get_ylim()

                    # Display the image
                    self.ax_seg.clear()
                    self.ax_seg.imshow(self.combined_all)
                    self.ax_seg.axis('off')

                    # Reset limits
                    self.ax_seg.set_xlim(xlim)
                    self.ax_seg.set_ylim(ylim)

                    # Redraw canvas
                    self.canvas.draw()

        # Function to fro mouse leave
        def on_mouse_leave(event):
            
            # Fix zoom issue if zoom button is turned on
            if self.toolbar.mode == 'zoom':
                self.toolbar.release(event)  # Simulates releasing the mouse button
                self.toolbar.zoom()          # Turns zoom mode off

            # Remove the brush
            else:
                # Remove previous point
                try:
                    for patch in self.ax_seg.patches:  
                        patch.remove()
                except:
                    pass

                # Redraw canvas
                self.canvas.draw_idle()

        # Initialize
        if self.pass_init == False:

            # Initialize segmentation number
            self.seg_num = 1

            # Get the image
            if len([self.listbox_seg.get(idx) for idx in self.listbox_seg.curselection()])> 0:
                self.img_name = [self.listbox_seg.get(idx) for idx in self.listbox_seg.curselection()][0]
                self.image_path = os.path.join(temp_dir, self.img_name)
            else:
                return
        else:
            self.pass_init = False

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

        # Save data from previous image
        self.save_image()

        # Set variables for a new image
        if self.Segment['Data'][self.img_name]['Predictor'] is None:
            self.image = self.Segment['Data'][self.img_name]['Original Image'] 
            self.combined_all = self.image.copy()

            for key in self.Segment['Data'][self.img_name]['Segments'].keys():
                self.Segment['Data'][self.img_name]['Segmented Image'] = self.combined_all.copy()

        # Define the original and segmented image
        self.image = self.Segment['Data'][self.img_name]['Original Image'] 
        self.combined_all = self.Segment['Data'][self.img_name]['Segmented Image']

        # Set the previous image
        self.prev_img = self.img_name

        # Create a Matplotlib figure
        # -- Get the image dimensions in pixels
        img_width = self.combined_all.width
        img_height = self.combined_all.height

        # -- Get the DPI
        dpi = window.winfo_fpixels('1i')  # pixels per inch
        
        # -- Convert max size to pixels
        max_width_px = int(self.Placement['Segment']['Canvas1'][2] * dpi)
        max_height_px = int(self.Placement['Segment']['Canvas1'][3] * dpi)

        # -- Get the scale
        scale = min(max_width_px / img_width, max_height_px / img_height)

        # -- Get the figure size
        new_width = int(img_width * scale)/dpi
        new_height = int(img_height * scale)/dpi

        # -- Create the figure
        self.fig_seg, self.ax_seg = plt.subplots(figsize=(new_width, new_height))
        self.fig_seg.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_seg, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(
                                width=int(self.fig_seg.get_figwidth() * self.fig_seg.get_dpi()),
                                height=int(self.fig_seg.get_figheight() * self.fig_seg.get_dpi())
                                )
        self.canvas_widget.place(
                                anchor='n', 
                                relx = self.Placement['Segment']['Canvas1'][0], 
                                rely = self.Placement['Segment']['Canvas1'][1]
                                )
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax_seg.clear() 
        self.ax_seg.imshow(self.combined_all)
        self.ax_seg.axis('off')
        self.canvas.draw()

        # Add the Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, window)
        self.toolbar.update()
        self.toolbar.place(
                        anchor='n', 
                        relx = self.Placement['Segment']['Toolbar1'][0], 
                        rely = self.Placement['Segment']['Toolbar1'][1]
                        )
        self.loc_att_list.append('self.toolbar')

        # Replace the title (canvas covers the title)
        self.label_title.destroy()
        self.label_title = ttk.Label(
                                    window,
                                    text='Segment Images',
                                    style = "ModernT.TLabel"
                                    )
        self.label_title.place(
                            anchor = 'center', 
                            relx = self.Placement['Segment']['LabelTitle'][0], 
                            rely = self.Placement['Segment']['LabelTitle'][1]
                            )
        self.att_list.append('self.label_title')
    
        # Get the segmentation model
        self.seg_mod = self.combo_segmod.get()

        # Load Segment Anything Model (SAM)
        if self.seg_mod == 'Segment Anything (SAM)':

            # Load the SAM Model if not in project
            if self.Segment['Data'][self.img_name]['Predictor'] is None or self.Segment['Data'][self.img_name]['Predictor'] == 'Load':

                # Function to open SAM Model
                def open_file(callback, loading):

                    # Check if a predictor exists
                    if hasattr(self,'predictor') == False:

                        # Get the model path
                        model_path = ''
                        # -- Check default location
                        def_direc = os.path.join(os.getcwd(),'ModelCreator','SegmentationModels','SAM','SAM Models')
                        ask_flag = 0
                        if os.path.isdir(def_direc):
                            # Search for .pth files in the directory
                            pth_files = glob.glob(os.path.join(def_direc, "*.pth"))
                            if pth_files:
                                model_path = os.path.abspath(pth_files[0]) 
                            else:
                                ask_flag = 1
                        else:
                            ask_flag = 1

                        # -- Ask for path from user if not found
                        if ask_flag == 1:
                            while '.pth' not in model_path:
                                model_path = filedialog.askopenfilename(
                                    title="Open a SAM *PTH file",
                                    filetypes=(("PTH Files", "*.pth"),)
                                )

                                if model_path == '':
                                    # Delete the page
                                    DeleteLocal(self)
                                    DeletePages(self)

                                    # Set Predictor
                                    self.predictor = None

                                    # Destory Loading Window
                                    loading.destroy()

                                    # Break Loop
                                    break

                                else:
                                    # Create the directory
                                    try:
                                        os.mkdir(def_direc)
                                    except:
                                        pass

                                    # Copy model to default directory
                                    shutil.copy(model_path,os.path.join(def_direc,os.path.basename(model_path)))


                        # -- Load the model and set the image
                        if hasattr(self,'predictor') == False:
                            model_type = os.path.basename(model_path)[4:9]
                            sam, self.predictor = LoadModel(os.path.join(def_direc,os.path.basename(model_path)), model_type)
                        else:
                            del self.predictor
                            return

                    # Set the predictor for the image
                    try:
                        self.predictor, self.image_Sam = SetImage(self.predictor, os.path.join(temp_dir, self.img_name))
                    except:
                        self.predictor = None

                    # Notify when done
                    callback()  # Notify when

                # Function to show the progress bar
                def show_loading_window():

                    # Create loading bar window
                    loading = tk.Toplevel(window)
                    loading.title("Loading SAM")
                    loading.geometry("300x100")
                    loading.resizable(False, False)
                    loading.configure(bg='white')
                    loading.grab_set() 

                    # Function for progress bar Exit Protocol
                    def on_closing_sam(self):
                        return
                    
                    # Create the window exit protocal
                    loading.protocol("WM_DELETE_WINDOW", lambda:on_closing_sam(self))

                    # Create the loading label
                    ttk.Label(
                            loading, 
                            text="Loading SAM for the image - Please Wait.", 
                            style = "Modern1.TLabel"
                            ).pack(pady=10)

                    # Create the progress bar
                    pb = ttk.Progressbar(
                                        loading, 
                                        mode='indeterminate', 
                                        style = "Modern.Horizontal.TProgressbar"
                                        )
                    pb.pack(fill='x', padx=20, pady=10)
                    pb.start(10)

                    # Function to close window when task is completed
                    def on_task_done():

                        # Stop the progress bar
                        pb.stop()

                        # Destroy the window
                        loading.destroy()

                    # Begin save on background thread
                    threading.Thread(target=open_file, args=(on_task_done,loading), daemon=True).start()

                    # Wait until loading window is closed
                    window.wait_window(loading)

                # Start Loading Model
                show_loading_window()

            # Get SAM model if already in project
            else:
                self.predictor = self.Segment['Data'][self.img_name]['Predictor']

            # Reload the page
            if self.predictor is None:
                self.load_page()

        # Manual Segmentation
        elif self.seg_mod == 'Manual':
            self.Segment['Data'][self.img_name]['Predictor'] = 'Load'
            
        # Creat an empty masked image
        self.mask_image_f = Image.open(self.image_path)
        pixels = self.mask_image_f.load()
        for i in range(self.mask_image_f.width):
            for j in range(self.mask_image_f.height):
                pixels[i, j] = (255, 255, 255, 0)

        # Create Button to Add Points (Brush)
        icon = Image.open(os.path.join(os.getcwd(),'GUI', 'Segment', "brush_w.png"))
        icon = icon.resize((24, 24))
        icon_img = ImageTk.PhotoImage(icon)
        self.icon_img = icon_img
        self.btn_add_pts = ttk.Button(
                                    window, 
                                    text = " Brush",
                                    image=self.icon_img,
                                    compound='left',
                                    style = "Modern5.TButton",                                  
                                    command = lambda:add_pixels(self),
                                    width = self.Placement['Segment']['ButtonAdd'][2],
                                    )
        self.btn_add_pts.place(
                            anchor = 'n', 
                            relx = self.Placement['Segment']['ButtonAdd'][0], 
                            rely = self.Placement['Segment']['ButtonAdd'][1]
                            )
        self.loc_att_list.append('self.btn_add_pts')
        self.add_selected = False

        # Create Button to Erase Points
        icon2 = Image.open(os.path.join(os.getcwd(),'GUI', 'Segment', "eraser_w.png"))
        icon2 = icon2.resize((24, 24))
        icon_img2 = ImageTk.PhotoImage(icon2)
        self.icon_img2 = icon_img2
        self.btn_rem_pts = ttk.Button(
                                    window,text = " Erase",
                                    image=self.icon_img2,
                                    compound='left',
                                    style = "Modern5.TButton",
                                    command = lambda:rem_pixels(self),
                                    width = self.Placement['Segment']['ButtonRemove'][2],
                                    )
        self.btn_rem_pts.place(
                            anchor = 'n',
                            relx = self.Placement['Segment']['ButtonRemove'][0], 
                            rely = self.Placement['Segment']['ButtonRemove'][1]
                            )
        self.loc_att_list.append('self.btn_rem_pts')
        self.rem_selected = False

        # Create Brush Size Slider
        self.slider_brush = ttk.Scale(
                                    window,
                                    from_=1,
                                    to=25,
                                    orient='horizontal',  
                                    length=self.Placement['Segment']['Slider1'][2],
                                    style="Modern.Horizontal.TScale"
                                    )
        self.slider_brush.place(
                            anchor = 'n', 
                            relx = self.Placement['Segment']['Slider1'][0], 
                            rely = self.Placement['Segment']['Slider1'][1]
                            )
        self.loc_att_list.append('self.slider_brush')

        # Get Available Masks
        mask_list = []
        for i in range(len(list(self.Segment['Data'][self.img_name]['Segments'].keys()))):
            mask_list.append('Segment ' + str(list(self.Segment['Data'][self.img_name]['Segments'].keys())[i]))

        # Create the dropdown (combobox) for Segmentation Options
        self.combo_color = ttk.Combobox(
                                        window,
                                        values=mask_list,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
        self.combo_color.bind("<<ComboboxSelected>>", change_combo)
        self.combo_color.place(
                                anchor='n', 
                                relx = self.Placement['Segment']['Combo1'][0], 
                                rely = self.Placement['Segment']['Combo1'][1]
                                )
        self.combo_color.set(mask_list[0]) 
        self.loc_att_list.append('self.combo_color')

        # Create the color image
        self.img_c = Image.open(os.path.join(os.getcwd(),'GUI', 'Segment', "blue.png"))
        scale = self.Placement['Segment']['Image1'][2]
        self.img_c = self.img_c.resize((int(self.img_c.width*scale), int(self.img_c.height*scale)))
        self.imgtk_c = ImageTk.PhotoImage(self.img_c)
        self.img_color = tk.Label(
                                window, 
                                image = self.imgtk_c, 
                                bg = 'white'
                                )
        self.img_color.place(
                            anchor = 'n', 
                            relx = self.Placement['Segment']['Image1'][0], 
                            rely = self.Placement['Segment']['Image1'][1]
                            )
        self.loc_att_list.append('self.img_color')

        # Initialize Drawing
        self.drawing = False

        # Bind Canvas Events
        self.canvas.draw()
        self.canvas.mpl_connect("button_press_event", lambda event: mouse_click(self, event))
        self.canvas.mpl_connect("motion_notify_event", lambda event : on_mouse_move(self, event))
        self.canvas.mpl_connect("button_release_event", lambda event : on_mouse_release(self, event))
        self.canvas_widget.bind("<Leave>", on_mouse_leave)

    # Function to continue to next page
    def next_page():

        # Try Save
        try:
            self.save_image()
        except:
            pass

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 5

        # Load the page
        self.load_page()

    # Function to go back to previous page
    def back_page():

        # Try Save
        try:
            self.save_image()
        except:
            pass

        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 3

        # Load the page
        self.load_page()

    # Funtion for Help Window
    def helper():

        # Create the help window
        helpwindow = tk.Toplevel(window)
        helpwindow.title("Help")
        helpwindow.geometry("800x700")
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
                                text='Label Images',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the Instructions
        instructions = ("The Label Images page allows labeling of each image in the project for training." + 
                        " Images can either be manually labeled or labeled using an available built-in segmentation model." 
                        "\n\n Button Functions:")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Set list of buttons and functions 
        image_list = ['help_btn.png', 'save_btn.png', 'back_btn.png','cont_btn.png']
        func_list = [f'Load the Help Window',
                     f'Save the MicroNet Segmentation Model project', 
                     f'Return to the Crop Selection page',
                     f'Continue to the Export Images page']

        # Add buttons and functions to frame
        for i in range(len(image_list)):
            # Load the image
            img_file = os.path.join(os.getcwd(),'GUI','Help',image_list[i])
            img = tk.PhotoImage(file=img_file)

            # Create a container for image + text
            row_frame = tk.Frame(frame, bg="white")
    
            # Image holder frame (fixed width)
            image_holder = tk.Frame(row_frame, width=180, height=40, bg="white")
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
        instructions = ("Select an image from the list and choose a labeling option " + 
                        "from the drop down menu. Press “Load Image” to display the " + 
                        "image and begin labeling.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','seg_view.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("When segmenting an image, the MicroNet Assistant Tool allows 3 distinct classes to " + 
                        "be labeled for segmentation. To change the class, use the drop down menu on the " + 
                        "righthand side to select a segmentation option. The associated color will automatically be updated.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','seg_choice.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("There are currently two options available for labeling: \n" + 
                        "\u2022 Segment Anyting (SAM)\n"+
                        "\u2022 Manual")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add subtitle
        subtitle = ("Segment Anyting (SAM)")

        label_sub1 = ttk.Label(
                            frame,
                            text=subtitle,
                            style = "Modern4.TLabel",
                            wraplength=750
                            )
        label_sub1.pack(padx = 5, pady=5, anchor="w")


        # Add more instructions
        instructions = ("The Segment Anything Model (SAM) from Meta enables rapid " + 
                        "labeling of images by taking input prompts as points labeled " + 
                        "either background or foreground for each individual body in " + 
                        "the class. To segment a body using SAM, use the left mouse " + 
                        "click to add foreground input prompt points (area to label " + 
                        "as in the class). Use the right mouse click to add background " + 
                        "input prompt points (area to label as not in the class). " + 
                        "Foreground points will display in green and background points " + 
                        "will display in red. Multiple input prompts can be used for " + 
                        "each individual body. The generated mask will automatically " + 
                        "appear over the image with each prompt.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','sam_1.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("To keep the current mask in the class, press “Enter”. " + 
                        "The mask will turn a darker shade when confirmed and " + 
                        "prompt points will be removed from the image.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','sam_2.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("To discard the current mask, press “Escape”. Repeat " + 
                        "for each individual body in the image – using multiple " + 
                        "prompts for multiple bodies without individually confirming " + 
                        "each body will likely result in poor results.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add subtitle
        subtitle = ("Manual")

        label_sub1 = ttk.Label(
                            frame,
                            text=subtitle,
                            style = "Modern4.TLabel",
                            wraplength=750
                            )
        label_sub1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("Manual labeling of images is available within all of " +
                        "the segmentation options and is used to edit an " + 
                        "automatic segmentation method or label images from " + 
                        "scratch. Manual labeling is performed using the drawing " + 
                        "tools on the righthand side of the page. The “Brush” " + 
                        "button enables adding pixels to the class and the “Erase” " + 
                        "button enables removing pixels from the class. When a " + 
                        "drawing tool is active, the button will appear gray, and " + 
                        "when it is inactive it will appear orange. The size of the " + 
                        "brush/eraser can be changed using the slider bar. Pixels " + 
                        "can only be added/erased for the current class selected on " + 
                        "the righthand drop down menu. The toolbar under the image " + 
                        "can be used to zoom in and out of a region of interest.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','erase_sel.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Hovering the mouse over the image will display the brush/eraser.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','man_1.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("To add/remove points, click with the left mouse button and drag " + 
                        "over the desired area, which will appear in white.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','man_2.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Releasing the left mouse button will add/remove all pixels in the path.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=750
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','man_3.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

    # Create Page Title
    self.label_title = ttk.Label(
                                window,
                                text='Label Images',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(
                        anchor = 'center', 
                        relx = self.Placement['Segment']['LabelTitle'][0], 
                        rely = self.Placement['Segment']['LabelTitle'][1]
                        )
    self.att_list.append('self.label_title')

    # Create scrollbar for segmentation images
    self.scrollbar_seg= ttk.Scrollbar(
                                    window, 
                                    orient= 'vertical', 
                                    style = "Vertical.TScrollbar"
                                    )
    self.scrollbar_seg.place(
                            anchor='n', 
                            relx = self.Placement['Segment']['Scrollbar1'][0], 
                            rely = self.Placement['Segment']['Scrollbar1'][1], 
                            height = self.Placement['Segment']['Scrollbar1'][2]
                            )
    self.att_list.append('self.scrollbar_seg')
    
    # Get all images for segmentation
    all_images = list(self.Segment['Data'].keys())
    all_images.sort()

    # Create the list box of images
    items = tk.StringVar(value=all_images)
    self.listbox_seg = tk.Listbox(
                                window, 
                                listvariable=items,
                                selectmode='single',
                                height = self.Placement['Segment']['Listbox1'][2],
                                width = self.Placement['Segment']['Listbox1'][3],
                                bg=self.style_man['ListBox']['ListBox1']['bg'],            
                                fg=self.style_man['ListBox']['ListBox1']['fg'],            
                                font=self.style_man['ListBox']['ListBox1']['font'],    
                                selectbackground=self.style_man['ListBox']['ListBox1']['selectbackground'], 
                                selectforeground=self.style_man['ListBox']['ListBox1']['selectforeground'],  
                                highlightthickness=self.style_man['ListBox']['ListBox1']['highlightthickness'],     
                                bd=self.style_man['ListBox']['ListBox1']['bd'],
                                exportselection=0
                                )
    self.listbox_seg.place(
                        anchor='n', 
                        relx = self.Placement['Segment']['Listbox1'][0], 
                        rely = self.Placement['Segment']['Listbox1'][1]
                        )
    self.att_list.append('self.listbox_seg')
    self.listbox_seg.config(yscrollcommand= self.scrollbar_seg.set)

    # Configure the scrollbar
    self.scrollbar_seg.config(command= self.listbox_seg.yview)

    # Create combo box for segmentation option
    seg_opts = ['Segment Anything (SAM)','Manual']

    # Create the dropdown (combobox) for Segmentation Options
    self.combo_segmod = ttk.Combobox(
                                    window,
                                    values=seg_opts,
                                    style="Modern.TCombobox",
                                    state="readonly",
                                    width = self.Placement['Segment']['Combo2'][2],
                                    )
    self.combo_segmod.place(
                        anchor='n', 
                        relx = self.Placement['Segment']['Combo2'][0], 
                        rely = self.Placement['Segment']['Combo2'][1]
                        )
    self.combo_segmod.set(seg_opts[0]) 
    self.att_list.append('self.combo_segmod')


    # Create button to load an image
    self.btn_load = ttk.Button(
                               window, 
                               text = "Load Image", 
                               command = lambda:load_image(self), 
                               style = 'Modern2.TButton',
                               width = self.Placement['Segment']['ButtonLoad'][2]
                               )
    self.btn_load.place(
                        anchor = 'n', 
                        relx = self.Placement['Segment']['ButtonLoad'][0], 
                        rely = self.Placement['Segment']['ButtonLoad'][1]
                        )
    self.att_list.append('self.btn_load')

    # Create Continue Button
    self.btn_cont = ttk.Button(
                            window, 
                            text = "Continue", 
                            command = next_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Segment']['ButtonCont'][2]
                            )
    self.btn_cont.place(
                        anchor = 'e', 
                        relx = self.Placement['Segment']['ButtonCont'][0], 
                        rely = self.Placement['Segment']['ButtonCont'][1]
                        )
    self.att_list.append('self.btn_cont')
    
    # Create Back Button
    self.btn_back = ttk.Button(
                            window, 
                            text = "Back", 
                            command = back_page, 
                            style = 'Modern2.TButton',
                            width = self.Placement['Segment']['ButtonBack'][2]
                            )
    self.btn_back.place(
                        anchor = 'e', 
                        relx = self.Placement['Segment']['ButtonBack'][0], 
                        rely = self.Placement['Segment']['ButtonBack'][1]
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
                            width = self.Placement['Segment']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['Segment']['Help'][0], 
                        rely = self.Placement['Segment']['Help'][1]
                        )
    self.att_list.append('self.btn_help')