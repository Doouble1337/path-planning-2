from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk


class MyScale:
    def __init__(self, root, label_name, func_name, color):
        self.Scale = Scale(root, orient=HORIZONTAL,
                           length=250,
                           label=label_name,
                           from_=0,
                           to=255,
                           troughcolor=color,
                           command=lambda i: func_name(i))


class GUI:
    def __init__(self, root):

        self.col_count, self.row_count = root.grid_size()
        for col in range(self.col_count):
            root.grid_columnconfigure(col, minsize=20)
        for row in range(self.row_count):
            root.grid_rowconfigure(row, minsize=20)

        self.scale_list = [0, 0, 0, 0, 0, 0, 0, 0]

        self.Lb = Listbox(root, height=3)
        self.Lb.grid(row=14, column=0, columnspan=4)
        self.Lb.insert(1, "1")
        self.Lb.insert(2, "2")
        self.Lb.insert(3, "3")
        self.Lb.insert(4, "4")
        self.Lb.insert(5, "5")
        self.Lb.insert(6, "6")

        self.canvas1 = Canvas(root, height=400, width=400)
        self.image1 = Image.open("D:\Image_test\Test_image.jpg")
        self.resized1 = self.image1.resize((400, 400))
        self.photo1 = ImageTk.PhotoImage(self.resized1)
        self.canvas1.create_image(0, 0, anchor='nw', image=self.photo1)
        self.canvas1.grid(row=1, column=6, columnspan=6, rowspan=15)

        self.canvas2 = Canvas(root, height=400, width=400)
        self.image2 = Image.open("D:\Image_test\Test_image2.jpg")
        self.resized2 = self.image2.resize((400, 400))
        self.photo2 = ImageTk.PhotoImage(self.resized2)
        self.canvas2.create_image(0, 0, anchor='nw', image=self.photo2)
        self.canvas2.grid(row=1, column=14, columnspan=6, rowspan=15)

        self.image = Image.open("D:\popug\chel.jpg")
        self.resized = self.image.resize((400, 400))
        self.photo = ImageTk.PhotoImage(self.resized)

        self.det = MyScale(root, "determine", self.func_det, '#F5E912')
        self.det.Scale.grid(row=0, column=6, columnspan=4)

        self.cac = MyScale(root, "contours approximation coefficient", self.func_cac, '#ff00ff')
        self.cac.Scale.grid(row=0, column=11, columnspan=6)

        self.scale1 = MyScale(root, "lower_red", self.func1, '#FF4A4A')
        self.scale1.Scale.grid(row=0, column=0, columnspan=4)

        self.scale2 = MyScale(root, "lower_green", self.func2, '#21FF77')
        self.scale2.Scale.grid(row=2, column=0, columnspan=4)

        self.scale3 = MyScale(root, "lower_blue", self.func3, '#73B5FA')
        self.scale3.Scale.grid(row=4, column=0, columnspan=4)

        self.scale4 = MyScale(root, "upper_red", self.func4, '#FF4A4A')
        self.scale4.Scale.grid(row=6, column=0, columnspan=4)

        self.scale5 = MyScale(root, "upper_green", self.func5, '#21FF77')
        self.scale5.Scale.grid(row=8, column=0, columnspan=4)

        self.scale6 = MyScale(root, "upper_blue", self.func6, '#73B5FA')
        self.scale6.Scale.grid(row=10, column=0, columnspan=4)

        self.but_sub = Button(root, text='Submit')
        self.but_sub.grid(row=15, column=18)

        self.but_calib = Button(root, text='Calibration', command=self.open_calib)
        self.but_calib.grid(row=15, column=19)

        self.list_label = Label(root, text="Some label")
        self.list_label.grid(row=13, column=1)

    def open_calib(self):
        self.calib = Toplevel(root)
        self.calib.title('Окно калибровки')
        self.calib.geometry("800x800")

        self.label = Label(self.calib, text="Some label")
        self.label.grid(row=0, column=0, columnspan=4)

        self.canvas = Canvas(self.calib, height=400, width=400)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=2, column=0, rowspan=3, columnspan=4)

        self.but_start = Button(self.calib, text='Start calibration')
        self.but_start.grid(row=7, column=0, rowspan=3, columnspan=4)

        self.but_stop = Button(self.calib, text='Stop calibration')
        self.but_stop.grid(row=7, column=2, rowspan=3, columnspan=4)

    def func_cac(self, i):
        self.scale_list[7] = i

    def func_det(self, i):
        self.scale_list[6] = i

    def func1(self, i):
        self.scale_list[0] = i

    def func2(self, i):
        self.scale_list[1] = i

    def func3(self, i):
        self.scale_list[2] = i

    def func4(self, i):
        self.scale_list[3] = i

    def func5(self, i):
        self.scale_list[4] = i

    def func6(self, i):
        self.scale_list[5] = i

    def click(self, event):
        x = event.x
        y = event.y


root = Tk()
root.geometry('1170x700')

gui = GUI(root)

root.bind('<Button-1>', gui.click)

root.mainloop()
