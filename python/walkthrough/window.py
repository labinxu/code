#coding utf-8

import tkinter

class Window(object):
    def __init__(self, name='', title=''):
        self.root = tkinter.Tk()
        self.root.wm_title(title)
        text = tkinter.Text()
        text.pack()
        text.focus_set()
        pass

    def show(self):
        tkinter.mainloop()

    def addMenu(self, menu):
        pass

class Menu(tkinter.Menu):
    def __init__(self,topLevel):
        tkinter.Menu.__init__(self, topLevel)

class Text(tkinter.Text):
    def __init__(self):
        tkinter.Text.__init__(self)

def createMainWindow():

    root = tkinter.Tk()
    root.wm_title('TkDemo')
    text = Text()

    text.pack()
    text.focus_set()
    #window.addMenu()
    menubar = Menu(root)
    def m():

        print('hell')
    # create a pulldown menu, and add it to the menu bar
    filemenu = tkinter.Menu(root, tearoff=0)
    filemenu.add_command(label="Open", command=m)
    filemenu.add_command(label="Save", command=m)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=m)

    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    tkinter.mainloop()
