# The Art Dealer Game

## Overview
The Art Dealer Game is an educational simulation designed to help K-8 students learn computational thinking and pattern recognition through an interactive card game. Students try to identify the hidden patterns that determine which cards the Art Dealer (AI) will buy.

This implementation supports two students playing collaboratively, includes audio prompts and feedback, and features an assessment system to track student progress and learning outcomes.

## Features
- Three difficulty levels for different grade ranges (K-2, 3-5, 6-8)
- Two-student collaborative play with turn tracking
- Audio prompts and feedback for enhanced engagement
- Assessment tracking and reporting of student performance
- Interactive GUI built with Tkinter
- Randomized card selection
- Pattern-based gameplay that encourages computational thinking
- Age-appropriate challenges for each grade level
- Feedback through prompts and celebration effects

---

## Target Users
- **Students** (primary users)
- **Teachers** (facilitators)

---

## Installation

### Option 1: Run the Included Executable (Recommended)
1. Clone this repository or download the ZIP
```bash
git clone https://github.com/mariogee11/final-project
```

2. Navigate to the `dist` folder
3. Run `art_dealer_game.exe`

The executable is included in this repository and requires no additional installation or dependencies.

### Option 2: Run from Source Code
1. Clone this repository or download the ZIP
```bash
git clone https://github.com/mariogee11/final-project
```

2. (Optional but recommended) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install pygame
```

4. Run the game:
```bash
python art_dealer_game.py
```

### Building Your Own Executable
If you want to build your own executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --hidden-import=pygame --add-data "assets/audio;assets/audio" art_dealer_game.py
```
The .exe will be in the `dist/` folder.

---

## Game Rules
- Enter names for two students when prompted.
- Select your grade level.
- Take turns clicking on the 4 "Draw Card" buttons.
- The art dealer (AI) will buy cards matching a secret pattern.
- Students take turns making guesses.
- You have 3 attempts collectively to guess the correct card pattern.
- Win by matching the pattern and get a celebration message with audio feedback!
- View assessment statistics to track progress.

---

## Project Structure
```
art-dealer-game/
├── art_dealer_game.py       # Main Python source file
├── assets/
│   └── audio/               # Audio files for game sounds
├── dist/                    # Compiled executable
├── design document.docx     # Design specifications
├── user manual.docx         # User guide
├── README.md                # Project overview
├── .gitignore               # Git ignore file
└── assets/                  # (Optional) Sounds/images
```

---

## Requirements
- Python 3.8+
- Tkinter (usually comes with Python)
- PyInstaller (for building .exe)

---

## License
MIT License

---

## Created for
Software Engineering Course – Final Project (Lewis University)