#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nico'

from auth import Authenticator
import getpass
import os
import sys
from optparse import OptionParser
import datetime, time
import logging

# Basedir
try:
    Basedir = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    Basedir = os.path.dirname(os.path.abspath(sys.argv[0]))

# ------------------------ LOGGER CONFIG ------------------------------

# Setting
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# # create a file handler
# handler = logging.FileHandler(os.path.join(Basedir, 'decoder.log'))
# handler.setLevel(logging.DEBUG)

# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# # add the handlers to the logger
# logger.addHandler(handler)
# logger.info('__Basedir__: Definiendo directorio del proyecto: %s' % Basedir)
# ----------------------------------------------------------------------

def header():
    print
    print ('###################################################################################')
    print ('############################   INMO ##################################')
    print ('###################################################################################')
    print ('###########    XML to PDF encoder    ## Date:  ' + str(datetime) + '  ########################')
    print ('###################################################################################')
    print()


#logger.info(header())

def parse_options():
    HELP = ("""
                  Decoder EXE can me executer either as Scheduled Task od from CMD:
                  1) Use the file 'config.cfg by set the parameter with -c {arg}' for Scheduled Task Mode
                  2) Run from command line otherwise.
                  3) Provide input PDF encoding with option -E.
            """)

    parser = OptionParser(usage='usage: run { $python3 %prog',
                          version='%prog 1.0', description=HELP)

    parser.add_option('-h', '--help', action='store', type='string', dest='input', help='Help')


    options, args = parser.parse_args()

class Inmueble:
    def __init__(self, metros_cuadrados='', habitaciones='',
             bans='', **kwargs):
        super().__init__(**kwargs)
        self.metros_cuadrados = metros_cuadrados
        self.num_habitaciones = habitaciones
        self.num_bans = bans

    def mostrar(self):
        print("DETALLES Inmueble")
        print("================")
        print("metros cuadrados: {}".format(self.metros_cuadrados))
        print("habitaciones: {}".format(self.num_habitaciones))
        print("baños: {}".format(self.num_bans))
        print()

    def prompt_init():
        return dict(metros_cuadrados=input("Escribe los metros cuadrados: "),
                habitaciones=input("Escribe el número de habitaciones: "),
                bans=input("Escribe el número de baños: "))
    prompt_init = staticmethod(prompt_init)

def obtener_input_valido(string_input, opciones_validas):
    string_input += " ({}) ".format((", ".join(opciones_validas)))
    respuesta = input(string_input)
    while respuesta.lower() not in opciones_validas:
        respuesta = input(string_input)
    return respuesta

class Apartamento(Inmueble):
    lavanderias_validas = ("moneda", "incluido", "ninguna")
    balcones_validos = ("si", "no", "solario")

    def __init__(self, balcon='', lavanderia='', **kwargs):
        super().__init__(**kwargs)
        self.balcon = balcon
        self.lavanderia = lavanderia

    def mostrar(self):
        super().mostrar()
        print("DETALLES APARTAMENTO")
        print("lavandería: {}".format(self.lavanderia))
        print("tiene balcón: {}".format(self.balcon))

    def prompt_init():
        parent_init = Inmueble.prompt_init()
        lavanderia = obtener_input_valido(
                "¿Qué sistema de lavandería "
                "tiene el inmueble? ",
                Apartamento.lavanderias_validas)
        balcon = obtener_input_valido(
                "¿tiene el inmueble balcón?",
                Apartamento.balcones_validos)
        parent_init.update({
            "lavanderia": lavanderia,
            "balcon": balcon
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)

class Casa(Inmueble):
    garaje_valido = ("anexo", "separado", "ninguno")
    jardin_valido = ("si", "no")

    def __init__(self, num_pisos='',
            garaje='', jardin='', **kwargs):
        super().__init__(**kwargs)
        self.garaje = garaje
        self.jardin = jardin
        self.num_pisos = num_pisos

    def mostrar(self):
        super().mostrar()
        print("DETALLES CASA")
        print("# de pisos: {}".format(self.num_pisos))
        print("garaje: {}".format(self.garaje))
        print("jardin: {}".format(self.jardin))

    def prompt_init():
        parent_init = Inmueble.prompt_init()
        jardin = obtener_input_valido("¿La casa tiene Jardín? ",
                    Casa.jardin_valido)
        garaje = obtener_input_valido("¿Hay un garaje? ",
                Casa.garaje_valido)
        num_pisos = input("¿Cuantos pisos? ")

        parent_init.update({
            "jardin": jardin,
            "garaje": garaje,
            "num_pisos": num_pisos
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)

class Compra:
    def __init__(self, precio='', impuestos='', **kwargs):
        super().__init__(**kwargs)
        self.precio = precio
        self.impuestos = impuestos

    def mostrar(self):
        super().mostrar()
        print("DETALLES COMPRAS")
        print("precio venta: {}".format(self.precio))
        print("impuestos estimados: {}".format(self.impuestos))

    def prompt_init():
        return dict(
            precio=input("¿Cuál es el precio de venta? "),
            impuestos=input("¿Cuáles son los impuestos estimados? "))
    prompt_init = staticmethod(prompt_init)

class Alquiler:
    def __init__(self, amueblado='', ajuar='',
            alquiler='', **kwargs):
        super().__init__(**kwargs)
        self.amueblado = amueblado
        self.alquiler = alquiler
        self.ajuar = ajuar

    def mostrar(self):
        super().mostrar()
        print("DETALLES ALQUILER")
        print("alquiler: {}".format(self.alquiler))
        print("ajuar estimado: {}".format(self.ajuar))
        print("amueblado: {}".format(self.amueblado))

    def prompt_init():
        return dict(
            alquiler=input("¿Cuál es el alquiler mensual? "),
            ajuar=input("¿Cuál es el ajuar estimado? "),
            amueblado = obtener_input_valido("¿Está amueblado el inmueble? ",
                    ("si", "no")))
    prompt_init = staticmethod(prompt_init)

class CasaAlquiler(Alquiler, Casa):
    def prompt_init():
        init = Casa.prompt_init()
        init.update(Alquiler.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class ApartamentoAlquiler(Alquiler, Apartamento):
    def prompt_init():
        init = Apartamento.prompt_init()
        init.update(Alquiler.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class ApartamentoCompra(Compra, Apartamento):
    def prompt_init():
        init = Apartamento.prompt_init()
        init.update(Compra.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class CasaCompra(Compra, Casa):
    def prompt_init():
        init = Casa.prompt_init()
        init.update(Compra.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class Agente:
    type_map = {
        ("casa", "alquiler"): CasaAlquiler,
        ("casa", "compra"): CasaCompra,
        ("apartamento", "alquiler"): ApartamentoAlquiler,
        ("apartamento", "compra"): ApartamentoCompra
        }
    def __init__(self):
        self.inmueble_list = []

    def mostrar_inmuebles(self):
        if self.inmueble_list:
            for inmueble in self.inmueble_list:
                inmueble.mostrar()
        else:
            return ("La lista esta vacía!!!")

    def add_inmueble(self):
        tipo_inmueble = obtener_input_valido(
                "¿Qué tipo de inmueble? ",
                ("casa", "apartamento")).lower()
        tipo_pago = obtener_input_valido(
                "¿Qué tipo de pago? ",
                ("compra", "alquiler")).lower()

        inmuebleClass = self.type_map[(tipo_inmueble, tipo_pago)]
        init_args = inmuebleClass.prompt_init()
        self.inmueble_list.append(inmuebleClass(**init_args))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Login:
    '''Muestra un menú y responde a elecciones cuando se ejecuta.'''
    def __init__(self):
        self.inicio = Authenticator()
        self.elecciones = {
                "1" : self.iniciar_sesion,
                "2" : self.registar_usuario,
                "3" : self.quit
                }

    def mostrar_menu(self):
        menu = '''
                                Menu Inmobiliaria

                                1) Iniciar sesión
                                2) Registrar nuevo usuario
                                3) Salir
                '''
        print(menu)

    def run(self):
        '''Muestra el menú y responde a las elecciones.'''
        while True:
            self.mostrar_menu()
            eleccion = input("Escribe una opción: ".center(30))
            accion = self.elecciones.get(str(eleccion))
            if accion:
                accion()
            else:
                print("{0} no es una elección válida".format(eleccion))

    def iniciar_sesion(self):
        clear()
        print("Iniciando sesión")
        print()
        user = input("Ingrese nombre de usuario: ")
        if self.inicio.is_logged_in(user):
            return False
        try:
            passw = getpass.getpass(prompt='Password: ', stream=None)
            self.inicio.login(user, passw)

        except:
            raise Exception("Error en inicio de sesión")
            sys.exit(0)
        return False

    def registar_usuario(self):
        clear()
        print("Registrando nuevo usuario")
        print()
        user = input("Ingrese nuevo usuario: ")
        try:
            if not self.inicio.user_exist(user):
                passw = getpass.getpass(prompt='Password: ', stream=None)
                self.inicio.add_user(user,passw)
            return False
        except:
            raise Exception("Error al registrar usuario: %s" % user)
            sys.exit(0)
        return True

    def quit(self):
        print("Gracias por usar Inmo.")
        sys.exit(0)

class Bienvenido:
    def __init__(self, text='', ch='-', length=100):
        self.text = text
        self.ch = ch
        self.length = length

    def displaybanner(self):
        spaced_text = ' %s ' % self.text
        banner = spaced_text.center(self.length, self.ch)
        print(banner)

    def __banner(self, text='', ch='-', length=100):
        spaced_text = ' %s ' % text
        banner = spaced_text.center(length, ch)
        print(banner)

    def printEOL(self):
        print('\n')

    def header(self):
        clear()
        self.__banner('-')
        self.__banner('-')
        self.__banner('Sistema de Gestion')
        self.__banner('-')
        self.__banner('Fecha: ' + str(datetime.datetime.now().strftime("%d/%m/%Y")) + ' - Hora: ' + str(time.strftime("%H:%M:%S")))
        self.__banner('  ',' ')
        self.__banner('Autor: Nicolas Magliaro - version 1.0 \n', ' ')
        self.__banner('  ',' ')
        self.printEOL()

class Menu:
    '''Muestra un menú y responde a elecciones cuando se ejecuta.'''
    def __init__(self):
        self.menu = Agente()
        self.elecciones = {
                "1" : self.show_inmuebles,
                "2" : self.add_inmueble,
                "3" : self.modificar_inmuebles,
                "4" : self.quit
                }

    def mostrar_menu(self):
        print("""
                        Menu Inmobiliaria

                        1) Mostrar Inmuebles
                        2) Añadir nuevo Inmueble
                        3) Editar Inmueble
                        4) Salir
            """)

    def run(self):
        '''Muestra el menú y responde a las elecciones.'''
        while True:
            self.mostrar_menu()
            eleccion = input("          Escribe una opción: ")
            accion = self.elecciones.get(str(eleccion))
            if accion:
                accion()
            else:
                print("{0} no es una elección válida".format(eleccion))

    def show_inmuebles(self):
        self.menu.mostrar_inmuebles()

    def search_notas(self):
        filter = input("Buscar por: ")
        notas = self.cuaderno.search(filter)
        self.mostrar_notas(notas)

    def add_inmueble(self):
        self.menu.add_inmueble()

    def modificar_inmuebles(self):
        pass
        id = input("Escribe el id de una nota: ")
        memo = input("Escribe un memo: ")
        tags = input("Escribe tags: ")
        if memo:
            self.cuaderno.modificar_memo(id, memo)
        if tags:
            self.cuaderno.modificar_tags(id, tags)

    def quit(self):
        print("Gracias por usar Inmo.")
        sys.exit(0)

if __name__ == "__main__":
    start, menu, banner = (Login(), Menu(), Bienvenido())
    banner.header()

    while True:
        start.run()
    menu.run()



