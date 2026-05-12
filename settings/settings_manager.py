import tkinter as tk 
from tkinter import HORIZONTAL, ttk 

class settingsWindow (tk.Toplevel):

    # this function builds the settings window that come up over the The game UI. 
    def __init__ (self, master, settings_manager):
        super().__init__ (master)
        self.settings = settings_manager
        self.title ("Settings")
        self.geometry("600x400")
        self.configure(bg="#2b2b2b")
        self.create_layout  # Calls the function that builds the entire UI layout.

    def create_layout(self):
        self.sidebar =tk.Frame(self, width = 150, bg = "#1e1e1e")  # this builds the container for widgets 
        self.sidebar.pack (side= "left", fill="y")
        self.content = tk.Frame(self, bg = "#2b2b2b")
        self.content.pack(side = "right", expand = True, fill = "both")  # this makes the setting bar responsive 

        buttons = [         # each button has ("label", function)
            ("Audio", self.show_audio_settings),   
            ("Theme", self.show_theme_settings),
            ("Display", self.show_display_settings),
            ("Save", self.show_save_settings)
        ]
        for text, command in buttons :    #this loops the list of buttons and creates them. 
            btn = tk.Button (self.sidebar, text=text, command=command, bg="#333333", fg = "white", relief="flat", height= 2)
            btn.pack (fill="x", pady= 2)

        self.show_audio_settings()

    def clear_content(self):   #Removes everything inside the content area, allows switching between panels
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_audio_settings(self):
        self.clear_content()
        tk.Label(self.content, text="Audio Settings", fg="white", bg="#2b2b2b", font=("Arial", 16))
        tk.Label.pack(pady=10)
        tk.Label(self.content , text="Music Settings", fg="white", bg="#2b2b2b")
        tk.Label.pack()
        tk.Scale(self.content, from_=0, to=100 , orient="HORIZONTAL", command= self.settings.set_sfx_volume)      #slider for music vol
        tk.Scale.pack()
        tk.Label(self.content , text="SFX Settings", fg="white", bg="#2b2b2b")
        tk.Label.pack()
        tk.Scale(self.content, from_=0, to=100 , orient="HORIZONTAL", command= self.settings.set_sfx_volume)     #slider for Sound FX vol

    def show_theme_settings(self):
        self.clear_content()
        tk.Label(self.content, text="Theme Settings", fg="white", bg="#2b2b2b", font=("Arial", 16))
        tk.Label.pack(pady=10)
        tk.Radiobutton(self.content, text="Light Theme", value="light", command= lambda : self settings.apply_theme("light"),bg="#2b2b2b", fg="white", selectcolor="#444")
        tk.Radiobutton.pack(anchor="w")
