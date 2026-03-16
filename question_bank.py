import csv
import random

class QuestionBank:
    def __init__(self, topic):
        topic_file = topic.lower().replace(" ", "_") if topic else "network_security"

        self.all_questions = []
        self.unused_questions = []

        # Load questions from csv
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
    
