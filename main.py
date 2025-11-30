import tkinter as tk
import calculator as calc 

master = tk.Tk()
master.geometry("300x100") 
master.title("Calculator")

text_area = tk.Entry(master, width=100, justify="center")
text_area.pack()

label = tk.Label(master, text = "results here")
label.pack()

def key_pressed(event):
    match event.keysym:
        case "Return":
            label.config(text = calc.calculate(text_area.get()))
        case "Escape":
            master.destroy()
        case x:
            print("pressed key " + x)

master.bind("<Key>", key_pressed)
master.mainloop()