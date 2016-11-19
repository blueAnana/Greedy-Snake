from Tkinter import *
import random
import threading


WIDTH = 500
HEIGHT = 500
BOUND_X = 10
BOUND_Y = 10
SPEED = 250
REVERSE = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
FOOD = None
NODE_MATRIX = [[0 for i in range(48)] for i in range(48)]
COLOR = {'BLACK': '#000000', 'RED': '#FF0000'}


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
        NODE_MATRIX[0][25] = 1
        NODE_MATRIX[1][25] = 1
        NODE_MATRIX[2][25] = 1
        self.direct = "Right"
        self.score = 0

    def move(self, gameOver):
        d_x, d_y = self.getDirect()
        if self.head.x + d_x == FOOD.x and self.head.y + d_y == FOOD.y:
            self.eatFood()

        d_x, d_y = self.getDirect()

        # hit the wall
        if self.head.x == 0 and self.direct == "Left" or self.head.x == 470 and self.direct == "Right"\
                or self.head.y == 0 and self.direct == "Up" or self.head.y == 470 and self.direct == "Down":
            print self.head.x, self.head.y
            return gameOver()

        if NODE_MATRIX[(self.head.x + d_x) / 10][(self.head.y + d_y) / 10] != 1:
            NODE_MATRIX[self.tail.x / 10][self.tail.y / 10] = 0
            tmp = self.tail.prev
            self.tail.moveTo(self.head.x + d_x, self.head.y + d_y)
            self.tail.prev = None
            self.tail.next = self.head
            self.head.prev = self.tail
            self.head = self.tail
            self.tail = tmp
            self.tail.next = None
        else:  # hit self-node
            return gameOver()
        NODE_MATRIX[self.head.x / 10][self.head.y / 10] = 1

        if self.head.x in range(0, 480) and self.head.y in range(0, 480):
            self.canvas_.after(SPEED, self.move, gameOver)

    def eatFood(self):
        self.score += 10
        FOOD.changeColor()
        self.head.prev = FOOD
        FOOD.next = self.head
        self.head = FOOD
        randomFood(self.canvas_)

    def getDirect(self):
        if self.direct == "Up":
            return 0, -10
        if self.direct == "Down":
            return 0, 10
        if self.direct == "Left":
            return -10, 0
        if self.direct == "Right":
            return 10, 0


class Node:
    def __init__(self, canvas_=None, x_=0, y_=0, color_=COLOR['BLACK']):
        self.canvas = canvas_
        self.x = x_
        self.y = y_
        self.color = color_
        self.next = None
        self.prev = None
        self.node = self.canvas.create_rectangle(BOUND_X + self.x, BOUND_Y + self.y,
                                                 BOUND_X + self.x + 10, BOUND_Y + self.y + 10, fill=self.color)

    def snakeMove(self, speed, toX , toY):
        self.canvas.move(self.node, toX, toY)
        self.canvas.after(speed, self.snakeMove, speed, toX, toY)

    def moveTo(self, toX, toY):
        self.x = toX
        self.y = toY
        self.canvas.coords(self.node, BOUND_X + self.x, BOUND_Y + self.y, BOUND_X + self.x + 10, BOUND_Y + self.y + 10)
        self.canvas.itemconfig(self.node)

    def changeColor(self):
        self.canvas.itemconfig(self.node, fill=COLOR['BLACK'])

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
        for x in range(48):
            for y in range(48):
                NODE_MATRIX[x][y] = 0
        self.snake = Snake(canvas=self._canvas)
        self._root.bind_all("<Key>", self.key)

        self._canvas.after(1, self.snake.move, self.gameOver)
        randomFood(self._canvas)

    def gameOver(self):
        self._canvas.create_text(WIDTH / 2, 150, text="GAME OVER!")
        self._canvas.create_text(WIDTH / 2, 170, text=self.snake.score)
        start_button = Button(self._canvas, text="Restart", command=self.newGame)
        self._canvas.create_window(200, 250, window=start_button)
        exit_button = Button(self._canvas, text="Exit", command=self._root.quit)
        self._canvas.create_window(300, 250, window=exit_button)
        self._root.unbind("<Key")

    def key(self, event):
        if event.keysym != REVERSE[self.snake.direct]:
            self.snake.direct = event.keysym

    def __init__(self, master=None):
        self._root = master
        self._canvas = Canvas(master, width=WIDTH, height=HEIGHT)
        self._canvas.pack()
        self.background()


def randomFood(canvas):
    global FOOD, NODE_MATRIX
    while True:
        x_food = random.randint(0, 47) * 10
        y_food = random.randint(0, 47) * 10
        if NODE_MATRIX[x_food/10][y_food/10] != 1:
            break
    FOOD = Node(canvas_=canvas, x_=x_food, y_=y_food, color_=COLOR['RED'])


root = Tk()
startDesk = Start(master=root)
root.mainloop()
