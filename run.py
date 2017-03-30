#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nico'


import sys

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

              1 Mostrar Inmuebles
              2 Añadir nuevo Inmueble
              3 Editar Inmueble
              4 Salir
        """)

    def run(self):
        '''Muestra el menú y responde a las elecciones.'''
        while True:
            self.mostrar_menu()
            eleccion = input("Escribe una opción: ")
            accion = self.elecciones.get(str(eleccion))
            if accion:
                accion()
            else:
                print("{0} no es una elección válida".format(eleccion))

    def show_inmuebles(self):
        self.menu.mostrar_inmuebles()

    """def search_notas(self):
        filter = input("Buscar por: ")
        notas = self.cuaderno.search(filter)
        self.mostrar_notas(notas)"""

    def add_inmueble(self):
        self.menu.add_inmueble()

    def modificar_inmuebles(self):
        pass
        """id = input("Escribe el id de una nota: ")
        memo = input("Escribe un memo: ")
        tags = input("Escribe tags: ")
        if memo:
            self.cuaderno.modificar_memo(id, memo)
        if tags:
            self.cuaderno.modificar_tags(id, tags)
        """

    def quit(self):
        print("Gracias por usar Inmo.")
        sys.exit(0)

if __name__ == "__main__":

    menu = Menu()
    menu.run()



