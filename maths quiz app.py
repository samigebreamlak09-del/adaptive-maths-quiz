import random
import time

TOTAL_QUESTIONS = 4
MAX_ATTEMPTS = 3


def show_menu():
    print("========== MATHS QUIZ ==========")
    print("1. Level 1 - Numeracy")
    print("2. Level 2 - Higher (trig and calculus)")
    print("3. Level 3 - Advanced Higher")
    print("--------------------------------")


def get_level():
    level = input("Choose your starting level (1, 2 or 3): ").strip()
    while level != "1" and level != "2" and level != "3":
        print("Invalid choice. Please enter 1, 2 or 3.")
        level = input("Choose your starting level (1, 2 or 3): ").strip()
    return int(level)


def clean(text):
    # remove spaces and capital letters so "Cos(x)" and "cos(x)" both match
    return text.replace(" ", "").lower()


def generate_problem():
    # Level 1: a new random problem every time (no eval needed)
    left = random.randint(3, 12)
    right = random.randint(3, 12)
    operator = random.choice(["+", "-", "*"])
    if operator == "+":
        answer = left + right
    elif operator == "-":
        answer = left - right
    else:
        answer = left * right
    question = str(left) + " " + operator + " " + str(right)
    return question, [str(answer)]


def get_fixed_questions(level):
    # each question has a list of accepted answers (already cleaned)
    if level == 2:
        questions = [
            "Exact value of sin(45 degrees) (format: 1/root 2)",
            "Gradient of y = 4x^2 at x = 1.5",
            "Derivative of sin(x) (format: sin(x))",
            "Value of log2(8)",
        ]
        answers = [
            ["1/root2", "1/sqrt2"],
            ["12"],
            ["cos(x)", "cosx"],
            ["3"],
        ]
    else:
        questions = [
            "Integral of x * e^x dx by parts (format: 2x*e^x - e^x)",
            "Cartesian form of z = 2(cos(pi/3) + i*sin(pi/3)) (format: 3 + 4i, use root for square root)",
            "Derivative of ln(sin(x)) using the chain rule (format: tan(x))",
            "Which proof method assumes the negation of the statement to find a contradiction?",
        ]
        answers = [
            ["x*e^x-e^x", "x*e^x-e^x+c"],
            ["1+root3i", "1+sqrt3i"],
            ["cot(x)", "cotx", "1/tan(x)"],
            ["proofbycontradiction", "contradiction"],
        ]
    return questions, answers


def ask_question(number, question, accepted):
    # returns True if the pupil gets it right within MAX_ATTEMPTS
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        guess = clean(input("Question " + str(number) + ": " + question + " = "))
        if guess in accepted:
            print("Correct!\n")
            return True
        attempts = attempts + 1
        remaining = MAX_ATTEMPTS - attempts
        if remaining > 0:
            print("Incorrect. " + str(remaining) + " attempts remaining.")
    print("Out of tries! The correct answer was: " + accepted[0] + "\n")
    return False


def play_round(level):
    if level == 1:
        questions = []
        answers = []
        for i in range(TOTAL_QUESTIONS):
            question, accepted = generate_problem()
            questions.append(question)
            answers.append(accepted)
    else:
        questions, answers = get_fixed_questions(level)

    input("Press enter to start ")
    print("--------------------------------")
    start_time = time.time()
    score = 0
    for i in range(len(questions)):
        if ask_question(i + 1, questions[i], answers[i]):
            score = score + 1
    total_time = round(time.time() - start_time, 2)
    return score, len(questions), total_time


def choose_next_level(level, score, total):
    # the quiz adapts to how the pupil performed
    if score == total and level < 3:
        print("Full marks! Moving you up to level " + str(level + 1) + ".")
        return level + 1
    elif score <= 1 and level > 1:
        print("Let's build confidence - moving you down to level " + str(level - 1) + ".")
        return level - 1
    else:
        print("Staying on level " + str(level) + ".")
        return level


def main():
    show_menu()
    level = get_level()
    playing = True
    while playing:
        print("\nLoading level " + str(level) + "...")
        score, total, seconds = play_round(level)
        print("--------------------------------")
        print("Well done! You got " + str(score) + " out of " + str(total) + " in " + str(seconds) + " seconds.")
        level = choose_next_level(level, score, total)
        print("--------------------------------")
        again = input("Do you want to play again? (yes/no): ").strip().lower()
        if again != "yes":
            playing = False
    print("Thanks for playing. Good luck with your exams!")


main()
