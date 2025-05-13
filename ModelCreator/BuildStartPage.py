#-----------------------------------------------------------------------------------------
#
#   BuildStartPage.py
#
#   PURPOSE: Allow user to start a new project or select an old project
#
#   INPUTS:
#       self    structure containing all GUI information
#       window  window
#-----------------------------------------------------------------------------------------
def BuildStartPage(self,window):
    #Import Modules
    import os
    from PIL import Image, ImageTk
    import tkinter as tk
    from tkinter import ttk

    #Initialize list of attributes for each page
    self.att_list = []

    # Function to create Help Window
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
                                text=' Main Menu',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Set list of buttons and functions
        image_list = ['new_mod.png', 'edit_mod.png','use_mod.png','exp_mod.png']
        func_list = [f'Create a new MicroNet model project', 
                     f'Edit a MicroNet model project',
                     f'Segment an image with an existing trained MicroNet model',
                     f'Export a segmented image to an analysis tool']

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

    # Create the frame for defining a new model
    self.box_frame1 = tk.Frame(
                            window, 
                            bd=3, 
                            relief="ridge", 
                            width = 300,
                            height = 300,
                            bg="white"
                            )
    self.box_frame1.place(anchor = 'c', relx=0.35, rely=0.5)
    self.att_list.append('self.box_frame1')

    # Create a label for creating a model
    self.label_01 = ttk.Label(
                            self.box_frame1,
                            text='Create a Model',
                            style = "Modern3.TLabel"
                            )
    self.label_01.place(anchor='n', relx = 0.5, rely = 0.1)
    self.att_list.append('self.label_02')

    # Create button to start a new project
    self.btn1 = ttk.Button(
                            self.box_frame1 , 
                            text = "New Model", 
                            command = self.new_project,
                            style="Modern.TButton", 
                            width = 18
                            )
    self.btn1.place(anchor = 'center', relx = 0.5, rely = 0.4)
    self.att_list.append('self.btn1')


    # Create button to load a project
    self.btn2 = ttk.Button(
                            self.box_frame1 , 
                            text = "Edit Model", 
                            command = self.load_project, 
                            style="Modern.TButton", 
                            width = 18
                            )
    self.btn2.place(anchor = 'center', relx = 0.5, rely = 0.75)
    self.att_list.append('self.btn2')

    # # Create Frame for Using a Model
    self.box_frame2 = tk.Frame(
                            window, 
                            bd=3, 
                            relief="ridge", 
                            width = 300,
                            height = 300,
                            bg="white"
                            )
    self.box_frame2.place(anchor = 'c', relx=0.65, rely=0.5)
    self.att_list.append('self.box_frame2')

    # Create a label for creating a model
    self.label_02 = ttk.Label(
                            self.box_frame2,
                            text='Load a Model',
                            style = "Modern3.TLabel"
                            )
    self.label_02.place(anchor='n', relx = 0.5, rely = 0.1)
    self.att_list.append('self.label_02')

    # Create button to load a project
    self.btn4 = ttk.Button(
                            self.box_frame2, 
                            text = "Use Model", 
                            command = self.segment_image, 
                            style="Modern.TButton", 
                            width = 18
                            )
    self.btn4.place(anchor = 'center', relx = 0.5, rely = 0.4)
    self.att_list.append('self.btn4')
    
    # Create button to export ruc data
    self.btn4 = ttk.Button(
                            self.box_frame2, 
                            text = "Export Data", 
                            command = self.start_export, 
                            style="Modern.TButton", 
                            width = 18
                            )
    self.btn4.place(anchor = 'center', relx = 0.5, rely = 0.75)
    self.att_list.append('self.btn4')

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