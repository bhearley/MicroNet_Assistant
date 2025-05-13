#-----------------------------------------------------------------------------------------
#
#   Getself.btn_style1s.py
#
#   PURPOSE: Set the self.btn_style1s for the GUI
#
#   INPUTS:
#       self    structure containing all GUI information
#-----------------------------------------------------------------------------------------
def GetStyles(self):
    # Import modules
    from tkinter import ttk

    # Initialize Syles
    self.style = ttk.Style()
    self.style.theme_use("alt") 
    self.style_man = {}

    # Buttons
    # -- Blue Large Text
    self.style.configure(
                        "Modern.TButton",
                        background='#0b3d91',
                        foreground="white",
                        font=("Segoe UI", 18),
                        borderwidth=2,
                        padding=10,
                        focuscolor='',
                        highlightthickness=0
                        )

    self.style.map(
                        "Modern.TButton",
                        background=[("active", "#428bca")]
                )
    
    # -- Blue Small Text
    self.style.configure(
                        "Modern2.TButton",
                        background='#0b3d91',
                        foreground="white",
                        font=("Segoe UI", 16),
                        borderwidth=2,
                        padding=10,
                        focuscolor='',
                        highlightthickness=0
                        )

    self.style.map(
                        "Modern2.TButton",
                        background=[("active", "#428bca")]
                )
    
    # -- Red Small Text
    self.style.configure(
                        "Modern3.TButton",
                        background='#DD361C',
                        foreground="white",
                        font=("Segoe UI", 12),
                        borderwidth=2,
                        padding=5,
                        focuscolor='',
                        highlightthickness=0
                        )

    self.style.map(
                        "Modern3.TButton",
                        background=[("active", "#FC3D21")]
                )

    # -- Red Arrow Text
    self.style.configure(
                        "Modern4.TButton",
                        background='#DD361C',
                        foreground="white",
                        font=("Segoe UI", 20, "bold"),
                        borderwidth=2,
                        padding=2,
                        focuscolor='',
                        highlightthickness=0
                        )
    
    self.style.map(
                        "Modern4.TButton",
                        background=[("active", "#FC3D21")]
                )
    
    # -- Red Medium Text
    self.style.configure(
                        "Modern5.TButton",
                        background='#DD361C',
                        foreground="white",
                        font=("Segoe UI", 14),
                        borderwidth=2,
                        padding=5,
                        focuscolor='',
                        highlightthickness=0,
                        anchor="center"
                        )

    self.style.map(
                        "Modern5.TButton",
                        background=[("active", "#FC3D21")]
                )
    
    # -- Red Medium Text Selected
    self.style.configure(
                        "Modern5Selected.TButton",
                        background="gray",
                        foreground="white",
                        font=("Segoe UI", 14),
                        borderwidth=2,
                        padding=5,
                        focuscolor='',
                        highlightthickness=0,
                        anchor="center"
                        )
    
    # Checkbutton
    self.style.configure(
                        "TCheckbutton",
                        focuscolor='none',
                        padding=10,               
                        font=("Segoe UI", 12),     
                        foreground="black",      
                        background="white"
                        )      
 
    # Combo Box Style
    self.style.configure(
                        "Modern.TCombobox",
                        fieldbackground="white",   
                        background="white",        
                        foreground="black",        
                        bordercolor="#cccccc",
                        lightcolor="#dddddd",
                        darkcolor="#aaaaaa",
                        borderwidth=1,
                        relief="flat",
                        padding=5
                        )
    
    self.style.map(
                        "Modern.TCombobox",
                        fieldbackground=[("readonly", "white"), ("active", "white")], 
                        foreground=[("readonly", "black"), ("active", "black")],  
                        background=[("readonly", "white"), ("active", "white")],  
                        selectbackground=[("active", "white"), ("readonly", "white")],  
                        selectforeground=[("active", "black"), ("readonly", "black")]  
                 )

    # Entry
    self.style.configure(
                        "Custom.TEntry", 
                        font=('Segoe UI', 14),
                        foreground='black',
                        background='white',
                        relief='flat',
                        borderwidth=1,
                        padding=2,
                        selectbackground='#428bca',  # Background color when text is selected
                        selectforeground='white',  # Color of the selected text
                        )
    self.style.map(
                        "Custom.TEntry",
                        foreground=[('disabled', 'black')],  
                        background=[('disabled', 'white')],
                        selectforeground=[('disabled', 'black')],  
                        selectbackground=[('disabled', 'white')]
                )

    # Listbox Style
    self.style_man['ListBox'] = {
                                'ListBox1':{
                                    'bg':"#ffffff",                 
                                    'fg':"#333333",                 
                                    'font':("Segoe UI", 9),         
                                    'selectbackground':"#428bca",   
                                    'selectforeground':"white",     
                                    'highlightthickness':1,         
                                    'bd':1                          
                                    }
                                }

    # Progress Bar
    self.style.configure(
                        "Modern.Horizontal.TProgressbar",
                        thickness=20,             
                        troughcolor="#d3d3d3",    
                        background="#0b3d91",     
                        )

    # Scale Style
    self.style.configure(
                        "Modern.Horizontal.TScale",
                        troughcolor="#DD361C", 
                        background="white",
                        borderwidth=1,
                        relief='rasied'
                        )
    
    # Scrollbar Style
    self.style.configure(
                        "Vertical.TScrollbar",
                        background="#0b3d91",
                        troughcolor="#d9d9d9",
                        bordercolor="#cccccc",
                        arrowcolor="#0b3d91"
                        )
    
    
    
    # Text Styles
    # -- Loading Bar Style
    self.style.configure(
                        "Modern1.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", 10),
                        padding=5
                        )
    
    # -- Label 1
    self.style.configure(
                        "Modern2.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", 12),
                        padding=0
                        )
    
    # -- Label 2
    self.style.configure(
                        "Modern3.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", 18),
                        padding=0
                        )
    
    # -- Label 3
    self.style.configure(
                        "Modern4.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", 10, 'bold'),
                        padding=5
                        )
    
    # -- Title
    self.style.configure(
                        "ModernT.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", 24, 'bold'),
                        padding=0
                        )
    
    
    
    
    


