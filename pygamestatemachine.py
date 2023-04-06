import pygame
import random
import csv
from tkinter import filedialog
from gtts import gTTS
import tempfile
import os
import time
import math

def read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)
        # Create a list of questions
        all_questions = [(row[0], row[1], row[2]) for row in reader]
        random.shuffle(all_questions)
    return all_questions
def playaudio(audio,language):
    tts = gTTS(text=audio, lang=language)
    # Save the audio to a temporary file
    filename = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Play the audio
    while pygame.mixer.music.get_busy():
        time.sleep(0.01)

    pygame.mixer.stop()
    pygame.mixer.quit()

    # Delete the temporary file after playing the audio
    os.remove(filename)
class Question:
    def __init__(self):
        pass

    def generate_answers(self):
        self.kanji, self.kana, self.english = menu_state.all_questions[menu_state.question_num]
        if menu_state.shuff:
            if menu_state.Test == 1:
                self.answers = [self.english]
                col = 2
            elif menu_state.Test == 2:
                self.answers = [self.kanji]
                col = 0
            elif menu_state.Test == 3:
                self.answers = [self.kana]
                col = 1

            while len(self.answers) < menu_state.Max_answers:
                random_answer = random.choice(menu_state.all_questions)[col]
                if random_answer not in self.answers:
                    self.answers.append(random_answer)
                menu_state.shuff = False
            random.shuffle(self.answers)

    def check_answer(self, selected_answer):
        if menu_state.Test == 1:
            real_answer = self.english
            answer_lang = "en"
            helper = self.kana
            helper_lang = "ja"
        elif menu_state.Test == 2:
            real_answer = self.kanji
            answer_lang = "ja"
            helper = self.english
            helper_lang = "en"
        elif menu_state.Test == 3:
            real_answer = self.kana
            answer_lang = "ja"
            helper = self.english
            helper_lang = "en"
            
        if selected_answer == real_answer:
            screen.fill(GREEN)
            correct_text = question_font.render(selected_answer, True, WHITE)
            correct_text_rect = correct_text.get_rect()
            correct_text_rect.center = (WIDTH // 2, 100)
            screen.blit(correct_text, correct_text_rect)
            correct_text = question_font.render("("+helper+")", True, WHITE)
            correct_text_rect = correct_text.get_rect()
            correct_text_rect.center = (WIDTH // 2, 150)
            screen.blit(correct_text, correct_text_rect)
            correct_text = question_font.render("is Correct!", True, WHITE)
            correct_text_rect = correct_text.get_rect()
            correct_text_rect.center = (WIDTH // 2, 200)
            screen.blit(correct_text, correct_text_rect)
            pygame.display.update()
            playaudio(selected_answer, answer_lang)
            playaudio(helper,helper_lang)
            playaudio("is Correct","en")
            menu_state.score += 1
        else:
            screen.fill(RED)
            incorrect_text = question_font.render(selected_answer, True, WHITE)
            incorrect_text_rect = incorrect_text.get_rect()
            incorrect_text_rect.center = (WIDTH // 2, 100)
            screen.blit(incorrect_text, incorrect_text_rect)
            incorrect_text = question_font.render("is Wrong :(", True, WHITE)
            incorrect_text_rect = incorrect_text.get_rect()
            incorrect_text_rect.center = (WIDTH // 2, 150)
            screen.blit(incorrect_text, incorrect_text_rect)
            incorrect_text = question_font.render("The Correct Answer is", True, WHITE)
            incorrect_text_rect = incorrect_text.get_rect()
            incorrect_text_rect.center = (WIDTH // 2, 200)
            screen.blit(incorrect_text, incorrect_text_rect)
            correct_text = question_font.render(real_answer, True, WHITE)
            correct_text_rect = correct_text.get_rect()
            correct_text_rect.center = (WIDTH // 2, 300)
            screen.blit(correct_text, correct_text_rect)
            correct_text = question_font.render("("+helper+")", True, WHITE)
            correct_text_rect = correct_text.get_rect()
            correct_text_rect.center = (WIDTH // 2, 350)
            screen.blit(correct_text, correct_text_rect)
            pygame.display.update()
            playaudio(selected_answer, answer_lang)
            playaudio("is wrong","en")
            playaudio("The correct answer is","en")
            playaudio(real_answer,answer_lang)
            playaudio(helper,helper_lang)
        menu_state.question_num += 1
        menu_state.shuff = True
        menu_state.play_audio = True
class MenuState:
    def __init__(self):
        self.done = False
        self.play_audio = True
        self.shuff = True
        self.Display = True
        self.Sound = True
        self.question_num = 0
        self.score = 0
        self.Test = 1
        self.Max_answers = 4
        self.file_path = ""

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.file_path != "":
                        self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.load_button.collidepoint(event.pos):
                    self.file_path = filedialog.askopenfilename()
                if self.sound_toggle.collidepoint(event.pos):
                    if self.Sound:
                        self.Sound = False
                    else:
                        self.Sound = True
                if self.display_toggle.collidepoint(event.pos):
                    if self.Display:
                        self.Display = False
                    else:
                        self.Display = True
                if self.answer_number.collidepoint(event.pos):
                    if self.Max_answers >= 9:
                        self.Max_answers = 2
                    else:
                        self.Max_answers += 1
                if self.test_type.collidepoint(event.pos):
                    if menu_state.Test >= 3:
                        menu_state.Test = 1
                    else:
                        menu_state.Test += 1

    def update(self):
        file_name = self.file_path
        if file_name:
            self.all_questions = read_csv(file_name)

    def draw(self, screen):
        self.load_button_location = (10, 10, 200, 40)
        self.sound_toggle_location = (10, 50, 200, 40)
        self.display_toggle_location = (10, 90, 200, 40)
        self.answer_number_location = (10, 130, 200, 40)
        test_type_location = (10, 170, 200, 40)
        screen.fill((255, 255, 255))

        # Load Button
        self.load_button = pygame.Rect(self.load_button_location)
        load_text = small_font.render('Load', True, BLACK)
        pygame.draw.rect(screen, BLACK, self.load_button, 2)
        screen.blit(load_text, (self.load_button_location[0]+10, self.load_button_location[1]+10))
        
        # Sound Button
        self.sound_toggle = pygame.Rect(self.sound_toggle_location)
        sound_toggle_text = small_font.render('Sound', True, BLACK)
        pygame.draw.rect(screen, BLACK, self.sound_toggle, 2)
        screen.blit(sound_toggle_text, (self.sound_toggle_location[0]+10, self.sound_toggle_location[1]+10))
        if self.Sound:
            sound_state = small_font.render('On', True, BLACK)
            screen.blit(sound_state, (75, 60))
        else:
            sound_state = small_font.render('Off', True, BLACK)
            screen.blit(sound_state, (75, 60))

        # Display Button
        self.display_toggle = pygame.Rect(self.display_toggle_location)
        display_toggle_text = small_font.render('Display', True, BLACK)
        pygame.draw.rect(screen, BLACK, self.display_toggle, 2)
        screen.blit(display_toggle_text, (self.display_toggle_location[0]+10, self.display_toggle_location[1]+10))
        if self.Display:
            display_state = small_font.render('On', True, BLACK)
            screen.blit(display_state, (100, 100))
        else:
            display_state = small_font.render('Off', True, BLACK)
            screen.blit(display_state, (100, 100))

        # Answer Number Button
        self.answer_number = pygame.Rect(self.answer_number_location)
        answer_number_text = small_font.render('Answers:', True, BLACK)
        pygame.draw.rect(screen, BLACK, self.answer_number, 2)
        screen.blit(answer_number_text, (self.answer_number_location[0]+10,self.answer_number_location[1]+10))
        num_text = small_font.render(str(self.Max_answers), True, BLACK)
        screen.blit(num_text,(120, 140))

        # Test Type Button
        self.test_type = pygame.Rect(test_type_location)
        if menu_state.Test == 1:
            test_type_text = small_font.render('Kanji -> English', True, BLACK)
        elif menu_state.Test == 2:
            test_type_text = small_font.render('English -> Kanji', True, BLACK)
        elif menu_state.Test == 3:
            test_type_text = small_font.render('Kanji -> Kana', True, BLACK)
        pygame.draw.rect(screen, BLACK, self.test_type, 2)
        screen.blit(test_type_text, (test_type_location[0]+10,test_type_location[1]+10))
        
        font = pygame.font.Font(None, 36)
        if self.file_path == "":
            text = font.render("Please Load a file", True, BLACK)
        else:
            text = font.render("Press SPACE to start", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(text, text_rect)

        chosen_file = font.render(((self.file_path).split("/")[-1]).replace(".csv",""), True, BLACK)
        chosen_file_rect = chosen_file.get_rect(center=(WIDTH // 2, 200))
        screen.blit(chosen_file,chosen_file_rect)

    def sound(self):
        pass
class GameState:
    def __init__(self):
        self.done = False
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done == True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button.collidepoint(event.pos):
                    self.done = True
                for i, option in enumerate(question.answers):
                    button = pygame.Rect(100, 150+i*answer_spacing, 500, answer_spacing)
                    if button.collidepoint(event.pos):
                        question.check_answer(option)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.key == pygame.K_r:
                    menu_state.play_audio = True
                for i, option in enumerate(question.answers):
                    selected_option_index = event.key - pygame.K_0 - 1
                    if selected_option_index == i:
                        question.check_answer(option)

    def update(self):
        if menu_state.question_num < len(menu_state.all_questions):
            question.generate_answers()
            if menu_state.Test == 1:
                self.question = question.kanji
                self.question_language = "ja"
            elif menu_state.Test == 2:
                self.question = question.english
                self.question_language = "en"
            elif menu_state.Test == 3:
                self.question = question.kanji
                self.question_language = "ja"
            self.question_text = question_font.render(self.question, True, WHITE)
            self.answer_texts = [medium_font.render(option, True, WHITE) for option in question.answers]
        else:
            self.done = True
            menu_state.question_num = 0
            menu_state.done = False

    def draw(self, screen):
        screen.fill(GRAY)
        if menu_state.Display:
            screen.blit(self.question_text, ((WIDTH - self.question_text.get_width()) // 2, 50))

        for i, option_text in enumerate(self.answer_texts):
            button = pygame.Rect(100, 150+i*answer_spacing, 500, answer_spacing)
            ans_num_text = small_font.render(str(i+1), True, WHITE)
            pygame.draw.rect(screen, BLACK, button, 2)
            screen.blit(option_text, (110, 155+i*answer_spacing))
            screen.blit(ans_num_text, (button[2]+80,120+(i+1)*answer_spacing))

        # Define the quit button
        self.quit_button_location = (WIDTH - 95, HEIGHT - 45, 90, 40)
        self.quit_button = pygame.Rect(self.quit_button_location)
        quit_text = small_font.render('Quit', True, WHITE)
        pygame.draw.rect(screen, BLACK, self.quit_button, 2)
        screen.blit(quit_text, (self.quit_button_location[0]+10, self.quit_button_location[1]+10))

    def sound(self):
        if menu_state.Sound:
            if menu_state.play_audio:
                playaudio(self.question,self.question_language)
                menu_state.play_audio = False
class GameOverState:
    def __init__(self):
        self.done = False

    def handle_events(self, events):
        global current_state
        for event in events:
            if event.type == pygame.QUIT:
                self.done == True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button.collidepoint(event.pos):
                    self.done = True     
                if self.menu_button.collidepoint(event.pos):
                    menu_state.score = 0
                    current_state = menu_state

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(WHITE)
        # Show Score
        self.score_text = question_font.render(f"You Scored {menu_state.score} Points", True, BLACK)
        screen.blit(self.score_text, ((WIDTH - self.score_text.get_width()) // 2, 50))

        # Define the quit button
        self.quit_button_location = (WIDTH - 95, HEIGHT - 45, 90, 40)
        self.quit_button = pygame.Rect(self.quit_button_location)
        quit_text = small_font.render('Quit', True, BLACK)
        pygame.draw.rect(screen, BLACK, self.quit_button, 2)
        screen.blit(quit_text, (self.quit_button_location[0]+10, self.quit_button_location[1]+10))

        # Define the menu button
        self.menu_button_location = (10, HEIGHT - 45, 90, 40)
        self.menu_button = pygame.Rect(self.menu_button_location)
        menu_text = small_font.render('Menu', True, BLACK)
        pygame.draw.rect(screen, BLACK, self.menu_button, 2)
        screen.blit(menu_text, (self.menu_button_location[0]+10, self.menu_button_location[1]+10))        

    def sound(self):
        pass
    
# Initialize Pygame
pygame.init()

# Define some font sizes
font_name = "MSGothic"
question_font = pygame.font.SysFont(font_name, 50)
medium_font = pygame.font.SysFont(font_name, 30)
small_font = pygame.font.SysFont(font_name, 20)

# Define the score variables
answer_spacing = math.floor((medium_font.get_height()*1.34))

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (64,64,64)
GREEN = (0,64,0)
RED = (64,0,0)

# Define screen dimensions
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Instantiate Classes
question = Question()
menu_state = MenuState()
game_state = GameState()
gameover_state = GameOverState()

# Set current state
current_state = menu_state

# Game loop
while not current_state.done:
    events = pygame.event.get()
    current_state.handle_events(events)

    current_state.update()
    current_state.draw(screen)
    pygame.display.update()
    current_state.sound()
    #clock.tick(60)

    if current_state.done:
        if current_state == menu_state:
            current_state = game_state
        elif current_state == game_state:
            current_state = gameover_state
        else:
            pass

# Quit
pygame.quit()
