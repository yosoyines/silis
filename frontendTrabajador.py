#Ventana de ingreso de datos a la base de datos
import data_base
from tkinter import *
from tkinter import ttk
import tkinter.messagebox

import random
#import nombres
#import apellidos

class Frontend():
    def __init__(self, root):
        self.root = root
        self.root.title("AMMNI Software - Añadir trabajador")
        self.root.geometry("1150x700+0+0")
        self.root.resizable(0,0)
        self.root.config(bg="SNOW2")

        #Declaramos las variables que vamos a utilizar en el frontend
        wrkID = StringVar()
        nombre = StringVar()
        apellido = StringVar()
        cedula = StringVar()
        bendiciones = StringVar()
        pareja = StringVar()
        fecha = StringVar()
        hora = StringVar()
        simp = StringVar()
        ext = StringVar()
        esp = StringVar()
        noc = StringVar()
        jesp = StringVar()
        wrkID.set("1")


        #========================================= FUNCIONES FRONTEND =======================================
        def clear():
            self.txtnombre.delete(0,END)
            self.txtapellido.delete(0,END)
            self.txtcedula.delete(0,END)
            self.txtbendiciones.delete(0,END)
            pareja.set("")
            self.txtwrkID.delete(0,END)
            self.txtfecha.delete(0,END)
            self.txtincome.delete(0,END)
            self.txtsimp.delete(0,END)
            self.txtext.delete(0,END)
            self.txtesp.delete(0,END)
            self.txtnoc.delete(0,END)
            self.txtjE.delete(0,END)

        def addData():
            #print("Este mensaje deberia de aparecer desde la ventana PRINCIPAL")
            if(len(wrkID.get())!=0):
                data_base.addInfo(nombre.get(), apellido.get(), cedula.get(), bendiciones.get(), pareja.get(),fecha.get(), hora.get(), simp.get(), ext.get(), esp.get(), noc.get(), jesp.get())
                listaTrabajadores.delete(0,END)
                listaTrabajadores.insert(END,(nombre.get(), apellido.get(), cedula.get(), bendiciones.get(), pareja.get(),fecha.get(), hora.get(), simp.get(), ext.get(), esp.get(), noc.get(), jesp.get()))
                tkinter.messagebox.showinfo("AMNNI-Software","Trabajador añadido correctamente, base de datos actualizada.")

        def Display():
            listaTrabajadores.delete(0,END)
            for row in data_base.displayInfo():
                listaTrabajadores.insert(END, row, str(""))

        def a(event):
            global sd
            buscarWrk = listaTrabajadores.curselection()[0]
            sd = listaTrabajadores.get(buscarWrk)
            #print(sd[0])
            #print(sd[1])
            #print(sd[2])
            #print(sd[3])
            #print(sd[4])
            #print(sd[5])
            #print(sd[6])
            #print(sd[7])
            #print(sd[8])
            #print(sd[9])
            print(sd)
            self.txtwrkID.delete(0,END)
            self.txtwrkID.insert(END, sd[0])

            self.txtnombre.delete(0,END)
            self.txtnombre.insert(END, sd[1])

            self.txtapellido.delete(0,END)
            self.txtapellido.insert(END, sd[2])

            self.txtcedula.delete(0,END)
            self.txtcedula.insert(END, sd[3])

            self.txtbendiciones.delete(0,END)
            self.txtbendiciones.insert(END, sd[4])

            pareja.set(sd[5])

            self.txtfecha.delete(0,END)
            self.txtfecha.insert(END, sd[6])

            self.txtincome.delete(0,END)
            self.txtincome.insert(END, sd[7])

            self.txtsimp.delete(0,END)
            self.txtsimp.insert(END, sd[8])

            self.txtext.delete(0,END)
            self.txtext.insert(END, sd[9])

            self.txtesp.delete(0,END)
            self.txtesp.insert(END, sd[7])

            self.txtnoc.delete(0,END)
            self.txtnoc.insert(END, sd[10])

            self.txtjE.delete(0,END)
            self.txtjE.insert(END, sd[11])

        def Delete():
            take = tkinter.messagebox.askyesno("AMNNI Software","Estas seguro que desea eliminar al trabajador de la base de datos? Los datos eliminados no pueden ser recuperados.")
            if take == True:
                if(len(wrkID.get())!=0):
                    data_base.deleteInfo(sd[0])
                    clear()
                    Display()
            else:
                pass

        def Search():
            listaTrabajadores.delete(0,END)
            for row in data_base.searchInfo(wrkID.get(), fecha.get(), hora.get(), simp.get(), ext.get(), esp.get(), noc.get(), jesp.get()):
                listaTrabajadores.insert(END,row,str(""))

        def Update():
            pass

        """
        def ingresoDatosDB(): #Esta funcion es en extremo peligrosa, usarla solo cuando la base de datos sea elimnada. Incorpora a la base: 1 millon de datos distintos
            global x
            global y
            for x in nombres.names:
                #print("Nombres: ",x)
                for y in apellidos.apellidos:
                    #print("Apellidos",y)
                    nombre.set(x)
                    apellido.set(y)
                    #print(x,y)
                    print("Nombre: ",x," Apellido: ",y)
                    wrkID.set("5")
                    cedula.set("cedulaEjemplo")
                    bendiciones.set("0")
                    pareja.set("No")
                    fecha.set("15/12/1974")
                    hora.set(random.randrange(100, 800, 20))
                    simp.set(random.randrange(50, 200, 30))
                    ext.set("0")
                    esp.set("0")
                    noc.set("0")
                    jesp.set("0")
                    addData()
        """
        #ingresoDatosDB()
        #====================================================================================================

        #Declaramos los contenedores (frames) donde iran los widget
        frameGeneral = Frame(self.root, bg="DarkOrchid4")
        frameGeneral.grid()
        #Titulo
        tituloContenedor = Frame(frameGeneral, bg="DarkOrchid4", width=1300, bd=2, padx=4,pady=8,relief=FLAT)
        tituloContenedor.pack(side=TOP)
        self.lblTitulo = Label(tituloContenedor, font=("Arial",37,"bold"),text="GESTOR BASE DE DATOS", bg="DarkOrchid4", fg="Cornsilk")
        self.lblTitulo.grid()
        #Botones
        botonesFrame = Frame(frameGeneral, bd=2, width=1300, height=70, padx=18, pady=10, bg="snow2", relief=FLAT) #DarkOrchid4
        botonesFrame.pack(side=BOTTOM)

        #Frame de ingreso de datos
        frameDato = Frame(frameGeneral, bd=1, width=1300,height=500,padx=20,pady=20,relief=FLAT, bg="snow2")
        frameDato.pack(side=BOTTOM)

        frameDatoIzq = LabelFrame(frameDato, bd=1, width=650, height=500,padx=10,pady=20,relief=FLAT,bg="snow2", font=("Arial",15,"bold"),text="Datos del trabajador")
        frameDatoIzq.pack(side=LEFT)
        frameDatoIzq.grid_propagate(False)

        frameDatoDer = LabelFrame(frameDato, bd=1, width=450, height=500,padx=31,pady=26,relief=FLAT,bg="snow2", font=("Arial",15,"bold"),text="Base de datos")
        frameDatoDer.pack(side=RIGHT)
        frameDatoDer.grid_propagate(False)

        #===============Labels y Entrys ====================
        """Nombre"""
        self.lblnombre = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Nombre:", padx=2, fg="gray13", bg="snow2")
        self.lblnombre.grid(row=0, column=0, sticky=W)
        self.txtnombre = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=nombre)
        self.txtnombre.grid(row=0, column=1, pady=3, padx=20)
        """Apellido"""
        self.lblapellido = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Apellido:", padx=2, fg="gray13", bg="snow2")
        self.lblapellido.grid(row=1, column=0, sticky=W)
        self.txtapellido = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=apellido)
        self.txtapellido.grid(row=1, column=1, pady=3, padx=20)

        """ Cedula identidad """
        self.lblcedula = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Cedula N°:", padx=2, fg="gray13", bg="snow2")
        self.lblcedula.grid(row=2, column=0, sticky=W)
        self.txtcedula = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=cedula)
        self.txtcedula.grid(row=2, column=1, pady=3, padx=20)
        """ Hijos a cargo """
        self.lblbendiciones = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Hijos a cargo:", padx=2, fg="gray13", bg="snow2")
        self.lblbendiciones.grid(row=3, column=0, sticky=W)
        self.txtbendiciones = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=bendiciones)
        self.txtbendiciones.grid(row=3, column=1, pady=3, padx=20)
        """ Conyuge a cargo """
        self.lblpareja = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Conyuge a cargo?:", padx=2, fg="gray13", bg="snow2")
        self.lblpareja.grid(row=4, column=0, sticky=W)
        self.comboCaja = ttk.Combobox(frameDatoIzq, width=52, textvariable=pareja)
        self.comboCaja["values"] = ["Si","No"]
        print("Resultado del combobox conyuge: ",self.comboCaja)
        self.comboCaja.grid(row=4,column=1, padx=2)


        """ ID trabajador"""

        self.lblwrkID = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Trabajador ID:", padx=2, fg="gray13", bg="snow2")
        self.lblwrkID.grid(row=5, column=0, sticky=W)
        self.txtwrkID = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=wrkID, state="disabled")
        self.txtwrkID.grid(row=5, column=1, pady=3, padx=20)
        """ fecha ingreso """
        self.lblfecha = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Fecha de ingreso:", padx=2, fg="gray13", bg="snow2")
        self.lblfecha.grid(row=6, column=0, sticky=W)
        self.txtfecha = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=fecha)
        self.txtfecha.grid(row=6, column=1, pady=3, padx=20)
        """ precio hora"""
        self.lblincome = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Precio de la hora:", padx=2, fg="gray13", bg="snow2")
        self.lblincome.grid(row=7, column=0, sticky=W)
        self.txtincome = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=hora)
        self.txtincome.grid(row=7, column=1, pady=3, padx=20)
        """ horas simples """
        self.lblsimp = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Horas simples trabajadas:", padx=2, fg="gray13", bg="snow2")
        self.lblsimp.grid(row=8, column=0, sticky=W)
        self.txtsimp = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=simp)
        self.txtsimp.grid(row=8, column=1, pady=3, padx=20)
        """ horas extras"""
        self.lblext = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Horas extras trabajadas:", padx=2, fg="gray13", bg="snow2")
        self.lblext.grid(row=9, column=0, sticky=W)
        self.txtext = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=ext)
        self.txtext.grid(row=9, column=1, pady=3, padx=20)
        """ horas especiales """
        self.lblesp = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Extras especiales acumuladas:", padx=2, fg="gray13", bg="snow2")
        self.lblesp.grid(row=10, column=0, sticky=W)
        self.txtesp = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=esp)
        self.txtesp.grid(row=10, column=1, pady=3, padx=20)
        """ horas nocturnas """
        self.lblnoc = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Nocturnas Acumuladas:", padx=2, fg="gray13", bg="snow2")
        self.lblnoc.grid(row=11, column=0, sticky=W)
        self.txtnoc = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=noc)
        self.txtnoc.grid(row=11, column=1, pady=3, padx=20)
        """ jornada especial """
        self.lbljE = Label(frameDatoIzq, font=("Sans", 12, "bold"),text="Jornal Especial:", padx=2, fg="gray13", bg="snow2")
        self.lbljE.grid(row=12, column=0, sticky=W)
        self.txtjE = Entry(frameDatoIzq, font=("Sans", 15, "bold"), width=30, textvariable=jesp)
        self.txtjE.grid(row=12, column=1, pady=3, padx=20)


        #==================== ScrollBar y listbox =============================
        scrollbar = Scrollbar(frameDatoDer)
        scrollbar.grid(row=0,column=1, sticky="ns")
        listaTrabajadores = Listbox(frameDatoDer, width=40,height=16, font=("Sans",12,"bold"), yscrollcommand=scrollbar.set)
        listaTrabajadores.bind("<<ListboxSelect>>",a)
        listaTrabajadores.grid(row=0,column=0, padx=8)
        scrollbar.config(command = listaTrabajadores.yview)

        #==================== BOTONES =========================================
        """ Añadir """
        self.btnAdd = Button(botonesFrame, text="Añadir", font=("Sans",12,"bold"), width=17,height=1, bd=4, command=addData)
        self.btnAdd.grid(row=0,column=0)
        """ Mostrar """
        self.btnShow = Button(botonesFrame, text="Mostrar", font=("Sans",12,"bold"), width=17,height=1, bd=4, command=Display)
        self.btnShow.grid(row=0,column=1)
        """ Limpiar """
        self.btnClear = Button(botonesFrame, text="Limpiar", font=("Sans",12,"bold"), width=17,height=1, bd=4, command=clear)
        self.btnClear.grid(row=0,column=2)
        """ Borrar """
        self.btnDelete = Button(botonesFrame, text="Borrar", font=("Sans",12,"bold"), width=17,height=1, bd=4, command=Delete)
        self.btnDelete.grid(row=0,column=3)
        """ Buscar """
        self.btnSearch = Button(botonesFrame, text="Buscar", font=("Sans",12,"bold"), width=17,height=1, bd=4, command=Search)
        self.btnSearch.grid(row=0,column=4)
        """ Actualizar """
        self.btnUpdate = Button(botonesFrame, text="Actualizar", font=("Sans",12,"bold"), width=17,height=1, bd=4)
        self.btnUpdate.grid(row=0,column=5)
        """ IMPORTAR """
        #self.btnImport = Button(botonesFrame, text="Importar a ventana principal", font=("Sans",12,"bold"), width=17,height=1, bd=4)
        #self.btnImport.grid(row=0,column=6)





if __name__ == "__main__":
    root = Tk()
    ventana = Frontend(root)
    root.mainloop()
