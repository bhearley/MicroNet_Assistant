#-----------------------------------------------------------------------------------------
#
#   ReviewImages.py
#
#   PURPOSE: Review the final images and save
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def ReviewImages(self,window):
    # Import Modules
    import copy
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

    # Setup Data Structure
    if 'Final' not in self.Segment.keys():
        self.Segment['Final'] = {}

    # Initialize Output Dictionary
    self.output = {}

    # Convert Images to pure RGB
    for item in self.Segment['Data'].keys():
        if self.Segment['Data'][item]['Original Image'] != None:
            # Get the original image
            if item not in self.Segment['Final'].keys():
                self.Segment['Final'][item] = None
            self.Segment['Final'][item] = copy.deepcopy(self.Segment['Data'][item]['Original Image'] )

            # Load the pizels
            pixels = self.Segment['Final'][item].load()

            # Get the Blue Channel
            blue_set = list(self.Segment['Data'][item]['Segments'][1]['Pixel List'])
            for pts in blue_set:
                pixels[pts[0], pts[1]] = (0,0,255,255)

            # Get the Red Channel
            red_set = list(self.Segment['Data'][item]['Segments'][2]['Pixel List'])
            for pts in red_set:
                pixels[pts[0], pts[1]] = (255,0,0,255)

            # Get the Green Channel
            green_set = list(self.Segment['Data'][item]['Segments'][3]['Pixel List'])
            for pts in green_set:
                pixels[pts[0], pts[1]] = (0,255,0,255)

            self.output[item] = self.Segment['Final'][item]
            
    # Function to load an image for display
    def load_image(self):
        if len([self.listbox_01.get(idx) for idx in self.listbox_01.curselection()]) > 0:
            # Delete Local Widgets
            if hasattr(self,"img_final"):
                self.img_final.destroy()

            # Dispaly the image 
            self.img_f = self.Segment['Final'][[self.listbox_01.get(idx) for idx in self.listbox_01.curselection()][0]]
            scale = 0.8
            self.img_f = self.img_f.resize((int(self.img_f.width*scale), int(self.img_f.height*scale)))
            self.imgtk_f = ImageTk.PhotoImage(self.img_f)
            self.img_final = tk.Label(window, image = self.imgtk_f, bg = 'white')
            self.img_final.place(anchor = 'n', relx = 0.5, rely = 0.2)
            self.loc_att_list.append('self.img_final')
        else:
            messagebox.showerror(message = 'No image selected.')

    # Function to save all images
    def save_images(self):
        try:
            # Get the folder
            save_path = filedialog.askdirectory(
                title="Select Folder to Save Images",)
            
            for item in self.Segment['Final'].keys():
                # Save the original picture
                fname = item.split('.')
                fname = fname[0] +'.png'
                self.img_o = self.Segment['Data'][item]['Original Image'].convert('RGB')
                self.img_o.save(os.path.join(save_path, item))

                # Save the labelled image
                self.img_l = self.Segment['Final'][item].convert('RGB')
                fname = item.split('.')
                fname = fname[0] + '_mask.png'
                self.img_l.save(os.path.join(save_path, fname))

            # Prompt user to save project
            if messagebox.askyesno("Save", "Images Saved! Do you want to save the project?"):
                self.save()

        except:
            messagebox.showerror(message = 'Save Failed!')

    # Function to continue to next page
    def next_page():
        # Delete the page
        DeleteLocal(self)
        DeletePages(self)

        
        # Get the Save Path
        dir_name = os.path.dirname(self.proj_file)
        
        # Define the Temp folder path
        save_path = os.path.join(dir_name, 'Temp')
        
        # Check if the Temp folder exists, create if not
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            os.makedirs(os.path.join(save_path,'Original'))
            os.makedirs(os.path.join(save_path,'Annotated'))

        # Remove All items in Temp Folder
        def delete_all_files(directory):
            # Check if the directory exists
            if not os.path.isdir(directory):
                print(f"The directory {directory} does not exist.")
                return
            
            # Loop through all items in the directory
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                
                # Check if it's a file (not a directory)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass
        delete_all_files(save_path)
            
        # Save to Project Temp Directory
        for item in self.Segment['Final'].keys():
            # Save the original picture
            fname = item.split('.')
            fname = fname[0] +'.png'
            self.img_o = self.Segment['Data'][item]['Original Image'].convert('RGB')
            self.img_o.save(os.path.join(save_path,'Original', item))

            # Save the labelled image
            self.img_l = self.Segment['Final'][item].convert('RGB')
            fname = item.split('.')
            fname = fname[0] + '_mask.png'
            self.img_l.save(os.path.join(save_path, 'Annotated', fname))
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 6

        # Load the page
        self.load_page()

    # Function to go back to previous page
    def back_page():
        # Delete the page
        DeleteLocal(self)
        DeletePages(self)
                
        # Update the page number
        self.Segment['GUI']['CurrentPage'] = 4

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
                                text='Export Images',
                                style = "ModernT.TLabel"
                                )
    self.label_title.place(anchor = 'center', relx = 0.5, rely = 0.125)
    self.att_list.append('self.label_title')

    # Create the scrollbar
    self.scrollbar_01= ttk.Scrollbar(window, orient= 'vertical', style = "Vertical.TScrollbar")
    self.scrollbar_01.place(anchor='n', relx = 0.25, rely = 0.2, height = 452)
    self.att_list.append('self.scrollbar_01')
    
    # Get all images
    all_images = list(self.Segment['Final'].keys())
    all_images.sort()

    # Create the list box of images
    items = tk.StringVar(value=all_images)
    self.listbox_01 = tk.Listbox(window, 
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

    #Configure the scrollbar
    self.scrollbar_01.config(command= self.listbox_01.yview)

    # Create button to load image
    self.load_btn = ttk.Button(
                               window, 
                               text = "Load Image", 
                               command = lambda:load_image(self), 
                               style = 'Modern2.TButton',
                               width = 12
                               )
    self.load_btn.place(anchor = 'n', relx = 0.1025, rely = 0.775)
    self.att_list.append('self.load_btn')

    # Create button to export images
    self.btn_exp = ttk.Button(window, text = "Export Images", 
                              command = lambda:save_images(self), 
                              style = 'Modern2.TButton',
                              width = 12)
    self.btn_exp.place(anchor = 'n', relx = 0.2074, rely = 0.775)
    self.att_list.append('self.btn_exp')

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
    self.btn_back1 = ttk.Button(window, 
                               text = "Back", 
                               command = back_page, 
                               style = 'Modern2.TButton',
                               width = 10)
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