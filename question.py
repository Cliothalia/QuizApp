import difflib
from colorama import Fore, Style

class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

        self.attempts = 0
        self.review = False
    
    def reset(self):
        # Reset question to original state
        self.attempts = 0
        self.review = False
    
    def is_correct(self, user):
        # Return True if user answer is close enough to correct answer.
        user = user.strip().lower()
        answer = self.answer.strip().lower()

        ratio = difflib.SequenceMatcher(None, user, answer).ratio()

        # Ratio set to 90% correct
        return ratio >= 0.9
            
    def mask_answer(self, user):
        # Compares user answer with actual answer in typing mode. Displays correct letters and displays '.' or ' ' for incorrect letters
        result = []

        for real, typed in zip(self.answer, user):
            if real == typed:
                result.append(real)
            elif real == " ":
                result.append(" ")
            else:
                result.append(".")
        
        # If user answer is shorter than actual answer, add '.' for any remaining letters
        result += ["." for _ in range(len(self.answer) - len(user))]

        # Return the result answer
        return "".join(result)
    
    def force_copy(self):
        # After three tries, user is forced to copy full answer
        # Display correct answer
        print("\nThe correct answer is: ", self.answer)

        # Give user opportunity to copy correct answer, but do not check whether it is correct
        input("Type the answer to continue (or press Enter to skip): ")

        # Add question to review if it is copied
        self.review = True
    
    def show_hint(self):
        # When user presses Enter, show first letter of each word as hint
        words = self.answer.split()

        hints = []

        for word in words:
            # For first hint, show the first letter of each word
            if self.attempts == 0:
                hints.append(word[0] + "." * (len(word) - 1))
            # For second hint, show the first two letters of each word
            elif self.attempts == 1:
                hints.append(word[:2] + "." * (len(word) - 2))

        # Print hint to user
        print("Hint: ", " ".join(hints))
    
    def check_command(self, user, quiz):
        # Checks whether user typed in a command. All commands start with '/'

        # Return if user input is not a command
        if not user.startswith("/"):
            return False
        
        # Reset command: Resets round with current questions
        if user == "/reset":
            print(Fore.RED + "\nResetting current round...")
            print(Style.RESET_ALL)
            for q in quiz.current_questions:
                q.reset()
            return True
        
        # Mode command: Switches between typing and flashcard mode
        elif user == "/mode":
            old_mode = quiz.mode
            quiz.mode = "f" if quiz.mode == "t" else "t"
            print(Fore.RED + f"\nSwitched mode from {old_mode} -> {quiz.mode}")
            print(Style.RESET_ALL)
            return True
        
        # Remaining command: Shows how many questions remain from the total number of questions in the bank
        elif user == "/remaining":
            total = len(quiz.bank.all_questions)
            left = len(quiz.bank.unused_questions)
            print(Fore.RED + f"\nQuestions remaining in bank: {left} / {total}")
            print(Style.RESET_ALL)
            return True

        # Help command: shows all commands
        elif user == "/help":
            print(Fore.RED + "Commands currently in use:")
            print("/reset   /mode   /remaining  /progress")
            print(Style.RESET_ALL)

        # Progress command: shows how many questions have been asked so far, how many were correct and user accuracy
        elif user == "/progress":
            print(Fore.RED + f"Questions asked so far: {quiz.total_answered}")
            print(f"Correct answers: {quiz.total_correct}")
            print(f"Accuracy: {quiz.total_correct/quiz.total_answered*100:.0f} %")
            print(Style.RESET_ALL)
