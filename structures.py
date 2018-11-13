from tkinter import Frame, Label, Canvas, ttk

from animate import Animator, FancyLoader

ITEM_HEIGHT = 60


#  TODO Deal with eliminating magic values with constants like the one above


class ItemExplorer(Frame):

    def __init__(self, parent, **options):
        super().__init__(parent, options)
        bar = Frame(self, bg="#505050", height=30)
        bar.pack(side="top", fill="x")
        style = ttk.Style()
        style.configure("Vertical.TScrollbar", troughcolor="#505050", activebackground="#404040", background="#404040")
        self.nav_bar = Frame(bar, bg="#505050", height=30)
        content = Frame(self, bg="#505050")
        content.pack(side="top", fill="both", expand=True)
        self.__root = Canvas(content, bg="#505050", highlightthickness=0)
        self.__root.pack(side="left", fill="both", expand=True)
        self.scroll_holder = Frame(content, bg="#505050", width=3)
        #  TODO Fix scroll bar appearance using ttk styling
        #  FIXME Make scrollbar appearance smooth. Trigger hide callback on scroll.
        self.scroll_holder.pack(side="left", fill="y")
        self.scroll_holder.pack_propagate(0)
        self.scroll = ttk.Scrollbar(self.scroll_holder, orient="vertical", command=self.__root.yview)
        self.scroll.bind("<Enter>", lambda ev: self.soft_show_scroll())
        self.scroll.bind("<Leave>", lambda ev: self.trigger_soft_hide())
        self.__root.config(yscrollcommand=self.scroll.set)
        self.window = self.__root.create_window(0, 0, anchor="nw")
        self.body = Frame(self.__root, bg="#505050", width=self.__root["width"], height=self.__root["height"])
        self.body.pack_propagate(0)
        self.__root.itemconfigure(self.window, window=self.body)
        self.__root.bind("<Configure>", self.on_configure)
        self.__root.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.back = Label(self.nav_bar, bg="#505050", fg="orange", text="\ue760", font="calibri 19", cursor="hand2")
        self.forward = Label(self.nav_bar, bg="#505050", fg="orange", text="\ue761", font="calibri 19", cursor="hand2")
        self.back.pack(side="left", padx=1)
        self.back.bind("<Button-1>", lambda ev: self.back_callback())
        self.forward.pack(side="left", padx=1)
        self.forward.bind("<Button-1>", lambda ev: self.forward_callback())

        self.no_content = Frame(self.body, bg="#505050")
        self.no_content_icon = Label(self.no_content, bg="#505050", fg="#404040", font="calibri 60")
        self.no_content_icon.pack(side="top", pady=2)
        self.no_content_text = Label(self.no_content, height=4, bg="#505050", fg="#1FB27B", font="calibri 12",
                                     wraplength=300)
        self.no_content_text.pack(side="top", fill="y", anchor="n")
        self.no_content.place(relx=0.3, rely=0.3, relwidth=0.8, relheight=0.8)

        self.expand_animate = Animator(3, 15, 1)
        self.contract_animate = Animator(15, 3, 1)
        self.loader = FancyLoader(self.no_content_icon)
        self.loader.start_load()
        self.scroll_soft_hide = True
        self.current_trigger = None
        self.items = []
        self.root_link = None
        self.nothing_to_display()
        self.supports_search = True

    def nothing_to_display(self):
        self.show_alt_text("You haven't tasked us yet")

    def clear_body(self):
        self.no_content.place_forget()

    def start_loader(self):
        self.no_content_text["text"] = "Working on it..."
        self.clear()
        self.loader.start_load()

    def on_configure(self, ev):
        self.__root.itemconfigure(self.window, width=ev.width)
        # self.body.config(width=ev.width)
        self.__root.update_idletasks()
        self.__root.config(scrollregion=self.__root.bbox("all"))
        self.__root.update_idletasks()

    def on_mouse_wheel(self, ev):
        if not self.root_link:
            return
        else:
            if not self.root_link.children:
                return
        self.__root.yview_scroll(-1 * int(ev.delta / 50), "units")
        self.soft_show_scroll()
        self.trigger_soft_hide()

    def trigger_soft_hide(self):
        self.current_trigger = self.scroll.after(2000, self.soft_hide_scroll)

    def soft_hide_scroll(self):
        if self.scroll_soft_hide:
            return
        self.scroll_soft_hide = True
        self.contract_animate.animate(self.scroll_holder, "width")

    def soft_show_scroll(self):
        try:
            self.scroll.after_cancel(self.current_trigger)
        except IndexError:
            pass
        if not self.scroll_soft_hide:
            return
        self.scroll_soft_hide = False
        self.expand_animate.animate(self.scroll_holder, "width")

    def add(self, item):
        self.clear_body()
        self.body.pack_propagate(1)
        self.loader.stop_load()
        item.pack(side="top", fill="x", expand=True, pady=3, padx=5)
        self.items.append(item)
        self.nav_bar.pack(side="top", fill="x")

    def check_scroll(self):
        if len(self.items) * (ITEM_HEIGHT + 6) > self.body["height"]:
            self.scroll.pack(fill="y", expand=True)
        else:
            self.scroll.pack_forget()

    def extract(self):
        if not len(self.root_link.children.keys()):
            self.show_error("We did not find any sub-URLs under {}.".format(self.root_link.web_content.url))
        else:
            if self.items:
                self.clear()
            for item in self.root_link.children:
                self.add(PathItem(self.root_link.children[item], self))
        self.check_scroll()

    def extract_from(self, link):
        self.root_link = link
        self.extract()

    def push(self, deep_recurse):
        if not self.root_link:
            if self.root_link.parent:
                self.root_link = deep_recurse.parent
        self.add(PathItem(deep_recurse, self))
        self.check_scroll()

    def clear(self):
        for item in self.items:
            item.pack_forget()
        self.items = []
        self.check_scroll()

    def back_callback(self):
        print("check")
        if self.root_link.parent:
            self.root_link = self.root_link.parent
            self.extract()

    def forward_callback(self):
        if self.root_link.next:
            self.extract_from(self.root_link.next)

    def show_alt_text(self, text, icon="\ue77f"):
        self.loader.stop_load()
        self.clear()
        self.body.pack_propagate(0)
        self.body.config(height=self.__root["height"], width=self.__root["height"])
        self.no_content_icon["text"] = icon
        self.no_content_text["text"] = text
        self.no_content.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.8)

    def show_error(self, text):
        self.show_alt_text(text, "\ue7ba")


class InvalidItemExplorer(ItemExplorer):

    def __init__(self, parent, **options):
        super().__init__(parent, **options)
        self.nav_bar.pack_forget()

    def push(self, web_content):
        self.add(InvalidItem(self, web_content))
        self.check_scroll()

    def add(self, item):
        super().add(item)
        self.nav_bar.pack_forget()


class PathItem(Frame):

    def __init__(self, recurse_obj=None, parent=None, **options):
        super().__init__(parent.body, options)
        self.content_txt = recurse_obj
        self.parent = parent
        self.title_txt = recurse_obj.web_content.title() if recurse_obj else ""
        self.config(bg="#404040", height=ITEM_HEIGHT)
        self.pack_propagate(0)
        self.thumbnail = Frame(self, bg="#404040", width=80)
        self.thumbnail.pack(side="left")
        self.icon = Label(self.thumbnail, text="\ue753", font="calibri 25", bg="#404040", fg="orange")
        self.icon.pack()
        self.body = body = Frame(self, bg="#404040")
        body.pack(side="left", fill="x", expand=True, anchor="w")
        self.title = Frame(body, bg="#404040")
        self.title.pack(side="top", anchor="w", fill="x")
        self.heading = Label(self.title, bg="#404040", fg="orange", font="calibri 15",
                             text=self.title_txt, anchor="w")
        self.heading.pack(fill="x", anchor="w", expand=True)
        self.heading.bind("<Button-1>", lambda x: self.select())
        self.content = Label(body, bg="#404040", fg="#1FB27B", font="calibri 12",
                             text=self.content_txt.web_content.url if recurse_obj else "",
                             anchor="w")
        self.content.pack(side="top", anchor="w", fill="x")
        self.content.bind("<Button-1>", lambda x: self.select())

    def select(self):
        self.parent.extract_from(self.content_txt)
        self.content_txt.parent.next = self.content_txt


class InvalidItem(PathItem):

    def __init__(self, parent, content, **options):
        super().__init__(None, parent, **options)
        self.content_txt = content
        self.content.config(text=content.error, font="calibri 12 italic")
        self.heading.config(text=content.url, font="calibri 13")
        self.icon.config(text="\ue7ba")

    def select(self):
        pass
