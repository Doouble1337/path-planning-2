from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk

root = Tk()

root.geometry('1170x700')

scale_list = [0, 0, 0, 0, 0, 0, 0, 0]


def open_calib():
    calib = Toplevel(root)
    calib.title('Окно калибровки')
    calib.geometry("200x200")


def func_cac(i):
    scale_list[7] = i


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


class MyScale:
    def __init__(self, root, label_name, func_name, color):
        self.Scale = Scale(root, orient=HORIZONTAL,
                           length=250,
                           label=label_name,
                           from_=0,
                           to=255,
                           troughcolor=color,
                           command=lambda i: func_name(i))


det = MyScale(root, "determine", func_det, '#F5E912')
det.Scale.grid(row=0, column=6, columnspan=4)

cac = MyScale(root, "contours approximation coefficient", func_cac, '#ff00ff')
cac.Scale.grid(row=0, column=11, columnspan=6)

scale1 = MyScale(root, "lower_red", func1, '#FF4A4A')
scale1.Scale.grid(row=0, column=0, columnspan=4)

scale2 = MyScale(root, "lower_green", func2, '#21FF77')
scale2.Scale.grid(row=2, column=0, columnspan=4)

scale3 = MyScale(root, "lower_blue", func3, '#73B5FA')
scale3.Scale.grid(row=4, column=0, columnspan=4)

scale4 = MyScale(root, "upper_red", func4, '#FF4A4A')
scale4.Scale.grid(row=6, column=0, columnspan=4)

scale5 = MyScale(root, "upper_green", func5, '#21FF77')
scale5.Scale.grid(row=8, column=0, columnspan=4)

scale6 = MyScale(root, "upper_blue", func6, '#73B5FA')
scale6.Scale.grid(row=10, column=0, columnspan=4)

but_sub = Button(root, text='Submit')
but_sub.grid(row=15, column=18)


but_calib = Button(root, text='Calibration', command=open_calib)
but_calib.grid(row=15, column=19)

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

canvas1 = Canvas(root, height=400, width=400)
image1 = Image.open("D:\Image_test\Test_image.jpg")
resized1 = image1.resize((400, 400))
photo1 = ImageTk.PhotoImage(resized1)
image1 = canvas1.create_image(0, 0, anchor='nw', image=photo1)
canvas1.grid(row=1, column=6, columnspan=6, rowspan=15)

canvas2 = Canvas(root, height=400, width=400)
image2 = Image.open("D:\Image_test\Test_image2.jpg")
resized2 = image2.resize((400, 400))
photo2 = ImageTk.PhotoImage(resized2)
image2 = canvas2.create_image(0, 0, anchor='nw', image=photo2)
canvas2.grid(row=1, column=14, columnspan=6, rowspan=15)


def click(event):
    x = event.x
    y = event.y
    s = "{}x{}".format(x, y)


root.bind('<Button-1>', click)

root.mainloop()

# отдельное окно - картинка, кнопка старта и завершения калибровки
# кнопка калибровки - главное окно
