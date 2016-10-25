from Tkinter import *
import random
import threading

WIDTH = 500
HEIGHT = 500
BOUND_X = 10
BOUND_Y = 10


class Snake:
    def __init__(self, canvas_, x_, y_):
        self.canvas = canvas_
        self.x = x_
        self.y = y_
        self.next = None
        self.prev = None
        self.node = self.canvas.create_rectangle(BOUND_X + self.x, BOUND_Y + self.y, BOUND_X + self.x + 10, BOUND_Y + self.y + 10, fill="#000", tag="node")

    def snakeMove(self, speed, toX , toY):
        self.canvas.move(self.node, toX, toY)
        self.canvas.after(speed, self.snakeMove, speed, toX, toY)

    def moveTo(self, toX, toY):
        self.x = toX
        self.y = toY
        self.canvas.delete(self.node)
        self.node = self.canvas.create_rectangle(BOUND_X + self.x, BOUND_Y + self.y, BOUND_X + self.x + 10, BOUND_Y + self.y + 10, fill="#000", tag="node")



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
        self.head = Snake(self._canvas, 20, 0)
        self.node2 = Snake(self._canvas, 10, 0)
        self.node3 = Snake(self._canvas, 0, 0)
        # self.snake_list = [head, node2, node3]
        self.head.next = self.node2
        self. node2.prev = self.head
        self.node2.next = self.node3
        self.node3.prev = self.node2
        self.tail = self.node3

        t = threading.Timer(0.7, self.move)
        t.start()

        # for snake in self.snake_list:
        #     snake.snakeMove(speed=50, toX=1, toY=0)

        # initial food
        self.food()

    def move(self):
        tmp = self.tail.prev
        self.tail.moveTo(self.head.x + 10, self.head.y)
        self.tail.prev = None
        self.tail.next = self.head
        self.head.prev = self.tail
        self.head = self.tail
        self.tail = tmp
        self.tail.next = None

        global t
        t = threading.Timer(0.7, self.move)
        t.start()


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
