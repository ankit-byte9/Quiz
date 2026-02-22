import random
import datetime
import re
import json

def registration():
    name = input("Enter your name: ")
    enrol = input("Enter your Enrollment number: ")
    with open("Cred/registration.txt", "r") as log:
        for line in log:
            data = line.strip().split(", ")
            if len(data) == 4:
                en=data[1]
                if enrol == en:
                    print('Enrollment number already exists: Enter another Enrollment or try logging in.')
                    break
                    
    pas = input("Enter the password you want: ")
    email = input("Enter your email: ")
    profile = name + ", " + enrol + ", " + pas + ", " + email

    with open("Cred/registration.txt", "a") as reg:
        reg.write(profile + "\n")

    cred = enrol + ", " + pas
    with open("Cred/login.txt", "a") as log:
        log.write(cred + "\n")

    firstpage()

def login():
    enrol = input("Enter your enrollment number: ")
    pas = input("Enter your password: ")
    found = False

    with open("Cred/login.txt", "r") as log:
        for line in log:
            data = line.strip().split(", ")
            if len(data) == 2:
                ori_enrol, ori_pass = data
                if enrol == ori_enrol and pas == ori_pass:
                    print("Login successful!")
                    found = True
                    dashboard()
                    break

    if not found:
        print("Login Unsuccessful")

def dashboard():
    while True:
        print("#" * 10 + " Welcome Player " + "#" * 10)
        print("""1. Score
2. Start Quiz
3. Update Profile
4. Logout""")
        a = input("Enter your choice: ")

        if a == "1":
            with open("score.txt", "r") as sco:
                print(sco.read())

        elif a == "2":
            b = input("Enter the quiz type:\n1. Python\n2. DSA\n3. DBMS\n> ")
            if b == "1":
                Quiz_quiz_data("python")
            elif b == "2":
                Quiz_quiz_data("dsa")
            else:
                Quiz_quiz_data("dbms")

        elif a == "3":
            update_credentials()

        elif a == "4":
            return

        else:
            print("Enter a correct option")

def firstpage():
    print("#" * 10 + " Welcome " + "#" * 10)
    print("""1. Register New User
2. Login
""")
    a = input("> ")
    if a == "1":
        registration()
    elif a=='2':
        login()
    else:
        print("enter correct values")
def load_questions(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def Quiz_quiz_data(type):
    data = load_questions(f"questions/{type}.txt")
    questions = data[type]["questions"]
    score = 0

    for i, q in enumerate(questions):
        print(f"\nQ{i+1}: {q['question']}")

        for j, option in enumerate(q["options"]):
            print(f"  {j+1}. {option}")

        answer = input("\nEnter the number of your answer (1-4): ")

        if int(answer) - 1 == q["correct"]:
            print("Correct!")
            score += 1
        else:
            correct_option = q["options"][q["correct"]]
            print(f"Wrong! The correct answer was: {correct_option}")

        print(f"Difficulty: {q['difficulty']}")

    date = datetime.datetime.today()
    print(f"\n--- Quiz Complete! Your score: {score}/{len(questions)} ---")

    with open("score.txt", "a") as sco:
        sco.write(f"{type} quiz score: {score} time: {date}\n")

def update_credentials():
    enrol = input("Enter your enrollment number to find your account: ")
    found = False
    
    with open("Cred/registration.txt", "r") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        data = line.strip().split(", ")
        
        if len(data) == 4 and data[1] == enrol:
            found = True
            while True:
                b = input("\nWhat would you like to update:\n name\n email\n password\n quit\n> ")
                if b == "quit":
                    break
                elif b == "name":
                    data[0] = input("Enter new name: ")
                elif b == "email":
                    data[3] = input("Enter new email: ")
                elif b == "password":
                    data[2] = input("Enter new password: ")
                    edit_log(enrol,data[2])
                else:
                    print("Invalid option, try again.")

            lines[i] = ", ".join(data) + "\n"
            break

    if not found:
        print("Account not found.")
        return

    with open("Cred/registration.txt", "w") as f:
        f.writelines(lines)

    print("Account updated successfully!")
def edit_log(username, new_password):
    updated = False
    lines = []

    with open("Cred/login.txt", "r") as file:
        for line in file:
            data = line.strip().split(", ")

            if len(data) == 2 and data[0] == username:
               
                lines.append(f"{data[0]}, {new_password}\n")
                updated = True
            else:
                lines.append(line)

    if updated:
        with open("Cred/login.txt", "w") as file:
            file.writelines(lines)
        print("Password updated successfully.")
    else:
        print("User not found.")
        
def main():
    firstpage()

main()