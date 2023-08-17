#region imports
import random
import csv
import os
import time
import pygame
import tempfile
from gtts import gTTS
import msvcrt
#endregion imports

#region functions
#clear screen function
def clear_screen():                                                             # Create a clear_screen function
    os.system('cls' if os.name == 'nt' else 'clear')                                # make a 'cls' call to the os if its NT based, otherwise use 'clear'

#read csv function
def read_csv(file_name):                                                        # Create a function with a 'file_name' argument
    with open(file_name, newline='', encoding='utf-8') as csvfile:                  # While the 'file_name' is open as csvfile
        reader = csv.DictReader(csvfile)                                            # Read the entire csv into 'reader'
        csv_array = []                                                              # Create a blank array variable called 'csv_array'
        for row in reader:                                                          # For every line (row) in 'reader'
            csv_array.append(row)                                                   # Append that row to the 'csv_array' array
    return csv_array                                                                # Return 'csv_array' so it can be assigned to the variable that calls this function

#play TTS
def playaudio(audio,language):
    tts = gTTS(text=audio, lang=language)
    # Save the audio to a temporary file
    filename = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    tts.save(filename)

    # Init pygame
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Play the audio
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Close pygame
    pygame.mixer.stop()
    pygame.mixer.quit()
    pygame.quit()

    # Delete the temporary file after playing the audio
    os.remove(filename)

#wait for input rather than use the console input
def getinput(numofinput):                                                       # Create a function with a 'numofinput' argument
    all_valid_inputs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]           # Create a list variable called 'all_valid_inputs' and set valid strings
    valid_inputs = all_valid_inputs[:numofinput]                                    # Shorten the number of 'valid_inputs' to 'numofinput' (range from blank : to 'numofinput')
    user_answer = ""                                                                # Create 'user_answer' variable and make it blank
    while user_answer not in valid_inputs:                                          # While 'user_answer' does not match anything in the shortened 'valid_inputs' array
        user_answer = msvcrt.getch().decode().upper()                               # Change 'user_answer' to be what ever key is currently being pressed and convert to upper case
    return user_answer                                                              # Return 'user_answer' so it can be assigned to the variable that calls this function

#ask a question and manage the answers
def question(question,qlang,helper,answer,alang,array,score,noa,user_choice):               # Create a function with arguments
    choices = [answer]                                                              # Create a list type var called 'choices' and store the contents of 'answer' as its first item
    used_answers = [answer]                                                         # Create a list type var called 'choices' and store the contents of 'answer' as its first item
    while len(choices) < noa:                                                       # While the length of the list 'choices' is less than the desired noa (number of answers)
        random_answer = random.choice(csv_array)[array]                             # Get a random item from the 'csv_array' from the 'array' column and store it as 'random_answer'
        if random_answer not in used_answers:                                       # If this 'random_answer' is not currently in the 'used_answers' list
            choices.append(random_answer)                                           # Then we append the 'random_answer' to the 'choices' list
            used_answers.append(random_answer)                                      # Finally we put that same 'random_answer' into the 'used_answers" list so its not picked again
    random.shuffle(choices)                                                         # Shuffle the choices around so the correct answer is not always the first answer
    if user_choice != "1":                                                            # If the helper argument is set to 'None'
        if display_choice & bit1 == bit1:                                           # If the binary value of 'display_choice' has a bit in the 1's column (if text is set to be displayed)
            print(f"What is \n\n{question}\n")                                      # Display the question without the 'helper' variable
    else:
        if display_choice & bit1 == bit1:                                           # If the binary value of 'display_choice' has a bit in the 1's column (if text is set to be displayed)
            print(f"What is \n\n{question} ({helper})\n")                           # Display the question with the 'helper' variable
    for i in range(noa):                                                            # For every 'i' in the range of numbers up to 'noa' (number of answers)
        print(f"{i+1}) {choices[i]}")                                               # Print a formatted string showing the sum of i+1) and each answer in the 'choices' list
    if qlang != None:                                                               # As long as 'qlang' is not empty
        if display_choice & bit2 == bit2:                                           # If the binary value of 'display_choice' has a bit in the 2's column (if sound is set to be heard)
            if user_choice == "1":
                playaudio(question,qlang)
            if user_choice == "2":
                playaudio(question,qlang)                                               # Play the TTS audio of the 'question' string with the 'qlang' language ('ja' or 'en')
            if user_choice == "3":
                playaudio(answer,qlang)
    #Wait for Input
    user_answer = getinput(noa)                                                     # Run the 'getinput' function and store its result in 'user_answer'
    for ans in range(noa):
        if user_answer == str(ans+1):                                               # If 'user_answer' is the same as the string value of the answer (this is the answer the user wants to compare)
            if choices[ans] == answer:                                              # If chosen answer matches the actual answer
                print("\nCorrect!")
                print(f"{answer} ({helper})\n")                                  # Display a "Correct" message
                playaudio(answer,alang)                                             # Play 'answer' TTS with 'alang' language ('ja' or 'en')
                playaudio("is correct","en")                                        # More audio affirmation
                score += 1                                                          # Increase your score
            else:
                print("Incorrect. The correct answer is ",answer,"\n")              # You dun fucked up
                playaudio("Incorrect, the correct answer is","en")                  # Audible insult to injury
                playaudio(answer,alang)                                             # It was this DUMBASS!
    return score                                                                    # Return the score to be assigned to the vairable that calls this function
#endregion functions

#region pick a file
path = os.getcwd()
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
while True:
    try:
        clear_screen()
        print("Select a file:")
        for i, f in enumerate(csv_files):
            print(f"{i+1}. {f}")
        selected_file = input()
        selected_file = csv_files[int(selected_file)-1]
        break
    except:
        clear_screen()
        print("This is not a valid selection")
        time.sleep(2)
        
print(f"You selected {selected_file}")
csv_array = read_csv(selected_file)
#endregion pick a file

#region Choose answers
clear_screen()
print("Enter\n1 Kanji -> English\n2 English -> Kanji\n3 Kanji -> Kana: ")
user_choice = getinput(3)
random.shuffle(csv_array)
score = 0
#endregion

#region Choose number of answers
clear_screen()
print("2-9 How many answers would you like displayed?")
answer_answer = int(getinput(9))
if answer_answer > len(csv_array):
    print("That is more answers than are in the test")
    print("defaulting to", len(csv_array))
    answer_answer = len(csv_array)
    time.sleep(3)
if answer_answer == 1:
    print("That is hardly a test!")
    print("2 answers is as easy as I am comforable making it")
    answer_answer = 2
    time.sleep(3)
#endregion

#region Choose Display / sound
clear_screen()
print("1) Text Only\n2) Sound Only\n3) Text and Sound")
display_choice = int(getinput(3))
bit1 = 0b1
bit2 = 0b10
#endregion

#region Endless Mode
clear_screen()
print("Endless Mode?\n1) Yes\n2) No")
endless = int(getinput(2))
#endregion

#region Main loop
if endless == 1:
    while True:
        member = random.choice(csv_array)
        clear_screen()                                                                  # Run the 'clear_screen()' function to clear the screen
        print(selected_file.split('.')[0])                                              # Print the name of the csv file to the console screen
        kanji = member["kanji"]                                                         # Assign the item in the "kanji" column of the 'member' row to a variable called 'kanji'
        kana = member["kana"]                                                           # Assign the item in the "kana" column of the 'member' row to a variable called 'kana'
        english = member["english"]                                                     # Assign the item in the "english" column of the 'member' row to a variable called 'english'
        #Answer in Engish
        if user_choice == "1":
            score = question(kanji,"ja",kana,english,"en","english",score,answer_answer,user_choice) # Run the 'question' function with parameters and store the output into the 'score' variable
        #Answer in Kana
        elif user_choice == "2":
            score = question(english,"en",kana,kanji,"ja","kanji",score,answer_answer,user_choice)   # Run the 'question' function with parameters and store the output into the 'score' variable
        #Answer in Kanji
        elif user_choice == "3":
            score = question(kanji,"ja",english,kana,"ja","kana",score,answer_answer,user_choice)      # Run the 'question' function with parameters and store the output into the 'score' variable
        #time.sleep(3)
else:
    for member in csv_array:                                                            # interate through each 'member' of the shuffled 'csv_array'
        clear_screen()                                                                  # Run the 'clear_screen()' function to clear the screen
        print(selected_file.split('.')[0])                                              # Print the name of the csv file to the console screen
        print(f"Score {score} / {len(csv_array)}")                                      # Print the current score situation to the console screen
        kanji = member["kanji"]                                                         # Assign the item in the "kanji" column of the 'member' row to a variable called 'kanji'
        kana = member["kana"]                                                           # Assign the item in the "kana" column of the 'member' row to a variable called 'kana'
        english = member["english"]                                                     # Assign the item in the "english" column of the 'member' row to a variable called 'english'
        #Answer in Engish
        if user_choice == "1":
            score = question(kanji,"ja",kana,english,"en","english",score,answer_answer,user_choice) # Run the 'question' function with parameters and store the output into the 'score' variable
        #Answer in Kana
        elif user_choice == "2":
            score = question(english,"en",kana,kanji,"ja","kanji",score,answer_answer,user_choice)   # Run the 'question' function with parameters and store the output into the 'score' variable
        #Answer in Kanji
        elif user_choice == "3":
            score = question(kanji,"ja",english,kana,"ja","kana",score,answer_answer,user_choice)      # Run the 'question' function with parameters and store the output into the 'score' variable
        #time.sleep(3)
    clear_screen()
    print(f"You scored {score} out of {len(csv_array)}")                                # When we run out of questions, just print the score
#endregion Main loop