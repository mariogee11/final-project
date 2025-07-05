# The Art Dealer Game - Educational Simulation for K-8 Students
# Developed in Python using Tkinter for GUI and random for card logic

import random
import os
import sys

# Try to import pygame, but continue if it's not available
try:
    import pygame
    pygame_available = True
except ImportError:
    pygame_available = False
    print("Pygame not available. Audio features will be disabled.")

# Check if tkinter is available
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("Tkinter is not available in this Python environment. GUI will not be available.")
    tk = None

# Card deck setup
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Define card object
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def is_red(self):
        return self.suit in ['Hearts', 'Diamonds']

    def is_black(self):
        return self.suit in ['Clubs', 'Spades']

    def value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        if self.rank == 'Ace':
            return 1
        return int(self.rank)

# Generate a deck of 52 cards
def create_deck():
    return [Card(suit, rank) for suit in SUITS for rank in RANKS]

# Simple pattern logic for K-2 (e.g., all red)
def k2_pattern(card_list):
    return all(card.is_red() for card in card_list)

# Patterns for grades 3-5
PRIMES = {2, 3, 5, 7}
def is_prime(card):
    return card.value() in PRIMES

def g3_5_pattern(card_list):
    return all(is_prime(card) for card in card_list)

# Complex pattern for grades 6-8: e.g., total value equals 21
def g6_8_pattern(card_list):
    return sum(card.value() for card in card_list) == 21

# Assessment tracker for student performance
class AssessmentTracker:
    def __init__(self, student1_name, student2_name):
        self.students = {
            student1_name: {"games": 0, "guesses": 0, "correct": 0},
            student2_name: {"games": 0, "guesses": 0, "correct": 0}
        }
        self.current_student = student1_name
        self.student_names = [student1_name, student2_name]
        
    def switch_turn(self):
        """Switch to the other student's turn"""
        current_index = self.student_names.index(self.current_student)
        next_index = (current_index + 1) % len(self.student_names)
        self.current_student = self.student_names[next_index]
        return self.current_student
        
    def record_guess(self, correct):
        """Record a guess for the current student"""
        self.students[self.current_student]["guesses"] += 1
        if correct:
            self.students[self.current_student]["correct"] += 1
            self.students[self.current_student]["games"] += 1
            
    def get_stats(self):
        """Get statistics for all students"""
        stats = {}
        for name, data in self.students.items():
            accuracy = 0
            if data["guesses"] > 0:
                accuracy = (data["correct"] / data["guesses"]) * 100
            stats[name] = {
                "games": data["games"],
                "guesses": data["guesses"],
                "correct": data["correct"],
                "accuracy": f"{accuracy:.1f}%"
            }
        return stats
        
    def get_current_student(self):
        """Get the name of the current student"""
        return self.current_student

# AudioManager class
class AudioManager:
    def __init__(self):
        self.enabled = pygame_available
        if self.enabled:
            try:
                pygame.mixer.init()
                self.sounds = {}
                self.ensure_audio_files()
            except Exception as e:
                print(f"Error initializing audio: {e}")
                self.enabled = False
            
    def ensure_audio_files(self):
        """Create assets directory and check for audio files"""
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
            
        # We'll use text-to-speech or placeholder messages if no audio files exist
        print("Note: Add audio files to the assets directory for full audio experience")
        
    def play_sound(self, sound_name):
        """Play a sound by name"""
        if not self.enabled:
            return
            
        # Map of sound names to messages (for text-to-speech fallback)
        sound_messages = {
            "welcome": "Welcome to the Art Dealer Game! Select your grade level and draw cards.",
            "correct": "Congratulations! You guessed the pattern correctly!",
            "incorrect": "That's not the pattern. Try again!",
            "game_over": "Game over! The pattern was not guessed correctly.",
            "draw_card": "Card drawn!",
            "level_select": "You selected a new grade level.",
            "hint": "Here's a hint: look for patterns in color, suit, or value."
        }
        
        # Check if we have the sound file (try both .wav and .mp3)
        sound_file = None
        for ext in ['.wav', '.mp3']:
            temp_file = os.path.join("assets", f"{sound_name}{ext}")
            if os.path.exists(temp_file):
                sound_file = temp_file
                break
                
        # Load and play the sound if available
        if sound_file and sound_name not in self.sounds:
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(sound_file)
            except:
                print(f"Could not load sound: {sound_file}")
                
        # Play the sound if available
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            # Text-to-speech fallback (just print the message for now)
            print(f"Audio: {sound_messages.get(sound_name, 'Sound effect')}")

# Game class managing state
if tk:
    class ArtDealerGame:
        def __init__(self, master):
            self.master = master
            self.master.title("The Art Dealer Game")

            self.level = tk.StringVar(value="K-2")
            self.deck = create_deck()
            self.selected_cards = []
            self.guess_count = 0
            self.audio_manager = AudioManager()
            
            # Get student names
            self.get_student_names()
            
            self.setup_gui()
            
        def get_student_names(self):
            """Show dialog to get two student names"""
            name_dialog = tk.Toplevel(self.master)
            name_dialog.title("Enter Student Names")
            name_dialog.geometry("300x150")
            name_dialog.transient(self.master)
            name_dialog.grab_set()
            
            tk.Label(name_dialog, text="Enter names for two students:").pack(pady=5)
            
            frame1 = tk.Frame(name_dialog)
            frame1.pack(fill="x", padx=5, pady=5)
            tk.Label(frame1, text="Student 1:").pack(side="left")
            student1_entry = tk.Entry(frame1)
            student1_entry.pack(side="right", expand=True, fill="x")
            student1_entry.insert(0, "Student 1")
            
            frame2 = tk.Frame(name_dialog)
            frame2.pack(fill="x", padx=5, pady=5)
            tk.Label(frame2, text="Student 2:").pack(side="left")
            student2_entry = tk.Entry(frame2)
            student2_entry.pack(side="right", expand=True, fill="x")
            student2_entry.insert(0, "Student 2")
            
            def submit_names():
                name1 = student1_entry.get().strip() or "Student 1"
                name2 = student2_entry.get().strip() or "Student 2"
                self.assessment = AssessmentTracker(name1, name2)
                name_dialog.destroy()
                self.audio_manager.play_sound("welcome")
                
            tk.Button(name_dialog, text="Start Game", command=submit_names).pack(pady=10)
            
            # Wait for the dialog to be closed
            self.master.wait_window(name_dialog)

        def setup_gui(self):
            tk.Label(self.master, text="Select Grade Level:").pack()
            for level in ["K-2", "3-5", "6-8"]:
                tk.Radiobutton(self.master, text=level, variable=self.level, value=level).pack()

            self.card_frame = tk.Frame(self.master)
            self.card_frame.pack(pady=10)
            self.card_buttons = [tk.Button(self.card_frame, text="Draw Card", command=lambda i=i: self.draw_card(i)) for i in range(4)]
            for btn in self.card_buttons:
                btn.pack(side=tk.LEFT, padx=5)

            self.submit_button = tk.Button(self.master, text="Submit Guess", command=self.check_pattern)
            self.submit_button.pack(pady=5)
            
            # Add current student indicator
            self.turn_label = tk.Label(self.master, text="Current Turn: " + self.assessment.get_current_student(), font=("Arial", 10, "bold"))
            self.turn_label.pack(pady=5)
            
            # Add assessment button
            self.assessment_button = tk.Button(self.master, text="View Assessment", command=self.show_assessment)
            self.assessment_button.pack(pady=5)

        def draw_card(self, index):
            card = random.choice(self.deck)
            self.card_buttons[index].config(text=str(card))
            if len(self.selected_cards) <= index:
                self.selected_cards.append(card)
            else:
                self.selected_cards[index] = card
            self.audio_manager.play_sound("draw_card")

        def check_pattern(self):
            if len(self.selected_cards) < 4:
                messagebox.showinfo("Info", "Draw all 4 cards before guessing.")
                return

            level = self.level.get()
            self.guess_count += 1
            current_student = self.assessment.get_current_student()

            if level == "K-2":
                match = k2_pattern(self.selected_cards)
            elif level == "3-5":
                match = g3_5_pattern(self.selected_cards)
            else:
                match = g6_8_pattern(self.selected_cards)

            if match:
                messagebox.showinfo("Congratulations!", f"{current_student} guessed the correct pattern!")
                self.audio_manager.play_sound("correct")
                self.assessment.record_guess(True)
                self.reset_game()
            elif self.guess_count >= 3:
                messagebox.showinfo("Game Over", f"Out of guesses! Try again, {current_student}.")
                self.audio_manager.play_sound("game_over")
                self.assessment.record_guess(False)
                self.reset_game()
            else:
                next_student = self.assessment.switch_turn()
                messagebox.showinfo("Try Again", f"Wrong pattern! {3 - self.guess_count} guesses left.\nNow it's {next_student}'s turn.")
                self.audio_manager.play_sound("incorrect")
                self.turn_label.config(text="Current Turn: " + next_student)

        def reset_game(self):
            self.deck = create_deck()
            self.selected_cards = []
            self.guess_count = 0
            for btn in self.card_buttons:
                btn.config(text="Draw Card")
            # Switch to the next student for the new game
            next_student = self.assessment.switch_turn()
            self.turn_label.config(text="Current Turn: " + next_student)
            
        def show_assessment(self):
            """Show assessment statistics"""
            stats = self.assessment.get_stats()
            
            assessment_window = tk.Toplevel(self.master)
            assessment_window.title("Student Assessment")
            assessment_window.geometry("400x300")
            
            # Create headers
            headers = ["Student", "Games Won", "Total Guesses", "Correct Guesses", "Accuracy"]
            for i, header in enumerate(headers):
                tk.Label(assessment_window, text=header, font=("Arial", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)
            
            # Add student data
            row = 1
            for name, data in stats.items():
                tk.Label(assessment_window, text=name).grid(row=row, column=0, padx=5, pady=5)
                tk.Label(assessment_window, text=str(data["games"])).grid(row=row, column=1, padx=5, pady=5)
                tk.Label(assessment_window, text=str(data["guesses"])).grid(row=row, column=2, padx=5, pady=5)
                tk.Label(assessment_window, text=str(data["correct"])).grid(row=row, column=3, padx=5, pady=5)
                tk.Label(assessment_window, text=data["accuracy"]).grid(row=row, column=4, padx=5, pady=5)
                row += 1
                
            # Learning outcomes section
            tk.Label(assessment_window, text="Learning Outcomes:", font=("Arial", 10, "bold")).grid(row=row+1, column=0, columnspan=5, sticky="w", padx=5, pady=10)
            
            outcomes = {
                "K-2": "Pattern recognition with colors (red/black)",
                "3-5": "Identifying prime numbers (2, 3, 5, 7)",
                "6-8": "Addition and numerical patterns (sum equals 21)"
            }
            
            row += 2
            for level, outcome in outcomes.items():
                tk.Label(assessment_window, text=f"{level}: {outcome}").grid(row=row, column=0, columnspan=5, sticky="w", padx=5, pady=2)
                row += 1
                
            tk.Button(assessment_window, text="Close", command=assessment_window.destroy).grid(row=row+1, column=0, columnspan=5, pady=10)

    if __name__ == '__main__':
        root = tk.Tk()
        app = ArtDealerGame(root)
        root.mainloop()
else:
    print("This script requires Tkinter for the GUI. Please run it in a local Python environment where Tkinter is enabled.")