from tkinter import *
from tkinter import ttk
from Warehouse import *


w = Warehouse(10)
s = Shelf()
w.add_shelf((0, 1), s)
print(w.grid[0][1].shelf)

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
frm.mainloop()