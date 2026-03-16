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
            print(f"Final Score: {quiz.total_correct} / {quiz.total_answered} correct")
            print(f"That is {quiz.total_correct/quiz.total_answered*100:.0f} %")
            break

        quiz.choose_next()