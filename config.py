import json

def getConfig():
    """
    Attempts to grab the settings specified by the config file.
    """
    try:
        return json.loads(open('config.json').read())
    except FileNotFoundError:
        print('Config file not found, using default settings')
        return saveDefaultConfig()

def saveDefaultConfig():
    """
    Writes default settings to config.json.
    """
    retVal = {'casualMistakes':9, 
              'normalMistakes':7, 
              'insaneMistakes':5, 
              'scoreFactor':13,
              'wordGuessBonus': 1.25}
    with open('config.json', 'w') as outfile:
        json.dump(retVal, outfile)
    print('Default settings written to config')
    return retVal