#!/usr/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------
#-------------------------------------------------------
# Tarea CRUD para el curso de Python Avanzado de la UGR
# Autor: Diego J. Martinez Garcia
#-------------------------------------------------------
#-------------------------------------------------------

import MySQLdb
from gi.repository import Gtk
import os, sys

def creaDb( ):
    """ Funcion encargada de Crear la base de datos"""
    try:
        conexion = MySQLdb.connect(host='localhost', user='root' ,passwd = 'vencejo')
        cursor = conexion.cursor()
        query = 'CREATE DATABASE DBdeConan4'
        cursor.execute(query)
        query = "GRANT ALL ON DBdeConan4.* TO \"conan\"@\"localhost\" IDENTIFIED BY \"crom\""
        cursor.execute(query)
        query = 'USE DBdeConan4'
        cursor.execute(query)
        query = 'CREATE TABLE Victimas (id INT, Nombre VARCHAR(100),Profesion VARCHAR(100),Muerte VARCHAR(100))'
        cursor.execute(query)
        conexion.commit()
    except:
        print "Hay un problema con la creacion de la base de datos, puede que ya exista"
       
#--------------------------------------------------
# Clase encargada de gestionar la Base de datos
#--------------------------------------------------

class Db:

    def __init__(self,host,user,passwd,db):

        # Establecemos la conexión
        self.conexion = MySQLdb.connect(host, user,passwd, db)
        # Creamos el cursor
        self.cursor = self.conexion.cursor()
        # Inicializamos la lista con los ids usados
        self.ids_usados = []
        # Inicializamos la base de datos
        self.initDB()

    def idUsado(self,identificador):
        """ Devuelve True si el identificador esta en la lista de ids usados """
        if identificador in self.ids_usados:
            return True
        else:
            return False
        
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
        query= "INSERT INTO Victimas (id,Nombre,Profesion,Muerte) VALUES (5, \"Sacerdote maligno\",\"Monstruo\",\"Desmembramiento a espada\");"
        self.cursor.execute(query)
       
        self.conexion.commit()
        self.ids_usados = [1,2,3,4,5]

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
                # ... imprimimos el registro...
                print registro
            registros= self.cursor.fetchmany(2)
       
    def deleteDB(self):
        """ Borra todos los registros de la base de datos """

        query= "DELETE FROM Victimas WHERE 1;"
        self.cursor.execute(query)
        self.conexion.commit()

    def crear(self,identificador, nombre,profesion,muerte):
        """ Inserta una fila en la base de datos que tenga el cursor especificado, si el id ya estaba
            creado devuelve False y no hace nada
            Solo se permiten ids del 1 al 5 para mantener la sencillez de la base de datos"""

        if identificador > 0 and identificador < 6 and not self.idUsado(identificador):
            self.ids_usados.append(identificador)
            query = "INSERT INTO Victimas VALUES ({0}, \"{1}\", \"{2}\",\"{3}\"); ".format(str(identificador),nombre,profesion,muerte)
            self.cursor.execute(query)
            self.conexion.commit()
            return True
        else:
            return False

    def obtener(self, identificador):
        """ Muestra la fila de la tabla con el identificador dado, si el id no existe devuelve None """

        query = "SELECT * FROM Victimas WHERE id = {0} ;".format(str(identificador))

        self.cursor.execute(query)
        self.conexion.commit()
        registro = self.cursor.fetchone()
        return registro
             
    def actualizar(self,identificador, nombre,profesion,muerte):
        """ Actualiza un id de la tabla con nuevos valores de nombre, profesion y muerte si no se puede actualizar devuelve None"""

        if self.idUsado(identificador):
            query = "UPDATE Victimas SET Nombre = \"{0}\", Profesion = \"{1}\", Muerte = \"{2}\" WHERE id = {3} ;".format(nombre,profesion,muerte,str(identificador))
            self.cursor.execute(query)
            self.conexion.commit()
            return True
        else:
            return False

    def borrar(self, identificador):
        """ Borra la entrada con el id especificado, si el id no existe devuelve None """
        if self.idUsado(identificador):
            self.ids_usados.pop(self.ids_usados.index(identificador))
            query = "DELETE FROM Victimas WHERE id = {0} ;".format(str(identificador))
            self.cursor.execute(query)
            self.conexion.commit()
            return True
        else:
            return False
        

#--------------------------------------------------
# Clase encargada de gestionar la interfaz grafica
#--------------------------------------------------    
class GUI:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("crudv2.glade")
        self.handlers = {"onDeleteWindow": self.onDeleteWindow ,
                         "onOpenAbout": self.onOpenAbout,
                         "onCloseAbout": self.onCloseAbout,
                         "onCrearActivate": self.onCrearActivate,
                         "onObtenerActivate": self.onObtenerActivate,
                         "onActualizarActivate": self.onActualizarActivate,
                         "onBorrarActivate": self.onBorrarActivate,
                                             
                         }
        self.builder.connect_signals(self.handlers)
        self.window = self.builder.get_object("window1")
        self.window.show_all()
        # Establecemos la conexión con la base de datos
        self.tabla = Db(host='localhost', user='conan',passwd='crom', db='DBdeConan4')
        self.tabla.deleteDB()   #Borro cualquier tabla guardada previamente
        self.tabla.initDB()     #Pueblo la tabla con unos valores iniciales
        self.onPopulateVisor()  #Visualizo la BD

    def onDeleteWindow(self, *args):
        Gtk.main_quit
        sys.exit()
        
    def onOpenAbout(self, *args):
        about = self.builder.get_object("aboutdialog1")
        about.show_all()

    def onCloseAbout(self, *args):
        about = self.builder.get_object("aboutdialog1")
        about.hide()

    def onCrearActivate(self, *args):

        #Conectamos con las etiquetas del GUI
        identificador = self.builder.get_object("id")
        nombre = self.builder.get_object("nombre")
        profesion = self.builder.get_object("profesion")
        muerte = self.builder.get_object("muerte")

        #Cogemos los valores
        valor_id = identificador.get_text()
        valor_nombre= nombre.get_text()
        valor_profesion = profesion.get_text()
        valor_muerte = muerte.get_text()
        #Consultamos la BD
        resultado = self.tabla.crear(int(valor_id), valor_nombre,valor_profesion,valor_muerte)
        # Informamos del proceso
        info = self.builder.get_object("info")
        if resultado == True:
            info.set_label("ELEMENTO CREADO")
            self.onPopulateVisor()
        else:
            info.set_label("ELEMENTO NO CREADO")


    def onObtenerActivate(self, *args):

        #Conectamos con las etiquetas del GUI
        identificador = self.builder.get_object("id")
        nombre = self.builder.get_object("nombre")
        profesion = self.builder.get_object("profesion")
        muerte = self.builder.get_object("muerte")
        #Miramos el id a obtener
        valor_id = identificador.get_text()
        #Consultamos la BD
        registro = self.tabla.obtener(valor_id)
        print registro
        # Informamos del proceso
        info = self.builder.get_object("info")
        if registro != None:
            info.set_label("OBTENIENDO ELEMENTO %s" % valor_id)
            #Escribimos la salida de cada elemento en la GUI
            nombre.set_text(str(registro[1]))
            profesion.set_text(str(registro[2]))
            muerte.set_text(str(registro[3]))
        else:
            info.set_label("ELEMENTO NO ENCONTRADO")
            nombre.set_text("---")
            profesion.set_text("---")
            muerte.set_text("---")
        
    def onActualizarActivate(self, *args):
        #Conectamos con las etiquetas del GUI
        identificador = self.builder.get_object("id")
        nombre = self.builder.get_object("nombre")
        profesion = self.builder.get_object("profesion")
        muerte = self.builder.get_object("muerte")

        #Cogemos los valores
        valor_id = identificador.get_text()
        valor_nombre= nombre.get_text()
        valor_profesion = profesion.get_text()
        valor_muerte = muerte.get_text()
        #Consultamos la BD
        resultado = self.tabla.actualizar(int(valor_id), valor_nombre,valor_profesion,valor_muerte)
        # Informamos del proceso
        info = self.builder.get_object("info")
        if resultado == True:
            info.set_label("ELEMENTO ACTUALIZADO")
            self.onPopulateVisor()
        else:
            info.set_label("ELEMENTO NO ACTUALIZADO")
    
    def onBorrarActivate(self, *args):
        #Conectamos con las etiquetas del GUI
        identificador = self.builder.get_object("id")
        #Miramos el id a obtener
        valor_id = identificador.get_text()
        #Consultamos la BD
        resultado = self.tabla.borrar(int(valor_id))
        # Informamos del proceso
        info = self.builder.get_object("info")
        if resultado == True:
            info.set_label("ELEMENTO BORRADO")
            self.onPopulateVisor()
        else:
            info.set_label("ELEMENTO NO BORRADO")

    def onPopulateVisor(self, *args):
        """ Llena el visor con los campos de la Base de Datos """

        ids = range(0,10)
        nombres = range(0,10)
        profesiones = range(0,10)
        muertes = range(0,10)
        #Conectamos con las etiquetas del GUI
        for i in range(1,6):
            ids[i] = self.builder.get_object("id" + str(i))
            nombres[i] = self.builder.get_object("nombre" + str(i))
            profesiones[i] = self.builder.get_object("profesion" + str(i))
            muertes[i] = self.builder.get_object("muerte" + str(i))
            
            #Consultamos la BD
            registro = self.tabla.obtener(i)
            #Actualizamos el visor
            if registro != None:
                ids[i].set_text(str(registro[0]))
                nombres[i].set_text(str(registro[1]))
                profesiones[i].set_text(str(registro[2]))
                muertes[i].set_text(str(registro[3]))
            else:
                ids[i].set_text("id " + str(i) + " borrado")
                nombres[i].set_text("---")
                profesiones[i].set_text("---")
                muertes[i].set_text("---")
        

def main():

    #La siguiente linea solo es necesaria la primera vez que se ejecute el programa, para crear la Bd
    creaDb()
    
    app = GUI()
    Gtk.main()
    return 0
    
if __name__ == '__main__':
    sys.exit(main())
    
    
   

