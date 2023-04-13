import customtkinter as tk

class PopupWindow(tk.CTkToplevel):
    def __init__(self, master, title, text):
        super().__init__()
        self.title = title
        self.geometry("250x80")
        self.geometry("+%d+%d" %(master.winfo_x()+125,master.winfo_y()+40))

        self.label = tk.CTkLabel(self, text=text)
        self.label.pack(pady=5)

        master.withdraw()

        def on_closing():
            master.deiconify()
            self.destroy()

        self.ok = tk.CTkButton(self, text="Ok", command=on_closing)
        self.protocol("WM_DELETE_WINDOW", on_closing)
        self.ok.pack()