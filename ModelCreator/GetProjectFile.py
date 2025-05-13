#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# GetProjectFile.py
#
# PURPOSE: Load existing project information or define a new project.
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateNewProject(self):
    #--------------------------------------------------------------------------
    #
    #   PURPOSE: Get the filepath for a new project.
    #
    #--------------------------------------------------------------------------

    # Import Modules
    from tkinter import filedialog

    # Preallocate file path
    file_path = ''

    # Ask where to save the new file
    while '.seg' not in file_path:
        file_path = filedialog.asksaveasfilename(
            title="Create a new project file",
            filetypes=(("Project Files", "*.seg"),)
        )

        if file_path == '':
            self.proj_file = None
            return
        
        elif '.seg' not in file_path:
            if '.' in file_path:
                file_path = file_path[:file_path.index('.')] + '.seg'
            else:
                file_path = file_path + '.seg'

    # Set the project file path
    self.proj_file = file_path

    # Initialize the Configuration
    self.Segment = {}
    self.Segment['GUI'] = {'CurrentPage':1}

    return
 

def LoadProject(self, window):
    #--------------------------------------------------------------------------
    #
    #   PURPOSE: Load an existing project file.
    #
    #--------------------------------------------------------------------------

    # Import Modules
    import os
    import threading
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    import pickle
    import zstandard as zstd

    # Import Functions
    from General.DeleteWidgets import DeletePages

    # Preallocate file path
    file_path = ''

    # Ask for the file name
    while '.seg' not in file_path:
        file_path = filedialog.askopenfilename(
            title="Open a project file",
            filetypes=(("Project Files", "*.seg"),)
        )

        if file_path == '':
            self.proj_file = None
            return
        
        elif '.seg' not in file_path:
            messagebox.showinfo("Wrong Filetype", "Project File not selected. Please select a valid file or press 'Cancel' and select 'New Project File'.")

    # Set the project file path
    self.proj_file = file_path

    # Initialize the data structure
    try:
        # Function to open file
        def open_file(callback):
            # Start Open
            dctx = zstd.ZstdDecompressor()
            with open(file_path, 'rb') as f:
                with dctx.stream_reader(f) as decompressor:
                    self.Segment = pickle.load(decompressor)

            # Notify when done
            callback()

        # Exit Protocol
        def on_closing_loading(self):
            # Force Quit the entire program
            if messagebox.askyesno("Quit", "Do you want to quit the program?"):
                window.destroy()

        # Create Loading Window
        def show_loading_window():
            loading = tk.Toplevel(window)
            loading.title("Opening File")
            loading.geometry("250x100")
            loading.resizable(False, False)
            loading.configure(bg='white')
            loading.grab_set()  # Make it modal

            # Create Window Exit Protocol
            loading.protocol("WM_DELETE_WINDOW", lambda:on_closing_loading(self))

            ttk.Label(loading, 
                        text="Opening Project File - Please Wait.", 
                        style = "Modern1.TLabel").pack(pady=10)

            pb = ttk.Progressbar(loading, mode='indeterminate',style='Modern.Horizontal.TProgressbar')
            pb.pack(fill='x', padx=20, pady=10)
            pb.start(10)

            def on_task_done():
                pb.stop()
                loading.destroy()

            # Run long task in background thread
            threading.Thread(target=open_file, args=(on_task_done,), daemon=True).start()

            # Wait until loading window is closed (blocks here)
            window.wait_window(loading)

        # Get the file size
        fsize = os.path.getsize(self.proj_file)

        # Start Load
        if fsize > 1E6:
            show_loading_window()
        else:
            dctx = zstd.ZstdDecompressor()
            with open(file_path, 'rb') as f:
                with dctx.stream_reader(f) as decompressor:
                    self.Segment = pickle.load(decompressor)
        
    except:
        # Return empty data structure
        self.Segment = {}
        self.Segment['GUI'] = {'CurrentPage':1}
    return