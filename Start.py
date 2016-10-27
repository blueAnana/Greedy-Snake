from Tkinter import *
import random
import threading
import pyHook
import pythoncom
import msvcrt

WIDTH = 500
HEIGHT = 500
BOUND_X = 10
BOUND_Y = 10

DIRECT = "Right"

class Snake:
    def __init__(self, canvas):
        self.canvas_ = canvas
        self.head = Node(self.canvas_, 20, 0)
        self.node = Node(self.canvas_, 10, 0)
        self.tail = Node(self.canvas_, 0, 0)
        self.head.next = self.node
        self.node.prev = self.head
        self.node.next = self.tail
        self.tail.prev = self.node

    def move(self):
        tmp = self.tail.prev
        self.tail.moveTo(self.head.x + 10, self.head.y)
        self.tail.prev = None
        self.tail.next = self.head
        self.head.prev = self.tail
        self.head = self.tail
        self.tail = tmp
        self.tail.next = None
        print DIRECT
        global t
        if self.head.x < 470:
            t = threading.Timer(0.7, self.move)
            t.start()
        print "END"


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
        self.x_food = random.randint(0, 48) * 10
        self.y_food = random.randint(0, 48) * 10
        self.food = Node(canvas_=self._canvas, x_=self.x_food, y_=self.y_food)

    # def getDirect(self):
    #     while True:
    #         key1 = msvcrt.getch()
    #         print ord(key1)
    #         if ord(key1) == '\xe0':
    #             key2 = msvcrt.getch()
    #             DIRECT = "Down"
    #             print ord(key2)

    def OnKeyboardEvent(event):
        print 'MessageName:', event.MessageName
        print 'Message:', event.Message
        print 'Time:', event.Time
        print 'Window:', event.Window
        print 'WindowName:', event.WindowName
        print 'Ascii:', event.Ascii, chr(event.Ascii)
        print 'Key:', event.Key
        print 'KeyID:', event.KeyID
        print 'ScanCode:', event.ScanCode
        print 'Extended:', event.Extended
        print 'Injected:', event.Injected
        print 'Alt', event.Alt
        print 'Transition', event.Transition
        print '---'

        if event.Key == "Left" or event.Key == "Right" or event.Key == "Down" or event.Key == "Up":
            DIRECT = event.Key

        # return True to pass the event to other handlers
        return True

    def getDirect(self):
        # create a hook manager
        hm = pyHook.HookManager()
        # watch for all mouse events
        hm.KeyDown = self.OnKeyboardEvent
        # set the hook
        hm.HookKeyboard()
        # wait forever
        pythoncom.PumpMessages()

    def __init__(self, master=None):
        self._root = master
        self._canvas = Canvas(master, width=WIDTH, height=HEIGHT)
        self._canvas.pack()
        t = threading.Timer(0.1, self.getDirect)
        t.start()
        self.background()

root = Tk()
startDesk = Start(master=root)
root.mainloop()
