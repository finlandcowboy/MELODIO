from tkinter import *
import db
import tkinter as tk
import p2

class Auth():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.usernameLabel = Label(self.frame, text="User Name").pack()
        self.username = StringVar()
        self.usernameEntry = Entry(self.frame, textvariable=self.username).pack()
        self.passwordLabel = Label(self.frame, text="Password").pack()
        self.password = StringVar()
        self.passwordEntry = Entry(self.frame, textvariable=self.password, show='*').pack()
        # login button
        self.loginButton = Button(self.frame, text="Login", command=self.validateLogin).pack()
        self.frame.pack()

    def get_user_id(self):
        return self.user_id
    def validateLogin(self):
        if self.username.get() != '' or self.password.get() != '':
            db.create_user(self.username.get(), self.password.get())
            self.master
            self.f = p2.FrameApp(self)
        else:
            print('invalid')

    def register(self):
        pass



def main():
    root = tk.Tk()
    app = Auth(root)

    root.mainloop()



main()