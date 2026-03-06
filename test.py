    display_answer = ""
    copied_answer = False

    if user_answer != "":
        # Loop through the letters of the real answer and compare them to the user answer
        for i, char in enumerate(answer):
            if i < len(user_answer):
                # If the char in the real answer is the same as the user answer, display the char
                if char == user_answer[i]:
                    display_answer += char
                else:
                    # If the char in the real answer is not the same as the user answer and is a space, display ' '
                    if char == ' ':
                        display_answer += ' '
                    else:
                        # If the char is incorrect, display '.'
                        display_answer += '.'
            else:
                # If the answer typed is shorter than the answer given, display spaces and periods for the remaining characters
                if char == ' ':
                    display_answer += ' '
                else:
                    display_answer += '.'
    else:
        if got_question_wrong == 2:
            display_answer = answer
            copied_answer = True
            return display_answer, copied_answer
        for i, char in enumerate(answer):
            # Only print the first letter of every word for the first try
            if i == 0 or answer[i - 1] == " ":
                display_answer += char
            # Print the first two letters of every word for the second try
            elif got_question_wrong == 1 and (i == 1 or answer[i - 2] == ' '):
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
        return display_answer, copied_answer

    Case 1: User typed something