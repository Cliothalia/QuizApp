import csv
import random

def check_answer(got_question_wrong, correct):
    display_answer, copied_answer = check_chars(got_question_wrong, real_answer)
    
    if display_answer != real_answer:
        print("Test2")
        got_question_wrong += 1

    else:
        if copied_answer == True:
            print("Copied!")
        else:
            print("Correct!")
            correct = True    

    if got_question_wrong > 0:
        questions_to_review.update({question: real_answer})
        print("quetions_to_review is updated")
    
    print(f"{got_question_wrong} times wrong pt2")
    return got_question_wrong, correct

def check_chars(got_question_wrong, real_answer):
        # Get answer from the user
    user_answer = input("Answer: ")
    display_answer = ""
    copied_answer = False

    if user_answer != "":
        display_answer = check_typed_answer(display_answer, user_answer)
    else:
        display_answer, copied_answer = check_blank_answer(display_answer, copied_answer, got_question_wrong)

    if user_answer == display_answer:
        return display_answer, copied_answer
    else:    
        # Print the display answer
        print(display_answer)
        return display_answer, copied_answer
    
def check_blank_answer(display_answer, copied_answer, got_question_wrong):
    if got_question_wrong >= 2:
        display_answer = real_answer
        print(display_answer)
        copied_answer = True
        return display_answer, copied_answer
    
    for i, char in enumerate(real_answer):
        # Only print the first letter of every word for the first try
        if i == 0 or real_answer[i - 1] == " ":
            display_answer += char
        # Print the first two letters of every word for the second try
        elif got_question_wrong == 1 and (i == 1 or real_answer[i - 2] == ' '):
            display_answer += char
        else:
            if char == " ":
                display_answer += " "
            else:
                display_answer += "."
    
    return display_answer, copied_answer

def check_typed_answer(display_answer, user_answer):
    # Loop through the letters of the real answer and compare them to the user answer
    for i, char in enumerate(real_answer):
        if i < len(user_answer):
            # If the char in the real answer is the same as the user answer, display the char
            if char == user_answer[i]:
                display_answer = display_answer + char
            else:
                # If the char in the real answer is not the same as the user answer and is a space, display ' '
                if char == ' ':
                    display_answer = display_answer + ' '
                else:
                    # If the char is incorrect, display '.'
                    display_answer = display_answer + '.'
        else:
            # If the answer typed is shorter than the answer given, display spaces and periods for the remaining characters
            if char == ' ':
                display_answer = display_answer + ' '
            else:
                display_answer = display_answer + '.'

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

def get_q_and_a(index, review_mode):
    if review_mode == "Incorrect":
        dictionary = questions_to_review
        index = 0
    else:
        dictionary = questions_to_ask

    # Get the first question fro the qa dict
    question = list(dictionary.keys())[index]

    # Print the question to the user
    print(question)

    # Get the real answer from the qa dict
    real_answer = list(dictionary.values())[index]

    return question, real_answer

def get_questions(review_mode, max_questions):
    for i in range(max_questions):
        # get random question from dict
        qa_random_add = random.choice(list(used_qa_dict.items()))
        if review_mode != "Next":
            questions_to_ask.update({qa_random_add[0]: qa_random_add[1]})
        else:
            # If review mode is 'next'. Clear the dict first so you only get new questions
            questions_to_ask.clear()
            questions_to_ask.update({qa_random_add[0]: qa_random_add[1]})
        # Remove used question from all questions dict
        used_qa_dict.pop(qa_random_add[0])

def set_mode(review_mode):
    # Get review mode from user
    review_input = input("Do you want to review your incorrect questions (incorrect), review all questions (all) or go to the next set of questions (type how many questions you want)? ")
    review_input = review_input.lower().strip().strip('.')

    # Set review mode to review incorrect questions
    if review_input == "incorrect":
        # Check if there are questions to review
        if len(questions_to_review) == 0:
            print("There are no questions to review!")
            exit
        else:
            # If there are questions to review, set review_mode to Incorrect
            review_mode = "Incorrect"
    # Set review mode to review all questions
    elif review_input == "all":
        review_mode = "All"
    # Get new questions to review
    elif review_input.isnumeric():
        review_mode = "Next"
        # TO DO: HOW TO IMPLEMENT THIS??

    return review_mode

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

    # Set mode
    review_mode = "Normal"
    first_run = True
    running = True

    while (running == True):
        # Get questions from file on first run
        if first_run == True:
            full_qa_dict = file_loader()
            used_qa_dict = full_qa_dict
        # On every other run, decide on the review mode
        else:
            if current_question == max_questions:
                review_mode = set_mode(review_mode)
                # Reset index and current question
                index = 0
                current_question = 0
            else:
                # TO DO: add the next questions thing here?
                pass
        
        get_questions(review_mode, max_questions)

        # Loop through a single question
        while current_question < max_questions:
            # Get question and answer
            question, real_answer = get_q_and_a(index, review_mode)

            # Set correct variable to False
            correct = False
            got_question_wrong = 0

            # Loop through user answers until they give the correct answer
            while (correct == False):
                check_answer(got_question_wrong, correct)
        
        # Increase index to next question in dictionary
        if review_mode != "Incorrect":
            index += 1
        else:
            index = 0

        # Up question counter by 1
        current_question += 1
        
        running = False

# End script



