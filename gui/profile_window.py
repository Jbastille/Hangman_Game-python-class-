import tkinter as tk
from tkinter import messagebox
from database.user_manager import UserManager
from database.score_manager import ScoreManager
from gui.sound_manager import SoundManager

class ProfileWindow:
    def __init__(self, parent, user_id: int, username: str):
        self.parent = parent
        self.user_id = user_id
        self.current_username = username
        
        self.window = tk.Toplevel(parent)
        self.window.title("My Profile - Hangman")
        self.window.geometry("1200x800")
        self.window.resizable(False, False)
        
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
        
        SoundManager.play("pop")
        
        # Title
        tk.Label(self.window, text="User Profile", font=("Arial", 32, "bold"),
                 bg=default_bg, fg="white").pack(pady=(40, 20))
        
        # --- Username section ---
        frame_username = tk.Frame(self.window, bg=default_bg)
        frame_username.pack(pady=20)
        
        tk.Label(frame_username, text="Username:", font=("Arial", 20),
                 bg=default_bg, fg="white").grid(row=0, column=0, padx=10)
        
        self.username_label = tk.Label(frame_username, text=self.current_username,
                                       font=("Arial", 20, "bold"),
                                       bg=default_bg, fg="#4CAF50")
        self.username_label.grid(row=0, column=1, padx=10)
        
        self.edit_btn = tk.Button(frame_username, text="Edit", command=self.edit_username,
                                  bg=default_bg, fg="white", font=("Arial", 14),
                                  relief=tk.FLAT, highlightthickness=0, takefocus=False)
        self.edit_btn.grid(row=0, column=2, padx=10)
        
        # --- Change Password button (new) ---
        self.change_pw_btn = tk.Button(self.window, text="Change Password",
                                       command=self.change_password_dialog,
                                       bg=default_bg, fg="white", font=("Arial", 14),
                                       relief=tk.FLAT, highlightthickness=0, takefocus=False)
        self.change_pw_btn.pack(pady=10)
        
        # --- Statistics section ---
        stats = ScoreManager.get_user_stats(self.user_id)
        total_games = stats.get('total_games', 0)
        wins = stats.get('wins', 0)
        total_score = stats.get('total_score', 0)
        avg_score = stats.get('avg_score', 0) or 0
        
        frame_stats = tk.Frame(self.window, bg=default_bg)
        frame_stats.pack(pady=30)
        
        stats_text = f"Games played: {total_games}\nWins: {wins}\nTotal score: {total_score}\nAverage score: {avg_score:.1f}"
        tk.Label(frame_stats, text=stats_text, font=("Arial", 18),
                 bg=default_bg, fg="white", justify=tk.LEFT).pack()
        
        # Close button
        tk.Button(self.window, text="Close", command=self.window.destroy,
                  bg=default_bg, fg="white", font=("Arial", 14),
                  relief=tk.FLAT, highlightthickness=0, takefocus=False).pack(pady=30)
    
    def edit_username(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Change Username")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.configure(bg="#2b2b2b")
        
        tk.Label(dialog, text="New username:", font=("Arial", 14),
                 bg="#2b2b2b", fg="white").pack(pady=(20, 5))
        entry = tk.Entry(dialog, width=30, font=("Arial", 12))
        entry.pack(pady=5)
        entry.insert(0, self.current_username)
        entry.focus()
        
        def apply():
            new_name = entry.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Username cannot be empty.")
                return
            if new_name == self.current_username:
                dialog.destroy()
                return
            success = UserManager.update_username(self.user_id, new_name)
            if success:
                SoundManager.play("success")
                self.current_username = new_name
                self.username_label.config(text=new_name)
                messagebox.showinfo("Success", f"Username changed to {new_name}")
                dialog.destroy()
            else:
                SoundManager.play("error")
                messagebox.showerror("Error", "Username already taken.")
        
        tk.Button(dialog, text="Save", command=apply,
                  bg="#2b2b2b", fg="white", font=("Arial", 12),
                  relief=tk.FLAT, highlightthickness=0, takefocus=False).pack(pady=10)
        
        dialog.bind("<Return>", lambda e: apply())
    
    # --- New method: change password dialog ---
    def change_password_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Change Password")
        dialog.geometry("450x250")
        dialog.resizable(False, False)
        dialog.configure(bg="#2b2b2b")
        
        tk.Label(dialog, text="Change your password", font=("Arial", 14, "bold"),
                 bg="#2b2b2b", fg="white").pack(pady=(15, 10))
        
        # Current password
        tk.Label(dialog, text="Current password:", font=("Arial", 12),
                 bg="#2b2b2b", fg="white").pack(pady=(10,0))
        old_entry = tk.Entry(dialog, show="*", width=30, font=("Arial", 12))
        old_entry.pack(pady=5)
        
        # New password
        tk.Label(dialog, text="New password:", font=("Arial", 12),
                 bg="#2b2b2b", fg="white").pack(pady=(10,0))
        new_entry = tk.Entry(dialog, show="*", width=30, font=("Arial", 12))
        new_entry.pack(pady=5)
        
        # Confirm new password
        tk.Label(dialog, text="Confirm new password:", font=("Arial", 12),
                 bg="#2b2b2b", fg="white").pack(pady=(10,0))
        confirm_entry = tk.Entry(dialog, show="*", width=30, font=("Arial", 12))
        confirm_entry.pack(pady=5)
        
        def apply_change():
            old = old_entry.get()
            new = new_entry.get()
            confirm = confirm_entry.get()
            if not old or not new or not confirm:
                messagebox.showerror("Error", "All fields are required.")
                return
            if new != confirm:
                messagebox.showerror("Error", "New passwords do not match.")
                return
            if len(new) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters.")
                return
            
            success = UserManager.change_password(self.user_id, old, new)
            if success:
                SoundManager.play("success")
                messagebox.showinfo("Success", "Password changed successfully.")
                dialog.destroy()
            else:
                SoundManager.play("error")
                messagebox.showerror("Error", "Current password is incorrect.")
        
        btn_frame = tk.Frame(dialog, bg="#2b2b2b")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Change", command=apply_change,
                  bg="#2b2b2b", fg="white", font=("Arial", 12),
                  relief=tk.FLAT, highlightthickness=0, takefocus=False).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                  bg="#2b2b2b", fg="white", font=("Arial", 12),
                  relief=tk.FLAT, highlightthickness=0, takefocus=False).pack(side=tk.LEFT, padx=10)
        
        # Bind Enter key
        dialog.bind("<Return>", lambda e: apply_change())
        old_entry.focus()