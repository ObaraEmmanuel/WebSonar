#  Makes WebSonar more friendly
#  Utilizes Tkinter
#  Written by Barracoder
#  Github at Triedcoders

from tkinter import Tk, Frame, Label
from animate import Animator
from dialogs import ClosePrompt, TreeSearch
from structures import ItemExplorer
from widgets import Search


class ToolItem(Label):

    def __init__(self, parent, callback, **options):
        super().__init__(parent, options)
        self.pack(side="left", anchor="w")
        self.bind("<Button-1>", lambda x: callback())


class MenuItem(Label):

    def __init__(self, parent, **options):
        super().__init__(parent, options)
        self.bg = "#404040"
        self.fg = "orange"
        self.parent = parent
        self.pack(side="left", fill="y")
        self.bind("<Enter>", lambda x: self.on_enter())
        self.bind("<Leave>", lambda x: self.on_exit())
        self.bind("<Button-1>", lambda x: self.show())
        self.frame = Frame(self.parent.drop_down, bg=self.bg, height=45)
        retract = Label(self.frame, text="\ue70e", fg="orange", bg="#404040", cursor="hand2")
        retract.pack(side="right")
        retract.bind("<Button-1>", lambda x: self.parent.collapse())

    def build(self, **callbacks):
        for key in callbacks:
            ToolItem(self.frame, callbacks[key], text=key, bg=self.bg, fg="#1FB27B", font="calibri 12", width=15,
                     cursor="hand2",
                     height=35, anchor="center")

    def on_enter(self):
        if self.parent.current_frame[0] == self.frame:
            self.config(bg="#505050", fg=self.fg)
        else:
            self.config(bg=self.bg, fg=self.fg)

    def on_exit(self):
        if self.parent.current_frame[0] == self.frame:
            self.config(bg=self.bg, fg=self.fg)
        else:
            self.config(bg=self.fg, fg=self.bg)

    def show(self):
        if self.parent.current_frame[0] == self.frame:
            return
        self.parent.force_collapse()
        self.parent.set_current(self.frame, self)
        self.config(bg=self.bg, fg=self.fg)
        self.parent.expand()


class MenuBar(Frame):

    def __init__(self, parent, **options):
        super().__init__(parent, options)
        self.pack(side="top", fill="x")
        self.pack_propagate(0)
        holder = Frame(parent, bg="#404040", height=50)
        holder.pack(side="top", fill="x")
        self.drop_down = Frame(holder, bg="#404040", height=0)
        self.drop_down.place(x=0, y=0, relwidth=0.6)
        self.drop_down.pack_propagate(0)
        self.search_bar = Frame(holder, bg="#404040", height=50)
        self.search_bar.place(relx=0.6, y=0, relwidth=0.4)
        self.search_input = Search(self.search_bar)
        self.search_input.config(fg="#1FB27B")
        self.search_input.pack(side="right", padx=5, pady=5)
        self.collapsed, self.expanded = 0, 50
        self.expander = Animator(self.collapsed, self.expanded, 1)
        self.contractor = Animator(self.expanded, self.collapsed, 1)
        self.bind("<Button-1>", lambda x: self.toggle())
        self.is_collapsed = True
        self.current_frame = (None, None)

    def toggle(self):
        if self.is_collapsed:
            self.expand()
        else:
            self.collapse()

    def expand(self):
        if self.is_collapsed:
            self.expander.animate(self.drop_down, "height")
            self.is_collapsed = False

    def force_collapse(self):
        if self.is_collapsed:
            return
        self.drop_down["height"] = 0
        self.is_collapsed = True

    def collapse(self):
        if self.is_collapsed:
            return
        self.contractor.animate(self.drop_down, "height")
        self.is_collapsed = True
        if self.current_frame[0]:
            self.current_frame[0].pack_forget()
            self.current_frame[1].config(bg="orange", fg="#404040")
        self.current_frame = (None, None)

    def set_current(self, frame, menu):
        if self.current_frame[0]:
            self.current_frame[0].pack_forget()
            self.current_frame[1].config(bg="orange", fg="#404040")
        frame.pack(side="top", fill="both", expand=True)
        self.current_frame = (frame, menu)


class App:

    def __init__(self):
        self.root = Tk()
        self.root.config(bg="#454545")
        self.root.geometry("1000x650+{}+{}".format(int((self.root.winfo_screenwidth() - 1000) / 2),
                                                   int((self.root.winfo_screenheight() - 690) / 2)))
        self.root.title("WebSonar 1.0.0")
        self.root.protocol("WM_DELETE_WINDOW", self.terminate)
        self.children = []
        self.content = SwipeFrame(self, bg="#505050")
        self.content.place(x=0, y=0, relwidth=1, relheight=1)

        self.menu = MenuBar(self.content, bg="orange", height=40, cursor="hand2")
        self.file = MenuItem(self.menu, bg="orange", fg="#505050", text="\ue8c8  file", font="calibri 12", width=15)
        self.file.build(**{"\ued25 open": self.blank,
                           "\ue74e Save": self.blank,
                           "\ue749 print": self.blank,
                           "\ue7e8 exit": self.terminate})
        self.search = MenuItem(self.menu, bg="orange", fg="#505050", text="\ue721  search", font="calibri 12",
                               width=15)
        self.search.build(**{"\ue81e tree search": self.tree_search,
                             "\ue71c keyword": self.blank,
                             "\ue773 file search": self.blank,
                             "\uec27 find url": self.blank})
        self.setting = MenuItem(self.menu, bg="orange", fg="#505050", text="\ue713  settings", font="calibri 12",
                                width=15)
        self.setting.build(**{"\ue790 appearance": self.blank,
                              "\uec3f connection": self.blank,
                              "\ue90f search": self.blank, })
        self.about = MenuItem(self.menu, bg="orange", fg="#505050", text="About", font="calibri 12", width=15)
        self.loader = Frame(self.content, bg="orange", height=2)
        # self.loader.pack(side="top", fill="x")
        self.body = Frame(self.content, bg="#404040")
        self.body.pack(side="top", fill="both", expand=True)

        self.nav = Frame(self.body, bg="#404040")
        self.nav.place(x=0, y=0, relwidth=0.3, relheight=1)
        self.base = Frame(self.body, bg="#505050")
        self.base.place(relx=0.3, y=0, relwidth=0.7, relheight=1)

        self.explorer = ItemExplorer(self.base, bg="#505050")
        self.explorer.pack(side="top", fill="both", expand=True)

        self.splash = SwipeFrame(self, bg="#505050")
        # self.splash.place(x=0, y=0, relwidth=1, relheight=1)
        self.start_text = Label(self.splash, text="WebSonar", font="calibri 40", fg="orange", bg="#505050")
        self.start_text.place(relwidth=0.3, relheight=0.2, rely=0.4, relx=0.35)
        # self.root.after(3000, self.splash.swipe)

        #  for i in range(30):
        #  self.explorer.add(PathItem(self.explorer.body))

    def run(self):
        self.root.mainloop()

    def blank(self):
        pass

    def terminate(self):
        ClosePrompt(self.root)

    def tree_search(self):
        TreeSearch(self.root, self.explorer)


class SwipeFrame(Frame):

    def __init__(self, app, **options):
        super().__init__(app.root, options)
        app.children.append(self)

    def swipe(self, animator=None):
        if not animator:
            animator = Animator(self.place_info()["relheight"], 0, 1)
        value = animator.get()
        # print(value)
        if value is None:
            self.place(relheight=0, x=0, y=-2)
            return
        self.place(relheight=animator.get(), x=0, y=-2)
        self.after(int(animator.duration * 10), lambda: self.swipe(animator))


if __name__ == "__main__":
    window = App()
    window.run()
