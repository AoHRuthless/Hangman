from enum import Enum

import random

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

class Mode(Enum):
    EASY = 0, EASY_WORDS, 7
    HARD = 1, HARD_WORDS, 5

    def getList(self):
        return self.value[1]

    def getNumMistakes(self):
        return self.value[2]

mode = Mode.EASY
currWord = ""
currGuess = ""
mistakesLeft = -1
score = 0

def start():
    chooseMode()
    restart()

def initData():
    global mistakesLeft
    global currGuess
    currGuess =  ""
    mistakesLeft = mode.getNumMistakes()

def restart():
    initData()
    chooseWord()
    play()

def promptRestart():
    choice = input("Would you like to restart? Yes/No: ").lower()
    if (choice == 'yes'):
        restart()
    else:
        end()

def end():
    print("Your final score is >> " + str(score) + "!")

def chooseMode():
    try:
        global mode
        value = input("Choose a Mode:\n0 -> EASY\n1 -> HARD\n")
        if (value == str(1)):
            mode = Mode.HARD
        elif (value == str(0)):
            mode = Mode.EASY
    except ValueError: pass

def chooseWord():
    global currWord
    currWord = random.choice(mode.getList())

def play():
    if (currWord == ""):
        promptRestart()
        return
    mutableCopy = currWord
    success = False
    while (not success and mistakesLeft > 0):
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
            if (mutableCopy.count(guess) > 0):
                handleCorrectLetter()
                mutableCopy = mutableCopy.replace(guess, "")
                if (len(mutableCopy) <= 0):
                    handleCorrectAnswer(False)
                    success = True
            else:
                handleIncorrect()
    if (success):
        promptRestart()
    else:
        end()

def handleCorrectAnswer(wordGuess):
    global currWord
    print("You got the right answer.")
    updateScore(wordGuess)
    currWord = ""

def handleCorrectLetter():
    print("Nice job!")

def handleIncorrect():
    global mistakesLeft

    print("Sorry, that is not correct.")
    mistakesLeft -= 1

def updateScore(wordGuess):
    global score
    increment = (len(currWord) * mistakesLeft * 10)
    if (wordGuess):
        increment += 30
    score += increment

start()