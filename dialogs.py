import threading
from tkinter import Toplevel, Label, Frame

import utilities
from scrapper import DeepRecurse, WebContent
from widgets import Input, SpinBox


class Dialog(Toplevel):

    def __init__(self, parent, content, **options):
        super().__init__(parent, options)
        self.grab_set()
        self.focus_force()
        self.resizable(0, 0)
        self.content = content
        self.config(bg="#404040")
        self.attributes("-toolwindow", True)
        self.parent = parent
        self.body = Frame(self, bg="#404040")
        self.body.pack(side="top", fill="both", expand=True, pady=10)
        self.buttons = Frame(self, bg="#404040")
        self.buttons.pack(side="top", fill="x")
        cancel = Label(self.buttons, font="calibri 12", width=20, fg="orange", bg="#505050", text="Cancel",
                       cursor="hand2")
        cancel.pack(side="left")
        cancel.bind("<Button-1>", lambda x: self.destroy())
        self.activator = activator = Label(self.buttons, font="calibri 12", width=20, fg="orange", bg="#505050",
                                           text="Exit", cursor="hand2")
        activator.pack(side="right")
        activator.bind("<Button-1>", lambda x: content.activate())

    def show_content(self):
        self.content.pack(fill="x", padx=3)
        self.update_idletasks()
        utilities.center_window(self.parent, self)

    def activate_text(self, text):
        self.activator["text"] = text


class ClosePrompt(Frame):

    def __init__(self, parent, **options):
        self.dialog = Dialog(parent, self, **options)
        super().__init__(self.dialog.body, options)
        self.dialog.activate_text("Exit")
        self.parent = parent
        self.message = Label(self, font="calibri 12", text="Are you sure you want to exit?", bg="#404040", fg="#1fb27b",
                             height=3)
        self.message.pack(side="top", fill="both", expand=True)
        self.dialog.show_content()

    def activate(self):
        self.parent.destroy()


class TreeSearch(Frame):

    def __init__(self, parent, explorer, **options):
        self.dialog = Dialog(parent, self, **options)
        super().__init__(self.dialog.body, options)
        self.dialog.show_content()
        self.dialog.activate_text("Search")
        self.explorer = explorer
        self.config(bg="#404040")
        self.lbl = Label(self, font="calibri 12", text="Enter url to be searched", bg="#404040", fg="#1fb27b",
                         height=1, anchor="w", width=20)
        self.lbl.pack(side="top", anchor="n", pady=3, padx=10, fill="x")
        self.link = Input(self, width=30)
        self.link.pack(side="top", anchor="n", fill="x", padx=10)
        self.lbl2 = Label(self, font="calibri 12", text="Search depth", bg="#404040", fg="#1fb27b",
                          height=1, anchor="w", width=30)
        self.lbl2.pack(side="top", anchor="w", pady=3, padx=10)
        self.depth = SpinBox(self, width=30)
        self.depth.val(5)
        self.depth.pack(side="top", anchor="w", padx=10)

    def get_depth(self):
        depth = 5
        try:
            depth = int(self.depth.get())
        except ValueError:
            pass
        return depth

    def start_extraction(self, depth):
        try:
            self.explorer["valid_urls"].root_link = DeepRecurse(WebContent(self.link.val(),
                                                                           {"User-Agent": "Mozilla/5.0"}),
                                                                max_depth=depth)
        except ValueError as e:
            self.explorer["valid_urls"].show_error(e)
            return
        self.explorer["valid_urls"].root_link.recurse(self.explorer)

    def activate(self):
        try:
            depth = self.get_depth()
            self.dialog.destroy()
            self.explorer["valid_urls"].start_loader()
            threading.Thread(target=lambda: self.start_extraction(depth)).start()
        except ValueError as e:
            self.dialog.destroy()
            self.explorer["valid_urls"].show_error(str(e))
