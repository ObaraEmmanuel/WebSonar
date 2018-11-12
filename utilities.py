#  Simple miscellaneous utilities


def center_window(parent, child):
    x = int((parent.winfo_width() - child.winfo_width()) / 2) + parent.winfo_x()
    y = int((parent.winfo_height() - child.winfo_width()) / 2) + parent.winfo_y()
    child.geometry("+{}+{}".format(x, y))


class Events:

    @staticmethod
    def on_click(element, callback):
        element.bind("<Button-1>", callback)

    @staticmethod
    def on_enter(element, callback):
        element.bind("<Enter>", callback)
