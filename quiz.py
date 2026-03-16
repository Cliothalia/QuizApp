from question_bank import QuestionBank
from question import Question
    


class Quiz:
    def __init__(self, topic, max_questions, mode):
        self.bank = QuestionBank(topic)
        self.max_questions = max_questions
        self.mode = mode

        self.current_questions = []
        self.wrong_questions = []

        # Score tracking
        self.total_answered = 0
        self.total_correct = 0
    
    def new_round(self):
        pairs = self.bank.get_questions(self.max_questions)

        self.current_questions = [Question(q, a) for q, a in pairs]

    def ask_round(self):
        self.wrong_questions = []

        for q in self.current_questions:
            print("\n", q.question)

            if self.mode == "typing":
                correct = q.ask_typing()
            
            elif self.mode == "flashcard":
                q.ask_flashcard()
                correct = not q.review
            
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

    def choose_next(self):
        print("\nOptions:")

        print("1. New Questions")

        if self.current_questions:
            print("2. Review All")
        
        if self.wrong_questions:
            print("3. Review wrong")
        
        choice = int(input("> "))

        if choice == 1:
            self.new_round()
        elif choice == 2:
            for q in self.current_questions:
                q.reset()
        elif choice == 3:
            self.current_questions = self.wrong_questions
            for q in self.current_questions:
                q.reset()