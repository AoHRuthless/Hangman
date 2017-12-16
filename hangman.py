import sys

### game module
import game

### EXECUTION ###

INVALID = 'Warning: Invalid command arguments specified'

def checkSecondArg(numArgs, flag):
    if numArgs > 3:
        if numArgs > 4:
            if sys.argv[3] == flag:
                return sys.argv[4]
        print(INVALID)
    return None

if __name__ == '__main__':
    gameMode = None
    wordsFile = None

    numArgs = len(sys.argv)
    if numArgs > 1:
        firstArg = sys.argv[1]
        if numArgs == 2:
            print(INVALID)
        else:
            secondArg = sys.argv[2]
            if firstArg == '-gm':
                gameMode = secondArg
                wordsFile = checkSecondArg(numArgs, '-if')
            elif firstArg == '-if':
                wordsFile = secondArg
                gameMode = checkSecondArg(numArgs, '-gm')
            else:
                print(INVALID)


    game.Hangman(gameMode, wordsFile)