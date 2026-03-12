import csv
import random

class QuestionBank:
    def __init__(self, topic):
        self.topic = topic
        self.full_qa_dict = {}
        self.unused_questions = {}
        self.load_questions()
    
    def load_questions(self):
        # Prep topic for finding file. If there is no topic, default to Network Security
        # TO DO: add topic handling
        if self.topic:
            topic_file = self.topic.lower().replace(' ', '_')
        else:
            topic_file = "network_security"

        # Get questions and answers from .csv file and add to dictionary
        with open(f'quiz_database/{topic_file}.csv', mode='r') as file:
            csvFile = csv.reader(file, delimiter=';')
            for line in csvFile:
                # Add questions and answers to dictionary. Questions = key, Answers = value
                self.full_qa_dict[line[0]] = line[1]
        
        self.unused_questions = self.full_qa_dict.copy()

    def get_random_question(self):
        question = random.choice(list(self.unused_questions.keys()))
        answer = self.unused_questions.pop(question)
        return question, answer

    def reset(self):
        self.unused_questions = self.full_qa_dict.copy()

class Quiz:
    def __init__(self, topic, mode, max_questions):
        self.bank = QuestionBank(topic)
        self.mode = mode.lower()
        self.max_questions = max_questions
        self.current_question = 0
        self.review_mode = "Normal"
        self.first_run = True
        self.questions_to_review = []
        self.questions_to_ask = []
    
    def prepare_questions(self):
        for i in range(self.max_questions):
            q, a = self.bank.get_random_question()
            question = Question(q, a)
            self.questions_to_ask.append(question)

class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.user_answer = ""
        self.display_answer = ""
        self.correct = False
        self.attempts = 0
        self.review = False
    
    def get_user_answer(self):
        while self.attempts < 3:
            self.user_answer = input("Answer: ")

            if self.user_answer == "":
                self.get_hint()
                print(self.display_answer)
            
            else:
                self.check_answer()

                if self.display_answer == self.answer:
                    print("Correct!")
                    self.correct = True
                    return
                else:
                    print(self.display_answer)
            self.attempts += 1
        
        # After 3 failed attempts
        self.force_copy()
    
    def force_copy(self):
        print(f"The correct answer is:\n{self.answer}")

        input("Type the answer to continue (or press Enter to skip): ")

        self.review = True

    def check_answer(self):
        result = []

        # Compare individual characters of what user typed to actual answer
        for real_char, user_char in zip(self.answer, self.user_answer):
            if real_char == user_char:
                result.append(real_char)
            elif real_char == " ":
                result.append(" ")
            else:
                result.append(".")
        
        # Handle remaining characters if user_answer is shorter
        if len(self.user_answer) < len(self.answer):
            for char in self.answer[len(self.user_answer):]:
                result.append(" " if char == " " else ".")
        
        self.display_answer = " ".join(result)

    def get_hint(self):
        # After three tries, display full answer
        if self.attempts > 3:
            self.display_answer = self.answer
            return

        result = []
        words = self.answer.split(" ")
        for word in words:
            if self.attempts == 0:
                # First hint: first letter only
                hint = word[0] + "." * (len(word) - 1)
            elif self.attempts == 1:
                # Second hint: first two letters
                hint = word[:2] + "." * (len(word) - 2)
            
            result.append(hint)
        
        self.display_answer = " ".join(result)


if __name__ == "__main__":
    topic = input("Choose topic: ")
    mode = input("Mode (typing/flashcard): ")
    max_questions = int(input("How many questions? "))

    quiz = Quiz(topic, mode, max_questions)

    # Prepare questions
    quiz.prepare_questions()

    for question in quiz.questions_to_ask:
        print(question.question)
        question.get_user_answer()

        if question.review:
            quiz.questions_to_review.append(question)
        print(question.display_answer)
