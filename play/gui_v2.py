import tkinter as tk
from ctypes import windll
import threading
from time import sleep

ct = 5
nums = list(range(5))

'''
A class that displays a list on a window, with a refresh button to update the values
Constructor: Test(size of list;)
'''
class Test():
    def __init__(self, ct):
        self.ct = ct
        self.window =tk.Tk()
        self.configureWindow()
        windll.shcore.SetProcessDpiAwareness(1)
        self.runner()
        self.window.mainloop()

    def configureWindow(self):
        self.window.geometry("650x250")

    def refresh(self):
        global nums
        for i in range(self.ct):
            self.objStrings[i].set(str(nums[i]))

    def runner(self):
        global nums
        self.objs = []
        self.objStrings = []
        for i in range(self.ct):
            self.objStrings.append(tk.StringVar())
            self.objStrings[i].set(str(nums[i]))
            obj = tk.Label(
                self.window, 
                textvariable=self.objStrings[i],
                font=("Arial", 25)
            )
            obj.grid(row=0, column=i) #position of label
            obj.config(width=4, height=4) #size of label
            self.objs.append(obj)
        tk.Button(self.window, text="refresh", command = self.refresh).grid()


x = threading.Thread(target=Test, args=(5,))
x.start()
sleep(5)
nums = [10] * ct
print("done constanting") 
x.join()