import csv
import os
import random

# Fill temp dictionary with how many questions the user wants
def get_questions(review_mode, max_questions):
    for i in range(max_questions):
        qa_random_add = random.choice(list(used_qa_dict.items()))
        if review_mode != "Next":
            questions_to_ask.update({qa_random_add[0]: qa_random_add[1]})
        else:
            questions_to_ask.clear()
            questions_to_ask.update({qa_random_add[0]: qa_random_add[1]})
        used_qa_dict.pop(qa_random_add[0])

def commands(user_input):
    # Skip question command
    if user_input == "/skip":
        pass

    # 'Close enough' command
    if user_input == "/correct":
        pass

    # Help command
    if user_input == "/help":
        pass

    # Switch between typing and flashcard mode
    if user_input == "/switch":
        pass

def get_q_and_a (index, review_mode):
    if review_mode == "Incorrect":
        dictionary = questions_to_review
        index = 0
    elif review_mode == "All" or review_mode == "Normal":
        dictionary = questions_to_ask

    # Get the first question from the qa dict
    question = list(dictionary.keys())[index]
    # Print the question to the user
    print(question)

    # Get the real answer from the qa dict
    real_answer = list(dictionary.values())[index]

    return question, real_answer

# Loops until the user gives the correct answer
def check_answer(got_question_wrong, real_answer):
    # Get answer from the user
    user_answer = input("Answer: ")
    display_answer = ""
    copied_answer = False

    # Compare letters if user actually typed something in
    if user_answer != "":
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

    # Display the first or second letter, or the whole world if the user pressed 'enter'
    elif user_answer == "":
        if got_question_wrong == 2:
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
    
    if user_answer == display_answer:
        return display_answer, copied_answer
    else:    
        # Print the display answer
        print(display_answer)
        return display_answer, copied_answer

def get_mode(review_mode, first_run, current_question, max_questions, index):

    if first_run == True:
        review_mode = "Normal"
    else:
        if current_question == max_questions:
            review_input = input("Do you want to review your incorrect questions (incorrect), review all questions (all) or go to the next set of questions (type how many questions you want)? ")
            review_input = review_input.lower().strip().strip('.')

            # Reset index and current question to 0
            index = 0
            current_question = 0

            if review_input == "incorrect":
                if len(questions_to_review) == 0:
                    print("There are no questions to review!")
                else:
                    review_mode = "Incorrect"
            elif review_input == "all":
                review_mode = "All"
            elif review_input.isnumeric():
                review_mode = "Next"
                max_questions = int(review_input)
                get_questions(review_mode, max_questions)
            else:
                exit
        else:
            pass
    
    return review_mode, current_question, max_questions, index


if __name__ == "__main__":
    # Prompt user for a topic they want to be quized on. Give list of topics, corresponding to .csv names. Also give option for 'random' and 'all topics'
    topic = input("Choose a topic\nCurrent topics: Network Security\n") # TO ADD: topics based on names of files in database
    topic = topic.lower().strip('.')

    # Prompt user for flashcard or typing mode
    # TO DO: input validation
    mode = input("Do you want flashcard or typing mode? ")
    mode = mode.lower().strip('.')

    # Prompt user for number of questions they want
    # TO DO: input validation
    max_questions = int(input("How many questions do you want? "))
    current_question = 0

    # Initiate dictionaries, one with the full question list of the csv file, and another will the used questions
    # TO ADD: wouldn't it be better to just store the used one, and if you want to reset just get the info from the .csv again?
    full_qa_dict = {}
    used_qa_dict = full_qa_dict

    # TO ADD: what if you want to read multiple files?
    # Variable to determine which topic file to retrieve
    qa_topic_file = "Network Security" # TO ADD: change this to user input
    qa_topic_file = qa_topic_file.lower().replace(' ', '_')

    # Get questions and answers from .csv file and add to dictionary
    with open(f'quiz_database/{qa_topic_file}.csv', mode = 'r') as file:
        csvFile = csv.reader(file, delimiter=';')
        for lines in csvFile:
            # Add questions and answers to dictionary. Questions = key, Answers = value
            full_qa_dict.update({lines[0]: lines[1]})

    # Create temporary dictionary
    questions_to_ask = {}
    questions_to_review = {}

    # Initiate index
    index = 0

    # Set mode
    review_mode = "Normal"
    first_run = True

    # Program Loop
    while (True):
        review_mode, current_question, max_questions, index = get_mode(review_mode, first_run, current_question, max_questions, index)

        first_run = False

    # Typing mode:
        if mode == "typing" or mode == "Typing" or mode == 'T' or mode == 't':
            get_questions(review_mode, max_questions)
            
            while current_question < max_questions:

                # Get question and answer
                question, real_answer = get_q_and_a(index, review_mode)

                # Set correct variable to False
                correct = False
                got_question_wrong = 0
                
                # Loop through a single question until user gives correct answer
                while (correct == False):
                    print(f"Got question wrong {got_question_wrong} times")
                    display_answer, copied_answer = check_answer(got_question_wrong, real_answer)

                    # if the answer is correct, set correc to True
                    if display_answer == real_answer and copied_answer == False:
                        if got_question_wrong == 0:
                            if question in questions_to_review:
                                questions_to_review.pop(question)
                            print("Correct!")
                            correct = True
                        else:
                            if got_question_wrong < 2:
                                got_question_wrong += 1
                            else:
                                got_question_wrong = 2
                            correct = True

                    elif (display_answer == real_answer and copied_answer == True) or display_answer != real_answer:
                        if got_question_wrong < 2:
                            got_question_wrong += 1
                        else:
                            got_question_wrong = 2

                    else:
                        print("Hey, you missed a scenario!") #test
                    
                    if got_question_wrong > 0:
                        questions_to_review.update({question: real_answer})

                # Increase index to next question in dictionary
                if review_mode != "Incorrect":
                    index += 1
                else:
                    index = 0
                # Up question counter by 1
                current_question += 1

# FLASHCARD MODE
        if mode == "Flashcard" or mode == "flashcard" or mode == "f" or mode == "F":
            while current_question < max_questions:
                # Get the first question from the qa dict
                question = list(questions_to_ask.keys())[0]
                # Print the question to the user
                print(f"Question {current_question}: {question}")

                # Get the real answer from the qa dict
                real_answer = list(questions_to_ask.values())[0]

                user_input = input("Do you know the answer?")

                print(real_answer)

                correct = input("Did you get it right? (Type yes or no)")

                if correct == "Yes" or correct == "yes" or correct == "y" or correct == "Y":
                    questions_to_ask.pop(question)
                    current_question += 1
                else:
                    pass


