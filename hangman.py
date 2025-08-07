import tkinter as tk
from tkinter import messagebox

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.configure(bg="#f0e68c")
        self.words = [
            ("success", "Easy", "It is related to victory"),
            ("winner", "Medium", "Word is related to success"),
            ("victory", "Hard", "It is related to winning"),
            ("triumph", "Extreme Hard", "It is related to success"),
            ("nevergiveup", "Impossible", "Famous motto of a famous wrestler")
        ]
        self.difficulty_frame = tk.Frame(master, bg="#f0e68c")
        self.difficulty_frame.pack(pady=30)
        tk.Label(self.difficulty_frame, text="Choose Difficulty", font=("Arial", 16, "bold"), bg="#f0e68c", fg="#2e8b57").pack(pady=5)
        for idx, (_, level, _) in enumerate(self.words):
            tk.Button(
                self.difficulty_frame,
                text=f"{idx+1}. {level}",
                font=("Arial", 12, "bold"),
                bg="#e0ffff",
                fg="#191970",
                width=18,
                command=lambda i=idx: self.start_game(i)
            ).pack(pady=3)

    def start_game(self, idx):
        self.secret_word, level, self.hint_text = self.words[idx]
        self.hint_used = False
        self.guessed_letters = []
        self.wrong_guesses = []
        self.tries = 6
        self.difficulty_frame.destroy()

        self.word_var = tk.StringVar()
        self.update_display_word()

        tk.Label(self.master, text=f"Welcome to Hangman! ({level})", font=("Arial", 16, "bold"), bg="#f0e68c", fg="#2e8b57").pack(pady=5)
        self.word_label = tk.Label(self.master, textvariable=self.word_var, font=("Consolas", 24, "bold"), bg="#f0e68c", fg="#191970")
        self.word_label.pack(pady=10)

        self.canvas = tk.Canvas(self.master, width=200, height=250, bg="#fffacd", highlightthickness=2, highlightbackground="#2e8b57")
        self.canvas.pack(pady=10)
        self.draw_hangman()

        self.entry = tk.Entry(self.master, font=("Arial", 14), justify="center", bg="#e0ffff")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.guess_letter)

        # Hint button
        self.hint_button = tk.Button(self.master, text="Hint", font=("Arial", 12, "bold"), bg="#ffecb3", fg="#b22222", command=self.show_hint)
        self.hint_button.pack(pady=5)

        self.info_var = tk.StringVar()
        self.info_label = tk.Label(self.master, textvariable=self.info_var, font=("Arial", 12), bg="#f0e68c", fg="#b22222")
        self.info_label.pack(pady=5)

        self.guessed_label = tk.Label(self.master, text="Guessed letters: []", font=("Arial", 12), bg="#f0e68c", fg="#8b008b")
        self.guessed_label.pack()
        self.wrong_label = tk.Label(self.master, text="Wrong guesses: []", font=("Arial", 12), bg="#f0e68c", fg="#b22222")
        self.wrong_label.pack()
        self.tries_label = tk.Label(self.master, text=f"Tries left: {self.tries}", font=("Arial", 12, "bold"), bg="#f0e68c", fg="#191970")
        self.tries_label.pack()

    def show_hint(self):
        if not self.hint_used:
            messagebox.showinfo("Hint", self.hint_text)
            self.hint_used = True
            self.hint_button.config(state=tk.DISABLED)
        else:
            self.info_var.set("Hint already used!")

    def update_display_word(self):
        display_word = ""
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        self.word_var.set(display_word.strip())

    def draw_hangman(self):
        self.canvas.delete("all")
        # Draw gallows
        self.canvas.create_line(20, 230, 180, 230, width=3, fill="#8b4513")  # base
        self.canvas.create_line(50, 230, 50, 20, width=3, fill="#8b4513")    # pole
        self.canvas.create_line(50, 20, 130, 20, width=3, fill="#8b4513")    # top
        self.canvas.create_line(130, 20, 130, 50, width=3, fill="#8b4513")   # rope

        wrong = len(self.wrong_guesses)
        # Draw hangman step by step with color
        if wrong > 0:
            self.canvas.create_oval(110, 50, 150, 90, width=3, outline="#191970", fill="#ffe4e1")  # head
        if wrong > 1:
            self.canvas.create_line(130, 90, 130, 160, width=3, fill="#191970")  # body
        if wrong > 2:
            self.canvas.create_line(130, 110, 110, 140, width=3, fill="#191970")  # left arm
        if wrong > 3:
            self.canvas.create_line(130, 110, 150, 140, width=3, fill="#191970")  # right arm
        if wrong > 4:
            self.canvas.create_line(130, 160, 110, 200, width=3, fill="#191970")  # left leg
        if wrong > 5:
            self.canvas.create_line(130, 160, 150, 200, width=3, fill="#191970")  # right leg

    def guess_letter(self, event=None):
        user = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        if not user or len(user) != 1 or not user.isalpha():
            self.info_var.set("Please enter a single letter.")
            return

        if user in self.guessed_letters or user in self.wrong_guesses:
            self.info_var.set("You already guessed that letter. Try again.")
            return

        if user in self.secret_word:
            self.guessed_letters.append(user)
            self.info_var.set("Good guess!")
        else:
            self.wrong_guesses.append(user)
            self.tries -= 1
            self.info_var.set(f"Wrong guess! You have {self.tries} tries left.")

        self.guessed_label.config(text=f"Guessed letters: {self.guessed_letters}")
        self.wrong_label.config(text=f"Wrong guesses: {self.wrong_guesses}")
        self.tries_label.config(text=f"Tries left: {self.tries}")
        self.update_display_word()
        self.draw_hangman()

        if all(letter in self.guessed_letters for letter in self.secret_word):
            messagebox.showinfo("Hangman", f"Congratulations! You've guessed the word: {self.secret_word}")
            self.master.destroy()
        elif self.tries == 0 or len(self.wrong_guesses) > 5:
            self.draw_hangman()
            messagebox.showinfo("Hangman", f"Sorry, you've run out of tries. The word was: {self.secret_word}")
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()