import tkinter as tk
from tkinter import ttk
from database.score_manager import ScoreManager
from gui.sound_manager import SoundManager

class LeaderboardWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Leaderboard - Hangman")
        self.window.geometry("1200x800")
        self.window.resizable(False, False)
        
        # Background
        default_bg = "#2b2b2b"
        try:
            from PIL import Image, ImageTk
            img = Image.open("assets/media/login_bg.jpg")
            bg_img = ImageTk.PhotoImage(img.resize((1200, 800), Image.LANCZOS))
            bg_label = tk.Label(self.window, image=bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_image = bg_img
            self.window.configure(bg=default_bg)
        except Exception:
            self.window.configure(bg=default_bg)
        
        SoundManager.play("leaderboard_open")  # use your existing sound
        
        # Title
        tk.Label(self.window, text="🏆 Leaderboard", font=("Arial", 32, "bold"),
                 bg=default_bg, fg="#FFD700").pack(pady=(40, 20))
        
        # Create Treeview (table)
        columns = ("Rank", "Username", "Total Score", "Games Played", "Wins")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=20)
        
        # Define headings
        self.tree.heading("Rank", text="Rank")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Total Score", text="Total Score")
        self.tree.heading("Games Played", text="Games Played")
        self.tree.heading("Wins", text="Wins")
        
        # Set column widths and alignment
        self.tree.column("Rank", width=100, anchor="center")
        self.tree.column("Username", width=300, anchor="w")
        self.tree.column("Total Score", width=150, anchor="center")
        self.tree.column("Games Played", width=150, anchor="center")
        self.tree.column("Wins", width=150, anchor="center")
        
        # Style for dark theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=default_bg,
                        foreground="white",
                        fieldbackground=default_bg,
                        font=("Arial", 12))
        style.configure("Treeview.Heading",
                        background="#3a3a3a",
                        foreground="white",
                        font=("Arial", 13, "bold"))
        style.map("Treeview", background=[('selected', '#4CAF50')])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, padx=(40, 0), pady=20, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 40))
        
        # Load data
        self.load_data()
        
        # Close button
        tk.Button(self.window, text="Close", command=self.window.destroy,
                  bg=default_bg, fg="white", font=("Arial", 14),
                  relief=tk.FLAT, highlightthickness=0, takefocus=False).pack(pady=20)
    
    def load_data(self):
        rankings = ScoreManager.get_user_rankings(limit=100)
        for entry in rankings:
            self.tree.insert("", tk.END, values=(
                entry['rank'],
                entry['username'],
                entry['total_score'],
                entry['total_games'],
                entry['wins']
            ))