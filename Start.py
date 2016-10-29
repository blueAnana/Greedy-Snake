from Tkinter import *
import random
import threading


WIDTH = 500
HEIGHT = 500
BOUND_X = 10
BOUND_Y = 10
DIRECT = "Right"
REVERSE = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}


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

    def move(self):
        d_x, d_y = self.getDirect()
        tmp = self.tail.prev
        self.tail.moveTo(self.head.x + d_x, self.head.y + d_y)
        self.tail.prev = None
        self.tail.next = self.head
        self.head.prev = self.tail
        self.head = self.tail
        self.tail = tmp
        self.tail.next = None
        print DIRECT
        global t
        if self.head.x in range(10, 470) and self.head.y in range(10, 470):
            t = threading.Timer(0.7, self.move)
            t.start()

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
    def __init__(self, canvas_, x_, y_):
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

        self.randomFood()

    def randomFood(self):
        x_food = random.randint(0, 48) * 10
        y_food = random.randint(0, 48) * 10
        self.food = Node(canvas_=self._canvas, x_=x_food, y_=y_food)

    def __init__(self, master=None):
        self._root = master
        self._canvas = Canvas(master, width=WIDTH, height=HEIGHT)
        self._canvas.pack()
        self._root.bind_all("<Key>", key)
        self.background()


def key(event):
    global DIRECT
    if event.keysym != REVERSE[DIRECT]:
        DIRECT = event.keysym
    print "key", event.keysym


root = Tk()
startDesk = Start(master=root)
root.mainloop()
