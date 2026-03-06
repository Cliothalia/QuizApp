import csv
import random

def check_answer(answer, user_answer, got_question_wrong):
    # Case 1: User typed something
    if user_answer:
        result = []

        for real_char, user_char in zip(answer, user_answer):
            if real_char == user_char:
                result.append(real_char)
            elif real_char == " ":
                result.append(" ")
            else:
                result.append(".")
        
        # Handle remaining characters if user_answer is shorter
        if len(user_answer) < len(answer):
            for char in answer[len(user_answer):]:
                result.append(" " if char == " " else ".")
        
        display_answer = "".join(result)
    
    # Case 2: User pressed Enter (hint mode)
    if got_question_wrong <= 2:
        return answer, True

    result = []
    words = answer.split(" ")

    for word in words:
        if got_question_wrong == 0:
            # First hint: first letter only
            hint = word[0] + "." * (len(word) - 1)
        elif got_question_wrong == 1:
            # Second hint: first two letters
            hint = word[:2] + "." * (len(word) - 2)
        result.append(hint)
    
    display_answer = "".join(result)
    return display_answer, False


def file_loader():
    # Variable to determine what topic file to retrieve
    qa_topic_file = "Network Security" #TO ADD: change this to user input
    qa_topic_file = qa_topic_file.lower().replace(' ', '_')

    full_qa_dict = {}

    # Get questions and answers from .csv file and add to dictionary
    with open(f'quiz_database/{qa_topic_file}.csv', mode = 'r') as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            # Add questions and answers to dictionary. Questions = key, Answers = value
            full_qa_dict.update({lines[0]: lines[1]})

    return full_qa_dict


if __name__ == "__main__":
    # Prompt user for topic they want to be quized on
    topic = input("Choose a topic you want to be quized on.\nCurrent topics: Network Security ").lower().strip('.')

    # Prompt user for flashcard or typing mode
    mode = input("Do you want flashcard mode or typing mode? ").lower().strip('.')

    # Prompt user for number of questions they want
    
    max_questions = int(input("How many questions do you want? "))

    # Initialize variables
    current_question = 0
    index = 0

    # Initialize session questions dicts
    questions_to_ask = {}
    questions_to_review = {}
    questions_asked = {}

    # Set mode
    review_mode = "Normal"
    first_run = True
    running = True

    # Quiz loop for all questions
    while (running == True):
        # 1. Load questions from file
        full_qa_dict = file_loader()
        used_qa_dict = full_qa_dict

        # 2. Display first question to user
        # create dictionary with number of questions user wants
        if first_run == True:
            for i in range(max_questions):
                question, answer = random.choice(list(used_qa_dict.items()))
                questions_to_ask.update({question: answer})
        # get the first question and answer from that dictionary
        question = next(iter(questions_to_ask))
        answer = next(iter(questions_to_ask.values()))


        # Print the first question if there are questions in the dict
        if len(questions_to_ask) != 0:
            print(question)
        else:
            print("There are no more questions!")

        # 3. Prompt user for input
        got_question_wrong = 0
        correct = False

        while (correct == False):
            user_answer = input("Answer: ")
            display_answer, copied_answer = check_answer(answer, user_answer, got_question_wrong)

            # 5. If correct, display correct and continue to next question
            if display_answer == answer and copied_answer == False:
                print("Correct!")
                correct = True
            
            # 6. If incorrect, display only correct letters and ask for input again
            else:
                questions_to_review[question] = answer
                print(display_answer)

                got_question_wrong += 1
        
        # Add question to questions asked
        questions_asked[question] = answer
        questions_to_ask.pop(question)
        current_question += 1

        # 9. Display next question
        if current_question == max_questions:
            running = False