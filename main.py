from quiz import Quiz

if __name__ == "__main__":

    topic = input("Choose topic: ")
    max_questions = int(input("Questions per round: "))
    mode = input("Mode (typing/flashcard): ").strip().lower()
    if mode == "t":
        mode = "typing"
    elif mode == "f":
        mode = "flashcard"

    quiz = Quiz(topic, max_questions, mode)

    quiz.new_round()

    while quiz.current_questions:
        quiz.ask_round()

        if not quiz.bank.unused_questions and not quiz.wrong_questions:
            print("\nQuiz finished!")
            break

        quiz.choose_next()