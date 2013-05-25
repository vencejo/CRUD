#!/usr/python
# -*- coding: utf-8 -*-

#--------------------------------------
# Autor: Diego J. Martinez Garcia
#--------------------------------------

import MySQLdb
from gi.repository import Gtk
import os, sys


class Db:

    def __init__(self,host,user,passwd,db):

        # Establecemos la conexión
        self.conexion = MySQLdb.connect(host, user,passwd, db)
        # Creamos el cursor
        self.cursor = self.conexion.cursor()
        # Inicializamos el id
        self.id = 0
        # Inicializamos la base de datos
        self.initDB()
        
    def initDB(self):
        """ Inicializa la base de datos introduciendole 5 registros"""
        
        query= "INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (1, \"Ejercito de Zombies\",\"Muertos Vivientes\",\"Desmembramiento a espada\");"
        self.cursor.execute(query)
        query= "INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (2, \"Vampiro feo\",\"Muertos Vivientes\",\"Estaca de madera\");"
        self.cursor.execute(query)
        query= "INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (3, \"Bestia del Pantano\",\"Monstruo\",\"Destripado\");"
        self.cursor.execute(query)
        query= "INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (4, \"Serpiente\",\"Monstruo\",\"Destripado\");"
        self.cursor.execute(query)
        query= "INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (5, \"Scerdote maligno\",\"Monstruo\",\"Desmembramiento a espada\");"
        self.cursor.execute(query)
       
        self.conexion.commit()


    def viewDB(self):
        """ Muestra todos los registros de la base de datos en pantalla """

        query= "SELECT * FROM Victimas WHERE 1;"
        self.cursor.execute(query)
        # Obtenemos el resultado con fetchmany
        registros= self.cursor.fetchmany(2)
        # para cada lista retornada (de 2 registros)
        while (registros):
            # recorremos la lista...
            for registro in registros:
                # ... mprimimos el registro...
                print registro
            registros= self.cursor.fetchmany(2)

    def consulta(self,query):
        """ Realiza una consulta a la base de datos e imprime un mensaje en el terminal si no se puede realizar o si la
            consulta no ha dado resultado"""
        try:
            result = self.cursor.execute(query)
            self.conexion.commit()

            if result == None:
                print "La consulta {0} no ha dado resultado".format(query)
        except:
            print ""
            print "Error: no se ha podido realizar la consulta: " + str(query)
        
    def deleteDB(self):
        """ Borra todos los registros de la base de datos """

        query= "DELETE FROM Victimas WHERE 1;"
        self.cursor.execute(query)
        self.conexion.commit()

    def crear(self,identificador, nombre,profesion,muerte):
        """ Inserta una fila en la base de datos que tenga el cursor especificado """

        query = "INSERT INTO Victimas VALUES ({0}, \"{1}\", \"{2}\",\"{3}\"); ".format(str(identificador),nombre,profesion,muerte)
        self.cursor.execute(query)
        self.conexion.commit()

    def obtener(self, identificador):
        """ Muestra la fila de la tabla con el identificador dado, si el id no existe devuelve None """

        query = "SELECT * FROM Victimas WHERE id = {0} ;".format(str(identificador))
        self.cursor.execute(query)
        self.conexion.commit()
        registro = self.cursor.fetchone()
        return registro

    def actualizar(self,identificador, nombre,profesion,muerte):
        """ Actualiza un id de la tabla con nuevos valores de nombre, profesion y muerte """
        
        query = "UPDATE Victimas SET Nombre = \"{0}\", Profesion = \"{1}\", Muerte = \"{2}\" WHERE id = {3} ;".format(nombre,profesion,muerte,str(identificador))
        self.consulta(query)

    def borrar(self, identificador):
        """ Borra la entrada con el id especificado """

        query = "DELETE FROM Victimas WHERE id = {0} ;".format(str(identificador))
        self.consulta(query)


        
class GUI:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("crudv1.glade")
        self.handlers = {"onDeleteWindow": self.onDeleteWindow ,
                         "onOpenAbout": self.onOpenAbout,
                         "onCloseAbout": self.onCloseAbout,}
        
        self.builder.connect_signals(self.handlers)
        self.window = self.builder.get_object("window1")
        self.populate_entry()
        self.window.show_all()

    def onDeleteWindow(self, *args):
        Gtk.main_quit
        sys.exit()
        
    def onOpenAbout(self, *args):
        about = self.builder.get_object("aboutdialog1")
        about.show_all()

    def onCloseAbout(self, *args):
        about = self.builder.get_object("aboutdialog1")
        about.hide()

        
    def get_datos(self):

        # Establecemos la conexión con la base de datos
        tabla = Db(host='localhost', user='conan',passwd='crom', db='DBdeConan')
        tabla.deleteDB()
        tabla.initDB()

        row1 = tabla.obtener(1)
        row2 = tabla.obtener(2)
        row3 = tabla.obtener(3)
        row4 = tabla.obtener(4)
        row5 = tabla.obtener(5)


        datos ={'d1': row1,'d2':row2,'d3': row3,'d4': row4,'d5': row5,'d6': None ,'d7': None,'d8': None,'d9': None,'d10': None,}
                        
        return datos



    def populate_entry(self):

        entradas = []
        for i in range(1,21):
            entrada = "entry" + str(i)
            entradas.append(self.builder.get_object(entrada))
				
                                        
        datos = self.get_datos()

        entradas[0].set_text(str(datos['d1'][0]))
        entradas[1].set_text(str(datos['d1'][1]))
        entradas[2].set_text(str(datos['d1'][2]))
        entradas[3].set_text(str(datos['d1'][3]))
        
        entradas[4].set_text(str(datos['d2'][0]))
        entradas[5].set_text(str(datos['d2'][1]))
        entradas[6].set_text(str(datos['d2'][2]))
        entradas[7].set_text(str(datos['d2'][3]))
        
        entradas[8].set_text(str(datos['d3'][0]))
        entradas[9].set_text(str(datos['d3'][1]))
        entradas[10].set_text(str(datos['d3'][2]))
        entradas[11].set_text(str(datos['d3'][3]))
        
        entradas[12].set_text(str(datos['d4'][0]))
        entradas[13].set_text(str(datos['d4'][1]))
        entradas[14].set_text(str(datos['d4'][2]))
        entradas[15].set_text(str(datos['d4'][3]))

        entradas[16].set_text(str(datos['d5'][0]))
        entradas[17].set_text(str(datos['d5'][1]))
        entradas[18].set_text(str(datos['d5'][2]))
        entradas[19].set_text(str(datos['d5'][3]))

def main():
    app = GUI()
    Gtk.main()
    return 0
    
if __name__ == '__main__':
    sys.exit(main())
    
    
   

