import os
from colorama import Fore, Back, Style, init

from quiz import Quiz

def list_files():
    # Path to database with question files
    path = "C://Users//SmeetsJulia(Calco)//OneDrive - Calco//Documenten//VScode//QuizApp//quiz_database"
    dir_list = os.listdir(path)
    display_list = []

    # Display readable versions of file names for selection
    for file in dir_list:
        display_name = file.strip(".csv").replace("_", " ").title()
        display_list.append(display_name)
        print(display_name)
    
    return display_list


if __name__ == "__main__":
    # Initialize Colorama for colorful terminal display
    init()

    # Print start menu
    print(Fore.CYAN + "Welcome to the Quiz App!")
    print("~~~")
    print("The following topics are ready for review:")
    print(Style.RESET_ALL)

    # Print list of files in database directory. All topics ready to review
    display_list = list_files()

    # Get user input on topic. Only continue if topic is valid
    while True:
        topic = input("Choose topic: ")

        if topic in display_list or topic == "":
            print("Topic selected!")
            break
        else:
            print("Topic invalid, try again.")

    # Get user input on max questions per round. Only continue if input is a number
    while True:
        try:
            max_questions = int(input("Questions per round: "))
            break
        except ValueError:
            print('Invalid input')


    # Get user input on mode. Only continue of input matches 't' or 'f'
    while True:
        mode = input("Mode (typing (t)/flashcard (f)): ").strip().lower().split()[0]
        if mode == "t" or mode == "f":
            print("Mode selected")
            break
        else:
            print("Invalid input")

    # Initialize quiz
    quiz = Quiz(topic, max_questions, mode)

    # Prepare questions for first round
    quiz.new_round()

    # Main game loop. Loops through prepared questions and ends when there are no more questions
    while quiz.current_questions:
        # Ask question and get user input. Check input until answer is correct or incorrect 3 times
        quiz.ask_round()

        # Break when there are no more questions
        if not quiz.bank.unused_questions and not quiz.wrong_questions:
            print("\nQuiz finished!")
            print(f"Final Score: {quiz.total_correct} / {quiz.total_answered} correct")
            print(f"That is {quiz.total_correct/quiz.total_answered*100:.0f} %")
            break

        # At the end of the round, ask user whether they want to review questions or get a set of new ones
        quiz.choose_next()