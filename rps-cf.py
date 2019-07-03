#!/usr/bin/python3

import random
#import json
#import requests
from pgtest import *

def main():
    data = {'user': "", 'win': 0, 'lose': 0, 'tie': 0}

#define rock paper scissors variables
    value = {0: 'ROCK', 1: 'PAPER', 2: "SCISSORS"}

#get user name, exit if invalid
    try:
      data['user'] = str.lower((input("Please enter your name: ")))
    except:
      print("You lose\nWhat instrument did you choose?")
      quit()

#get user input, exit if invalid
    try:
      playerValue = int(input("Press the number for your selection\n0. ROCK\n1. PAPER\n2. SCISSORS\nInput: "))
    except:
      print("You lose\nWhat instrument did you choose?")
      quit()

#get enemy value
    enemyValue = random.randint (0,2)
#print enemy selection
    print('Enemy selected ', value.get(enemyValue))

#determine win/lose
    if playerValue == enemyValue:
      print('You tie!')
      data['tie'] = 1
    elif playerValue == 0 and enemyValue == 1:
      print('You lose!')
      data['lose']= 1
    elif playerValue == 0 and enemyValue == 2:
      print('You win!')
      data['win'] = 1
    elif playerValue == 1 and enemyValue == 0:
      print('You win!')
      data['win'] = 1
    elif playerValue == 1 and enemyValue == 2:
      print('You lose!')
      data['lose'] = 1
    elif playerValue == 2 and enemyValue == 0:
      print('You lose!')
      data['lose'] = 1
    elif playerValue == 2 and enemyValue == 1:
      print('You win!')
      data['win'] = 1
    else:
      print("You lose\nWhat instrument did you choose?") 
      data['lose'] = 1
    postgres_put(data)
    results = postgres_get(data['user'])
    print("Name: {0}".format(results[0]))
    print("You have lost this many times: {0}".format(results[1]))
    print("You have won this many times: {0}".format(results[2]))
    print("You have tied this many times: {0}".format(results[3]))

if __name__== "__main__":
  main()    