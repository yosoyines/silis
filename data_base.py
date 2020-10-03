"""
Sistema liquidacion de sueldos - Backend
Copyright 2019 - AMNII Software
"""
import sqlite3

def workerData():
    start = sqlite3.connect("trabajadores.db")
    start.execute("CREATE TABLE IF NOT EXISTS trabajadores(Workerid INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, apellido TEXT, cedula TEXT, hijos TEXT, pareja TEXT, ingreso TEXT, valorHora TEXT, simples TEXT, extras TEXT, especiales TEXT, nocturnas TEXT, jorEspecial TEXT)")
    start.commit()
    start.close()

def addInfo(nombre, apellido, cedula, hijos, pareja, ingreso, valorHora, simples, extras, especiales, nocturnas, jorEspecial):
    start = sqlite3.connect("trabajadores.db")
    pointer = start.cursor()
    test = pointer.execute("INSERT INTO trabajadores VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)",(nombre, apellido, cedula, hijos, pareja, ingreso, valorHora, simples, extras, especiales, nocturnas, jorEspecial))
    print(test)
    start.commit()
    start.close()

def displayInfo():
    start = sqlite3.connect("trabajadores.db")
    pointer = start.cursor()
    pointer.execute("SELECT * FROM trabajadores")
    row = pointer.fetchall() #Te da una tupla con todos los datos
    start.close()
    return row

def selectUnique(Workerid):
    start = sqlite3.connect("trabajadores.db")
    pointer = start.cursor()
    pointer.execute("SELECT * FROM trabajadores WHERE Workerid=?",(Workerid,))
    row = pointer.fetchall()
    start.close()
    return row

def getID():
    start = sqlite3.connect("trabajadores.db")
    pointer = start.cursor()
    pointer.execute("SELECT Workerid FROM trabajadores")
    row = pointer.fetchall()
    start.close()
    return row

def deleteInfo(Workerid):
    start = sqlite3.connect("trabajadores.db")
    pointer = start.cursor()
    pointer.execute("DELETE FROM trabajadores WHERE Workerid=?",(Workerid,))
    pointer.execute("DELETE FROM sqlite_sequence WHERE name = 'trabajadores' ")
    start.commit()
    start.close()

def searchInfo(ingreso="", cedula="", valorHora="", simples="", extras="", especiales="", nocturnas="", jorEspecial=""):
    start = sqlite3.connect("trabajadores.db")
    pointer = start.cursor()
    pointer.execute("SELECT * FROM trabajadores WHERE ingreso =? OR cedula=? OR valorHora =? OR simples =? OR extras =? OR especiales =? OR nocturnas =? OR jorEspecial =?",(ingreso, valorHora, simples, extras, especiales, nocturnas, jorEspecial))
    row = pointer.fetchall()
    start.close()
    return row


workerData()
