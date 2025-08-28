import tkinter as tk
import random
from vocabulary import vocab
from paradigm import paradigms


class SwedishLearningGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Swedish Learning Game")
        self.score = 0  # Score will not reset when switching categories
        self.mode = "vocab"  # "vocab" or "paradigm"
        self.current_category = None
        self.current_word = None
        self.current_translation = None
        self.current_infinitive = None
        self.current_forms = None  # (simple_past, past_participle)
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

        # Verb paradigms mode button
        self.paradigm_button = tk.Button(self.category_frame, text="Verb paradigms", command=self.start_paradigm_mode)
        self.paradigm_button.pack(side="left", padx=5)

        # Quiz frame
        self.quiz_frame = tk.Frame(root)

        # English word label
        self.word_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 14))
        self.word_label.pack(pady=5)

        # Entry boxes
        # For vocab mode (single answer)
        self.answer_entry = tk.Entry(self.quiz_frame, font=("Helvetica", 14))
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind("<Return>", self.check_answer)

        # For paradigm mode (two answers)
        self.past_label = tk.Label(self.quiz_frame, text="Simple past:", font=("Helvetica", 12))
        self.past_entry = tk.Entry(self.quiz_frame, font=("Helvetica", 14))
        self.participle_label = tk.Label(self.quiz_frame, text="Past participle:", font=("Helvetica", 12))
        self.participle_entry = tk.Entry(self.quiz_frame, font=("Helvetica", 14))
        # Not packed by default; will be packed in paradigm mode
        self.past_entry.bind("<Return>", self.check_paradigm_answer)
        self.participle_entry.bind("<Return>", self.check_paradigm_answer)

        # Check answer button (dynamically bound based on mode)
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
        self.mode = "vocab"
        self.current_category = category
        self.used_words = []  # Clear used words for the new category
        self._show_vocab_widgets()
        self.update_score()
        self.show_next_word()
        self.quiz_frame.pack(pady=10)

    def start_paradigm_mode(self):
        """Start verb paradigms mode (infinitive → simple past + past participle)."""
        self.mode = "paradigm"
        self.current_category = None
        self.used_words = []
        self._show_paradigm_widgets()
        self.update_score()
        self.show_next_paradigm()
        self.quiz_frame.pack(pady=10)

    def _show_vocab_widgets(self):
        """Configure widgets for vocab mode."""
        # Ensure paradigm widgets are hidden
        self._hide_paradigm_widgets()
        # Ensure vocab widgets are visible and button is bound correctly
        if not self.answer_entry.winfo_ismapped():
            self.answer_entry.pack(pady=5)
        self.check_button.config(command=self.check_answer)
        self.answer_entry.bind("<Return>", self.check_answer)

    def _show_paradigm_widgets(self):
        """Configure widgets for paradigm mode."""
        # Hide vocab widgets (ensure it's forgotten even if not yet mapped)
        self.answer_entry.pack_forget()
        # Show paradigm widgets
        self.past_label.pack(pady=(10, 0))
        self.past_entry.pack(pady=5)
        self.participle_label.pack(pady=(10, 0))
        self.participle_entry.pack(pady=5)
        self.check_button.config(command=self.check_paradigm_answer)
        self.past_entry.bind("<Return>", self.check_paradigm_answer)
        self.participle_entry.bind("<Return>", self.check_paradigm_answer)

    def _hide_paradigm_widgets(self):
        if self.past_label.winfo_ismapped():
            self.past_label.pack_forget()
        if self.past_entry.winfo_ismapped():
            self.past_entry.pack_forget()
        if self.participle_label.winfo_ismapped():
            self.participle_label.pack_forget()
        if self.participle_entry.winfo_ismapped():
            self.participle_entry.pack_forget()

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

    def show_next_paradigm(self):
        """Select a new infinitive that hasn't been used in this mode."""
        remaining = [item for item in paradigms.items() if item not in self.used_words]
        if remaining:
            self.current_infinitive, self.current_forms = random.choice(remaining)
            self.used_words.append((self.current_infinitive, self.current_forms))
            self.word_label.config(text=f"Provide the two other forms for the verb {self.current_infinitive.upper()}")
            self.past_entry.delete(0, tk.END)
            self.participle_entry.delete(0, tk.END)
            self.feedback_label.config(text="")
        else:
            self.word_label.config(text="All verbs have been used in Verb paradigms mode!")
            self.feedback_label.config(text="Choose another mode to continue.", fg="blue")

    def check_answer(self, event=None):
        """Check if the user's answer is correct."""
        user_answer = self.answer_entry.get().strip().lower()
        if user_answer == self.current_translation:
            self.feedback_label.config(text="Correct!", fg="green")
            self.score += 1
            # Briefly show feedback before moving on
            delay_ms = 800
        else:
            self.feedback_label.config(text=f"Incorrect. The correct answer is '{self.current_translation}'.", fg="red")
            # Give the user time to read the correct answer
            delay_ms = 2500
        self.update_score()
        # Temporarily disable controls while showing feedback
        self.answer_entry.config(state="disabled")
        self.check_button.config(state="disabled")
        self.root.after(delay_ms, self._next_question)

    def check_paradigm_answer(self, event=None):
        """Check answers for paradigm mode."""
        simple_past_expected, past_participle_expected = self.current_forms
        user_past = self.past_entry.get().strip().lower()
        user_participle = self.participle_entry.get().strip().lower()

        past_correct = user_past == simple_past_expected
        part_correct = user_participle == past_participle_expected

        if past_correct and part_correct:
            self.feedback_label.config(text="Correct!", fg="green")
            self.score += 1
            delay_ms = 800
        else:
            self.feedback_label.config(
                text=f"Incorrect. Correct forms: {simple_past_expected}, {past_participle_expected}.",
                fg="red",
            )
            delay_ms = 2500
        self.update_score()
        # Temporarily disable controls while showing feedback
        self.past_entry.config(state="disabled")
        self.participle_entry.config(state="disabled")
        self.check_button.config(state="disabled")
        self.root.after(delay_ms, self._next_paradigm_question)

    def update_score(self):
        """Update the score display."""
        self.score_label.config(text=f"Score: {self.score}")

    def _next_question(self):
        """Re-enable controls and advance to the next word."""
        self.answer_entry.config(state="normal")
        self.check_button.config(state="normal")
        self.show_next_word()

    def _next_paradigm_question(self):
        """Re-enable controls and advance to the next verb in paradigm mode."""
        self.past_entry.config(state="normal")
        self.participle_entry.config(state="normal")
        self.check_button.config(state="normal")
        self.show_next_paradigm()

# Run the application
root = tk.Tk()
game = SwedishLearningGame(root)
root.mainloop() 
