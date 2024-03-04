import customtkinter as ctk

class SubscriptionsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.label = ctk.CTkLabel(self)
        self.label.pack()





class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        #'''  # Comment out to make NOT fullscreen.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #'''

        self.my_frame = SubscriptionsScrollableFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")


app = App()
app.mainloop()