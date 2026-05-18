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

class LoginWindow:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success

        self.window = tk.Toplevel(parent)
        self.window.title("Sign In - Hangman")
        self.window.geometry("1200x800")
        self.window.resizable(False, False)

        default_bg = "#2b2b2b"

        # Background image
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
            icon = Feather("log-in", size=80).icon
            lbl_icon = tk.Label(self.window, image=icon, bg=default_bg)
            lbl_icon.place(relx=0.5, rely=0.20, anchor='center')

        tk.Label(self.window, text="Welcome back!", font=("Arial", 28, "bold"),
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

        # --- LOGIN BUTTON (no visual feedback on click) ---
        self.btn_login = tk.Button(
            self.window,
            text="LOGIN",
            command=self.login,
            bg=default_bg,
            fg="white",
            font=("Arial", 16, "bold"),
            padx=40,
            pady=12,
            relief=tk.FLAT,
            highlightthickness=0,      # remove focus ring
            takefocus=False            # prevent focus highlight
        )
        self.btn_login.place(relx=0.5, rely=0.68, anchor='center')

        # --- Sign-up link (no visual feedback) ---
        self.btn_signup = tk.Button(
            self.window,
            text="Don't have an account? Sign up",
            command=self.open_signup,
            bg=default_bg,
            fg="white",
            font=("Arial", 12),
            relief=tk.FLAT,
            highlightthickness=0,
            takefocus=False
        )
        self.btn_signup.place(relx=0.5, rely=0.78, anchor='center')

        self.entry_pass.bind("<Return>", lambda e: self.login())

    def login(self):
        SoundManager.play("click")
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()
        user_id = UserManager.login(username, password)
        if user_id:
            SoundManager.play("success")
            self.window.destroy()
            self.on_login_success(user_id, username)
        else:
            SoundManager.play("error")
            messagebox.showerror("Error", "Invalid username or password.")

    def open_signup(self):
        from gui.signup_window import SignUpWindow
        SoundManager.play("click")
        SignUpWindow(self.parent, on_success=self.autofill_login)

    def autofill_login(self, username, password):
        self.entry_user.delete(0, tk.END)
        self.entry_user.insert(0, username)
        self.entry_pass.delete(0, tk.END)
        self.entry_pass.insert(0, password)