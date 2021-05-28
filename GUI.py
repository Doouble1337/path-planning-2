import tkinter as tk

window = tk.Tk()

frame1 = tk.Frame(master=window, width=800, height=100, bg="grey")
frame1.pack(fill=tk.BOTH, expand=True)

frame2 = tk.Frame(master=window, width=800, height=500, bg="DarkGrey")
frame2.pack(fill=tk.BOTH, expand=True)

frame3 = tk.Frame(master=window, width=800, height=100, bg="LightGrey")
frame3.pack(fill=tk.BOTH, expand=True)

window.mainloop()