from question_bank import QuestionBank
from question import Question
    


class Quiz:
    def __init__(self, topic, max_questions, mode):
        self.bank = QuestionBank(topic)
        self.max_questions = max_questions
        self.mode = mode

        self.current_questions = []
        self.wrong_questions = []
        self.asked_questions = []

        # Score tracking
        self.total_answered = 0
        self.total_correct = 0
    
    def new_round(self):
        pairs = self.bank.get_questions(self.max_questions)

        self.current_questions = [Question(q, a) for q, a in pairs]

        # Track questions asked without duplicates
        for q in self.current_questions:
            if q not in self.asked_questions:
                self.asked_questions.append(q)

    def ask_round(self):
        self.wrong_questions = []

        for q in self.current_questions:
            print("\n", q.question)
            correct = False

            if self.mode == "typing":
                correct = self.ask_typing(q)
            
            elif self.mode == "flashcard":
                correct = self.ask_flashcard(q)
            
            self.progress(q, correct)

    def progress(self, q, correct):
        # Update score
        self.total_answered += 1
        if correct:
            self.total_correct += 1
        else:
            self.wrong_questions.append(q)
        
        # Progress feedback
        print(f"Progress: {self.total_answered} answered, {self.total_correct} correct\n"
                f"{self.total_correct/self.total_answered*100:.0f} %")

    def ask_typing(self, q):
        while True:
            user = input("Answer (Enter for hint): ").strip()
            
            # Check whether user input was a command
            if q.check_command(user, self):
                continue

            # Correct answer
            if q.is_correct(user):
                print("Correct!")
                return True

            # User asked for hint
            if user == "":
                if q.attempts < 2:
                    q.show_hint()
                else:
                    q.force_copy()
                    return False
            
            # Wrong answer
            else:
                print(q.mask_answer(user))
            
            q.attempts += 1

            # Too many attempts --> reveal answer
            if q.attempts >= 3:
                q.force_copy()
                return False

    def ask_flashcard(self, q):
        while True:
            user = input("Press Enter to see the answer or type a command: ").strip()

            if q.check_command(user, self):
                continue
            
            if user == "":
                print("Answer: ", q.answer)
                knew_it = input("Did you know it? (y/n): ").strip().lower()
                if knew_it != "y":
                    q.review = True

                return True

    def choose_next(self):
        print("\nOptions:")

        print("1. New Questions")

        if self.current_questions:
            print("2. Review All (Current Round)")
        
        if self.asked_questions:
            print("3. Review All Asked Questions")
        
        if self.wrong_questions:
            print("4. Review wrong")
        
        choice = int(input("> "))

        if choice == 1:
            if not self.bank.unused_questions:
                print("No new questions left!")
            else:
                self.new_round()

        elif choice == 2:
            for q in self.current_questions:
                q.reset()
        
        elif choice == 3:
            self.current_questions = self.asked_questions.copy()

            for q in self.current_questions:
                q.reset()

        elif choice == 4 and self.wrong_questions:
            self.current_questions = self.wrong_questions
            for q in self.current_questions:
                q.reset()