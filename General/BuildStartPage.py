#-----------------------------------------------------------------------------------------
#
#   BuildStartPage.py
#
#   PURPOSE: Allow user to start a new project or select an existing project.
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
        canvas = tk.Canvas(
                        helpwindow, 
                        height=500, 
                        width=700, 
                        bg="white"
                        )
        scrollbar = tk.Scrollbar(
                                helpwindow, 
                                orient="vertical", 
                                command=canvas.yview
                                )
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
                                text='Main Menu',
                                style = "ModernT.TLabel"
                                )
        label_title.pack(padx = 5, pady=0, anchor="w")

        # Create the instructions
        instructions = ("The main menu presents four options:")
        label_inst1 = ttk.Label(
                                frame,
                                text=instructions,
                                style = "Modern1.TLabel",
                                wraplength=550
                                )
        label_inst1.pack(padx = 5, pady=5, anchor="w")

        # Set list of buttons and functions
        image_list = ['new_mod.png', 'edit_mod.png','use_mod.png','exp_mod.png']
        func_list = [f'Create a new MicroNet Segmentation Model project', 
                     f'Edit an existing MicroNet Segmentation Model project',
                     f'Segment an image with a trained MicroNet Model',
                     f'Export the geometry of a segmented image to an analysis tool']

        # Add buttons and functions to frame
        for i in range(len(image_list)):
            # Load the image
            img_file = os.path.join(os.getcwd(),'GUI','Help',image_list[i])
            img = tk.PhotoImage(file=img_file)

            # Create a container for image + text
            row_frame = tk.Frame(frame, bg="white")
    
            # Image holder frame (fixed width)
            image_holder = tk.Frame(row_frame, width=220, height=40, bg="white")
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
    self.frame_create = tk.Frame(
                            window, 
                            bd=self.Placement['MainPage']['Frame1'][2], 
                            relief="ridge", 
                            width = self.Placement['MainPage']['Frame1'][3],
                            height = self.Placement['MainPage']['Frame1'][4],
                            bg="white"
                            )
    self.frame_create.place(
                            anchor = 'c', 
                            relx = self.Placement['MainPage']['Frame1'][0], 
                            rely = self.Placement['MainPage']['Frame1'][1]
                            )
    self.att_list.append('self.frame_create')

    # Create a label for defining a new model
    self.label_create = ttk.Label(
                            self.frame_create,
                            text='Segmentation Model Training',
                            style = "Modern3.TLabel"
                            )
    self.label_create.place(
                        anchor='n', 
                        relx = self.Placement['MainPage']['Label1'][0], 
                        rely = self.Placement['MainPage']['Label1'][1]
                        )
    self.att_list.append('self.label_create')

    # Create button to start a new project
    self.btn_new_mod = ttk.Button(
                                self.frame_create , 
                                text = "New Model", 
                                command = self.new_project,
                                style="Modern.TButton", 
                                width = self.Placement['MainPage']['Button1'][2]
                                )
    self.btn_new_mod.place(
                        anchor = 'center', 
                        relx = self.Placement['MainPage']['Button1'][0], 
                        rely = self.Placement['MainPage']['Button1'][1]
                        )
    self.att_list.append('self.btn_new_mod')

    # Create button to load a project
    self.btn_load_mod = ttk.Button(
                            self.frame_create , 
                            text = "Edit Model", 
                            command = self.load_project, 
                            style="Modern.TButton", 
                            width = self.Placement['MainPage']['Button2'][2]
                            )
    self.btn_load_mod.place(
                        anchor = 'center', 
                        relx = self.Placement['MainPage']['Button2'][0], 
                        rely = self.Placement['MainPage']['Button2'][1]
                        )
    self.att_list.append('self.btn_load_mod')

    # # Create Frame for Using a Model
    self.frame_use = tk.Frame(
                            window, 
                            bd=self.Placement['MainPage']['Frame2'][2], 
                            relief="ridge", 
                            width = self.Placement['MainPage']['Frame2'][3],
                            height = self.Placement['MainPage']['Frame2'][4],
                            bg="white"
                            )
    self.frame_use.place(
                        anchor = 'c', 
                        relx = self.Placement['MainPage']['Frame2'][0], 
                        rely = self.Placement['MainPage']['Frame2'][1]
                        )
    self.att_list.append('self.frame_use')

    # Create a label for using/loading a model
    self.label_use = ttk.Label(
                            self.frame_use,
                            text='Segmentation & Modeling',
                            style = "Modern3.TLabel"
                            )
    self.label_use.place(
                        anchor='n', 
                        relx = self.Placement['MainPage']['Label2'][0], 
                        rely = self.Placement['MainPage']['Label2'][1]
                        )
    self.att_list.append('self.label_use')

    # Create button to segment an image with a trained model
    self.btn_use_mod = ttk.Button(
                            self.frame_use, 
                            text = "Segment Image", 
                            command = self.segment_image, 
                            style="Modern.TButton", 
                            width = self.Placement['MainPage']['Button3'][2]
                            )
    self.btn_use_mod.place(
                        anchor = 'center', 
                        relx = self.Placement['MainPage']['Button3'][0], 
                        rely = self.Placement['MainPage']['Button3'][1]
                        )
    self.att_list.append('self.btn_use_mod')
    
    # Create button to export ruc data
    self.btn_ruc = ttk.Button(
                            self.frame_use, 
                            text = "Export Geometry", 
                            command = self.start_export, 
                            style="Modern.TButton", 
                            width = self.Placement['MainPage']['Button4'][2]
                            )
    self.btn_ruc.place(
                    anchor = 'center', 
                    relx = self.Placement['MainPage']['Button4'][0], 
                    rely = self.Placement['MainPage']['Button4'][1]
                    )
    self.att_list.append('self.btn_ruc')

    # Create Help Button
    # -- Load an image using PIL
    self.image_path_help = os.path.join(os.getcwd(),'GUI','General','help.png') 
    self.image_help = Image.open(self.image_path_help)
    scale = self.Placement['MainPage']['Help'][3]
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
                            width = self.Placement['MainPage']['Help'][2]
                            )
    self.btn_help.place(
                        anchor = 'w', 
                        relx = self.Placement['MainPage']['Help'][0], 
                        rely = self.Placement['MainPage']['Help'][1]
                        )
    self.att_list.append('self.btn_help')