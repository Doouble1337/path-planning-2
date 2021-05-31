from tkinter import *

root = Tk()

root.geometry('1100x700')

det = Scale(root, orient=HORIZONTAL, length=250)
det.grid(row=0, column=6, columnspan=4)

scale1 = Scale(root, orient=HORIZONTAL, length=250)
scale1.grid(row=0, column=0, columnspan=4)

scale2 = Scale(root, orient=HORIZONTAL, length=250)
scale2.grid(row=1, column=0, columnspan=4)

scale3 = Scale(root, orient=HORIZONTAL, length=250)
scale3.grid(row=2, column=0, columnspan=4)

scale4 = Scale(root, orient=HORIZONTAL, length=250)
scale4.grid(row=3, column=0, columnspan=4)

scale5 = Scale(root, orient=HORIZONTAL, length=250)
scale5.grid(row=4, column=0, columnspan=4)

scale6 = Scale(root, orient=HORIZONTAL, length=250)
scale6.grid(row=5, column=0, columnspan=4)

but_sub = Button(root, text='Submit')
but_sub.grid(row=25, column=30)

Lb = Listbox(root, height=3)
Lb.grid(row=7, column=0, columnspan=4)
Lb.insert(1, "1")
Lb.insert(2, "2")
Lb.insert(3, "3")
Lb.insert(4, "4")
Lb.insert(5, "5")
Lb.insert(6, "6")

col_count, row_count = root.grid_size()
for col in range(col_count):
    root.grid_columnconfigure(col, minsize=20)
for row in range(row_count):
    root.grid_rowconfigure(row, minsize=20)

root.mainloop()