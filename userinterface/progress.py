from os import system

def update(sections, done):
    system("clear")
    print("ORDER \t\t SECTION \t STATUS")

    for num, sect in enumerate(sections):
        text = "[{:03d}] \t\t " + sect + " \t\t"

        if num < done:
            text += " DONE"
        elif num == done:
            text+= " IN PROGRESS"
        else:
            text += " WAITING"

        print(text.format(num+1))

def start(sections):
    update(sections, 0)