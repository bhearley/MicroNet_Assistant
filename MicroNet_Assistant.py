#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# MicroNetAssistant.py
#
# Brandon Hearley - LMS
# brandon.l.hearley@nasa.gov
# 4/25/2025
#
# PURPOSE: Prepare images for segmentation using MicroNet. Images
#          can be scaled, cropped, and labelled for segmentation
#          manually or using the Segment Anything Model from Meta.
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Import Modules
import os
import pickle
from PIL import ImageTk, Image
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import zstandard as zstd

# Import Functions
from General.BuildStartPage import *
from General.DeleteWidgets import *
from GUI.GetStyles import *
from GUI.Placement import *
from ModelCreator.CreateFileSelection import *
from ModelCreator.CropImages import *
from ModelCreator.DataDefinition import *
from ModelCreator.GetProjectFile import *
from ModelCreator.ResizeImages import *
from ModelCreator.ReviewImages import *
from ModelCreator.SegmentImages import *
from ModelCreator.TrainModel import *
from ModelInference.UseModel import *
from RUCGenerator.BuildRUCGenerator import *

#Create the GUI
class MicroNetAssistant:
    #Initialize
    def __init__(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Initialize the GUI.
        #
        #--------------------------------------------------------------------------

        # Set global variales
        global window

        #Create Background Window
        window = tk.Tk()
        window.title("MicroNet Assistant")
        window.state('zoomed')
        window.configure(bg='white')

        # Placement Information
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        Placement(self, str(screen_width) + "x" + str(screen_height))

        # Define Images
        title_img = os.path.join(os.getcwd(),'GUI','General','TitleHeader.png') # Set the title image path
        logo_img = os.path.join(os.getcwd(),'GUI','General','NasaLogo.png')     # Set the logo image path

        #Add the Title
        img = Image.open(title_img)
        scale = self.Placement['MainPage']['Title'][2]
        img = img.resize((int(img.width*scale), int(img.height*scale)))
        self.img_hdr = ImageTk.PhotoImage(img)
        self.panel_hdr = tk.Label(window, image = self.img_hdr, bg = 'white')
        self.panel_hdr.place(anchor = 'n', relx = self.Placement['MainPage']['Title'][0], rely = self.Placement['MainPage']['Title'][1])

        #Add the NASA Logo
        img = Image.open(logo_img)
        scale = self.Placement['MainPage']['Logo'][2]
        img = img.resize((int(img.width*scale), int(img.height*scale)))
        self.img_nasa = ImageTk.PhotoImage(img)
        self.panel_nasa = tk.Label(window, image = self.img_nasa, bg = 'white')
        self.panel_nasa.place(anchor = 'e', relx = self.Placement['MainPage']['Logo'][0], rely = self.Placement['MainPage']['Logo'][1])

        # Load the style
        GetStyles(self)

        # Function for GUI Exit
        def on_closing(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Set exit protocol for the GUI.
            #
            #----------------------------------------------------------------------

            # Check if project file exists
            if hasattr(self,'proj_file'):

                # Prompt user to save
                if messagebox.askyesno("Quit", "Do you want to save before exiting?"):
                    self.save()

            # Destory the window
            window.destroy()

        # Create Window Exit Protocol
        window.protocol("WM_DELETE_WINDOW", lambda:on_closing(self))

        # Build Start Page
        BuildStartPage(self, window)

        #Main Loop
        window.mainloop()

    # Function to create the save button
    def create_save_btn(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create the save button for the GUI.
        #
        #--------------------------------------------------------------------------

        # Check if button exists
        if hasattr(self,"btn_save") == False:
            # Create the Save Button
            # -- Load an image using PIL
            self.image_path_save = os.path.join(os.getcwd(),'GUI','General','save.png') 
            self.image_save = Image.open(self.image_path_save)
            scale = 0.065
            self.image_save = self.image_save.resize((int(self.image_save.width*scale), int(self.image_save.height*scale)))

            # -- Convert the image to a Tkinter-compatible format
            self.photo_save = ImageTk.PhotoImage(self.image_save)

            # -- Create the Button
            self.btn_save = ttk.Button(
                                window, 
                                text = " Save",
                                image=self.photo_save,
                                compound='left',                                 
                                command = self.save,
                                style = "Modern2.TButton",
                                width = self.Placement['MainPage']['Save'][2]
                                )
            self.btn_save.place(anchor = 'w', 
                                relx = self.Placement['MainPage']['Save'][0], 
                                rely = self.Placement['MainPage']['Save'][1])
            

    # Function to create a new project
    def new_project(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Initialize a new project file.
        #
        #--------------------------------------------------------------------------

        # Initialize the data structure
        CreateNewProject(self)

        if self.proj_file is not None:
            # Delete the Previous Page
            DeletePages(self)

            # Create the Save Button
            self.create_save_btn()

            # Load the page
            self.load_page()

    # Function to load an existing project
    def load_project(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Load a project.
        #
        #--------------------------------------------------------------------------

        # Load the data structure
        LoadProject(self, window)

        if self.proj_file is not None:
            # Delete the Previous Page
            DeletePages(self)

            # Create the Save Button
            self.create_save_btn()

            # Load the page
            self.load_page()

    # Function to load an existing model
    def segment_image(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Load a trained model and segment an imate
        #
        #--------------------------------------------------------------------------

        # Load the data structure
        self.Segment = {'GUI':{'CurrentPage':8}}

        # Delete the Previous Page
        DeletePages(self)

        # Load the page
        self.load_page()

    # Function to start exporting a segmentation
    def start_export(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Enable exporting segmentation to a model.
        #
        #--------------------------------------------------------------------------

        # Load the data structure
        self.Segment = {'GUI':{'CurrentPage':9}}

        # Delete the Previous Page
        DeletePages(self)

        # Load the page
        self.load_page()

            
    # Function to load a GUI Page
    def load_page(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Load the correct page of the GUI
        #
        #--------------------------------------------------------------------------

        # Load the correct page
        if self.Segment['GUI']['CurrentPage'] == 0:
            if hasattr(self,"btn_save"):
                self.btn_save.destroy()
                del self.btn_save
            BuildStartPage(self, window)
        
        if self.Segment['GUI']['CurrentPage'] == 1:
            CreateFileSelection(self, window)

        if self.Segment['GUI']['CurrentPage'] == 2:
            ResizeImages(self, window)

        if self.Segment['GUI']['CurrentPage'] == 3:
            CropImages(self, window)

        if self.Segment['GUI']['CurrentPage'] == 4:
            SegmentImages(self, window)

        if self.Segment['GUI']['CurrentPage'] == 5:
            ReviewImages(self, window)

        if self.Segment['GUI']['CurrentPage'] == 6:
            DataDefinition(self, window)

        if self.Segment['GUI']['CurrentPage'] == 7:
            TrainModel(self, window)

        if self.Segment['GUI']['CurrentPage'] == 8:
            if hasattr(self,'btn_save'):
                self.btn_save.destroy()
            UseModel(self, window)

        if self.Segment['GUI']['CurrentPage'] == 9:
            if hasattr(self,'btn_save'):
                self.btn_save.destroy()
            BuildRUCGenerator(self, window)

    # Function to save the project file
    def save(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Save the project file.
        #
        #--------------------------------------------------------------------------

        # Check the max page number corresponds to the Train Model Page
        if self.Segment['GUI']['CurrentPage'] > 7:
            self.Segment['GUI']['CurrentPage'] = 7

        # Save the current segmentation image
        try:
            self.save_image()
        except:
            pass

        # Remove the Predictor from the data structure
        if 'Data' in self.Segment.keys():
            for key in self.Segment['Data'].keys():
                if self.Segment['Data'][key]['Predictor'] is not None:
                    self.Segment['Data'][key]['Predictor'] = 'Load'

        # Save Model Information
        try:
            self.save_model()
        except:
            pass

        # Get the model data
        data = self.Segment

        # Function to save the data
        def save_file(callback):
            cctx = zstd.ZstdCompressor()
            with open(self.proj_file, 'wb') as f:
                with cctx.stream_writer(f) as compressor:
                    pickle.dump(data, compressor, protocol=pickle.HIGHEST_PROTOCOL)

            # Notify when done
            callback()

        # Function to display progress bar while saving
        def show_loading_window():
            # Create the window
            loading = tk.Toplevel(window)
            loading.title("Saving File")
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

            # Create the label
            ttk.Label(loading, 
                        text="Saving Project File - Please Wait.", 
                        style = "Modern1.TLabel").pack(pady=10)

            # Create the progress bar
            pb = ttk.Progressbar(loading, mode='indeterminate',style = "Modern.Horizontal.TProgressbar")
            pb.pack(fill='x', padx=20, pady=10)
            pb.start(10)

            # Function to close window when task is completed
            def on_task_done():
                pb.stop()
                loading.destroy()

            #Begin save on background thread
            threading.Thread(target=save_file, args=(on_task_done,), daemon=True).start()

            # Wait until loading window is closed
            window.wait_window(loading)

        # Start Save
        show_loading_window()

        # Show save message to user
        messagebox.showinfo(title = 'Save', message = 'Project Saved!')

    # Function to save the current segmentation
    def save_image(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Save the current segmentation.
        #
        #--------------------------------------------------------------------------

        # Save the image
        if self.prev_img is not None:
            self.Segment['Data'][self.prev_img]['Original Image'] = self.image
            self.Segment['Data'][self.prev_img]['Segmented Image'] = self.combined_all
            try:
                self.Segment['Data'][self.prev_img]['Predictor'] = self.predictor
            except:
                pass

    # Function to save the current segmentation
    def save_model(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Save the current segmentation.
        #
        #--------------------------------------------------------------------------

        # Save the image
        if hasattr(self,"sheet_7_01"):
            self.Segment['Model Information'] = [
                self.sheet_7_01.data,
                self.sheet_7_02.data,
                self.sheet_7_03.data,
                self.combo_7_01.get(),
                self.combo_7_02.get(),
                self.combo_7_03.get(),
                self.combo_7_04.get()
            ]

# Start the GUI
MicroNetAssistant()