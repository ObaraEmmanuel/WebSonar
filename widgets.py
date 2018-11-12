from tkinter import Frame, Entry, StringVar, Spinbox, IntVar, Label


class Input(Entry):

    def __init__(self, parent, **options):
        self.underline = Frame(parent, bg=options.get("fg", "orange"), width=200, height=30)
        self.var = StringVar()
        super().__init__(self.underline, bg=options.get("bg", "#404040"), fg=options.get("fg", "orange"),
                         textvariable=self.var, relief="flat", font="calibri 13", width=30)

    def pack(self, **options):
        self.underline.pack(options)
        self.place(x=0, y=0, relheight=0.95, relwidth=1)

    def val(self, value=None):
        if value:
            self.var.set(value)
        else:
            return self.var.get()


class Search(Entry):

    def __init__(self, parent, **options):
        self.underline = Frame(parent, bg=options.get("fg", "orange"), width=200, height=30)
        self.var = StringVar()
        super().__init__(self.underline, bg=options.get("bg", "#404040"), fg=options.get("fg", "orange"),
                         textvariable=self.var, relief="flat", font="calibri 13", width=30)
        self.search_btn = Label(self.underline,text="\ue721",bg="#404040",fg="orange",font="calibri 13")
        self.search_btn.place(relx=0.8,y=0,relwidth=0.2,relheight=0.95)

    def pack(self, **options):
        self.underline.pack(options)
        self.place(x=0, y=0, relheight=0.95, relwidth=0.8)

    def val(self, value=None):
        if value:
            self.var.set(value)
        else:
            return self.var.get()


class SpinBox(Spinbox):

    def __init__(self, parent, **options):
        self.underline = Frame(parent, bg=options.get("fg", "orange"), width=200, height=30)
        self.var = IntVar()
        super().__init__(self.underline, bg=options.get("bg", "#404040"), fg=options.get("fg", "orange"),
                         textvariable=self.var, relief="flat", font="calibri 13", width=15,
                         buttonbackground=options.get("fg", "#505050"), buttonup="flat", buttondownrelief="flat",
                         from_=options.get("from_", 0), to=options.get("to", 100),
                         )

    def pack(self, **options):
        self.underline.pack(options)
        self.place(x=0, y=0, relheight=0.95, relwidth=1)

    def val(self, value=None):
        if value:
            self.var.set(value)
        else:
            return self.var.get()
