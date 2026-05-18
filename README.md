# Hangman_Game
🎮 Hangman Game — Python + Tkinter  + SQLite

A modern, feature‑rich Hangman game built with Python, Tkinter, Pillow, Pygame, and SQLite.  
Play as a **guest** or **create an account** to track your scores, view leaderboards, and manage your profile.

✨ Features
🧩 Multiple Categories
Choose from several themed word lists:

Animals

Food

Countries

Sports

Technology

Each category includes:

A unique background image

A themed color palette

Category‑specific background music

🎚️ Difficulty Levels
Three difficulty modes:

Easy — More lives, more time, unlimited reveals

Medium — Moderate lives, moderate time, 2 reveals

Hard — Fewer lives, less time, 1 reveal

Difficulty affects:

Lives

Timer duration

Reveal limits

⏳ Timer System
A dynamic countdown timer:

Starts automatically when the game begins

Updates every second

Stops on win/lose

Resets cleanly on restart

Cancels safely when switching screens

🔊 Sound & Music
Powered by Pygame:

Click sound for each letter

Win sound

Lose sound

Category‑specific background music

Menu theme music

🖼️ Custom Backgrounds
Each category loads a themed background image using Pillow (PIL):

Automatically resized to fit the window

Clean, modern UI layering

🧠 Hints & Reveals
Each word includes a hint.
Players can reveal hidden letters based on difficulty rules.

🔤 Interactive Letter Buttons
A–Z clickable buttons

Disable after use

Clean layout

Works with sound effects

🔁 Restart & Navigation
Restart the current game

Return to category selection

Return to main menu

---

## 👤 User System 

### 🔐 Guest or Account
- **Play as Guest** — play immediately, scores are **not** saved
- **Login / Sign Up** — create a personal account with hashed password storage

### 🏆 Leaderboard
- View global rankings by total score
- Displays rank, username, total score, games played, wins

### 📊 Profile & Stats
- View personal game statistics:
  - Total games played
  - Wins / Losses
  - Average score
  - Total score
- Change username
- Change password (requires current password)

### 💾 Score Tracking
- Every game result (word, difficulty, attempts, hints, time, win/loss) is saved to an SQLite database (`database/hangman.db`)
- Score is calculated dynamically:
  - Base points per difficulty
  - Bonus for remaining attempts
  - Penalty for hints used
  - Time bonus for fast wins
- Total score accumulates across all games
- Total_score = base_points + attempt_bonus - hint_penalty + time_bonus

### 👨‍💻 Database Structure
- `users` — username, password hash, creation date
- `scores` — game results (word, difficulty, attempts, hints, time, win, score)


---




▶️ How to Run
1. Install dependencies

-pip install pygame pillow
2. Run the game from the project root:

-python main.py

Important:  
Do not run files inside the gui/ folder directly — imports will break.

🛠️ Requirements
Python 3.8+

Tkinter (included with most Python installations)

Pillow

Pygame

SQLite3 

🚀 Future Improvements

Animated hangman graphics

Custom category editor

Online multiplayer mode

📜 License
This project is open for personal or educational use.
Feel free to modify and expand it.
