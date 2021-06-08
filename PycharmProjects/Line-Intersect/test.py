# Python 3 program for Bresenham’s Line Generation
# Assumptions :
# 1) Line is drawn from left to right.
# 2) x1 < x2 and y1 < y2
# 3) Slope of the line is between 0 and 1.
# We draw a line from lower left to upper
# right.


# function for line generation
from tkinter import *
window = Tk()
window.title('Minecraft')

canvas = Canvas(window,width=600,height=600,bg="white",
          cursor='pencil')

canvas.create_rectangle(
    30, 10, 120, 80,
    outline="#fb0", fill="#fb0"
)
k=20
def bresenham(x1, y1, x2, y2):
    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)

    y = y1
    for x in range(x1, x2 + 1):
        canvas.create_rectangle(x * k, y * k, x * k - k, y * k - k, fill="white",
                                outline="blue")

        # Add slope to increment angle formed
        slope_error_new = slope_error_new + m_new

        # Slope error reached limit, time to
        # increment y and update slope error.
        if (slope_error_new >= 0):
            y = y + 1
            slope_error_new = slope_error_new - 2 * (x2 - x1)


# driver function

x1 = 3
y1 = 2
x2 = 16
y2 = 5
bresenham(x1, y1, x2, y2)

# This code is contributed by ash264
canvas.create_line(x1 * k,y1 * k,x2 * k,y2 * k,width=1,fill="red")
canvas.pack()
window.mainloop()
