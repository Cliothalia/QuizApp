import csv
import random

class QuestionBank:
    def __init__(self, topic):
        self.topic = topic
        self.full_qa_dict = {}
        self.unused_questions = {}
        self.load_questions()

    def load_questions(self):
        filename = self.topic.lower().replace(" ", "_")
        with open(f'quiz_database/{filename}.csv', 'r') as file:
            csvFile = csv.reader(file, delimiter=';')
            for line in csvFile:
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
        self.first_run = False
        self.questions_to_review = {}

    def prepare_questions(self):
        self.questions_to_ask = {}
        for i in range(self.max_questions):
            q, a = self.bank.get_random_question()
            self.questions_to_ask[q] = a

    def start(self):
        if self.mode == "typing" or self.mode == 't':
            self.mode = "Typing"
        elif self.mode == "flashcard" or self.mode == 'f':
            self.mode = "Flashcard"
    
    def typing_mode(self):
        pass

    def flashcard_mode(self):
        pass

if __name__ == "__main__":
    topic = input("Choose topic: ")
    if topic == "":
        topic = "Network Security"
    mode = input("Mode (typing/flashcard): ")
    max_questions = int(input("How many questions? "))

    quiz = Quiz(topic, mode, max_questions)
    quiz.start()