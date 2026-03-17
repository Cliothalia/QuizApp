from question_bank import QuestionBank
from question import Question
    


class Quiz:
    def __init__(self, topic, max_questions, mode):
        # Initialize quiz based on user input
        self.bank = QuestionBank(topic)
        self.max_questions = max_questions
        self.mode = mode

        # Used for tracking questions used
        # Stores questions for current round
        self.current_questions = []
        # Stores wrong questions from current round
        self.wrong_questions = []
        # Stores all questions asked over all quizes
        self.asked_questions = []

        # Score tracking
        self.total_answered = 0
        self.total_correct = 0
    
    def new_round(self):
        # Prepares questions
        pairs = self.bank.get_questions(self.max_questions)

        # Fill self.current_questions with pairs of questions and answers corresponding to self.max_questions
        self.current_questions = [Question(q, a) for q, a in pairs]

        # Track questions asked without duplicates
        for q in self.current_questions:
            if q not in self.asked_questions:
                self.asked_questions.append(q)

    def ask_round(self):
        # Reset wrong questions
        self.wrong_questions = []

        # Loop through questions for this round
        for q in self.current_questions:
            # Print question to user
            print("\n", q.question)
            correct = False

            # If mode is 'typing', use typing 
            if self.mode == "t":
                correct = self.ask_typing(q)
            
            # If mode is 'flashcard', use flashcard
            elif self.mode == "f":
                correct = self.ask_flashcard(q)
            
            # Track progress
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
        # Typing mode
        while True:
            user = input("Answer (Enter for hint): ").strip()
            
            # Check whether user input was a command
            if q.check_command(user, self):
                continue

            # Correct answer
            if q.is_correct(user):
                print("Correct!")
                return True

            # User asked for hint by pressing Enter
            if user == "":
                if q.attempts < 2:
                    q.show_hint()
                else:
                    # After three attempts, display full answer and let user copy answer
                    q.force_copy()
                    return False
            
            # Wrong answer
            else:
                print(q.mask_answer(user))
            
            # Increase attempts
            q.attempts += 1

            # Too many attempts --> reveal answer
            if q.attempts >= 3:
                q.force_copy()
                return False

    def ask_flashcard(self, q):
        # Flashcard mode
        while True:
            # Let user press enter to show answer, or type a command
            user = input("Press Enter to see the answer or type a command (/help for commands): ").strip()

            # Check for command
            if q.check_command(user, self):
                continue
            
            # Show answer if user presses Enter
            if user == "":
                print("Answer: ", q.answer)

                # Let user answer whether they knew the answer
                knew_it = input("Did you know it? (y/n): ").strip().lower()

                # Add question to review if user did not know the answer
                if knew_it != "y":
                    q.review = True

                return True

    def choose_next(self):
        # All questions in quiz loop are answered. Ask user what they want to do next
        print("\nOptions:")

        print("1. New Questions")

        print("2. Review All (Current Round)")
        
        print("3. Review All Asked Questions")
        
        # Only show option if user got questions wrong
        if self.wrong_questions:
            print("4. Review wrong")
        
        # User input choice. Can only be a number
        while True:
            try:
                choice = int(input("> "))
                break
            except ValueError:
                print("Input was not a number. Try again")

        # Choice 1: Get a new set of questions, if there are still questions to be asked
        if choice == 1:
            if not self.bank.unused_questions:
                print("No new questions left!")
            else:
                self.new_round()

        # Choice 2: Review all questions in the current round. Resets all current questions to original state
        elif choice == 2:
            for q in self.current_questions:
                q.reset()
        
        # Choice 3: Review all asked questions. Resets current questions to asked questions and resets questions to original state
        elif choice == 3:
            self.current_questions = self.asked_questions.copy()

            for q in self.current_questions:
                q.reset()

        # Choice 4: Review all wrong questions. Resets current questions to wrong questions and resets questions to original state
        elif choice == 4 and self.wrong_questions:
            self.current_questions = self.wrong_questions
            for q in self.current_questions:
                q.reset()