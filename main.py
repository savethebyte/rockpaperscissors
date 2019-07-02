#!/usr/bin/python3

import random

def main():

#define rock paper scissors variables
  value = {0: 'ROCK', 1: 'PAPER', 2: "SCISSORS"}

#get user input, exit if invalid
  try:
    playerValue = int(input("Press the number for your selection\n0. ROCK\n1. PAPER\n2. SCISSORS\nInput: "))
  except:
    print("You lose\nWhat fucking instrument did you choose?")
    quit()

#get enemy value
  enemyValue = random.randint (0,2)
#print enemy selection
  print('Enemy selected ', value.get(enemyValue))

#determine win/lose
  if playerValue == enemyValue:
    print('You tie!')
  elif playerValue == 0 and enemyValue == 1:
    print('You lose!')
  elif playerValue == 0 and enemyValue == 2:
    print('You win!')
  elif playerValue == 1 and enemyValue == 0:
    print('You win!')
  elif playerValue == 1 and enemyValue == 2:
    print('You lose!')
  elif playerValue == 2 and enemyValue == 0:
    print('You lose!')
  elif playerValue == 2 and enemyValue == 1:
    print('You win!')
  else:
    print("You lose\nWhat fucking instrument did you choose?")    

if __name__== "__main__":
  main()