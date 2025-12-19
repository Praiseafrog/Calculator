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
            try:
                label.config(text = calc.calculate(text_area.get()))
            except Exception as e:
                label.config(text = f"Error: {e}")
        case "Escape":
            master.destroy()

master.bind("<Key>", key_pressed)
master.mainloop()