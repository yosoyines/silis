# -- coding: utf-8 --
"""
Software liquidacion de sueldos automatico
Copyright 2018 - AMNNI Software
Version Alpha

"""

"""
NOTAS:
-Tomar valores de una fuente en comun del convenio de salarios para actualizacion automatica
-Agregar los datos del trabajador
-Corregir valor fonasa cuando se selecciona hijos a cargo pero se ingresa valor cero (0)
-Agregar pago de feriado no laborable
- Si Nominal es menor a 15000, alerta por ser menor a Sueldo minimo nacional, y que suba el valor hora

"""

#================ DEVELOPER PLACE ================
"""
NOTAS DE ACTUALIZACION (Aqui estaria bueno añadir las modificaciones y añadidos que le agregamos al programa con el fin de documentar un poco mejor el codigo e ir plasmando los avances)
** Ajuste de GUI para sistema operativo Windows - 7/2/2019
** Correccion de error cuando se creaba la ventana de mensual, ahora la ventana se ejecuta correctamente y elimina la ventana anterior
mostrando los datos del mensual dentro de los Entry correspondientes - 8/2/2019 22:45
** Añadido funciones de liquidacion Aguinaldo y Licencia (en proceso de creacion) y conexion con el frontend de la base de datos - 10/2/2019
** Funcionalidad de impresion de sueldos, correccion de varios errores - 3/3/2019
** Eliminacion de Entry conyuge, colocacion de un combobox con opciones si o no - 3/3/2019
"""
#=================================================


from tkinter import *
from tkinter import ttk
import random #Esto servira para asignar el valor de ID del trabajador
import tkinter.messagebox
from datetime import datetime
import time
from frontendTrabajador import *
from data_base import *
import os
#from PIL import *
#from frontendTrabajador import bendiciones


hora1 = ""
valorFonasa = 0.045
liquidoreal = 0
i = 0

class Jornalero():

    def __init__(self, root):
        global conyugee

        self.root = root
        self.root.title("- Liquidacion de trabajador -")


        self.widthroot = 1710
        self.heightroot = 763

        self.xPosition = (self.root.winfo_screenwidth()/2) - (self.widthroot/2)
        self.yPosition = (self.root.winfo_screenheight()/2) - (self.heightroot/2)

        self.root.geometry("{}x{}+{}+{}".format(self.widthroot,self.heightroot,round(self.xPosition),round(self.yPosition))) #geometry(width,height,x,y)


        self.root.resizable(0, 0) #resizable(x,y)

        #self.root.minsize(1350, 750)
        self.root.config(background="SNOW2")

        # Frame contenedor de los demas frames
        contenedor = Frame(self.root, bg="SNOW2", bd=15, relief=FLAT)
        contenedor.grid()

        # Frame del nombre del trabajador
        nombre = Frame(contenedor, bd=14, width=1670, height=100, padx=10, relief=FLAT, bg="steelblue3")
        nombre.grid(row=0, column=0, columnspan=4, sticky=W)

        # Frame de ingreso de datos trabajados
        ingresoDatos = LabelFrame(contenedor, bd=14, width=450, height=610, padx=10, relief=FLAT, bg="SNOW3") #SNOW3
        ingresoDatos.grid(row=1, column=0, columnspan=4, sticky=W)

        # Frame adicional a ingresos de datos
        datosAdicional = Frame(contenedor, bd=14, width=440, height=610, padx=10, relief=FLAT, bg="SNOW2") #SNOW2
        datosAdicional.grid(row=1, column=1, sticky=E)

        # Frame contenedor del visor de datos
        contenedorVisor = Frame(contenedor, bd=14, width=780, height=610,padx=6, relief=FLAT, bg="SNOW2")
        contenedorVisor.grid(row=1, column=2, columnspan=4, sticky=E)

        # Frame donde se ubicara el visor de datos
        #textoVisorDatos=(font=14)
        visorDatos = LabelFrame(contenedorVisor, bd=14, width=370,height=340, padx=5, relief=FLAT, bg="SNOW2", text="Nominal",font=("Sans", 14, "bold"))
        visorDatos.grid(row=0, column=0, sticky=W)


        # Frame donde se ubicara el visor de datos de descuento
        visorDescuento = LabelFrame(contenedorVisor, bd=14, width=370, height=340, padx=10, relief=FLAT, bg="SNOW2", text="Descuentos",font=("Sans", 14, "bold"))
        visorDescuento.grid(row=0, column=1, sticky=E)

        # Frame donde se va a mostrar la liquidacion
        contenedorLiquidacion = Frame(contenedorVisor, bd=14, width=740,height=120, padx=10, relief=FLAT, bg="snow2")
        contenedorLiquidacion.grid(row=1, column=0, columnspan=4, sticky=W)

        # Frame donde estaran los botones: ATRAS - LIQUIDAR - SIGUIENTE
        contenedorBotones = Frame(contenedorVisor, bd=14, width=740,height=140, padx=10, relief=FLAT, bg="SNOW2") #, bg="SNOW2"
        contenedorBotones.grid(row=2, column=0, columnspan=4, sticky=W)

        # Sucesion de comandos para evitar la redimension de los frames
        nombre.grid_propagate(False)
        ingresoDatos.grid_propagate(False)
        datosAdicional.grid_propagate(False)
        contenedorVisor.grid_propagate(False)
        visorDatos.grid_propagate(False)
        visorDescuento.grid_propagate(False)
        contenedorBotones.grid_propagate(False)
        contenedorLiquidacion.grid_propagate(False)


        #==================================== CONEXION BASE DE DATOS BACKEND ===================================================
        def seleccion_Hora_Liquidacion_Automatica():
            global minutosReloj
            global segundosReloj
            global horasReloj
            global i
            global texto
            xyz = data_base.getID()
            #print(horasReloj,minutosReloj, segundosReloj)
            print(i)
            print(xyz)

            def re2():

                tkinter.messagebox.showinfo("AMNNI-SOFTWARE","Dia y hora guardados, liquidacion automatica configurada para el dia {} a la hora {}:{}.".format(day.get(),hour.get(),minute.get()))
                screen2.destroy()

                def recall():

                    print(day.get(), hour.get(), minute.get())

                    if day.get()==time.strftime("%d") and hour.get()== horasReloj and minute.get() == minutosReloj:
                        siguiente()

                    self.root.after(200,recall) #Esto genera un bucle
                recall()


            #tkinter.messagebox.showinfo("AMMNI-SOFTWARE","""
            #En la ventana que se generara a continuacion de este mensaje, debera ingresar el dia y la hora que desea que se realice la liquidacion de toda la base de datos de forma completamente automatica. Tenga cuidado, esta funcion podria llegar a fallar en ciertas circunstancias que podrian provocar un problema para su empresa. Sea responsable y este igualmente pendiente del sistema el dia de la liquidacion.

            #-AMNNI SOFTWARE
            #""")
            screen2 = Toplevel(self.root)
            screen2.title("Seleccione el dia y la hora para liquidacion automatica")
            tlevelWidth = 350
            tlevelHeight = 110
            tLevelxPosition = (screen2.winfo_screenwidth()/2) - (tlevelWidth/2)
            tLevelyPosition = (screen2.winfo_screenheight()/2) - (tlevelHeight/2)
            screen2.geometry("{}x{}+{}+{}".format(tlevelWidth,tlevelHeight,round(tLevelxPosition),round(tLevelyPosition)))
            screen2.resizable(0,0)
            day = StringVar()
            hour = StringVar()
            minute = StringVar()

            tLevelFrame = LabelFrame(screen2, text="Ingrese los datos", bg="steelblue3", width=350, height=150)
            tLevelFrame.grid()
            tLevelFrame.grid_propagate(False)

            tLevelLbl = Label(tLevelFrame, text="DIA: ", font=("Sans", 12, "bold"), bg="snow3")
            tLevelLbl.grid(row=0, column=0)

            tLevelEntryDay = Entry(tLevelFrame, textvariable=day, width=10)
            tLevelEntryDay.grid(row=0, column=1, padx=20, pady=20)

            tLevelLblHour = Label(tLevelFrame, text="HORA: ", font=("Sans", 12, "bold"), bg="snow3")
            tLevelLblHour.grid(row=0,column=2, padx=20, pady=20)

            tLevelEntryHour = Entry(tLevelFrame, textvariable=hour, width=5)
            tLevelEntryHour.grid(row=0, column=3, pady=20)

            tLevelLblHour = Label(tLevelFrame, text=":", font=("Sans", 12, "bold",), bg="steelblue3", fg="white")
            tLevelLblHour.grid(row=0,column=4)

            tLevelEntryMinute = Entry(tLevelFrame, textvariable=minute, width=5)
            tLevelEntryMinute.grid(row=0, column=5, pady=20)

            tLevelbtnAceptar = Button(tLevelFrame, text="Aceptar", command=re2)
            tLevelbtnAceptar.grid(row=1,column=5)


        def siguiente():
            global data
            global i
            global active
            global trade
            global xy
            global texto
            #print("Este print deberia de aparecer en el minuto seleccionado")

            self.txtWorker_ID.configure(state="disabled")
            self.txtfechaIngreso.configure(state="disabled")
            self.txtpesoHora.configure(state="disabled")
            self.txtHs_simples.configure(state="disabled")
            self.txtHs_extra.configure(state="disabled")
            self.txtHs_esp.configure(state="disabled")
            self.txtHs_noc.configure(state="disabled")
            self.txtjornadaEsp.configure(state="disabled")

            xy = data_base.getID()

            i = 0
            active = True


            if active == True:
                while active:
                    i +=1
                    #print("Esto es el valor de i: ",i)

                    if i > len(xy):
                        #print("Esto deberia de aparecer en la consola si i es mayor al tamaño de la base")
                        texto = tkinter.messagebox.showinfo("AMNNI-Software","Liquidacion finalizada. Recibos de sueldos generados")

                        self.txtWorker_ID.configure(state="normal")
                        self.txtfechaIngreso.configure(state="normal")
                        self.txtpesoHora.configure(state="normal")
                        self.txtHs_simples.configure(state="normal")
                        self.txtHs_extra.configure(state="normal")
                        self.txtHs_esp.configure(state="normal")
                        self.txtHs_noc.configure(state="normal")
                        self.txtjornadaEsp.configure(state="normal")

                        break


                    for data in data_base.selectUnique(i):


                        idTrabajador.set(data[0])
                        fechaIngresoTrabajador.set(data[6])

                        pesoHora.set(data[7])
                        hsSimples.set(data[8])
                        hsExtra.set(data[9])
                        hsEspeciales.set(data[10])
                        hsNocturnas.set(data[11])
                        jornadaEsp.set(data[12])


                        self.progress_bar_db['value'] = data[0]
                        self.progress_bar_db['maximum'] = len(xy)
                        self.progress_bar_db.update()


                        Liquidar()
                        reciboSueldo()

        def reciboSueldo():
            global data
            global jornales
            global totalextras
            global totalEspeciales
            global totalNocturnas
            global totalJornadaEspecial
            global nominalDescuento
            global irpf
            global liquidoreal
            global descBPS
            global descFonasa
            global descFRL
            global descGral
            global liquido1
            global hora2
            global recibo

            recibo = open("ReciboSueldos/recibo sueldo {} {} FECHA {}.txt".format(data[1],data[2],fecha.get()), "w", encoding="utf-8")
            recibo.write(
            """

        ╔══════════════════════════════════ DATOS EMPRESA ══════════════════════════════════════════╗
        ║                                                                                           ║
        ║   Empresa: AMMNI Software  RUT:  210326540017     Nro BPS: 1234567890  Nro MTSS: 98765432 ║
        ║   Zonamerica, Perimetral y Ruta 8, MONTEVIDEO                                             ║
        ║                                                                                           ║
        ╠══════════════════════════════════ DATOS TRABAJADOR ═══════════════════════════════════════╣
        ║                                                                                           ║
        ║    Nombre: {0} {1}                   Documento: {32}      Ingreso: {2}                    ║
        ║    Cargo: Programador Jr           Oficina: Zonamerica         Nro Funcionario: {3}       ║
        ║    Fecha liquidacion: {4}           Tipo: JORNALERO                                       ║
        ║                                                                                           ║
        ╠═══════════════════════════════════════════════════════════════════════════════════════════╣
        ║    CONCEPTO                Cant                  Unid                     TOTAL           ║
        ║                                                                                           ║
        ║    Horas simples            {5}                   {6}                     {7}             ║
        ║    Horas extras             {8}                    {9}                     {10}           ║
        ║    Horas extras especiales  {11}                     {12}                     {13}        ║
        ║    Horas Nocturnas          {14}                     {15}                        {16}     ║
        ║    Feriado pago             {17}                       {18}                        {19}   ║
        ║                                                                                           ║
        ╠══════╦═══════════════════════════════════════════════════════════════════════════╦════════╣
        ║      ║    TOTAL NOMINAL:                                                   {20}  ║        ║
        ║      ╚═══════════════════════════════════════════════════════════════════════════╝        ║
        ║                                                                                           ║
        ║    BPS:                     {21}                                            {22}          ║
        ║    Fonasa:                  {23}                                           {24}           ║
        ║    FRL:                     {25}                                           {26}           ║
        ║    IRPF:                                                                   {27}           ║
        ╚══════╦═══════════════════════════════════════════════════════════════════════════╦════════╝
               ║    TOTAL DESCUENTOS:                                                {28}  ║
               ╠═══════════════════════════════════════════════════════════════════════════╣
               ║    LIQUIDO A COBRAR:                                                {29}  ║
               ╚═══════════════════════════════════════════════════════════════════════════╝

        ╔═══════════════════════════════════════════════════════════════════════════════════════════╗
        ║                                       --- Via 1 ---                                       ║
        ║    La empresa declara haber efectuado los aportes de seguridad social correspondientes a  ║
        ║                        los haberes liquidados el mes anterior                             ║
        ╠═══════════════════════════════════════════════════════════════════════════════════════════╣
        ║                                                                                           ║
        ╠════════════════════════════ Firma de conformidad del trabajador ══════════════════════════╣
        ║                                                                                           ║
        ║    Recibi el importe mencionado y las copias correspondientes a la liquidacion            ║
        ║    Fecha liquidacion: {30}                                                                ║
        ║    Hora liquidacion:  {31}                                                                ║
        ║                                                                                           ║
        ║    Firma: ______________________________________________________                          ║
        ╚═══════════════════════════════════════════════════════════════════════════════════════════╝
            """.format(data[1],data[2],data[6],data[0],fecha.get(), hsSimples.get(), pesoHora.get(), round(jornales), hsExtra.get(), pesoHora.get(), round(totalextras), hsEspeciales.get(), pesoHora.get(), round(totalEspeciales), hsNocturnas.get(), pesoHora.get(), round(totalNocturnas), jornadaEsp.get(), round(totalJornadaEspecial), round(totalJornadaEspecial), nominalDescuento, bps.get(), round(descBPS), fonasa.get(), round(descFonasa), frl.get(), round(descFRL), round(irpf), round(liquido1), round(liquidoreal),   fecha.get(), hora2, data[3])
            )
            #print(data[1])
            recibo.close()


        def Display():
            listaTrabajadores.delete(0,END)
            for row in data_base.displayInfo():
                #print(row)
                listaTrabajadores.insert(END, row, str(""))


        def a(event):
            global sd
            buscarWrk = listaTrabajadores.curselection()[0]
            sd = listaTrabajadores.get(buscarWrk)

            self.txtWorker_ID.delete(0,END)
            self.txtWorker_ID.insert(END, sd[0])


            self.txtfechaIngreso.delete(0,END)
            self.txtfechaIngreso.insert(END, sd[6])

            self.txtpesoHora.delete(0,END)
            self.txtpesoHora.insert(END, sd[7])

            self.txtHs_simples.delete(0,END)
            self.txtHs_simples.insert(END, sd[8])

            self.txtHs_extra.delete(0,END)
            self.txtHs_extra.insert(END, sd[9])

            self.txtHs_esp.delete(0,END)
            self.txtHs_esp.insert(END, sd[10])

            self.txtHs_noc.delete(0,END)
            self.txtHs_noc.insert(END, sd[11])

            self.txtjornadaEsp.delete(0,END)
            self.txtjornadaEsp.insert(END, sd[12])

        scrollbar = Scrollbar(datosAdicional)
        scrollbar.grid(row=0,column=1, sticky="ns")
        listaTrabajadores = Listbox(datosAdicional, width=40,height=16, font=("Sans",14,"bold"), yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)
        listaTrabajadores.bind("<<ListboxSelect>>",a)
        listaTrabajadores.grid(row=0,column=0, padx=8)
        scrollbar.config(command = listaTrabajadores.yview)
        #=======================================================================================================================



        # Comienzo de la funcion que hace andar el reloj
        def tick():
            global hora1
            global hora2
            global minutosReloj
            global segundosReloj
            global horasReloj
            # Hora actual de la pc
            hora2 = time.strftime('%H:%M:%S')

            # actualizamos el texto cuando cambia
            if hora2 != hora1:
                hora1 = hora2
                minutosReloj = time.strftime("%M")
                segundosReloj = time.strftime("%S")
                horasReloj = time.strftime("%H")
                self.lblTitleHora.config(text=hora2)

            self.lblTitleHora.after(200, tick)
        # FIN DEL RELOJ


        #Creamos una barra de menu
        def men():
            tkinter.messagebox.showinfo("AMNNI-Software","Pestaña en proceso de creacion")

        def jor():
            tkinter.messagebox.showinfo("AMNNI-Software","Ya te encuentras dentro de la ventana Jornalero")

        def det():
            tkinter.messagebox.showinfo("AMNNI-Software","Pestaña en proceso de creacion")
        def diario():
            tkinter.messagebox.showinfo("AMNNI-Software","Pestaña en proceso de creacion")
        def aguinaldo():
            tkinter.messagebox.showinfo("AMNNI-Software","Pestaña en proceso de creacion")
        def licencia():
            tkinter.messagebox.showinfo("AMNNI-Software","Pestaña en proceso de creacion")


        def anadir(): #Ejecuta el frontend para añadir trabajadores a la base de datos
            root.destroy() #Destruye la ventana principal de jornalero

            def anadirVentana():
                if __name__ == "__main__" or __name__=="proyecto_bit":
                    root = Tk()
                    ventana = Frontend(root)
                    root.mainloop()
            anadirVentana()

            def x():
                if __name__ == "__main__" or __name__=="proyecto_bit":
                    root = Tk()
                    ventana = Jornalero(root)
                    root.mainloop()
            x()


        def barra():
            menubar = Menu(self.root)
            #file = Menu(menubar, tearoff=0)
            sueldo = Menu(menubar, tearoff=0)
            help = Menu(menubar, tearoff=0)
            dbWork = Menu(menubar, tearoff=0)
            selectHour = Menu(menubar, tearoff=0)
            self.root.config(menu=menubar)

            sueldo.add_command(label="Mensual", command=men)
            sueldo.add_command(label="Jornalero", command=jor)
            sueldo.add_command(label="Destajista", command=det)
            sueldo.add_command(label="Aguinaldo", command=aguinaldo)
            sueldo.add_command(label="Licencia", command=licencia)
            menubar.add_cascade(menu=sueldo, label="Liquidacion")

        #Añadimos la pestaña Añadir a la base de datos
            dbWork.add_command(label="Gestionar Base de Datos", command=anadir)
            menubar.add_cascade(menu=dbWork, label="Gestionar")

        #Añadimos la pestaña seleccionar hora de liquidacion
            selectHour.add_command(label="Seleccionar fecha para liquidacion automatica", command=seleccion_Hora_Liquidacion_Automatica)
            menubar.add_cascade(menu=selectHour, label="Liquidacion Automatica")
        #Añadimos menu "acerca de"
            help.add_command(label="Sobre GDA", command=diario)
            help.add_command(label="Como utilizar", command=diario)
            menubar.add_cascade(menu=help, label="Acerca de")







        def seleccionar():
            global valorFonasa
            """
            if(bendiciones.get()!= "0"):
                print("esto ")
                hijos.set(1)
                fonasa.set("6%")
                valorFonasa = 0.06
                hijoscargo.set("")
                self.txthijosCargo.configure(state="normal")
                self.txthijosCargo.configure({"background": "lightgreen"})

            elif(hijos.get() != 1):
                self.txthijosCargo.configure(state="disabled")
                hijoscargo.set("0")
        """
            if(hijos.get() == 1 and conyuge.get() == 1):
                fonasa.set("8%")
                valorFonasa = 0.08
                self.txthijosCargo.configure(state="normal")
                self.txthijosCargo.configure({"background": "lightgreen"})
                self.txtconyugeCargo.configure(state="normal")
                self.txtconyugeCargo.configure({"background": "lightgreen"})
            elif(conyuge.get() != 1):
                #self.txtconyugeCargo.configure(state="disabled")
                self.cmBox.set("")
                self.cmBox["values"] = ["",""]

            if(conyuge.get() == 1 and hijos.get() == 0):
                fonasa.set("6.5%")
                valorFonasa = 0.065
                #self.txtconyugeCargo.configure(state="normal")
                #self.txtconyugeCargo.configure({"background": "lightgreen"})
                self.cmBox = ttk.Combobox(ingresoDatos)
                self.cmBox["values"] = ["Si","No"]
                self.cmBox.grid(row=16, column=1, pady=3, padx=20)

            elif(conyuge.get() != 1):
                #self.txtconyugeCargo.configure(state="disabled")
                #conyugecargo.set("")
                self.cmBox.set("")
                self.cmBox["values"] = ["",""]

            if(hijos.get() == 0 and conyuge.get() == 0):
                fonasa.set("4.5%")
                valorFonasa = 0.045

        def discapacidad():

            if opcion.get() == 1:
                self.lblCuantosDisca = Label(ingresoDatos, font=("Sans", 12, "bold"), text="Cuantos:", padx=2, fg="grey14", bg="SNOW3")
                self.lblCuantosDisca.grid(row=16, column=0)
                self.txtCuantosDisca = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, textvariable=cantidadDisca)
                self.txtCuantosDisca.grid(row=16, column=1, pady=3, padx=20)
                cantidadDisca.set("")

                self.lblconyugeCargo.grid(row=17, column=0, sticky=W)
                #self.txtconyugeCargo.grid(row=17, column=1, pady=3, padx=20)

                self.cmBox = ttk.Combobox(ingresoDatos)
                self.cmBox.grid(row=17, column=1, pady=3, padx=20)

            elif opcion.get() != 1:
                opcion.set(2)
                self.lblCuantosDisca.grid_remove()
                self.txtCuantosDisca.grid_remove()

                self.lblconyugeCargo.grid(row=16, column=0, sticky=W)
                #self.txtconyugeCargo.grid(row=16, column=1, pady=3, padx=20)
                self.cmBox.grid(row=16, column=1, pady=3, padx=20)




        valorBPS = 0.15
        valorFRL = 0.00125

        fecha = StringVar()
        bps = StringVar()
        fonasa = StringVar()
        frl = StringVar()
        hijoscargo = StringVar()
        conyugecargo = StringVar()

        cantidadDisca = StringVar()

        idTrabajador = StringVar()
        fechaIngresoTrabajador = StringVar()
        pesoHora = StringVar()
        hsSimples = StringVar()
        hsExtra = StringVar()
        hsEspeciales = StringVar()
        hsNocturnas = StringVar()
        jornadaEsp = StringVar()

        hijos = IntVar()
        conyuge = IntVar()
        opcion = IntVar()
        opcionConyuge = IntVar()
        #hijos.set(1)
        pesoHora.set("")
        hsSimples.set("")
        hsExtra.set("")
        hsEspeciales.set("")
        hsNocturnas.set("")
        jornadaEsp.set("")

        hijoscargo.set("0") #Valores fijos, no cambiar
        #conyugecargo.set("0") #Valores fijos, no cambiar
        cantidadDisca.set("0") #Valores fijos, no cambiar


        def Liquidar():
            global valorFonasa
            global liquidoreal
            global jornales
            global totalextras
            global totalEspeciales
            global totalNocturnas
            global totalJornadaEspecial
            global nominalDescuento
            global irpf
            global liquidoreal
            global descBPS
            global descFonasa
            global descFRL
            global descGral
            global liquido1
            global data
            global conyugee
            global recibo

            # Liquidamos el sueldo del trabajador, ingresado en los entry de la ventana main
            # ================ Calculo nominal ========================

            hora = float(pesoHora.get())
            base = float(hsSimples.get())
            extra = float(hsExtra.get())
            especiales = float(hsEspeciales.get())
            nocturnas =  float(hsNocturnas.get())
            jornadaEspecial = float(jornadaEsp.get())

            jornales = hora * base
            totalextras = (hora * extra) * 2
            totalEspeciales = (hora * especiales)*2.5
            totalNocturnas = (hora + (hora * 0.20)) * nocturnas
            totalJornadaEspecial = ((8 * hora)) * jornadaEspecial

            nominalBruto = jornales + totalextras + totalEspeciales
            nominalDescuento = jornales + totalextras + totalEspeciales

            if nocturnas != 0:
                nominalBruto = jornales + totalextras + totalEspeciales + totalNocturnas
                nominalDescuento = jornales + totalextras + totalEspeciales + totalNocturnas

            if jornadaEspecial != 0:
                nominalBruto = jornales + totalextras + totalEspeciales + totalJornadaEspecial
                nominalDescuento = jornales + totalextras + totalEspeciales + totalJornadaEspecial

            if nocturnas != 0 and jornadaEsp != 0:
                nominalBruto = jornales + totalextras + totalEspeciales + totalNocturnas + totalJornadaEspecial
                nominalDescuento = jornales + totalextras + totalEspeciales + totalNocturnas + totalJornadaEspecial

            BPC = 3848 * 10
            rango8 = ""
            rango7 = round((442520-288601)*0.31)
            rango6 = round((288600-192401)*0.27)
            rango5 = round((192400-115441)*0.25)
            rango4 = round((115440-57721)*0.24)
            rango3 = round((57720-38481)*0.15)
            rango2 = round((38480-26937)*0.10)
            rango1 = ""

            if nominalBruto > BPC:
                nominalBruto = nominalBruto * 1.06

            if nominalBruto > 442521:
                tabla1 = rango2 + rango3 + rango4 + rango5 + \
                    rango6 + rango7 + ((nominalBruto - 442521)*0.36)
                ###print("Rango 8",tabla1)
            if nominalBruto > 288601:
                tabla1 = rango2 + rango3 + rango4 + rango5 + rango6 + ((nominalBruto - 288601)*0.31)
                ##print("Rango 7",tabla1)
            if nominalBruto > 192401:
                tabla1 = rango2 + rango3 + rango4 + rango5 + ((nominalBruto - 192401)*0.27)
                ##print("Rango 6",tabla1)
            if nominalBruto > 115441:
                tabla1 = rango2 + rango3 + rango4 + ((nominalBruto - 115441)*0.25)
                ##print("Rango 5",tabla1)
            if nominalBruto > 57721:
                tabla1 = rango2 + rango3 + ((nominalBruto - 57721)*0.24)
                ##print("Rango 4",tabla1)
            if nominalBruto > 38481:
                tabla1 = rango2 + ((nominalBruto - 38481)*0.15)
                ##print("Rango 3",tabla1)
            if nominalBruto > 26937:
                tabla1 = ((nominalBruto - 26937)*0.10)
                ##print("Rango 2",tabla1)
            if nominalBruto <= 26936:
                tabla1 = nominalBruto - 26936
                ##print("Rango 1",tabla1)
            if tabla1 < 0:
                tabla1 = 0


            # Comienzo de los descuentos TABLA 2
            precioHijos = 4169
            precioDiscapacitado = 8337
            descBPS = nominalDescuento * valorBPS
            descFonasa = nominalDescuento * valorFonasa
            descFRL = nominalDescuento * valorFRL
            descGral = descBPS + descFonasa + descFRL
            totalDiscap = float(cantidadDisca.get())

            discaDescuentos = 0
            conyugeDisca = 0

            """ Entry del hijo cuando esta vacio, cambia de color el fondo """
            if hijoscargo.get() == '':
                self.txthijosCargo.configure({"background": "#FFC300"})

            """ entry del conyuge """
            if conyuge.get() == 1:

                if self.cmBox.get() == "Si":
                    print("Esto deberia de aparecer si selecciono SI")
                    conyugeDisca = precioDiscapacitado
                    print(conyugeDisca)
                else:
                    print("Esto deberia de aparecer si selecciono NO")
                    print(conyugeDisca)
                    conyugeDisca = 0

            totalhijos = float(hijoscargo.get())

            if totalhijos <= 5:
                #self.txthijosCargo.configure({"background": "lightgreen"})
                hijosDescuento = totalhijos * precioHijos

            else:
                #self.txthijosCargo.configure({"background": "#E35454"})
                hijosDescuento = 5 * precioHijos

            try:
                if totalDiscap > totalhijos:
                    self.txtCuantosDisca.configure({"background": "#E35454"})
                else:
                    self.txtCuantosDisca.configure({"background": "lightgreen"})
            except:
                pass

            if opcion.get() == 1:
                # Aca filtramos si tiene 1 hijo y ese hijo es discapacitado, solo sumamos el discapacitado para las deducciones
                if cantidadDisca.get() == "1" and hijoscargo.get() == "1":
                    hijosDescuento = 0
                    discaDescuentos = totalDiscap * precioDiscapacitado
                    totalDescuentoMasDisca = descGral + discaDescuentos

                # Aca filtramos para las deducciones ya con los hijos sumados y en el caso de que sea discapacitado
                else:
                    discaDescuentos = totalDiscap * precioDiscapacitado
                    hijosDescuento = (totalhijos * precioHijos) - (precioHijos * totalDiscap)
                    totalDescuentoMasDisca = descGral + discaDescuentos + hijosDescuento

                if totalDescuentoMasDisca > 57720:
                    tabla2 = totalDescuentoMasDisca * 0.08
                    ##print("Los descuentos superaron los 57720")
                else:
                    tabla2 = totalDescuentoMasDisca * 0.10
                    ##print("los descuentos no superaron los 57720")

            else:
                cantidadDisca.set("0")
                discaDescuentos = 0
                totalDescuento = descGral + hijosDescuento
                if totalDescuento > 57720:
                    tabla2 = totalDescuento * 0.08
                    ##print("Los descuentos superaron los 57720")
                else:
                    tabla2 = totalDescuento * 0.10
                    ##print("los descuentos no superaron los 57720")

            irpf = tabla1 - tabla2
            if irpf < 0:
                irpf = 0
                liquido1 = descGral + irpf
                liquidoreal = nominalDescuento - liquido1
            else:
                liquido1 = descGral + irpf
                liquidoreal = nominalDescuento - liquido1

            def imprimirLiquido():
                global liquidoreal
                self.txtVisor.delete(1.0, "end")
                self.txtVisorDesc.delete(1.0, "end")
                self.lblLiquido = Label(contenedorLiquidacion, text="                    ", font=("Sans", 50, "bold"), padx=5, fg="black", bg="skyblue2").place(x=350, y=45, anchor=CENTER)
                self.lblLiquido = Label(contenedorLiquidacion, text=("$", round(liquidoreal)),width=800, font=("Sans", 50, "bold"), padx=5, fg="black", bg="skyblue2").place(x=350, y=45, anchor=CENTER)
                self.txtVisor.insert(END, "$ por Hora:\t\t\t\t$" + pesoHora.get()+"\n")
                self.txtVisor.insert(END, "Horas Simples:\t\t\t\t" + hsSimples.get()+"\n")
                self.txtVisor.insert(END, "Horas Extras:\t\t\t\t" + hsExtra.get()+"\n")
                self.txtVisor.insert(END, "Horas Especiales:\t\t\t\t" + hsEspeciales.get()+"\n")
                self.txtVisor.insert(END, "Horas Nocturnas:\t\t\t\t" + hsNocturnas.get()+"\n")
                self.txtVisor.insert(END, "Jornadas Especiales:\t\t\t\t" + jornadaEsp.get()+"\n")
                self.txtVisor.insert(END, "\t\t\t\t\t" + "\n")
                self.txtVisor.insert(END, "Sueldo Nominal:\t\t\t\t${}".format(round(nominalDescuento)) + "\n")
                self.txtVisor.insert(END, "Sueldo Nominal para IRPF:\t\t\t\t${}".format(round(nominalBruto)) + "\n")
                self.txtVisor.insert(END, "Valor de la Tabla 1 para IRPF:\t\t\t\t${}".format(round(tabla1)) + "\n")

                self.txtVisorDesc.insert(END, "Sueldo Nominal:\t\t\t\t${}".format(round(nominalDescuento)) + "\n")
                self.txtVisorDesc.insert(END, "Descuento BPS:\t\t\t\t${}".format(round(descBPS)) + "\n")
                self.txtVisorDesc.insert(END, "Descuento Fonasa:\t\t\t\t${}".format(round(descFonasa)) + "\n")
                self.txtVisorDesc.insert(END, "Descuento FRL:\t\t\t\t${}".format(round(descFRL)) + "\n")
                self.txtVisorDesc.insert(END, "Total Descuentos:\t\t\t\t${}".format(round(descGral)) + "\n")
                self.txtVisorDesc.insert(END, "Hijos a cargo:\t\t\t\t" + hijoscargo.get() + "\n")
                self.txtVisorDesc.insert(END, "\t\t\t\t\t" + "\n")
                self.txtVisorDesc.insert(END, "IRPF:\t\t\t\t${}".format(round(irpf)) + "\n")


            for data in data_base.selectUnique(self.txtWorker_ID.get()):
                #print("ESTO ES LA VARIABLE INCREMENTABLE: ",i)
                #print("ESTO ES EL DATA: ",data)
                self.txtWorker_ID.delete(0,END)
                self.txtWorker_ID.insert(END, data[0])

                self.txtfechaIngreso.delete(0,END)
                self.txtfechaIngreso.insert(END, data[6])

                pesoHora.set(data[7])
                hsSimples.set(data[8])
                hsExtra.set(data[9])
                hsEspeciales.set(data[10])
                hsNocturnas.set(data[11])
                jornadaEsp.set(data[12])



            imprimirLiquido()
            reciboSueldo()

            # ------------------ FIN DE LA LIQUIDACION ------------------





        bps.set("15%")
        frl.set("0.125%")
        fonasa.set("4.5%")
        fecha.set(time.strftime("%d-%m-%Y"))
        tipoTrabajo = StringVar()
        tipoTrabajo.set("JORNALERO")

        self.lbldate = Label(nombre, textvariable=fecha, font=("Sans", 30, "bold"),pady=8, bd=5, bg="steelblue3", fg="Cornsilk").grid(row=0, column=0)

        self.lblTitle = Label(nombre, textvariable=tipoTrabajo, font=("Sans", 30, "bold"),pady=8, bd=5, bg="steelblue3", fg="Cornsilk", anchor=CENTER).place(x=815, y=36, anchor=CENTER)

        self.lblTitleHora = Label(nombre, font=("Sans", 30, "bold"),pady=8, bd=5, bg="steelblue3", fg="Cornsilk")
        self.lblTitleHora.place(x=1630, y=0, anchor=NE)

        # Añadir informacion nominal
        self.lblWorker_ID = Label(ingresoDatos, font=("Sans", 12, "bold"),text="Trabajador ID:", padx=2, fg="gray13", bg="snow3")
        self.lblWorker_ID.grid(row=0, column=0, sticky=W)
        self.txtWorker_ID = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, textvariable=idTrabajador)
        self.txtWorker_ID.grid(row=0, column=1, pady=3, padx=20)

        # ==== Fecha de ingreso del trabajador ====
        self.lblfechaIngreso = Label(ingresoDatos, font=("Sans", 12, "bold"), text="Fecha de ingreso:", padx=2, fg="gray13", bg="snow3")
        self.lblfechaIngreso.grid(row=1, column=0, sticky=W)
        self.txtfechaIngreso = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, textvariable=fechaIngresoTrabajador)
        self.txtfechaIngreso.grid(row=1, column=1, pady=3, padx=20)

        # ==== Valor de la hora ====
        pesohs = StringVar()
        pesohs.set("$ x Hora:")
        self.lblpesoHora = Label(ingresoDatos, font=("Sans", 12, "bold"),textvariable=pesohs, padx=2, fg="gray13", bg="snow3")
        self.lblpesoHora.grid(row=2, column=0, sticky=W)
        self.txtpesoHora = Entry(ingresoDatos, font=("Sans", 12, "bold"),width=15, textvariable=pesoHora)
        self.txtpesoHora.grid(row=2, column=1, pady=3, padx=20)

        # =====horas simples ====
        hsS = StringVar()
        hsS.set("Horas Simples:")
        self.lblHs_simples = Label(ingresoDatos, font=("Sans", 12, "bold"),textvariable=hsS, padx=2, fg="gray13", bg="snow3")
        self.lblHs_simples.grid(row=3, column=0, sticky=W)
        self.txtHs_simples = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, textvariable=hsSimples)
        self.txtHs_simples.grid(row=3, column=1, pady=3, padx=20)

        # ==== horas extras ===
        hsE = StringVar()
        hsE.set("Horas Extras:")
        self.lblHs_extra = Label(ingresoDatos, font=("Sans", 12, "bold"),textvariable=hsE, padx=2, fg="gray13", bg="snow3")
        self.lblHs_extra.grid(row=4, column=0, sticky=W)
        self.txtHs_extra = Entry(ingresoDatos, font=("Sans", 12, "bold"),width=15, textvariable=hsExtra)
        self.txtHs_extra.grid(row=4, column=1, pady=3, padx=20)

        # ==== Horas extras especiales ====
        hsEsp = StringVar()
        hsEsp.set("Horas Extras Especiales:")
        self.lblHs_esp = Label(ingresoDatos, font=("Sans", 12, "bold"),textvariable=hsEsp, padx=2, fg="gray13", bg="snow3")
        self.lblHs_esp.grid(row=5, column=0, sticky=W)
        self.txtHs_esp = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, textvariable=hsEspeciales)
        self.txtHs_esp.grid(row=5, column=1, pady=3, padx=20)

        # ==== Horas Nocturnas ====
        self.lblHs_noc = Label(ingresoDatos, font=("Sans", 12, "bold"),text="Horas Nocturnas:", padx=2, fg="gray13", bg="snow3")
        self.lblHs_noc.grid(row=6, column=0, sticky=W)
        self.txtHs_noc = Entry(ingresoDatos, font=("Sans", 12, "bold"),width=15, textvariable=hsNocturnas)
        self.txtHs_noc.grid(row=6, column=1, pady=3, padx=20)

        # ==== Jormadas especiales ====
        self.lbljornadaEsp = Label(ingresoDatos, font=("Sans", 12, "bold"),text="Jornadas Especiales:", padx=2, fg="gray13", bg="snow3")
        self.lbljornadaEsp.grid(row=7, column=0, sticky=W)
        self.txtjornadaEsp = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, textvariable=jornadaEsp)
        self.txtjornadaEsp.grid(row=7, column=1, pady=3, padx=20)

        # ==== Gente a cargo ====
        self.lblGente = Label(ingresoDatos, font=("Sans", 12, "bold"), text="Gente a cargo:", padx=2, fg="gray13", bg="snow3").place(x=12, y=250, anchor=W)
        Checkbutton(ingresoDatos, text="Hijos", variable=hijos, onvalue=1, offvalue=0, bg="snow3", font=("Sans", 12, "bold"), command=seleccionar).place(x=334, y=250, anchor=W)
        Checkbutton(ingresoDatos, text="Conyuge", variable=conyuge, onvalue=1, offvalue=0, bg="snow3", font=("Sans", 12, "bold"), command=seleccionar).place(x=330, y=250, anchor=E)

        # Separador ============
        self.lbljornadaEsp = Label(ingresoDatos, font=("Sans", 12, "bold"),text=" ", padx=2, fg="gray13", bg="snow3")
        self.lbljornadaEsp.grid(row=9, column=0, sticky=W)
        self.lbljornadaEsp = Label(ingresoDatos, font=("Sans", 12, "bold"),text=" ", padx=2, fg="gray13", bg="snow3")
        self.lbljornadaEsp.grid(row=10, column=0, sticky=W)

        # Añadir informacion descuentos
        self.lblBPS = Label(ingresoDatos, font=("Sans", 12, "bold"),text="BPS", padx=2, fg="gray13", bg="snow3")
        self.lblBPS.grid(row=11, column=0, sticky=W)
        self.txtBPS = Entry(ingresoDatos, font=("Sans", 12, "bold"),width=15, textvariable=bps, state="disabled")
        self.txtBPS.grid(row=11, column=1, pady=3, padx=20)

        self.lblFONASA = Label(ingresoDatos, font=("Sans", 12, "bold"),text="Fonasa", padx=2, fg="gray13", bg="snow3")
        self.lblFONASA.grid(row=12, column=0, sticky=W)
        self.txtFONASA = Entry(ingresoDatos, font=("Sans", 12, "bold"),width=15, textvariable=fonasa, state="disabled")
        self.txtFONASA.grid(row=12, column=1, pady=3, padx=20)

        self.lblFRL = Label(ingresoDatos, font=("Sans", 12, "bold"),text="FRL", padx=2, fg="gray13", bg="snow3")
        self.lblFRL.grid(row=13, column=0, sticky=W)
        self.txtFRL = Entry(ingresoDatos, font=("Sans", 12, "bold"),width=15, textvariable=frl, state="disabled")
        self.txtFRL.grid(row=13, column=1, pady=3, padx=20)

        self.lblhijosCargo = Label(ingresoDatos, font=("Sans", 12, "bold"), text="Hijos a cargo:", padx=2, fg="gray13", bg="snow3")
        self.lblhijosCargo.grid(row=14, column=0, sticky=W)
        self.txthijosCargo = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, state="disabled", textvariable=hijoscargo)
        self.txthijosCargo.grid(row=14, column=1, pady=3, padx=20)

        # Filtrando si tiene hijos discapacitados a su cargo
        self.lblhijosDisca = Label(ingresoDatos, font=("Sans", 12, "bold"), text="Alguno es discapacitado?:", padx=2, fg="gray13", bg="snow3")
        self.lblhijosDisca.grid(row=15, column=0, sticky=W)
        Radiobutton(ingresoDatos, text="Si", variable=opcion, value=1, bg="snow3",font=("Sans", 12, "bold"), command=discapacidad).place(x=278, y=395)
        Radiobutton(ingresoDatos, text="No", variable=opcion, value=2, bg="snow3",font=("Sans", 12, "bold"), command=discapacidad).place(x=335, y=395)


        self.lblconyugeCargo = Label(ingresoDatos, font=("Sans", 12, "bold"), text="Conyuge Discapacitado?:", padx=3, fg="gray13", bg="snow3")
        self.lblconyugeCargo.grid(row=16, column=0, sticky=W)
        self.cmBox = ttk.Combobox(ingresoDatos, textvariable=conyugecargo)
        self.cmBox["values"] = ["Si","No"]
        self.cmBox.grid(row=16, column=1, pady=3, padx=20)
        #self.txtconyugeCargo = Entry(ingresoDatos, font=("Sans", 12, "bold"), width=15, state="disabled", textvariable=conyugecargo)
        #self.txtconyugeCargo.grid(row=16, column=1, pady=3, padx=20)

        # Añadir visor y botones
        # Botones
        self.btnAtras = Button(datosAdicional, text="MOSTRAR DATOS", padx=20, pady=10, bd=2, font=("Sans", 26, "bold"), width=15, height=1, bg="snow3", command=Display).place(x=35, y=525, anchor=W)

        self.btnLiquidar = Button(ingresoDatos, text="LIQUIDAR INDIVIDUAL", padx=20, pady=10, bd=2, font=("Sans", 26, "bold"), width=16, height=1, bg="steelblue3", command=Liquidar).place(x=375, y=570, anchor=SE)

        self.btnSiguiente = Button(contenedorBotones, text="LIQUIDAR BASE DE DATOS COMPLETA", padx=20, pady=10, bd=2, font=("Sans", 26, "bold"), width=33,height=1, bg="steelblue2", command=siguiente).place(x=702, y=52, anchor=E)

        self.progress_bar_db = ttk.Progressbar(contenedorBotones, orient=HORIZONTAL, length=730, mode="determinate")
        self.progress_bar_db.place(x=702, y=110, anchor=E)

        """
        xy = data_base.getID() #ESTO ES UNA LISTA
        print(xy)
        self.prueba = Scale(contenedorBotones, from_=0, to=len(xy), orient=HORIZONTAL, tickinterval=2, length=700, bg="snow2", command=siguiente).place(x=702, y=45, anchor=E)
        """
        # Visor
        self.txtVisor = Text(visorDatos, width=46, height=19, bd=8,pady=5, padx=2, font=("Sans", 9, "bold"))
        self.txtVisor.place(x=-5, y=1)

        self.txtVisorDesc = Text(visorDescuento, width=46, height=19, bd=8,pady=5, padx=2, font=("Sans", 9, "bold"))
        self.txtVisorDesc.place(x=-10, y=1)

        #Label de copyright
        cr = StringVar()
        cr.set("- SILIS Alpha 0.0.1 - AMMNI Software -")
        screen = Label(root, textvar=cr, justify="left")
        screen.grid(row=1, column=0)

        # Funcion que hace andar el reloj
        tick()
        #Funcion que inicializa la barra de comandos
        barra()




""" ---------------------------------------------------------- """
if __name__ == '__main__':
    root = Tk()
    application = Jornalero(root)

    root.mainloop()
