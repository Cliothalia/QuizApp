import csv
import random

class QuestionBank:
    def __init__(self, topic):
        topic_file = topic.lower().replace(" ", "_") if topic else "network_security"

        # Store all questions and answers from csv file. All_questions is only used to reset unused_questions 
        self.all_questions = []
        self.unused_questions = []

        # Load questions from csv
        with open(f"quiz_database/{topic_file}.csv") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                # Continue of answer or question is missing
                if len(row) < 2:
                    continue

                q, a = row[0].strip(), row[1].strip()

                # Store questions and answer in all_questions list
                if q and a:
                    self.all_questions.append((q, a))
        
        # Copy all_questions, so that a full copy of csv content always exists for reset purposes
        self.unused_questions = self.all_questions.copy()
    
    def get_questions(self, amount):
        # Load questions based on max_questions user input
        # Choose either user input for max_questions or the number of questions left if that is less than user input
        amount = min(amount, len(self.unused_questions))

        # Get a number of random questions, equal to max_questions
        selected = random.sample(self.unused_questions, amount)

        # Remove questions from unused_questions
        for q in selected:
            self.unused_questions.remove(q)
        
        # Return question + answer pairs
        return selected
    
