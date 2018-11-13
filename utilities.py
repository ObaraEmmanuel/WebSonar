#  Simple miscellaneous utilities


def center_window(parent, child):
    x = int((parent.winfo_width() - child.winfo_width()) / 2) + parent.winfo_x()
    y = int((parent.winfo_height() - child.winfo_height()) / 2.5) + parent.winfo_y()
    #  2.5 has been used to raise the pop-up windows for convenience
    child.geometry("+{}+{}".format(x, y))


class Events:

    @staticmethod
    def on_click(callback, *elements):
        for element in elements:
            element.bind("<Button-1>", lambda x: callback())

    @staticmethod
    def on_enter(element, callback):
        element.bind("<Enter>", lambda x: callback())
