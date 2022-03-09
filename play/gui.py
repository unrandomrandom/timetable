from textwrap import TextWrapper
import tkinter as tk
from ctypes import windll
from time import sleep
import atexit

window = 0

#helper
def display(msg):
    obj = tk.Label(window, textvariable=str(msg))
    obj.pack()
    return obj

def update(nums, objs):
    if type(objs) is not list:
        objs.set(str(nums))
    else:
        for i in range(len(nums)):
            objs[i].set(str(nums[i]))

def runFunction(myFunction):
    windll.shcore.SetProcessDpiAwareness(1)
    window = tk.Tk()
    myFunction()
    window.mainloop()

def increment(nums, objs):
    for i in range(len(nums)):
        objs[i].text.set(str(nums[i]))
    # update(nums, objs)

def runner():
    nums = [str(i) for i in range(5)]
    objs = [tk.Label(window, textvariable=tk.StringVar()) for i in range(len(nums))]
    # foo = [tk.Label(window, textvariable=i) for i in objs]
    list(map(lambda x: x.pack(), objs))
    # update(nums, objs)
    tk.Button(window, text="refresh", command = (increment, nums, objs)).pack()

runFunction(runner)