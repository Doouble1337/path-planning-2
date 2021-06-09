from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from enum import IntEnum


class MyScale:
    def __init__(self, root, index, label_name, callback, color):
        self.Scale = Scale(root, orient=HORIZONTAL,
                           length=250,
                           label=label_name,
                           from_=0,
                           to=100,
                           troughcolor=color,
                           command=lambda value: callback(index, int(value) / 100))


class Param(IntEnum):
    LOWER_RED = 0,
    LOWER_GREEN = 1,
    LOWER_BLUE = 2,

    UPPER_RED = 3,
    UPPER_GREEN = 4,
    UPPER_BLUE = 5,

    DETALIZATION = 6,

    APPROXIMATION_COEF = 7,
    MORPHOLOGY_COEF = 8

class GUI:


    def __init__(self, on_param_change):
        self.root = Tk()
        self.root.geometry('1170x700')

        self.params = [0]*8

        self.col_count, self.row_count = self.root.grid_size()
        for col in range(self.col_count):
            self.root.grid_columnconfigure(col, minsize=20)
        for row in range(self.row_count):
            self.root.grid_rowconfigure(row, minsize=20)

        self.Lb = Listbox(self.root, height=3)
        self.Lb.grid(row=14, column=0, columnspan=4)
        self.Lb.insert(1, "1")
        self.Lb.insert(2, "2")
        self.Lb.insert(3, "3")
        self.Lb.insert(4, "4")
        self.Lb.insert(5, "5")
        self.Lb.insert(6, "6")

        self.img_sz = (800, 600)
        self.canvas = Canvas(self.root, width=self.img_sz[0], height = self.img_sz[1])
        self.image = Image.open("test.png")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=1, column=6, columnspan=6, rowspan=15)

        self.det = MyScale(self.root, Param.DETALIZATION, "detalization", on_param_change, '#555555')
        self.det.Scale.grid(row=0, column=6, columnspan=1)

        self.morph = MyScale(self.root, Param.MORPHOLOGY_COEF, "morphology coefficient", on_param_change, '#555555')
        self.morph.Scale.grid(row=0, column=8, columnspan=1)

        self.cac = MyScale(self.root, Param.APPROXIMATION_COEF, "contours approximation coefficient", on_param_change, '#555555')
        self.cac.Scale.grid(row=0, column=7, columnspan=1)

        self.scale1 = MyScale(self.root, Param.LOWER_RED, "lower_red", on_param_change, '#FF4A4A')
        self.scale1.Scale.grid(row=0, column=0, columnspan=4)

        self.scale2 = MyScale(self.root, Param.LOWER_GREEN, "lower_green", on_param_change, '#21FF77')
        self.scale2.Scale.grid(row=2, column=0, columnspan=4)

        self.scale3 = MyScale(self.root, Param.LOWER_BLUE, "lower_blue", on_param_change, '#73B5FA')
        self.scale3.Scale.grid(row=4, column=0, columnspan=4)

        self.scale4 = MyScale(self.root, Param.UPPER_RED, "upper_red", on_param_change, '#FF4A4A')
        self.scale4.Scale.grid(row=6, column=0, columnspan=4)

        self.scale5 = MyScale(self.root, Param.UPPER_GREEN, "upper_green", on_param_change, '#21FF77')
        self.scale5.Scale.grid(row=8, column=0, columnspan=4)

        self.scale6 = MyScale(self.root, Param.UPPER_BLUE, "upper_blue", on_param_change, '#73B5FA')
        self.scale6.Scale.grid(row=10, column=0, columnspan=4)

        self.but_sub = Button(self.root, text='Submit', command = self.submit)
        self.but_sub.grid(row=17, column=6)

        self.but_calib = Button(self.root, text='Calibration', command=self.open_calib)
        self.but_calib.grid(row=17, column=7)

        self.list_label = Label(self.root, text="Some label")
        self.list_label.grid(row=13, column=1)

        self.root.bind('<Button-1>', self.click)

    def open_calib(self):
        self.calib = Toplevel(self.root)
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

    def submit(self):
        print("hello")

    def click(self, event):
        self.x1 = event.x
        self.y1 = event.y

    def set_image(self, image):
        self.image = Image.fromarray(image)
        scale = min(self.img_sz[0] / self.image.size[0], self.img_sz[1] / self.image.size[1])
        self.image = self.image.resize((int(self.image.size[0]*scale), int(self.image.size[1]*scale)))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)
