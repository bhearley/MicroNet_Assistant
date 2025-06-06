#-----------------------------------------------------------------------------------------
#
#   BuildRUCGenerator.py
#
#   PURPOSE: Build the Export Geometry page.
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def BuildRUCGenerator(self,window):
    #Import Modules
    import copy
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import os
    from PIL import Image, ImageTk
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import ttk
    import tkinter.font as tkfont
    import tksheet

    # Import Functions
    from General.DeleteWidgets import DeleteLocal
    from General.DeleteWidgets import DeletePages

    # Function to set file
    def get_file():

        # Delete Existing Items
        for widget in self.loc_att_list:
            try:
                eval(widget).destroy()
            except:
                pass
        try:
            del self.canvas
            del self.canvas2
        except:
            pass

        # Remove all canvases
        for widget in window.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        # Preallocate file path
        file_path = ''

        # Ask for the file name
        while '.png' not in file_path:
            file_path = filedialog.askopenfilename(
                title="Open an image",
                filetypes=(("Segmented Files", "*.png"),)
            )
            
            if '.png' not in file_path:
                messagebox.showinfo("Wrong Filetype", "Image File not selected. Please select a valid filetype.")

        # Open the image
        self.image_file = file_path
        self.image = Image.open(file_path)

        # Initialize Color Manager
        self.ColorManager = {}
        color_list = [
                    (0,255,0),
                    (255,0,0),
                    (0,0,255)
                    ]
        color_list_used = []
        pixels_orig = self.image.load()
        mat_ct = 0
        for i in range(self.image.width):
            for j in range(self.image.height):
                if pixels_orig[i,j] in color_list:
                    if pixels_orig[i,j] not in color_list_used:
                        mat_ct = mat_ct + 1
                        color_list_used.append(pixels_orig[i,j])
                        self.ColorManager[mat_ct] = pixels_orig[i,j]
        self.ColorManager[mat_ct + 1] = "Other"

        # Create the RUC Generator widgets
        create_ruc_generation()

    # Function to manage colors
    def color_manager():

        # Function to create the color manager table
        def create_sheet():

            # Function to Add a Row
            def add_row(self):

                # Get Keys
                keys = list(self.ColorManager.keys())

                # Add Row
                self.ColorManager[keys[-1]+1] = 'None'

                # Recreate sheet
                create_sheet()

            # Function to Delte a Row
            def del_row(self):

                # Get Selected
                currently_selected = self.color_sheet.get_currently_selected()
                key = self.color_sheet.data[currently_selected.row][0]

                # Delete Row
                del self.ColorManager[key]

                # Redraw Sheet
                create_sheet()

            # Function to Set color as "Other"
            def set_other(self):

                # Get Selected
                currently_selected = self.color_sheet.get_currently_selected()
                key = self.color_sheet.data[currently_selected.row][0]

                # Find existing other key
                key_o = None
                for dkey in self.ColorManager.keys():
                    if self.ColorManager[dkey] == 'Other':
                        key_o = dkey

                # Ask if user wants to remove previous Other
                if key_o != None:
                    if messagebox.askyesno("Quit", 'Do you want to remove "Other" from ' + str(key_o) + '?') == False:
                        return
                    self.ColorManager[key_o] = 'None'

                # Set new color to Other
                self.ColorManager[key] = 'Other'

                # Redraw Sheet
                create_sheet()

            # Function to set color with color picker
            def set_picker(self):

                # Function for color recognition on movement
                def on_mouse_move(self, event, pixels):

                    # Check if event exists
                    if event.xdata is not None and event.ydata is not None:
                        x = int(event.xdata)
                        y = int(event.ydata)

                        # Check if event is in the image
                        if 0 <= x < self.image.width and 0 <= y < self.image.height:

                            # Set the color
                            r, g, b = pixels[x, y]
                            hex_color = f"#{r:02x}{g:02x}{b:02x}"
                            self.label_color.config(bg=hex_color)
                            self.label_color_RGB.config(text = str(r) +', '+ str(g) +', '+ str(b))
                
                
                # Function for color selection on click
                def on_mouse_click(self, event, pixels):

                    # Initialize flag
                    cont_flag = 0

                    # Check for left moust click
                    if event.button == 1:
                        cont_flag = 1

                        # Check if event is in the axes
                        if event.xdata is not None and event.ydata is not None:
                            x = int(event.xdata)
                            y = int(event.ydata)

                            # Check if event is in the image
                            if 0 <= x < self.image.width and 0 <= y < self.image.height:

                                # Get Color
                                r, g, b = pixels[x, y]

                            # Get Selected
                            currently_selected = self.color_sheet.get_currently_selected()
                            key = self.color_sheet.data[currently_selected.row][0]

                            # Set Color Manager
                            self.ColorManager[key] = (r,g,b)

                    # Right Click to cancel
                    elif event.button == 3:
                         cont_flag = 1

                    # Update sheet
                    if cont_flag == 1:
                        # Unbind Buttons
                        self.canvas.mpl_disconnect(self.mot)
                        self.canvas.mpl_disconnect(self.clk)

                        # Delete Color Widgets
                        self.label_color.destroy()
                        self.label_color_RGB.destroy()

                        # Redraw the table
                        create_sheet()

                # Create the color selection label
                self.label_color = tk.Label(
                                            window,
                                            text = '',
                                            width = self.Placement['RUC']['LabelCol'][2]
                                            )
                self.label_color.place(
                                    anchor = 'n', 
                                    relx = self.Placement['RUC']['LabelCol'][0], 
                                    rely = self.Placement['RUC']['LabelCol'][1]
                                    )
                self.label_color_RGB = tk.Label(
                                                window,
                                                text = '',
                                                width = self.Placement['RUC']['LabelCol2'][2],
                                                font = ('Segoe UI',12,"normal"),
                                                bg = 'white'
                                                )
                self.label_color_RGB.place(
                                        anchor = 'n', 
                                        relx = self.Placement['RUC']['LabelCol2'][0], 
                                        rely = self.Placement['RUC']['LabelCol2'][1]
                                        )

                # Load Pixels
                pixels = self.image.load()

                # Bind the canvas button press
                self.mot = self.canvas.mpl_connect("motion_notify_event", lambda event: on_mouse_move(self, event, pixels))
                self.clk = self.canvas.mpl_connect("button_press_event", lambda event: on_mouse_click(self, event, pixels))

            # Function to renumber materials
            def renumber(self):

                # Get Current Keys
                keys = list(self.ColorManager.keys())
                
                # Get New Keys
                new_keys = []
                for i in range(len(keys)):
                    new_keys.append(i+1)

                # Create Copy of the Color Manager
                ClrMngCopy = {}
                for i in range(len(keys)):
                    ClrMngCopy[new_keys[i]] = self.ColorManager[keys[i]]
                self.ColorManager = copy.deepcopy(ClrMngCopy)
                    
                # Redraw the sheet
                create_sheet()

            # Destory previous sheet
            if hasattr(self,"color_sheet"):
                self.color_sheet.destroy()

            # Set Columns
            Cols = ['Material', 'Color']

            # Set rows
            rows = []
            for key in self.ColorManager.keys():
                rows.append([key])

            # Create sheet
            self.color_sheet = tksheet.Sheet(
                                            window, 
                                            total_rows = len(rows), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            width = self.Placement['RUC']['SheetCol'][2], 
                                            height = self.Placement['RUC']['SheetCol'][3], 
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ('Segoe UI',12,"normal"),
                                            header_font = ('Segoe UI',12,"bold")
                                            )
            self.color_sheet.place(
                                anchor = 'n', 
                                relx = self.Placement['RUC']['SheetCol'][0], 
                                rely = self.Placement['RUC']['SheetCol'][1]
                                )
            self.loc_att_list.append('self.color_sheet')

            # Format sheet
            self.color_sheet.set_index_width(0)
            self.color_sheet.column_width(column = 0, width = self.Placement['RUC']['SheetCol'][4], redraw = True)
            self.color_sheet.column_width(column = 1, width = self.Placement['RUC']['SheetCol'][5], redraw = True)
            self.color_sheet.table_align(align = 'c',redraw=True)

            # Function for RGB to Hexcode conversion
            def rgb_to_hex(r, g, b):
                return f"#{r:02x}{g:02x}{b:02x}"
            
            # Set values
            for i in range(len(rows)):
                self.color_sheet.create_dropdown(r=i, c = 0,values=list(self.ColorManager.keys()))
                self.color_sheet.set_cell_data(i,0,rows[i][0])
                if self.ColorManager[rows[i][0]] != 'None':
                    if self.ColorManager[rows[i][0]] != 'Other':
                        color = (self.ColorManager[rows[i][0]][0],self.ColorManager[rows[i][0]][1],self.ColorManager[rows[i][0]][2])
                        hex_color = rgb_to_hex(*color)
                        self.color_sheet.highlight_cells(i, 1, bg=hex_color, fg='black')
                    else:
                        self.color_sheet.set_cell_data(i,1,'Other')
                else:
                    self.color_sheet.set_cell_data(i,1,'None')
            self.color_sheet.redraw()

            # Enable Bindings
            self.color_sheet.enable_bindings('single_select','cell_select', 'column_select', "arrowkeys", "right_click_popup_menu")
            self.color_sheet.popup_menu_add_command('Add Color', lambda : add_row(self), table_menu = True, index_menu = True, header_menu = True)
            self.color_sheet.popup_menu_add_command('Delete Color', lambda : del_row(self), table_menu = True, index_menu = True, header_menu = True)
            self.color_sheet.popup_menu_add_command('Set As "Other"', lambda : set_other(self), table_menu = True, index_menu = True, header_menu = True)
            self.color_sheet.popup_menu_add_command('Set with Picker', lambda : set_picker(self), table_menu = True, index_menu = True, header_menu = True)
            self.color_sheet.popup_menu_add_command('Renumber Materials', lambda : renumber(self), table_menu = True, index_menu = True, header_menu = True)

        # Create the sheet
        create_sheet()
        
    # Function for Validation for Entry
    def only_numbers(char):

        # Check if the character is a digit or a decimal point
        return char.isdigit()

    # Function to create RUC Generator widgets
    def create_ruc_generation():

        # Function to create RUC
        def create_ruc():

            # Function for popup menu
            def menu_action(key, x, y):
                # Disconnect event
                if hasattr(self, 'cid'):
                    self.canvas2.mpl_disconnect(self.cid)
                    del self.cid

                # Load the pixel data
                pixels = self.ruc_image.load()

                # Assign new color
                if self.ColorManager[key] != "Other":
                    pixels[x,y] = self.ColorManager[key]
                else:
                    pixels[x,y] = (255,255,255,255)

                # Get the limits
                self.xlim = self.ax_ruc.get_xlim()
                self.ylim = self.ax_ruc.get_ylim()

                # Redraw the canvas
                redraw_ruc()
            
            # Function for mouse click event
            def mouse_click(self, event):

                # Check if zoom is on
                if self.toolbar.mode == 'zoom rect':
                    return  
                
                # Check for right click
                if event.button == 3:

                    # Check if event exists
                    if event.xdata is not None and event.ydata is not None:
                        x = int(round(event.xdata))
                        y = int(round(event.ydata))

                        # Check if event is in the image
                        if 0 <= x < self.ruc_image.width and 0 <= y < self.ruc_image.height:
                            
                            # Create the option menu
                            self.popup_menu = tk.Menu(window, tearoff=0)
                            for key in self.ColorManager.keys():
                                if self.ColorManager[key] != 'None':
                                    self.popup_menu.add_command(label="Material " + str(key), command=lambda k=key: menu_action(k, x, y))
                            self.popup_menu.tk_popup(event.guiEvent.x_root, event.guiEvent.y_root)
                    else:
                        return

            # Function to redraw the RUC
            def redraw_ruc():

                # Delete old canvas
                try:
                    self.toolbar.destory()
                    self.canvas_widget2.destroy()
                    del self.canvas2
                except:
                    pass
                
                # Create the Matplotlib Figure
                # -- Get the image dimensions in pixels
                img_width = self.image.width
                img_height = self.image.height

                # -- Get the DPI
                dpi = window.winfo_fpixels('1i')  # pixels per inch

                # -- Convert max size to pixels
                max_width_px = int(self.Placement['RUC']['Canvas2'][2] * dpi)
                max_height_px = int(self.Placement['RUC']['Canvas2'][3] * dpi)

                # -- Get the scale
                scale = min(max_width_px / img_width, max_height_px / img_height)

                # -- Get the figure size
                new_width = int(img_width * scale)/dpi
                new_height = int(img_height * scale)/dpi

                # -- Create the figure
                if hasattr(self,"fig_ruc") == False:
                    self.fig_ruc, self.ax_ruc = plt.subplots(figsize=(new_width, new_height))
                    self.fig_ruc.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

                # Embed the Matplotlib figure in Tkinter
                self.canvas2 = FigureCanvasTkAgg(self.fig_ruc, master=window)
                self.canvas_widget2 = self.canvas2.get_tk_widget()
                self.canvas_widget2.config(width=int(self.fig_segim.get_figheight() * self.image.width/self.image.height  * self.fig_segim.get_dpi()),
                                        height=int(self.fig_segim.get_figheight() * self.fig_segim.get_dpi()))
                self.canvas_widget2.place(
                                            anchor='n', 
                                            relx = self.Placement['RUC']['Canvas2'][0], 
                                            rely = self.Placement['RUC']['Canvas2'][1]
                                            )
                self.loc_att_list.append('self.canvas2')
                self.loc_att_list.append('self.canvas_widget2')

                # Display the image
                self.ax_ruc.clear()  # Clear previous image
                self.ax_ruc.imshow(self.ruc_image, aspect=self.ruc_image.width/self.ruc_image.height)
                self.ax_ruc.set_aspect('auto')

                # Create toolbar
                if hasattr(self,"toolbar"):
                    self.toolbar.destroy()
                self.toolbar = NavigationToolbar2Tk(self.canvas2, window)
                self.toolbar.update()
                self.toolbar.push_current()
                self.toolbar.place(
                                anchor='n', 
                                relx = self.Placement['RUC']['Toolbar2'][0], 
                                rely = self.Placement['RUC']['Toolbar2'][1]
                                )
                self.loc_att_list.append('self.toolbar')
                
                # Draw borders (grid lines)
                # -- Vertical lines
                for x in range(self.xsub + 1):
                    self.ax_ruc.axvline(x - 0.5, color='black', linewidth=0.1)

                # -- Horizontal lines
                for y in range(self.ysub + 1):
                    self.ax_ruc.axhline(y - 0.5, color='black', linewidth=0.1)
                self.canvas2.draw()

                # Draw the canvas
                self.ax_ruc.axis('off')  # Hide axes

                # Set the axes limits
                if self.xlim is not None:
                    self.ax_ruc.set_xlim(self.xlim)
                    self.ax_ruc.set_ylim(self.ylim)
                self.canvas2.draw()

                # Bind Mouse Click Event
                if hasattr(self,'cid') == False:
                    self.cid = self.canvas2.mpl_connect("button_press_event", lambda event: mouse_click(self, event))
                self.clicked = 0

            # Resize Image
            self.image_copy = self.image.resize((int(self.xsub), int(self.ysub)))

            # Create an empty image
            self.ruc_image= Image.new("RGBA", (self.image_copy.width, self.image_copy.height), color="white")

            # Get Pixels of old and new image
            pixels_orig = self.image_copy.load()
            pixels = self.ruc_image.load()

            # Get Color List
            Color_List = []
            for key in self.ColorManager.keys():
                if self.ColorManager[key] != 'Other':
                    Color_List.append(self.ColorManager[key])

            # Assign Colors
            for i in range(self.image_copy.width):
                for j in range(self.image_copy.height):
                    if pixels_orig[i,j] in Color_List:
                        pixels[i,j] = pixels_orig[i,j] 

            # Draw the RUC
            self.xlim = None
            self.ylim = None
            redraw_ruc()
                    
        # Function to create X Slider
        def create_x_slider(event):

            # Delete old slider
            if hasattr(self, "sliderx"):
                self.sliderx.destroy()

            # Get new lower bound
            if int(self.entry_XL.get()) > 0 and int(self.entry_XL.get()) < int(self.xboundU):
                self.xboundL = self.entry_XL.get()

            # Get new upper bound
            if int(self.entry_XU.get()) > int(self.xboundL) and int(self.entry_XU.get()) <= self.image.width:
                self.xboundU = self.entry_XU.get()

            # Set Bounds
            self.entry_XL.delete(0, 'end')  
            self.entry_XL.insert(0, self.xboundL)  
            self.entry_XU.delete(0, 'end')  
            self.entry_XU.insert(0, self.xboundU)

            # Create the slider
            self.sliderx = ttk.Scale(
                                    window,
                                    from_=self.xboundL,
                                    to=self.xboundU,
                                    orient='horizontal',  
                                    length=self.Placement['RUC']['SliderX'][2],
                                    style="Modern.Horizontal.TScale",
                                    command = change_x_slider
                                    )
            self.sliderx.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['SliderX'][0], 
                            rely = self.Placement['RUC']['SliderX'][1]
                            )
            self.loc_att_list.append('self.sliderx')
            self.sliderx.bind("<ButtonRelease-1>", on_slider_release)

            # Initialize Slider
            if int(self.xboundL) <= int(self.xsub) < int(self.xboundU):
                self.sliderx.set(self.xsub)
            else:
                self.sliderx.set(self.xboundL)

            # Generate ruc
            create_ruc()

        # Function to create Y Slider
        def create_y_slider(event):

            # Delete old slider
            if hasattr(self, "slidery"):
                self.slidery.destroy()

            # Get new lower bound
            if int(self.entry_YL.get()) > 0 and int(self.entry_YL.get()) < int(self.yboundU):
                self.yboundL = self.entry_YL.get()

            # Get new upper bound
            if int(self.entry_YU.get()) > int(self.yboundL) and int(self.entry_YU.get()) <= self.image.height:
                self.yboundU = self.entry_YU.get()

            # Set Bounds
            self.entry_YL.delete(0, 'end')  
            self.entry_YL.insert(0, self.yboundL)  
            self.entry_YU.delete(0, 'end')  
            self.entry_YU.insert(0, self.yboundU)

            # Create the slider
            self.slidery = ttk.Scale(
                                    window,
                                    from_=self.yboundL,
                                    to=self.yboundU,
                                    orient='horizontal',  
                                    length=self.Placement['RUC']['SliderY'][2],
                                    style="Modern.Horizontal.TScale",
                                    command = change_y_slider
                                    )
            self.slidery.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['SliderY'][0], 
                            rely = self.Placement['RUC']['SliderY'][1]
                            )
            self.loc_att_list.append('self.slidery')
            self.slidery.bind("<ButtonRelease-1>", on_slider_release)

            # Initialize Slider
            if int(self.yboundL) <= int(self.ysub) < int(self.yboundU):
                self.slidery.set(self.ysub)
            else:
                self.slidery.set(self.yboundL)

            # Generate ruc
            create_ruc()

        # Function for Slider Release
        def on_slider_release(event):

            # Get the x value
            self.xsub = int(self.sliderx.get())

            # Get the y value
            self.ysub = int(self.slidery.get())

            # Redraw the canvas
            create_ruc()

        # Function for x slider value change
        def change_x_slider(event):

            # Delete the previous X value
            self.entry_XV.delete(0, 'end')

            # Insert the new X value  
            self.entry_XV.insert(0, round(float(event)))

        # Function for y slider value change
        def change_y_slider(event):

            # Delete the previous Y value
            self.entry_YV.delete(0, 'end') 

            # Insert the new Y value 
            self.entry_YV.insert(0, round(float(event)))

        # Function for Updating the x slider
        def update_x_slider(event):

            # Get Value
            val = int(self.entry_XV.get())

            # Check lower bound
            if val < int(self.entry_XL.get()):
                self.xboundL = val
                self.entry_XL.delete(0, 'end')  
                self.entry_XL.insert(0, self.xboundL)

            # Check upper bound
            if val > int(self.entry_XU.get()):
                self.xboundU = val
                self.entry_XU.delete(0, 'end')  
                self.entry_XU.insert(0, self.xboundU) 

            # Set X 
            self.xsub = val

            # Create the slider
            create_x_slider(None)

        # Function for Updating the y slider
        def update_y_slider(event):

            # Get Value
            val = int(self.entry_YV.get())

            # Check lower bound
            if val < int(self.entry_YL.get()):
                self.yboundL = val
                self.entry_YL.delete(0, 'end')  
                self.entry_YL.insert(0, self.yboundL)

            # Check upper bound
            if val > int(self.entry_YU.get()):
                self.yboundU = val
                self.entry_YU.delete(0, 'end')  
                self.entry_YU.insert(0, self.yboundU) 

            # Set Y 
            self.ysub = val

            # Create the slider
            create_y_slider(None)

        # Function for Exporting data
        def export(self):

            # Function for Validation for Entry
            def only_numbers_and_decimal(char, current_value):

                # Check if the character is a digit or a decimal point
                if char.isdigit():
                    return True
                elif char == '.' and current_value.count('.') == 1:  # Allow only one decimal point
                    return True
                return False

            # Function to Export Data
            def export_data(self):

                # Check data
                pixels = self.ruc_image.load()

                # Check that all materials are defined
                color_list = []
                for key in self.ColorManager.keys():
                    color_list.append(self.ColorManager[key])

                if "Other" not in color_list:
                    for i in range(self.ruc_image.width):
                        for j in range(self.ruc_image.height):
                            if pixels[i,j] not in color_list:
                                mod_select.destroy()
                                messagebox.showerror(message = "Color " + str(pixels[i,j]) + " not defined - either add to the color table or add an 'Other' option")                         
                                return
     
                # Get the option
                if self.combo_mods.get() == 'NASMAT':
                    from RUCGenerator.NASMAT import NASMAT
                    NASMAT(self)

                # Show save message
                mod_select.destroy()
                messagebox.showinfo(message="Export File Saved!")

            # Create a window for option selection
            mod_select = tk.Toplevel(window)
            mod_select.title("Export RUC")
            mod_select.geometry("250x400")
            mod_select.resizable(False, False)
            mod_select.configure(bg='white')
            mod_select.grab_set()

            # Create a label
            ttk.Label(
                    mod_select, 
                    text="Select an Export Option:", 
                    style = "Modern1.TLabel"
                    ).place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelExp'][0], 
                            rely = self.Placement['RUC']['LabelExp'][1]
                            )
            
            # Create the selection box
            mod_opts = ['NASMAT']
            self.combo_mods = ttk.Combobox(
                                        mod_select,
                                        values=mod_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.combo_mods.place(
                                anchor='n', 
                                relx = self.Placement['RUC']['ComboExp'][0], 
                                rely = self.Placement['RUC']['ComboExp'][1]
                                )
            self.combo_mods.set(mod_opts[0]) 

            # Create label for conversion
            ttk.Label(
                    mod_select, 
                    text="Conversion from pixels to distance:", 
                    style = "Modern1.TLabel"
                    ).place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelConv'][0], 
                            rely = self.Placement['RUC']['LabelConv'][1]
                            )
            
            # Create label for X conversion
            ttk.Label(
                    mod_select, 
                    text="X:", 
                    style = "Modern1.TLabel"
                    ).place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelConvX'][0], 
                            rely = self.Placement['RUC']['LabelConvX'][1]
                            )
            
            # Register the validation function
            vcmd2 = (window.register(only_numbers_and_decimal), "%S", "%P")

            # Create X conversion entry box
            self.entry_convx = ttk.Entry(
                                        mod_select, 
                                        validate="key", 
                                        validatecommand=vcmd2, 
                                        style="Custom.TEntry",
                                        justify='center',
                                        width = self.Placement['RUC']['EntryConvX'][2],
                                        font = tkfont.Font(family="Segoe UI", size=14)
                                        )
            self.entry_convx.place(
                                anchor='n', 
                                relx = self.Placement['RUC']['EntryConvX'][0], 
                                rely = self.Placement['RUC']['EntryConvX'][1]
                                )
            self.entry_convx.insert(0, 1)

            # Create label for Y conversion
            ttk.Label(
                    mod_select, 
                    text="Y:", 
                    style = "Modern1.TLabel"
                    ).place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelConvY'][0], 
                            rely = self.Placement['RUC']['LabelConvY'][1]
                            )

            # Create Y conversion entry box
            self.entry_convy = ttk.Entry(
                                        mod_select, 
                                        validate="key", 
                                        validatecommand=vcmd2, 
                                        style="Custom.TEntry",
                                        justify='center',
                                        width = self.Placement['RUC']['EntryConvY'][2],
                                        font = tkfont.Font(family="Segoe UI", size=14)
                                        )
            self.entry_convy.place(
                                anchor='n', 
                                relx = self.Placement['RUC']['EntryConvY'][0], 
                                rely = self.Placement['RUC']['EntryConvY'][1]
                                )
            self.entry_convy.insert(0, 1)

            # Create button to write exported data
            ttk.Button(
                    mod_select, 
                    text = "Export", 
                    command = lambda:export_data(self), 
                    style = 'Modern2.TButton',
                    width = self.Placement['RUC']['ButtonExpW'][2]
                    ).place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['ButtonExpW'][0], 
                            rely = self.Placement['RUC']['ButtonExpW'][1]
                            )

        # Create the label for the segmented image
        self.label_seg = ttk.Label(
                                window,
                                text='Segmented Image',
                                style = "Modern3.TLabel"
                                )
        self.label_seg.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelSeg'][0], 
                            rely = self.Placement['RUC']['LabelSeg'][1]
                            )
        self.att_list.append('self.label_seg')

        # Create the canvas to display the image
        # -- Get the image dimensions in pixels
        img_width = self.image.width
        img_height = self.image.height

        # -- Get the DPI
        dpi = window.winfo_fpixels('1i')  # pixels per inch
        
        # -- Convert max size to pixels
        max_width_px = int(self.Placement['RUC']['Canvas1'][2] * dpi)
        max_height_px = int(self.Placement['RUC']['Canvas1'][3] * dpi)

        # -- Get the scale
        scale = min(max_width_px / img_width, max_height_px / img_height)

        # -- Get the figure size
        new_width = int(img_width * scale)/dpi
        new_height = int(img_height * scale)/dpi

        # -- Create the figure
        self.fig_segim, self.ax_segim = plt.subplots(figsize=(new_width, new_height))
        self.fig_segim.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig_segim, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(
                                width=int(self.fig_segim.get_figwidth() * self.fig_segim.get_dpi()),
                                height=int(self.fig_segim.get_figheight() * self.fig_segim.get_dpi())
                                )
        self.canvas_widget.place(
                                anchor='n', 
                                relx = self.Placement['RUC']['Canvas1'][0], 
                                rely = self.Placement['RUC']['Canvas1'][1]
                                )
        self.loc_att_list.append('self.canvas')
        self.loc_att_list.append('self.canvas_widget')

        # Display the image
        self.ax_segim.clear()  # Clear previous image
        self.ax_segim.imshow(self.image)
        self.ax_segim.axis('off')  # Hide axes
        self.canvas.draw()

        # Create the label for the RUC
        self.label_ruc = ttk.Label(
                                window,
                                text='Model',
                                style = "Modern3.TLabel"
                                )
        self.label_ruc.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelRUC'][0], 
                            rely = self.Placement['RUC']['LabelRUC'][1]
                            )
        self.att_list.append('self.label_ruc')

        # Set Default number of subcells in X and Y
        self.xsub = int(self.image.width/5)
        self.ysub = int(self.image.height/5)

        # Set initial slider bounds
        self.xboundL = int(self.image.width/10)
        self.xboundU = int(self.image.width)
        self.yboundL = int(self.image.height/10)
        self.yboundU = int(self.image.height)

        # Register the validation function
        vcmd = (window.register(only_numbers), "%S")

        # Create the label for X subcells
        self.label_xsub = ttk.Label(
                                    window,
                                    text='X Subcells',
                                    style = "Modern2.TLabel"
                                    )
        self.label_xsub.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelSubX'][0], 
                            rely = self.Placement['RUC']['LabelSubX'][1]
                            )
        self.att_list.append('self.label_xsub')

        # Create the lower X entry bound
        self.entry_XL = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['RUC']['EntryXL'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_XL.insert(0, self.xboundL) # Set defualt value
        self.entry_XL.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['EntryXL'][0], 
                            rely = self.Placement['RUC']['EntryXL'][1]
                            )
        self.loc_att_list.append('self.entry_XL')
        self.entry_XL.bind("<Return>", lambda event: create_x_slider(event))

        # Create the upper X entry bound
        self.entry_XU = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['RUC']['EntryXU'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_XU.insert(0, self.xboundU) # Set defualt value
        self.entry_XU.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['EntryXU'][0], 
                            rely = self.Placement['RUC']['EntryXU'][1]
                            )
        self.loc_att_list.append('self.entry_XU')
        self.entry_XU.bind("<Return>", lambda event: create_x_slider(event))

        # Create the X value
        self.entry_XV = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['RUC']['EntryXV'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_XV.insert(0, self.xsub) # Set defualt value
        self.entry_XV.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['EntryXV'][0], 
                            rely = self.Placement['RUC']['EntryXV'][1]
                            )
        self.loc_att_list.append('self.entry_XV')
        self.entry_XV.bind("<Return>", lambda event: update_x_slider(event))

        # Create slider for adjusting in X
        create_x_slider(None)

        # Create the label for Y subcells
        self.label_ysub = ttk.Label(
                                    window,
                                    text='Y Subcells',
                                    style = "Modern2.TLabel"
                                    )
        self.label_ysub.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['LabelSubY'][0], 
                            rely = self.Placement['RUC']['LabelSubY'][1]
                            )
        self.att_list.append('self.label_ysub')

        # Create the lower Y entry bound
        self.entry_YL = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['RUC']['EntryYL'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_YL.insert(0, self.yboundL) # Set defualt value
        self.entry_YL.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['EntryYL'][0], 
                            rely = self.Placement['RUC']['EntryYL'][1]
                            )
        self.loc_att_list.append('self.entry_YL')
        self.entry_YL.bind("<Return>", lambda event: create_y_slider(event))

        # Create the upper Y entry bound
        self.entry_YU = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['RUC']['EntryYU'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_YU.insert(0, self.xboundU) # Set defualt value
        self.entry_YU.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['EntryYU'][0], 
                            rely = self.Placement['RUC']['EntryYU'][1]
                            )
        self.loc_att_list.append('self.entry_YU')
        self.entry_YU.bind("<Return>", lambda event: create_y_slider(event))

        # Create the Y value
        self.entry_YV = ttk.Entry(
                                window, 
                                validate="key", 
                                validatecommand=vcmd, 
                                style="Custom.TEntry",
                                justify='center',
                                width = self.Placement['RUC']['EntryYV'][2],
                                font = tkfont.Font(family="Segoe UI", size=14)
                                )
        self.entry_YV.insert(0, self.xsub) # Set defualt value
        self.entry_YV.place(
                            anchor = 'n', 
                            relx = self.Placement['RUC']['EntryYV'][0], 
                            rely = self.Placement['RUC']['EntryYV'][1]
                            )
        self.loc_att_list.append('self.entry_YV')
        self.entry_YV.bind("<Return>", lambda event: update_y_slider(event))

        # Create button to remake the RUC
        self.btn_ruc = ttk.Button(
                                window, 
                                text = "Update Model", 
                                command = create_ruc, 
                                style = 'Modern3.TButton',
                                width = self.Placement['RUC']['ButtonRUC'][2]
                                )
        self.btn_ruc.place(
                        anchor = 'n', 
                        relx = self.Placement['RUC']['ButtonRUC'][0], 
                        rely = self.Placement['RUC']['ButtonRUC'][1]
                        )
        self.att_list.append('self.btn_ruc')

        # Create button to export data
        self.btn_exp = ttk.Button(
                                window, 
                                text = "Export", 
                                command = lambda:export(self), 
                                style = 'Modern3.TButton',
                                width = self.Placement['RUC']['ButtonExp'][2]
                                )
        self.btn_exp.place(
                        anchor = 'n', 
                        relx = self.Placement['RUC']['ButtonExp'][0], 
                        rely = self.Placement['RUC']['ButtonExp'][1]
                        )
        self.att_list.append('self.btn_exp')

        # Create slider for adjusting in X
        create_y_slider(None)

        # Create the color manager window
        color_manager()

        # Generate the RUC and show
        create_ruc()

    #Initialize list of attributes for each page
    self.att_list = []
    self.loc_att_list = []

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
                                text='Export Geometry',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the Instructions
        instructions = ("The Export Geometry page enables generation of geometric input files for " + 
                        "various analysis tools that captures the segmented microstructure." +
                        "\n\n Button Functions:")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Set list of buttons and functions 
        image_list = ['help_btn.png','home_btn.png','sel_file.png']
        func_list = [f'Load the Help Window', 
                     f'Return to the Main Menu',
                     f'Select a segmented file to export geometry']

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
        instructions = ("To select an image to export the geometry of, press the “Select File” and " + 
                        "choose a segmented image. Once a file is selected, the segmentation will " + 
                        "appear on the lefthand side of the window and the voxelated geometry will " + 
                        "appear on the righthand size of the window. The control panel and color " + 
                        "manager will appear on the center of the screen. \n\n" +
                        "The color manager allows editing of material assignment for the generated " + 
                        "geometric model. Right clicking on any row allows::")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Set menu options and descriptions
        menu_list = ['      \u2022 Add Color', 
                     '      \u2022 Delete Color', 
                     '      \u2022 Set as "Other"', 
                     '      \u2022 Set with Picker',  
                     '      \u2022 Renumber Materials']
        menu_desc = ['Add a color/material',
                     'Remove a color/material',
                     'Set the current material color to "Other" (background)',
                     'Use the picker tool to set the color for the material',
                     'Renumber all materials sequentially']

        # Add menu iptions and descriptions to frame
        for i in range(len(menu_list)):
            # Create a container for text + text
            row_frame = tk.Frame(frame, bg="white")

            # First text frame (left label)
            left_frame = tk.Frame(row_frame, width=150, height = 20, bg="white")
            left_frame.pack_propagate(False)
            left_label = tk.Label(left_frame, text=menu_list[i], anchor="nw", justify="left", bg="white", wraplength=250)
            left_label.pack(fill="both", expand=True)
            left_frame.pack(side="left", padx=10, pady=5)

            # Second text frame (right label)
            right_frame = tk.Frame(row_frame, width=400, bg="white")
            right_label = tk.Label(right_frame, text=menu_desc[i], anchor="nw", justify="left", bg="white", wraplength=300)
            right_label.pack(fill="both", expand=True)
            right_frame.pack(side="left", padx=10, pady=5)
    
            # Pack the row
            row_frame.pack(anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','color_mng.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Add a Material:")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern4.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=0, anchor="w")

        instructions = ("To add a material and corresponding color the model, use the “Add Color” " + 
                        "menu option to create a new row in the color manager table. The new material " + 
                        "color will default to “None”. To set the color, use either the “Set as Other” or " + 
                        "“Set with Picker” menu options.\n\n" + 
                        "“Set as Other” will assign the corresponding material number for that row to any " + 
                        "color not defined in the color manager table and will display as white in the " + 
                        "voxelated model.\n\n" + 
                        "“Set with Picker” enables setting the material color by picking from the Segmented " + 
                        "Image. Hovering over the image will display the color and corresponding RGB values. " + 
                        "Left clicking the mouse will confirm the color for the material. Right clicking will " + 
                        "cancel the color assignment. \n\n " + 
                        "Press the “Update Model” button to generate a new geometric model with the new colors.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','color_picker.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Remove a Material:")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern4.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=0, anchor="w")

        instructions = ("To remove a material and corresponding color from the model, use the " + 
                        "“Delete Color” menu option to delete a row in the color manager table. " + 
                        "Press the “Update Model” button to generate a new geometric model with " + 
                        "the new colors.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("Assigning Materials to Colors:")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern4.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=0, anchor="w")

        instructions = ("To assign a material number to a color, use the drop down menu in each row of " + 
                        "the color manager table. Material numbers are assumed to start at 1. All rows " + 
                        "can be reassigned material numbers sequentially using the “Renumber Materials” " + 
                        "menu option.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add more instructions
        instructions = ("Editing the Model Geometry:")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern4.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=0, anchor="w")

        instructions = ("The voxelated model with assigned materials/colors is generated and displayed on " + 
                        "the righthand side of the window.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','ruc_mng.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        instructions = ("To edit the dimensions of the model, us the model control panel on the center " + 
                        "of the screen. The number of voxels in X and Y can be manually entered in the " + 
                        "entry box above the corresponding slider bar or with the slider bar itself. " + 
                        "The bounds for the slider bar can also be manually adjusted using the entry " + 
                        "boxes on either side of a given slider bar.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")
        
        # Add more instructions
        instructions = ("Manually Assigning Materials:")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern4.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=0, anchor="w")

        instructions = ("Individual voxels can be manually assigned a material by rick clicking on an " + 
                        "individual voxel on the model image and selecting a material from the popup menu. " + 
                        "The toolbar below the model image can be used to zoom in on the image. Note: the " + 
                        "zoom tool must be unselected for material assignment with the popup menu.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','man_edit.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

        # Add more instructions
        instructions = ("Exporting the Model:")

        label_inst1 = ttk.Label(
                                    frame,
                                    text=instructions,
                                    style = "Modern4.TLabel",
                                    wraplength=550
                                    )
        label_inst1.pack(padx = 5, pady=0, anchor="w")

        instructions = ("To export the model, press the “Export” button, which will create the Export " + 
                        "Window. Use the drop down menu to select a configured analysis tool to export " + 
                        "the model to. Pixels can be converted to distance using the entry boxes on the " + 
                        "window for X and Y. Press “Export to generate and save the export file.")

        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Add associated image
        img_file = os.path.join(os.getcwd(),'GUI','Help','exp_ruc.png')
        img = Image.open(img_file)
        img_tk = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=img_tk, bg="white", width=img.width, height=img.height)
        image_label.image = img_tk
        image_label.pack(anchor="center")

    # Function for Home
    def home():

        # Delete all items
        for widget in window.winfo_children():
            if widget != self.panel_hdr and widget != self.panel_nasa:
                try:
                    widget.destroy()
                except:
                    pass
                try:
                    widget.delete("all")
                except:
                    pass
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 0

        # Load the page
        self.load_page()
    
    # Create Page Title
    self.label_title = ttk.Label(
                                window,
                                text='Export Geometry',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(
                        anchor = 'center', 
                        relx = self.Placement['RUC']['LabelTitle'][0], 
                        rely = self.Placement['RUC']['LabelTitle'][1]
                        )
    self.att_list.append('self.label_title')

    # Create Button to select file
    self.btn_file = ttk.Button(
                            window, 
                            text = "Select File", 
                            command = get_file, 
                            style = 'Modern2.TButton',
                            width = self.Placement['RUC']['ButtonFile'][2]
                            )
    self.btn_file.place(
                        anchor = 'n', 
                        relx = self.Placement['RUC']['ButtonFile'][0], 
                        rely = self.Placement['RUC']['ButtonFile'][1]
                        )
    self.att_list.append('self.btn_file')

    # Create Help Button
    # -- Load an image using PIL
    self.image_path_help = os.path.join(os.getcwd(),'GUI','General','help.png') 
    self.image_help = Image.open(self.image_path_help)
    scale = self.Placement['RUC']['Help'][3]
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
                            width = self.Placement['RUC']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['RUC']['Help'][0], 
                        rely = self.Placement['RUC']['Help'][1]
                        )
    self.att_list.append('self.btn_help')

    # Create Home Button
    # -- Load an image using PIL
    self.image_path_home = os.path.join(os.getcwd(),'GUI','General','home.png') 
    self.image_home = Image.open(self.image_path_home)
    scale = self.Placement['RUC']['ButtonHome'][3]
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
                            width = self.Placement['RUC']['ButtonHome'][2]
                            )
    self.btn_home.place(
                        anchor = 'e', 
                        relx = self.Placement['RUC']['ButtonHome'][0], 
                        rely = self.Placement['RUC']['ButtonHome'][1]
                        )
    self.att_list.append('self.btn_home')