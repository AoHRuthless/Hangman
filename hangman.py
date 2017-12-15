from enum import Enum

import random
import math

"""
Hard-written lists of words to sample gameplay.
"""
EASY_WORDS = [
    'apple', 'bananas', 'elephant', 'chinchilla', 'ecstatic', 'ravine', 'cavern', 'monastery', 'eggplant',
    'garden', 'house', 'homestead', 'divine', 'wonderful', 'bottom', 'terrific', 'speed', 'coast', 'salamander',
    'shenanigans', 'ostrich', 'giraffe', 'birch', 'cedar', 'league' 
]

HARD_WORDS = [
	'awkward', 'blowfish', 'glowworm', 'crypt', 'fishhook', 'quark', 'kayak', 'oxygen', 'haphazard', 'gazebo', 
	'phlegm', 'toady', 'rhythm', 'mystify', 'sphinx', 'squawk', 'yeast', 'zealous', 'quad', 'pajamas', 'kiosk', 
	'jukebox', 'zombie', 'bagpipes', 'dwarves', 'ivory', 'sly', 'topaz'
]

"""
Mode represents the relevant list of words and the number of mistakes a user can make.
"""
class Mode(Enum):
    EASY = (EASY_WORDS, 7)
    HARD = (HARD_WORDS, 5)

    def getList(self):
        return self.value[0]

    def getNumMistakes(self):
        return self.value[1]

mode = Mode.EASY
currWord = ""
mistakesLeft = -1
score = 0

def start():
    """
    Starts the game by allowing the user to pick the mode then calling the restart() function to handle the
    rest of initialization.
    """
    chooseMode()
    restart()

def restart():
    """
    Initializes the game by resetting the number of mistakes allowed (specified by the mode) and randomly
    selecting the word, before proceeding to play.
    """
    global mistakesLeft
    mistakesLeft = mode.getNumMistakes()

    chooseWord()
    play()

def promptRestart():
    """
    Prompts the client to restart. If the user selects not to restart, end the game.
    """
    choice = input("Would you like to play again? Yes/No: ").lower()
    if (choice == 'yes'):
        restart()
    else:
        end()

def end():
    """
    Simply prints the final score to the user.
    """
    print("Your final score is >> " + str(math.ceil(score)) + "!")

def chooseMode():
    try:
        global mode
        value = input("Choose a Mode:\n0 -> EASY\n1 -> HARD\n")
        if (value == str(1)):
            mode = Mode.HARD
        elif (value == str(0)): # Technically useless since we start in easy mode, kept for clarity
            mode = Mode.EASY
    except ValueError: pass # Just keep in easy mode if the input is invalid

def chooseWord():
    global currWord
    currWord = random.choice(mode.getList())

def play():
    """
    Handles the game logic. Allows the user to make repeated guesses until they run out of guesses or solve it,
    Like in conventional hangman, the user can elect to guess the entire word. If the user runs out of guesses,
    the game is ended. Otherwise, if the user successfully finds the solution, they may elect to play again in
    the same mode.
    """
    tmp = currWord
    success = False
    while ((not success) and mistakesLeft > 0):
        guess = input("Choose a letter or guess the word.")
        if (len(guess) > 1):
            if (guess == currWord):
                handleCorrectAnswer(True)
                success = True
            else:
                handleIncorrect()
        elif (len(guess) == 0):
            handleIncorrect()
            print("Please guess a letter or the whole word.")
        else:
            if (tmp.count(guess) > 0):
                handleCorrectLetter()
                tmp = tmp.replace(guess, "")
                if (len(tmp) <= 0):
                    handleCorrectAnswer(False)
                    success = True
            else:
                handleIncorrect()
    if (success):
        promptRestart()
    else:
        print("The word was " + currWord + ".")
        end()

def handleCorrectAnswer(wordGuess):
    """
    If the user guesses the correct answer, update the score and remove the current word.
    """
    global currWord
    print("You got the right answer.")
    updateScore(wordGuess)
    currWord = ""

def handleCorrectLetter():
    """
    Give the user an indication that they guessed a letter correctly.
    """
    print("Correct.")

def handleIncorrect():
    """
    If an incorrect guess is given, decrement the number of available guesses.
    """
    global mistakesLeft

    print("Incorrect.")
    mistakesLeft -= 1

def updateScore(wordGuess):
    """
    Updates the score. The score is directly dependent upon the number of tries the user took as well 
    as the amount of unique guesses required. If the user guesses the word correctly, they are given a bonus.
    """
    global score
    increment = max(13, 13 * (26 - len(set(currWord))) + 
        math.ceil(182 / mode.getNumMistakes() - mistakesLeft) - 208)
    if (wordGuess):
        increment *= 1.25
    score += round(increment)

### EXECUTION ###
start()