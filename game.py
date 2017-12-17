from enum import Enum

import random
import math

### config module
import config

config = config.getConfig()

"""
Mode represents the number of mistakes the user is allowed to make.
"""
class Mode(Enum):
    CASUAL = config['casualMistakes']
    NORMAL = config['normalMistakes']
    INSANE = config['insaneMistakes']

    def getNumMistakes(self):
        return self.value

"""
Hangman object to run the game.
"""
class Hangman():
    mode = Mode.CASUAL
    currWord = ""
    mistakesLeft = -1
    score = 0
    ### Default word list
    words = ['apple', 'bananas', 'elephant', 'chinchilla', 'ecstatic', 'ravine', 'cavern', 'monastery', 
             'eggplant', 'garden', 'house', 'homestead', 'divine', 'wonderful', 'bottom', 'terrific', 'topaz',
             'speed', 'coast', 'salamander', 'shenanigans', 'ostrich', 'giraffe', 'birch', 'cedar', 'sly', 
             'league', 'awkward', 'blowfish', 'glowworm', 'crypt', 'fishhook', 'quark', 'kayak', 'oxygen', 
             'haphazard', 'gazebo', 'phlegm', 'toady', 'rhythm', 'mystify', 'sphinx', 'squawk', 'yeast', 
             'zealous', 'quad', 'pajamas', 'kiosk', 'jukebox', 'zombie', 'bagpipes', 'dwarves', 'ivory'
            ]

    def __init__(self, gameMode = None, wordsFile = None):
        """
        Constructor can specify a valid gamemode and/or a valid input file.
        """
        if wordsFile is not None:
            try:
                self.words = [line.rstrip('\n') for line in open(wordsFile)]
            except FileNotFoundError:
                print(wordsFile + " is an invalid file name. Defaulting to program word dictionary")
        if gameMode is not None:
            try:
                self.mode = Mode[gameMode.upper()]
                self.restart()
                return
            except KeyError: pass
        self.start()

    def start(self):
        """
        Starts the game by allowing the user to pick the mode then calling the restart() function to handle the
        rest of initialization.
        """
        self.chooseMode()
        self.restart()

    def restart(self):
        """
        Initializes the game by resetting the number of mistakes allowed (specified by the mode) and randomly
        selecting the word, before proceeding to play.
        """
        self.mistakesLeft = self.mode.getNumMistakes()

        self.chooseWord()
        self.play()

    def promptRestart(self):
        """
        Prompts the client to restart. If the user selects not to restart, end the game.
        """
        choice = input("Would you like to play again? Yes/No: ").lower()
        if choice == 'yes' or choice == 'y':
            self.restart()
        else:
            self.end()

    def end(self):
        """
        Simply prints the final score to the user.
        """
        print("Your final score is >> " + str(math.ceil(self.score)) + "!")

    def chooseMode(self):
        try:
            value = int(input("Choose a Mode:\n0 -> CASUAL\n1 -> NORMAL\n2 -> INSANE\n"))
            if value == 1:
                self.mode = Mode.NORMAL
                return
            elif value == 2:
                self.mode = Mode.INSANE
                return
        except ValueError: pass # Just keep in easy mode if the input is invalid
        self.mode = Mode.CASUAL

    def chooseWord(self):
        self.currWord = random.choice(self.words)

    def play(self):
        """
        Handles the game logic. Allows the user to make repeated guesses until they run out of guesses or solve it,
        Like in conventional hangman, the user can elect to guess the entire word. If the user runs out of guesses,
        the game is ended. Otherwise, if the user successfully finds the solution, they may elect to play again in
        the same mode.
        """
        tmp = list(self.currWord)
        progress = list('-'*len(self.currWord))
        usedLetters = []
        success = False
        while (not success) and self.mistakesLeft > 0:
            print("Word Progress          : " + "".join(progress))
            print("Letters guessed so far : " + str(usedLetters))

            guess = input("Choose a letter or guess the word.\n")

            if len(guess) > 1:
                if guess == self.currWord:
                    self.handleCorrectAnswer(True)
                    success = True
                else:
                    self.handleIncorrect()

            elif len(guess) == 0:
                self.handleIncorrect()
                print("Please guess a letter or the whole word.")

            else:
                if guess in usedLetters and self.mode != Mode.INSANE:
                    print("You have already guessed this letter. Try another one.")
                    continue;

                usedLetters.append(guess)
                if tmp.count(guess) > 0:
                    tmp = [e for e in tmp if e != guess]

                    for i in self.findOccurrences(self.currWord, guess):
                        progress[i] = guess

                    self.handleCorrectLetter()
                    if len(tmp) <= 0:
                        self.handleCorrectAnswer(False)
                        success = True
                else:
                    self.handleIncorrect()
        if success:
          self.promptRestart()
        else:
            print("The word was " + self.currWord + ".")
            self.end()

    def handleCorrectAnswer(self, wordGuess):
        """
        If the user guesses the correct answer, update the score and remove the current word.
        """
        print("You got the right answer.")
        self.updateScore(wordGuess)
        self.currWord = ""

    def handleCorrectLetter(self):
        """
        Give the user an indication that they guessed a letter correctly.
        """
        print("Correct.")

    def findOccurrences(self, s, ch):
        """
        Finds occurrences of the given character in the given string as a list of numbers.
        """
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def handleIncorrect(self):
        """
        If an incorrect guess is given, decrement the number of available guesses.
        """
        print("Incorrect.")
        self.mistakesLeft -= 1

    def updateScore(self, wordGuess):
        """
        Updates the score. The score is directly dependent upon the number of tries the user took as well 
        as the amount of unique guesses required. If the user guesses the word correctly, they are given a bonus.
        """
        tmp = config['scoreFactor']
        increment = max(tmp, tmp * (2 * tmp - len(set(self.currWord))) + 
            math.ceil(14 * tmp / (max(self.mode.getNumMistakes() - self.mistakesLeft, 1))) - 16 * tmp)
        if wordGuess:
            increment *= config['wordGuessBonus']
            self.score += round(increment)