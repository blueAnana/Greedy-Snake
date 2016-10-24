from Tkinter import *
import random

WIDTH = 500
HEIGHT = 500
BOUND_X = 10
BOUND_Y = 10


class Snake:
    def __init__(self, canvas, x, y):
        self._canvas = canvas
        self._x = x
        self._y = y
        self._node = canvas.create_rectangle(BOUND_X + self._x, BOUND_Y + self._y, BOUND_X + self._x + 10, BOUND_Y + self._y + 10, fill="#000", tag="node")

    def snakeMove(self, speed, toX , toY):
        self._canvas.move(self._node, toX, toY)
        self._canvas.after(speed, self.snakeMove, speed, toX, toY)


class Start:
    def background(self):
        self._root.title("Greedy Snake!")

        self.w = Label(self._canvas, text="Welcom to Greedy Snake!")
        self._canvas.create_window(250, 100, window=self.w)

        self.start_button = Button(self._canvas, text="Start", command=self.newGame)
        self._canvas.create_window(200, 250, window=self.start_button)
        self.quit_button = Button(self._canvas, text="Exit", command=self._root.quit)
        self._canvas.create_window(300, 250, window=self.quit_button)

    def newGame(self):
        print "Start Game"
        self._canvas.delete("all")
        # Draw the bounding wall
        self._canvas.create_rectangle(10, 10, 490, 490, fill='#fff')

        # initial snake with 3 nodes
        head = Snake(self._canvas, 20, 0)
        node2 = Snake(self._canvas, 10, 0)
        node3 = Snake(self._canvas, 0, 0)
        self.snake_list = [head, node2, node3]

        for snake in self.snake_list:
            snake.snakeMove(speed=50, toX=1, toY=0)

        # initial food
        self.food()

    def isEnd(self):
        return True

    def food(self):
        self.x_food = random.randint(0, 48) * 10
        self.y_food = random.randint(0, 48) * 10
        self.food = self._canvas.create_rectangle(BOUND_X + self.x_food, BOUND_Y + self.y_food, BOUND_X + self.x_food + 10, BOUND_Y + self.y_food + 10, fill="#000", tag="food")

    def __init__(self, master=None):
        self._root = master
        self._canvas = Canvas(master, width=WIDTH, height=HEIGHT)
        self._canvas.pack()
        self.background()

root = Tk()
startDesk = Start(master=root)
root.mainloop()
