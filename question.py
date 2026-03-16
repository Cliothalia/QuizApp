import difflib

class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

        self.attempts = 0
        self.review = False
    
    def reset(self):
        self.attempts = 0
        self.review = False
    
    def ask_typing(self):
        while True:
            user = input("Answer (Enter for hint): ").strip()

            # Correct answer
            if self.is_correct(user):
                print("Correct!")
                return True

            # User asked for hint
            if user == "":
                if self.attempts < 2:
                    self.show_hint()
                else:
                    self.force_copy()
                    return False
            
            # Wrong answer
            else:
                print(self.mask_answer(user))
            
            self.attempts += 1

            # Too many attempts --> reveal answer
            if self.attempts >= 3:
                self.force_copy()
                return False
    
    def is_correct(self, user):
        # Return True if user answer is close enough to correct answer.

        user = user.strip().lower()
        answer = self.answer.strip().lower()

        ratio = difflib.SequenceMatcher(None, user, answer).ratio()
        # Ratio set to 90% correct
        return ratio >= 0.9
            
    def ask_flashcard(self):
        input("Press Enter to see the answer...")
        print("Answer: ", self.answer)
        
        knew_it = input("Did you know it? (y/n): ").strip().lower()
        if knew_it != "y":
            self.review = True

    def mask_answer(self, user):
        result = []

        for real, typed in zip(self.answer, user):
            if real == typed:
                result.append(real)
            elif real == " ":
                result.append(" ")
            else:
                result.append(".")
        
        result += ["." for _ in range(len(self.answer) - len(user))]

        return "".join(result)
    
    def force_copy(self):
        print("\nThe correct answer is: ", self.answer)

        input("Type the answer to continue (or press Enter to skip): ")

        self.review = True
    
    def show_hint(self):
        words = self.answer.split()

        hints = []

        for word in words:
            if self.attempts == 0:
                hints.append(word[0] + "." * (len(word) - 1))
            elif self.attempts == 1:
                hints.append(word[:2] + "." * (len(word) - 2))

        print("Hint: ", " ".join(hints))