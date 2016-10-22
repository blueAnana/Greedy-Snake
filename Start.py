from Tkinter import *
# from random import randint
import random

WIDTH = 500
HEIGHT = 500
BOUNDX = 10
BOUNDY = 10


class Start(Canvas):
    def backgound(self):
        self.master.title("Greedy Snake!")

        self.w = Label(self, text="Welcom to Greedy Snake!")
        self.create_window(250, 100, window=self.w)

        self.start_button = Button(self, text="Start", command=self.newGame)
        self.create_window(200, 250, window=self.start_button)
        self.quit_button = Button(self, text="Exit", command=self.quit)
        self.create_window(300, 250, window=self.quit_button)

    def newGame(self):
        print "Start Game"
        self.delete("all")
        # Draw the bounding wall
        self.create_rectangle(10, 10, 490, 490, fill='#fff')

        # initial snake with 3 nodes
        self.head = self.create_rectangle(BOUNDX + 20, BOUNDY + 0, BOUNDX + 30, BOUNDY+10, fill="#000", tag="head")
        self.node2 = self.create_rectangle(BOUNDX + 10, BOUNDY + 0, BOUNDX + 20, BOUNDY + 10, fill="#000", tag="node2")
        self.node3 = self.create_rectangle(BOUNDX + 0, BOUNDY + 0, BOUNDX + 10, BOUNDY + 10, fill="#000", tag="node3")

        # initial food
        self.food()

    def move(self):
        while self.end():
            print "move"


    def end(self):
        return True

    def food(self):
        self.x_food = random.randint(0, 48) * 10
        self.y_food = random.randint(0, 48) * 10
        self.food = self.create_rectangle(BOUNDX + self.x_food, BOUNDY + self.y_food, BOUNDX + self.x_food + 10, BOUNDY + self.y_food + 10, fill="#000", tag="food")

    def __init__(self, master=None):
        Canvas.__init__(self, master, width=WIDTH, height=HEIGHT)
        self.pack()
        self.backgound()
#
# class Food():
#     def __init__(self):
#
# class Snake():
#     def __init__(self):

root = Tk()
startDesk = Start(master=root)
startDesk.mainloop()
