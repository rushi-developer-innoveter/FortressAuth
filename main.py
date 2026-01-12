import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
from auth import login_user, register_user
from session import create_session, load_session, destroy_session

BG="#0b0f14"; CARD="#11161d"; ACCENT="#1f6feb"; TEXT="#e6edf3"; GREEN="#2ea043"; RED="#ff5c5c"

class App:
    def __init__(self, root):
        self.root=root
        root.geometry("500x540")
        root.configure(bg=BG)
        root.title("FortressAuth")
        self.card=tk.Frame(root,bg=CARD)
        self.card.place(relx=0.5,rely=0.5,anchor="center",width=440,height=480)

        session=load_session()
        if session:
            self.dashboard(session["user"])
        else:
            self.login_ui()

    def clear(self):
        for w in self.card.winfo_children(): w.destroy()

    def entry(self,placeholder,secret=False):
        e=tk.Entry(self.card,bg="#0d1117",fg=TEXT,relief="flat",font=("Segoe UI",11),show="*" if secret else "")
        e.pack(pady=10,ipady=12,fill="x",padx=40)
        e.insert(0,placeholder)
        e.bind("<FocusIn>",lambda a: e.delete(0,"end"))
        return e

    def button(self,text,cmd,color=ACCENT):
        b=tk.Button(self.card,text=text,command=cmd,bg=color,fg="white",relief="flat",font=("Segoe UI",11,"bold"))
        b.pack(pady=12,ipady=12,fill="x",padx=40)

    def login_ui(self):
        self.clear()
        tk.Label(self.card,text="FortressAuth",fg=TEXT,bg=CARD,font=("Segoe UI",20,"bold")).pack(pady=30)
        self.u=self.entry("Username")
        self.p=self.entry("Password",True)
        self.msg=tk.Label(self.card,bg=CARD,fg=RED); self.msg.pack()
        self.button("LOGIN",self.login)
        self.button("REGISTER",self.register_ui,CARD)

    def register_ui(self):
        self.clear()
        tk.Label(self.card,text="Register",fg=TEXT,bg=CARD,font=("Segoe UI",18)).pack(pady=30)
        self.u=self.entry("Username")
        self.p=self.entry("Password",True)
        self.msg=tk.Label(self.card,bg=CARD,fg=RED); self.msg.pack()
        self.button("CREATE",self.register)
        self.button("BACK",self.login_ui,CARD)

    def success_popup(self,text,user):
        popup=tk.Frame(self.root,bg="#0d1117")
        popup.place(relx=0.5,rely=0.4,anchor="center",width=300,height=140)
        tk.Label(popup,text="✔",fg=GREEN,bg="#0d1117",font=("Segoe UI",40)).pack()
        tk.Label(popup,text=text,fg=TEXT,bg="#0d1117").pack()
        self.root.after(1200,lambda:[popup.destroy(),self.dashboard(user)])

    def login(self):
        ok,msg=login_user(self.u.get(),self.p.get())
        if ok:
            create_session(self.u.get())
            self.success_popup("Login Successful",self.u.get())
        else:
            self.msg.config(text=msg)

    def register(self):
        ok,msg=register_user(self.u.get(),self.p.get())
        if ok:
            self.success_popup("Registration Successful",self.u.get())
        else:
            self.msg.config(text=msg)

    def dashboard(self,user):
        self.clear()
        tk.Label(self.card,text=f"Welcome {user}",fg=GREEN,bg=CARD,font=("Segoe UI",20)).pack(pady=50)
        self.button("LOGOUT",self.logout,RED)

    def logout(self):
        destroy_session()
        self.login_ui()

root=tk.Tk()
App(root)
root.mainloop()
