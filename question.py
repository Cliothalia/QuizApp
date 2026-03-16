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
    
    def is_correct(self, user):
        # Return True if user answer is close enough to correct answer.

        user = user.strip().lower()
        answer = self.answer.strip().lower()

        ratio = difflib.SequenceMatcher(None, user, answer).ratio()

        # Ratio set to 90% correct
        return ratio >= 0.9
            
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
    
    def check_command(self, user, quiz):
        if not user.startswith("/"):
            return False
        
        if user == "/reset":
            print("\nResetting current round...")
            for q in quiz.current_questions:
                q.reset()
            return True
        
        elif user == "/mode":
            old_mode = quiz.mode
            quiz.mode = "flashcard" if quiz.mode == "typing" else "typing"
            print(f"\nSwitched mode from {old_mode} -> {quiz.mode}")
            return True
        
        elif user == "/remaining":
            total = len(quiz.bank.all_questions)
            left = len(quiz.bank.unused_questions)
            print(f"\nQuestions remaining in bank: {left} / {total}")
            return True
        elif user == "/help":
            print("Commands currently in use:")
            print("/reset   /mode   /remaining  /progress")

        elif user == "/progress":
            print(f"Questions asked so far: {quiz.total_answered}")
            print(f"Correct answers: {quiz.total_correct}")
            print(f"Accuracy: {quiz.total_correct/quiz.total_answered*100:.0f} %")
