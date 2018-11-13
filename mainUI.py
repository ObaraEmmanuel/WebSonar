#  Makes WebSonar more friendly
#  Utilizes Tkinter
#  Written by Barracoder
#  Github at Triedcoders

from tkinter import Tk, Frame, Label, StringVar, Canvas

from animate import Animator
from dialogs import ClosePrompt, TreeSearch
from structures import ItemExplorer, InvalidItemExplorer
from utilities import Events
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
        # retract.pack(side="right")
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
        self.file.show()
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

        self.valid_urls = ItemExplorer(self.base, bg="#505050")
        self.invalid_urls = InvalidItemExplorer(self.base, bg="#505050")
        self.commandline = Frame(self.base, bg="#505050")
        self.file_explorer = ItemExplorer(self.base, bg="#505050")
        self.net_test = Frame(self.base, bg="#505050")

        self.explorer = {"valid_urls": self.valid_urls,
                         "invalid_urls": self.invalid_urls,
                         "commandline": self.commandline,
                         "file_explorer": self.file_explorer,
                         "net_test": self.net_test}

        self.navigator = NavHandler(self.nav, self.base)
        self.navigator.add("Valid URLs", "\ue77f", self.valid_urls)
        self.navigator.add("Invalid URLs", "\ue7ba", self.invalid_urls)
        self.navigator.add("Command line", "\ue756", self.commandline)
        self.navigator.add("Retrieved files", "\uec50", self.file_explorer)
        self.navigator.add("Network speed", "\uec4a", self.net_test)
        self.navigator.select(self.navigator[0])

        self.splash = SwipeFrame(self, bg="#505050")
        # self.splash.place(x=0, y=0, relwidth=1, relheight=1)
        self.start_text = Label(self.splash, text="WebSonar", font="calibri 40", fg="orange", bg="#505050")
        self.start_text.place(relwidth=0.3, relheight=0.2, rely=0.4, relx=0.35)
        # self.root.after(3000, self.splash.swipe)

    def run(self):
        self.root.mainloop()

    def blank(self):
        pass

    def terminate(self):
        ClosePrompt(self.root)

    def tree_search(self):
        TreeSearch(self.root, self.explorer)


class NavHandler(Frame):

    def __init__(self, parent, display, **options):
        super().__init__(parent, options)
        self.config(bg="#404040")
        self.selected = None
        self.navigators = []
        self.indicator = Canvas(self, bg="#404040", highlightthickness=0)
        self.indicator.place(relwidth=0.1, relx=0.9, y=0, height=62)
        self.indicator.create_polygon(30, 10, 10, 30, 30, 50, fill="#505050")
        self.pack(fill="both", expand=True)
        self.animator = Animator(0, 62, 0.8)
        self.show_pad = display
        self.currently_displayed = None

    def add(self, text, icon, explorer=None):
        self.navigators.append(NavItem(self, text, icon, explorer))

    def __getitem__(self, index):
        return self.navigators[index]

    def select(self, item):
        if self.selected == item:
            return
        if self.currently_displayed:
            self.currently_displayed.pack_forget()
        self.selected = item
        item.explorer.pack(side="top", fill="both", expand=True)
        self.animator.update(self.indicator.place_info()["y"], self.navigators.index(item) * 62, 0.8)
        self.slide()
        self.currently_displayed = item.explorer

    def slide(self):
        value = self.animator.get()
        if value is None:
            self.indicator.place(relwidth=0.1, relx=0.9, y=self.animator.final, height=62)
            return
        self.indicator.place(y=self.animator.get(), relx=0.9, relwidth=0.1, height=62)
        self.indicator.after(int(self.animator.duration * 10), lambda: self.slide())


class NavItem(Frame):

    def __init__(self, parent, text="Valid URLs", icon="\ue77f", explorer=None, **options):
        super().__init__(parent, options)
        self.parent = parent
        self.config(bg="orange", height=60, cursor="hand2", takefocus=1)
        self.icon = Label(self, bg="#404040", fg="orange", font="calibri 20", text=icon)
        self.icon.place(rely=0.01, relx=0, relheight=0.99, relwidth=0.22)
        self.label = Label(self, bg="#404040", fg="#1fb27b", font="calibri 13", text=text, takefocus=1)
        self.label.place(rely=0.01, relx=0.22, relheight=0.99, relwidth=0.4)
        self.count = StringVar()
        self.count_lbl = Label(self, bg="#404040", fg="orange", font="calibri 11", text="2000", textvariable=self.count)
        self.count_lbl.place(rely=0.01, relx=0.62, relheight=0.99, relwidth=0.38)
        self.place(relwidth=0.9, height=60, y=len(parent.navigators) * 62, x=6)
        # self.pack(side="top",fill="x")
        Events.on_click(self.select_self, self, self.icon, self.label, self.count_lbl)
        self.bind("<FocusIn>", lambda x: self.select_self())
        self.explorer = explorer

    def update_val(self, value):
        self.count.set(value)

    def select_self(self):
        self.parent.select(self)


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
