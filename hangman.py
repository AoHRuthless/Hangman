from enum import Enum

import random
import math
import sys

"""
Default word list
"""
DEFAULT = [
    'apple', 'bananas', 'elephant', 'chinchilla', 'ecstatic', 'ravine', 'cavern', 'monastery', 'eggplant',
    'garden', 'house', 'homestead', 'divine', 'wonderful', 'bottom', 'terrific', 'speed', 'coast', 'salamander',
    'shenanigans', 'ostrich', 'giraffe', 'birch', 'cedar', 'league', 'awkward', 'blowfish', 'glowworm', 'crypt', 
    'fishhook', 'quark', 'kayak', 'oxygen', 'haphazard', 'gazebo', 'phlegm', 'toady', 'rhythm', 'mystify', 
    'sphinx', 'squawk', 'yeast', 'zealous', 'quad', 'pajamas', 'kiosk', 'jukebox', 'zombie', 'bagpipes', 
    'dwarves', 'ivory', 'sly', 'topaz'
]

"""
Mode represents the number of mistakes the user is allowed to make.
"""
class Mode(Enum):
    CASUAL = 9
    NORMAL = 7
    INSANE = 5

    def getNumMistakes(self):
        return self.value

mode = Mode.CASUAL
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
        value = int(input("Choose a Mode:\n0 -> CASUAL\n1 -> NORMAL\n2 -> INSANE\n"))
        if (value == 1):
            mode = Mode.NORMAL
        elif (value == 2):
            mode = Mode.INSANE
    except ValueError: pass # Just keep in easy mode if the input is invalid

def chooseWord():
    global currWord

    words = DEFAULT
    if (len(sys.argv) > 1):
        words = [line.rstrip('\n') for line in open(sys.argv[1])]
    currWord = random.choice(words)

def play():
    """
    Handles the game logic. Allows the user to make repeated guesses until they run out of guesses or solve it,
    Like in conventional hangman, the user can elect to guess the entire word. If the user runs out of guesses,
    the game is ended. Otherwise, if the user successfully finds the solution, they may elect to play again in
    the same mode.
    """
    tmp = list(currWord)
    progress = list('-'*len(currWord))
    usedLetters = []
    success = False
    while ((not success) and mistakesLeft > 0):
        print("Word Progress          : " + "".join(progress))
        print("Letters guessed so far : " + str(usedLetters))

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
            if (guess in usedLetters and mode != Mode.INSANE):
                print("You have already guessed this letter. Try another one.")
                continue;

            usedLetters.append(guess)
            if (tmp.count(guess) > 0):
                tmp = [e for e in tmp if e != guess]

                for i in findOccurrences(currWord, guess):
                    progress[i] = guess

                handleCorrectLetter()
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

def findOccurrences(s, ch):
    """
    Finds occurrences of the given character in the given string as a list of numbers.
    """
    return [i for i, ltr in enumerate(s) if ltr == ch]

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