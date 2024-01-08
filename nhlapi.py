import requests
import pyfirmata2
import time
from datetime import date
from enum import Enum

# https://github.com/Zmalski/NHL-API-Reference#game-information
    

def watchForGoals(dateToSearch = date.today().strftime("%Y-%m-%d")):
    goalTotal = 0
    while True:
        # request the api for the scores of every game on entered date, default is current date
        URL = rf"https://api-web.nhle.com/v1/score/{dateToSearch}"
        r = requests.get(url=URL)
        data = r.json()
        goals = ""

        # search for a wings game
        for game in data['games']:
            if (game['homeTeam']['abbrev'] == 'DET' or game['awayTeam']['abbrev'] == 'DET'):
                try:
                    goals = game['goals']
                except:
                    print("No goals have been scored so far")

        # Here we can check for new goals and blink an led when a team scores
        goalTotal = checkForNewGoals(goals, goalTotal)

        # Check for new goals every minute
        time.sleep(60)

def checkForNewGoals(goals, goalTotal):
    goalCount = 0
    # check for new goals
    for goal in goals:
        goalCount += 1
        if (goalCount > goalTotal):
            # new goal has been scored
            goalTotal = goalCount

            # Check if the wings scored
            if (goal['teamAbbrev'] == 'DET'):
                # flash red led on pin 13, 20 times
                scoredby = goal['name']['default']
                print("RED WINGS SCORE!")
                print(rf"Goal scored by: {scoredby}")
                blink(13, 20)
            else:
                # flash blue led on pin 8, 20 times
                scoredby = goal['name']['default']
                badguys = goal['teamAbbrev']
                print(f"{badguys} scores.")
                print(rf"Goal scored by: {scoredby}")
                blink(8, 20)
    
    return goalTotal

def blink(pin, numofblinks):
    for blink in range(numofblinks):
        arduino.digital[pin].write(1)
        time.sleep(.1)
        arduino.digital[pin].write(0)
        time.sleep(.1)

if __name__ == "__main__":
    # connect to arduino
    arduino = pyfirmata2.Arduino('COM7')
    watchForGoals()