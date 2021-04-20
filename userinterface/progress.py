from os import system
import sys

def update(sections, done):
    if done > 0:
        sys.stdout.write("\033[F")
        for _ in sections:
            sys.stdout.write("\033[F")

    print("ORDER \t\t SECTION \tSTATUS")

    for num, sect in enumerate(sections):
        text = "[{:03d}] \t\t " + sect + " \t\t"

        if num < done:
            text += u'\u2713'
        elif num == done:
            text+= '.'
        else:
            text += u'\u2717'

        print(text.format(num+1))

def start(sections):
    update(sections, 0)