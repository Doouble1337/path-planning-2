from bresenham import bresenham
from tkinter import *
x1 = 1
y1 = 1
x2 = 4
y2 = 10
A = list(bresenham(x1, y1, x2, y2))


window = Tk()
window.title('Работа с canvas')

canvas = Canvas(window,width=600,height=600,bg="white",
          cursor="pencil")
k=40
for i in range (len(A)):
    canvas.create_rectangle(A[i][0]*k,A[i][1]*k,A[i][0]*k + k,A[i][1]*k + k,fill="white",outline="blue")
canvas.create_line(x1 * k,y1 * k,x2 * k,y2 * k,width=1,fill="red")
canvas.pack()
window.mainloop()
