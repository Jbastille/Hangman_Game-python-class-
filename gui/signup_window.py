import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database.user_manager import UserManager
from gui.sound_manager import SoundManager

try:
    from tkfeather import Feather
    HAS_ICONS = True
except ImportError:
    HAS_ICONS = False

class SignUpWindow:
    def __init__(self, parent, on_success=None):
        self.parent = parent
        self.on_success = on_success

        self.window = tk.Toplevel(parent)
        self.window.title("Sign Up - Hangman")
        self.window.geometry("1200x800")
        self.window.resizable(False, False)

        default_bg = "#2b2b2b"

        try:
            img = Image.open("assets/media/login_bg.jpg")
            bg_img = ImageTk.PhotoImage(img.resize((1200, 800), Image.LANCZOS))
            bg_label = tk.Label(self.window, image=bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_image = bg_img
            self.window.configure(bg=default_bg)
        except Exception as e:
            print(f"Background not loaded: {e}")
            self.window.configure(bg=default_bg)

        SoundManager.play("pop")

        if HAS_ICONS:
            icon = Feather("user-plus", size=80).icon
            tk.Label(self.window, image=icon, bg=default_bg).place(relx=0.5, rely=0.20, anchor='center')

        tk.Label(self.window, text="Create a new account", font=("Arial", 28, "bold"),
                 bg=default_bg, fg='white').place(relx=0.5, rely=0.32, anchor='center')

        # Username
        tk.Label(self.window, text="Username:", font=("Arial", 16),
                 bg=default_bg, fg='white').place(relx=0.40, rely=0.45, anchor='e')
        self.entry_user = tk.Entry(self.window, width=30, font=("Arial", 14))
        self.entry_user.place(relx=0.42, rely=0.45, anchor='w')

        # Password
        tk.Label(self.window, text="Password:", font=("Arial", 16),
                 bg=default_bg, fg='white').place(relx=0.40, rely=0.55, anchor='e')
        self.entry_pass = tk.Entry(self.window, show="*", width=30, font=("Arial", 14))
        self.entry_pass.place(relx=0.42, rely=0.55, anchor='w')

        # --- REGISTER BUTTON (no visual feedback) ---
        self.btn_register = tk.Button(
            self.window,
            text="REGISTER",
            command=self.register,
            bg=default_bg,
            fg="white",
            font=("Arial", 16, "bold"),
            padx=40,
            pady=12,
            relief=tk.FLAT,
            highlightthickness=0,
            takefocus=False
        )
        self.btn_register.place(relx=0.5, rely=0.68, anchor='center')

        # --- Back to login link (no visual feedback) ---
        self.btn_back = tk.Button(
            self.window,
            text="Already have an account? Sign in",
            command=self.go_to_login,
            bg=default_bg,
            fg="white",
            font=("Arial", 12),
            relief=tk.FLAT,
            highlightthickness=0,
            takefocus=False
        )
        self.btn_back.place(relx=0.5, rely=0.78, anchor='center')

        self.entry_pass.bind("<Return>", lambda e: self.register())

    def register(self):
        SoundManager.play("click")
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()
        if not username or not password:
            SoundManager.play("error")
            messagebox.showerror("Error", "Please fill in both fields.")
            return
        success = UserManager.register(username, password)
        if success:
            SoundManager.play("success")
            messagebox.showinfo("Success", f"Account '{username}' created! You can now log in.")
            if self.on_success:
                self.on_success(username, password)
            self.window.destroy()
        else:
            SoundManager.play("error")
            messagebox.showerror("Error", "Username already exists. Choose another.")

    def go_to_login(self):
        self.window.destroy()