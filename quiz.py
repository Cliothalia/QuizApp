import csv
import random

class QuestionBank:
    def __init__(self, topic):
        topic_file = topic.lower().replace(" ", "_") if topic else "network_security"

        self.all_questions = []
        self.unused_questions = []

        with open(f"quiz_database/{topic_file}.csv") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:

                if len(row) < 2:
                    continue

                q, a = row[0].strip(), row[1].strip()

                if q and a:
                    self.all_questions.append((q, a))
        
        self.unused_questions = self.all_questions.copy()
    
    def get_questions(self, amount):
        amount = min(amount, len(self.unused_questions))

        selected = random.sample(self.unused_questions, amount)

        for q in selected:
            self.unused_questions.remove(q)
        
        return selected
    
class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

        self.attempts = 0
        self.review = False
    
    def reset(self):
        self.attempts = 0
        self.review = False
    
    def ask(self):
        while True:
            user = input("Answer (Enter for hint): ").strip()

            # Correct answer
            if user.lower() == self.answer.lower():
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

class Quiz:
    def __init__(self, topic, max_questions, mode="typing"):
        self.bank = QuestionBank(topic)
        self.max_questions = max_questions
        self.mode = mode

        self.current_questions = []
        self.wrong_questions = []
    
    def new_round(self):
        pairs = self.bank.get_questions(self.max_questions)

        self.current_questions = [Question(q, a) for q, a in pairs]

    def ask_round(self):
        self.wrong_questions = []

        for q in self.current_questions:
            print("\n", q.question)

            if self.mode == "typing":
                correct = q.ask()

                if not correct:
                    self.wrong_questions.append(q)
            
            elif self.mode == "flashcard":
                input("Press Enter to see the answer...")
                print("Answer: ", q.answer)

                knew_it = input("Did you know it? (y/n): ").strip().lower()
                if knew_it != "y":
                    self.wrong_questions.append(q)
    
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

if __name__ == "__main__":

    topic = input("Choose topic: ")
    max_questions = int(input("Questions per round: "))
    mode = input("Mode (typing/flashcard): ").strip().lower()

    quiz = Quiz(topic, max_questions)

    quiz.new_round()

    while quiz.current_questions:
        quiz.ask_round()

        if not quiz.bank.unused_questions and not quiz.wrong_questions:
            print("\nQuiz finished!")
            break

        quiz.choose_next()