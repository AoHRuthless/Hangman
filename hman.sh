#!/bin/sh

# Compiles and runs Hangman using the provided word dictionary.
py -c 'import hangman; hangman.start()' dictionary.txt
