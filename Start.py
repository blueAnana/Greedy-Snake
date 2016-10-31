from Tkinter import *
import random
import threading
import tkMessageBox


WIDTH = 500
HEIGHT = 500
BOUND_X = 10
BOUND_Y = 10
DIRECT = "Right"
REVERSE = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
FOOD = None
SCORE = 0
NODE_MATRIX = [[0 for i in range(48)] for i in range(48)]


class Snake:
    def __init__(self, canvas):
        self.canvas_ = canvas
        self.head = Node(self.canvas_, 20, 250)
        self.node = Node(self.canvas_, 10, 250)
        self.tail = Node(self.canvas_, 0, 250)
        self.head.next = self.node
        self.node.prev = self.head
        self.node.next = self.tail
        self.tail.prev = self.node
        NODE_MATRIX[0][0] = 1
        NODE_MATRIX[1][0] = 1
        NODE_MATRIX[2][0] = 1

    def move(self):
        # hit the wall
        if self.head.x == 0 and DIRECT == "Left" or self.head.x == 470 and DIRECT == "Right"or self.head.y == 0 and DIRECT == "Up" or self.head.y == 470 and DIRECT == "Down":
            gameOver()

        d_x, d_y = self.getDirect()
        if self.head.x + d_x == FOOD.x and self.head.y + d_y == FOOD.y:
            self.eatFood()
        if NODE_MATRIX[(self.head.x + d_x)/10][(self.head.y + d_y)/10] != 1:
            NODE_MATRIX[self.tail.x/10][self.tail.y/10] = 0
            tmp = self.tail.prev
            self.tail.moveTo(self.head.x + d_x, self.head.y + d_y)
            self.tail.prev = None
            self.tail.next = self.head
            self.head.prev = self.tail
            self.head = self.tail
            self.tail = tmp
            self.tail.next = None
            NODE_MATRIX[self.head.x/10][self.head.y/10] = 1
        else:
            gameOver()

        print DIRECT
        global t
        if self.head.x in range(0, 470) and self.head.y in range(0, 470):
            t = threading.Timer((100 - SCORE)*0.01, self.move)
            t.start()

    def eatFood(self):
        global SCORE
        SCORE += 10
        self.head.prev = FOOD
        FOOD.next = self.head
        self.head = FOOD
        randomFood(self.canvas_)

    def getDirect(self):
        if DIRECT == "Up":
            return 0, -10
        if DIRECT == "Down":
            return 0, 10
        if DIRECT == "Left":
            return -10, 0
        if DIRECT == "Right":
            return 10, 0


class Node:
    def __init__(self, canvas_=None, x_=0, y_=0):
        self.canvas = canvas_
        self.x = x_
        self.y = y_
        self.next = None
        self.prev = None
        self.node = self.canvas.create_rectangle(BOUND_X + self.x, BOUND_Y + self.y,
                                                 BOUND_X + self.x + 10, BOUND_Y + self.y + 10, fill="#000")

    def snakeMove(self, speed, toX , toY):
        self.canvas.move(self.node, toX, toY)
        self.canvas.after(speed, self.snakeMove, speed, toX, toY)

    def moveTo(self, toX, toY):
        self.x = toX
        self.y = toY
        self.canvas.delete(self.node)
        self.node = self.canvas.create_rectangle(BOUND_X + self.x, BOUND_Y + self.y,
                                                 BOUND_X + self.x + 10, BOUND_Y + self.y + 10, fill="#000")


class Start:
    def background(self):
        self._root.title("Greedy Snake!")

        w = Label(self._canvas, text="Welcom to Greedy Snake!")
        self._canvas.create_window(250, 100, window=w)

        start_button = Button(self._canvas, text="Start", command=self.newGame)
        self._canvas.create_window(200, 250, window=start_button)
        quit_button = Button(self._canvas, text="Exit", command=self._root.quit)
        self._canvas.create_window(300, 250, window=quit_button)

    def newGame(self):
        print "Start Game"
        self._canvas.delete("all")
        # Draw the bounding wall
        self._canvas.create_rectangle(10, 10, 490, 490, fill='#fff')
        self.snake = Snake(canvas=self._canvas)

        t = threading.Timer(0.7, self.snake.move)
        t.start()

        randomFood(self._canvas)

    def __init__(self, master=None):
        self._root = master
        self._canvas = Canvas(master, width=WIDTH, height=HEIGHT)
        self._canvas.pack()
        self._root.bind_all("<Key>", key)
        self.background()


def randomFood(canvas):
    global FOOD
    x_food = random.randint(0, 47) * 10
    y_food = random.randint(0, 47) * 10
    print x_food, y_food
    FOOD = Node(canvas_=canvas, x_=x_food, y_=y_food)


def key(event):
    global DIRECT
    if event.keysym != REVERSE[DIRECT]:
        DIRECT = event.keysym
    print "key", event.keysym


def gameOver():
    tkMessageBox.showinfo("END", "GAME OVER")


root = Tk()
startDesk = Start(master=root)
root.mainloop()
