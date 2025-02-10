import tkinter as tk
from tkinter import messagebox
import random
from vocabulary import vocab


class SwedishLearningGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Swedish Learning Game")
        self.score = 0  # Score will not reset when switching categories
        self.current_category = None
        self.current_word = None
        self.current_translation = None
        self.used_words = []  # Track words that have already been shown

        # Title label
        self.title_label = tk.Label(root, text="Welcome to the Swedish Learning Game!", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Category Frame
        self.category_frame = tk.Frame(root)
        self.category_frame.pack(pady=10)

        # Category buttons
        for category in vocab.keys():
            button = tk.Button(self.category_frame, text=category.capitalize(), command=lambda cat=category: self.start_category(cat))
            button.pack(side="left", padx=5)

        # Quiz frame
        self.quiz_frame = tk.Frame(root)

        # English word label
        self.word_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 14))
        self.word_label.pack(pady=5)

        # Entry box for the Swedish translation
        self.answer_entry = tk.Entry(self.quiz_frame, font=("Helvetica", 14))
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind("<Return>", self.check_answer)

        # Check answer button
        self.check_button = tk.Button(self.quiz_frame, text="Check Answer", command=self.check_answer)
        self.check_button.pack(pady=5)

        # Feedback label
        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=5)

        # Score label
        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack(pady=10)

    def start_category(self, category):
        """Initialize the quiz for the chosen category without resetting the score."""
        self.current_category = category
        self.used_words = []  # Clear used words for the new category
        self.update_score()
        self.show_next_word()
        self.quiz_frame.pack(pady=10)

    def show_next_word(self):
        """Select a new word from the current category that hasn't been used."""
        if self.current_category:
            remaining_words = [word for word in vocab[self.current_category].items() if word not in self.used_words]

            if remaining_words:
                self.current_word, self.current_translation = random.choice(remaining_words)
                self.used_words.append((self.current_word, self.current_translation))  # Mark word as used
                self.word_label.config(text=f"What is the Swedish word for '{self.current_word}'?")
                self.answer_entry.delete(0, tk.END)
                self.feedback_label.config(text="")
            else:
                # All words have been used; notify the player
                self.word_label.config(text=f"All words in '{self.current_category}' have been used!")
                self.feedback_label.config(text="Select a new category to continue.", fg="blue")

    def check_answer(self, event=None):
        """Check if the user's answer is correct."""
        user_answer = self.answer_entry.get().strip().lower()
        if user_answer == self.current_translation:
            self.feedback_label.config(text="Correct!", fg="green")
            self.score += 1
        else:
            self.feedback_label.config(text=f"Incorrect. The correct answer is '{self.current_translation}'.", fg="red")
        self.update_score()
        self.show_next_word()

    def update_score(self):
        """Update the score display."""
        self.score_label.config(text=f"Score: {self.score}")

# Run the application
root = tk.Tk()
game = SwedishLearningGame(root)
root.mainloop()
