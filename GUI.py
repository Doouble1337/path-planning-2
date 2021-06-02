from tkinter import *
from PIL import Image, ImageTk

root = Tk()

root.geometry('1170x700')

scale_list = [0, 0, 0, 0, 0, 0, 0]

a = 100

det = Scale(root, orient=HORIZONTAL, length=250, label="determine", to=a, command=lambda i: func_det(i))
det.grid(row=0, column=6, columnspan=4)

scale1 = Scale(root, orient=HORIZONTAL, length=250, label="lower_red", to=a, command=lambda i: func1(i))
scale1.grid(row=0, column=0, columnspan=4)

scale2 = Scale(root, orient=HORIZONTAL, length=250, label="lower_green", to=255, command=lambda i: func2(i))
scale2.grid(row=2, column=0, columnspan=4)

scale3 = Scale(root, orient=HORIZONTAL, length=250, label="lower_blue", to=255, command=lambda i: func3(i))
scale3.grid(row=4, column=0, columnspan=4)

scale4 = Scale(root, orient=HORIZONTAL, length=250, label="upper_red", to=255, command=lambda i: func4(i))
scale4.grid(row=6, column=0, columnspan=4)

scale5 = Scale(root, orient=HORIZONTAL, length=250, label="upper_green", to=255, command=lambda i: func5(i))
scale5.grid(row=8, column=0, columnspan=4)

scale6 = Scale(root, orient=HORIZONTAL, length=250, label="upper_blue", to=255, command=lambda i: func6(i))
scale6.grid(row=10, column=0, columnspan=4)

but_sub = Button(root, text='Submit')
but_sub.grid(row=15, column=31)

list_label = Label(root, text="Some label")
list_label.grid(row=13, column=1)

Lb = Listbox(root, height=3)
Lb.grid(row=14, column=0, columnspan=4)
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


def func_det(i):
    scale_list[6] = i


def func1(i):
    scale_list[0] = i


def func2(i):
    scale_list[1] = i


def func3(i):
    scale_list[2] = i


def func4(i):
    scale_list[3] = i


def func5(i):
    scale_list[4] = i


def func6(i):
    scale_list[5] = i


canvas1 = Canvas(root, height=400, width=400)
image1 = Image.open("D:\Image_test\Test_image.jpg")
resized1 = image1.resize((400, 400))
photo1 = ImageTk.PhotoImage(resized1)
image1 = canvas1.create_image(0, 0, anchor='nw', image=photo1)
canvas1.grid(row=1, column=4, columnspan=15, rowspan=15)

canvas2 = Canvas(root, height=400, width=400)
image2 = Image.open("D:\Image_test\Test_image2.jpg")
resized2 = image2.resize((400, 400))
photo2 = ImageTk.PhotoImage(resized2)
image2 = canvas2.create_image(0, 0, anchor='nw', image=photo2)
canvas2.grid(row=1, column=19, columnspan=6, rowspan=15)


def click(event):
    x = event.x
    y = event.y
    s = "{}x{}".format(x, y)


root.bind('<Button-1>', click)

root.mainloop()
