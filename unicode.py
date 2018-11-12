from tkinter import Tk, Label, Button, Spinbox, IntVar

is_loop = 0


def check():
    data["text"] = chr(int(input_t.get()))
    unicode["text"] = hex(input_t.get()).replace("0x","")


def looper():
    global is_loop
    if is_loop:
        is_loop = 0
    else:
        is_loop = 1


def loop_func():
    if is_loop:
        data["text"] = chr(int(input_t.get()))
        unicode["text"] = hex(input_t.get()).replace("0x", "")
        input_t.set(input_t.get() + 1)
    data.after(100, loop_func)

root = Tk()
root.geometry("400x400")
data = Label(root, font="calibri 30", height=1, width=2)
data.pack()
data.after(100, loop_func)
input_t = IntVar()
input = Spinbox(root, width=30, textvariable=input_t, from_=0,to=100000,command=check)
input.pack()
press = Button(root, text="change", command=check)
press.pack()
loop = Button(root, text="loop", command=looper)
loop.pack()
unicode = Label(root)
unicode.pack()
root.mainloop()
