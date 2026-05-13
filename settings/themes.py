LIGHT_THEME = {
    "bg": "#FFFFFF",
    "fg": "#000000",
    "button_bg": "#E0E0E0",
    "button_fg": "#000000"
}

DARK_THEME = {
    "bg": "#1E1E1E",
    "fg": "#FFFFFF",
    "button_bg": "#333333",
    "button_fg": "#FFFFFF"
}
# fuction that will allow the theme to be switched this calls the FG & BG variable that were made in the theme settings above Lines 1-13. 

def apply_theme(root, theme):
    root.configure(bg = theme["bg"])
    for widget in root.winfo.children():
        widget.configure(bg = theme["bg"], fg = theme["fg"])





