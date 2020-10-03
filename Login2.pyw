from tkinter import *
import os
from proyecto_bit import *
import time
from tkinter import ttk


"""
self.widthroot = 1710
self.heightroot = 763

self.xPosition = (self.root.winfo_screenwidth()/2) - (self.widthroot/2)
self.yPosition = (self.root.winfo_screenheight()/2) - (self.heightroot/2)

self.root.geometry("{}x{}+{}+{}".format(self.widthroot,self.heightroot,round(self.xPosition),round(self.yPosition))) #geometry(width,height,x,y)
"""


def delete2():
    screen3.destroy()

def delete3():
    screen4.destroy()

def delete4():
    screen5.destroy()

def delete5():
    screen6.destroy()

def login_sucess():

#global screen3
#screen3 = Toplevel(screen)
#screen3.title("Inicio de sesión")
#screen3.geometry("150x100")
#Label(screen3, text = "Sesión iniciada").pack()
#Button(screen3, text = "Aceptar", command =delete2).pack()
    screen2.destroy()
    screen.destroy()

    if __name__ == '__main__':
        root = Tk()
        application = Jornalero(root)
        root.mainloop()


    #delete2()
    #delete3()
    #delete4()


def password_not_recognised():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Error")
    screen4.geometry("150x100+600+300")
    Label(screen4, text = "Contraseña incorrecta").pack()
    ttk.Button(screen4, text = "Aceptar", command =delete3).pack()

def user_not_found():
    global screen5
    screen5 = Toplevel(screen)
    screen5.title("Error")
    screen5.geometry("150x100+600+300")
    Label(screen5, text = "Usuario no encontrado").pack()
    ttk.Button(screen5, text = "Aceptar", command =delete4).pack()


def register_user():
    username_info = username.get()
    password_info = password.get()

    file=open(username_info, "w")
    file.write(username_info+"\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    screen1.destroy()

    global screen6
    screen6 = Toplevel(screen)
    screen6.title("Registro")
    screen6.geometry("150x100+700+400")
    Label(screen6, text = "Registro Exitoso", fg = "green" ,font = ("Sans", 11)).pack()
    ttk.Button(screen6, text = "Aceptar", command = delete5).pack()



def login_verify():

    username1 = username_verify.get()
    password1 = password_verify.get()
    username_entry1.delete(0, END)
    password_entry1.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
        else:
            password_not_recognised()

    else:
        user_not_found()



def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Registrarse")
    screen1.geometry("300x220+600+300")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(screen1, text = "Ingrese sus datos",pady=10).pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Usuario ").pack()

    username_entry = Entry(screen1, textvariable = username)
    username_entry.pack()
    Label(screen1, text = "Contraseña").pack()

    password_entry =  Entry(screen1, textvariable = password, show = '*')
    password_entry.pack()
    Label(screen1, text = "").pack()
    ttk.Button(screen1, text = "Registrarse", width = 10, command = register_user).pack()


def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Iniciar sesión")
    screen2.geometry("280x220+600+300")
    Label(screen2, text = "Ingrese sus datos",pady=10).pack()
    Label(screen2, text = "").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen2, text = "Usuario").pack()
    username_entry1 = Entry(screen2, textvariable = username_verify)
    username_entry1.pack()
    Label(screen2, text = "Contraseña").pack()
    password_entry1 = Entry(screen2, textvariable = password_verify, show = '*')
    password_entry1.pack()
    Label(screen2, text = "").pack()
    ttk.Button(screen2, text = "Iniciar", width = 10, command = login_verify).pack()


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("300x180+600+300")
    screen.resizable(0,0)
    screen.title("SiLiS")
    Label(text = "SiLiS", bg = "grey", width = "300", height = "2", font = ("Sans", 13)).pack()
    Label(text = "").pack()
    ttk.Button(text = "Iniciar sesión", width = "35", command = login).pack()
    Label(text = "").pack()
    ttk.Button(text = "Registrarse", width = "35", command = register).pack()

    screen.mainloop()

main_screen()
