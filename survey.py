# This are the various packages that are used throughout the program

import time
import random

# Ask the user to input their names
firs_name = input('Enter Your First Name : ')
last_name = input('Enter Your Last Name : ')
# Welcome the user to the game
print('Welcome ', firs_name, last_name,
      ', You will be showed 5 random question for subject from a random subject, Please give all answers to complete '
      'survey.')

# Open the file containing all the random questions
f = open("question.txt", "r")
if f.mode == 'r':
    # Put all the questions in variable called contents
    contents = f.readlines()
    # Create an empty list called questions
    questions = []
    # Loop through the questions 5 time while selecting a random question each time
    for i in range(5):
        # Add the random question to the question list
        que = random.choice(contents)
        questions.append(que)
    # Create an empty list called answer list
    answer_list = []
    # Get the time now and store it in value called now
    now = time.time()
    # Loop through all the choosen question while getting the answers from the user
    for i, item in enumerate(questions):
        print('Question ' + str(i) + ':')
        # Print question
        print(item)
        # Get answer
        answer = input()
        # Add the answer to answer list
        answer_list.append(answer)
    # GEt the time after the user has answered all the questions
    end_time = time.time()
    # Get the difference betwwen the start time and the end tiem and assign the value to time taken
    time_taken = end_time - now
    total_characters = 0
    for ans in answer_list:
        total_characters += len(ans)
    print('You wrote ', total_characters, ' in total in your answers')
    print('You answered 5 question in ', int(time_taken), ' seconds')
