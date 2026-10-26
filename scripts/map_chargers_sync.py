# -*- coding: utf-8 -*-
"""
Sincronizador de Estaciones de Carga Eléctrica de Uruguay para EV Uruguay (ev.servicioti.com.uy)
Mapea la red oficial de cargadores públicos de UTE Mueve y redes asociadas (ANCAP, Evergo, DISA)
a lo largo de las rutas nacionales (1, 2, 3, 5, 8, 9, Interbalnearia) y todos los departamentos.
Sin costo de API key - Renderizado nativo en Leaflet con OpenStreetMap.
"""

from db_manager import get_connection

RED_NACIONAL_CARGADORES = [
    # MONTEVIDEO
    {
        "id": "ute-trouville-mvd",
        "operador": "UTE Mueve",
        "nombre": "Cargador UTE Rambla Trouville",
        "direccion": "Rambla Gandhi y 21 de Setiembre",
        "departamento": "Montevideo",
        "latitud": -34.9255,
        "longitud": -56.1528,
        "conectores": "Type 2 (22 kW) / GB/T",
        "potencia_kw": 22.0,
        "tipo_carga": "AC Media"
    },
    {
        "id": "ute-palacio-la-luz",
        "operador": "UTE Mueve",
        "nombre": "Hub Central UTE Palacio de la Luz",
        "direccion": "Paraguay 2431 y Aguilar",
        "departamento": "Montevideo",
        "latitud": -34.8912,
        "longitud": -56.1951,
        "conectores": "CCS2, CHAdeMO, Type 2, GB/T",
        "potencia_kw": 60.0,
        "tipo_carga": "DC Ultrarrápida"
    },
    {
        "id": "ute-tres-cruces",
        "operador": "UTE Mueve",
        "nombre": "Terminal Tres Cruces Hub",
        "direccion": "Bulevar Artigas y Goes",
        "departamento": "Montevideo",
        "latitud": -34.8942,
        "longitud": -56.1662,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-punta-carretas",
        "operador": "UTE Mueve",
        "nombre": "Punta Carretas Shopping Hub",
        "direccion": "Ellauri 350",
        "departamento": "Montevideo",
        "latitud": -34.9248,
        "longitud": -56.1585,
        "conectores": "Type 2, GB/T",
        "potencia_kw": 22.0,
        "tipo_carga": "AC Media"
    },
    {
        "id": "ute-portones-shopping",
        "operador": "UTE Mueve",
        "nombre": "Portones Shopping Carrasco",
        "direccion": "Av. Bolivia y Av. Italia",
        "departamento": "Montevideo",
        "latitud": -34.8812,
        "longitud": -56.0825,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },

    # CANELONES
    {
        "id": "ancap-aeropuerto-carrasco",
        "operador": "ANCAP / UTE Mueve",
        "nombre": "Estación ANCAP Aeropuerto de Carrasco",
        "direccion": "Ruta 101 km 19",
        "departamento": "Canelones",
        "latitud": -34.8258,
        "longitud": -56.0275,
        "conectores": "CCS2, Type 2, GB/T",
        "potencia_kw": 60.0,
        "tipo_carga": "DC Ultrarrápida"
    },
    {
        "id": "evergo-costa-urbana",
        "operador": "Evergo / UTE",
        "nombre": "Costa Urbana Shopping Hub",
        "direccion": "Av. Giannattasio km 21",
        "departamento": "Canelones",
        "latitud": -34.8471,
        "longitud": -55.9961,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-atlantida-centro",
        "operador": "UTE Mueve",
        "nombre": "Estación UTE Atlántida",
        "direccion": "Ruta Interbalnearia km 45 y Calle 1",
        "departamento": "Canelones",
        "latitud": -34.7731,
        "longitud": -55.7592,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },

    # MALDONADO
    {
        "id": "ute-punta-del-este-puerto",
        "operador": "UTE Mueve",
        "nombre": "Puerto de Punta del Este Hub",
        "direccion": "Rambla Gral. Artigas y Calle 10",
        "departamento": "Maldonado",
        "latitud": -34.9664,
        "longitud": -54.9498,
        "conectores": "CCS2, Type 2, GB/T",
        "potencia_kw": 60.0,
        "tipo_carga": "DC Ultrarrápida"
    },
    {
        "id": "ute-piriapolis-rambla",
        "operador": "UTE Mueve",
        "nombre": "Piriápolis Rambla de los Argentinos",
        "direccion": "Rambla de los Argentinos y Armenia",
        "departamento": "Maldonado",
        "latitud": -34.8642,
        "longitud": -55.2755,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-maldonado-centro",
        "operador": "UTE Mueve",
        "nombre": "Maldonado Centro Cívico",
        "direccion": "Av. Acuña de Figueroa y Burnett",
        "departamento": "Maldonado",
        "latitud": -34.9085,
        "longitud": -54.9582,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },

    # ROCHA
    {
        "id": "ute-la-paloma-rocha",
        "operador": "UTE Mueve",
        "nombre": "La Paloma Terminal Portuaria",
        "direccion": "Av. Nicolás Solari y del Faro",
        "departamento": "Rocha",
        "latitud": -34.6612,
        "longitud": -54.1615,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 43.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-chuy-frontera",
        "operador": "UTE Mueve",
        "nombre": "Chuy Estación Fronteriza Ruta 9",
        "direccion": "Av. Brasil y Ruta 9",
        "departamento": "Rocha",
        "latitud": -33.6975,
        "longitud": -53.4612,
        "conectores": "CCS2, Type 2, GB/T",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },

    # COLONIA
    {
        "id": "ute-colonia-sacramento",
        "operador": "UTE Mueve",
        "nombre": "Colonia del Sacramento Puerto",
        "direccion": "Av. Franklin D. Roosevelt y Río de la Plata",
        "departamento": "Colonia",
        "latitud": -34.4681,
        "longitud": -57.8423,
        "conectores": "Type 2, CCS2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-rosario-ruta1",
        "operador": "UTE Mueve",
        "nombre": "Rosario Corredor Ruta 1 km 130",
        "direccion": "Ruta 1 y Acceso a Rosario",
        "departamento": "Colonia",
        "latitud": -34.3167,
        "longitud": -57.3500,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 60.0,
        "tipo_carga": "DC Ultrarrápida"
    },

    # SAN JOSÉ & FLORIDA (RUTA 1 Y 5)
    {
        "id": "ute-san-jose-centro",
        "operador": "UTE Mueve",
        "nombre": "San José de Mayo Terminal",
        "direccion": "Manuel D. Rodríguez y Artigas",
        "departamento": "San José",
        "latitud": -34.3375,
        "longitud": -56.7135,
        "conectores": "Type 2, CCS2",
        "potencia_kw": 43.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-florida-ruta5",
        "operador": "UTE Mueve",
        "nombre": "Florida Centro Corredor Ruta 5",
        "direccion": "Independencia y Gallinal",
        "departamento": "Florida",
        "latitud": -34.0956,
        "longitud": -56.2142,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },

    # DURAZNO & TACUAREMBÓ (CENTRO DEL PAÍS)
    {
        "id": "ute-durazno-centro",
        "operador": "UTE Mueve",
        "nombre": "Durazno Centro Ruta 5 km 183",
        "direccion": "Manuel Oribe y Artigas",
        "departamento": "Durazno",
        "latitud": -33.3792,
        "longitud": -56.5278,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-tacuarembo-ruta5",
        "operador": "UTE Mueve",
        "nombre": "Tacuarembó Hub Ruta 5 km 390",
        "direccion": "Av. Héctor Gutiérrez Ruiz y 18 de Julio",
        "departamento": "Tacuarembó",
        "latitud": -31.7131,
        "longitud": -55.9811,
        "conectores": "CCS2, Type 2, GB/T",
        "potencia_kw": 60.0,
        "tipo_carga": "DC Ultrarrápida"
    },

    # RIVERA (FRONTERA NORTE)
    {
        "id": "ute-rivera-frontera",
        "operador": "UTE Mueve",
        "nombre": "Rivera Frontera / Siñeriz Shopping",
        "direccion": "Av. Sarandí y Agustín de Aragón",
        "departamento": "Rivera",
        "latitud": -30.9056,
        "longitud": -55.5394,
        "conectores": "CCS2, Type 2, GB/T",
        "potencia_kw": 60.0,
        "tipo_carga": "DC Ultrarrápida"
    },

    # LITORAL: PAYSANDÚ, SALTO, FRAY BENTOS
    {
        "id": "ute-paysandu-terminal",
        "operador": "UTE Mueve",
        "nombre": "Paysandú Terminal de Ómnibus",
        "direccion": "Monte Caseros y Artigas",
        "departamento": "Paysandú",
        "latitud": -32.3214,
        "longitud": -58.0756,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-salto-dayman",
        "operador": "UTE Mueve",
        "nombre": "Salto Hub Termas del Daymán",
        "direccion": "Ruta 3 km 487",
        "departamento": "Salto",
        "latitud": -31.4667,
        "longitud": -57.9167,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-fray-bentos",
        "operador": "UTE Mueve",
        "nombre": "Fray Bentos Acceso Puente Internacional",
        "direccion": "Rambla Costanera y 25 de Mayo",
        "departamento": "Río Negro",
        "latitud": -33.1311,
        "longitud": -58.3033,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },

    # ESTE: LAVALLEJA Y TREINTA Y TRES (RUTA 8)
    {
        "id": "ute-minas-ruta8",
        "operador": "UTE Mueve",
        "nombre": "Minas Centro Turístico Ruta 8",
        "direccion": "18 de Julio y Washington Beltrán",
        "departamento": "Lavalleja",
        "latitud": -34.3758,
        "longitud": -55.2378,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    },
    {
        "id": "ute-treinta-y-tres",
        "operador": "UTE Mueve",
        "nombre": "Treinta y Tres Corredor Ruta 8",
        "direccion": "Manuel Lavalleja y Pablo Zufriategui",
        "departamento": "Treinta y Tres",
        "latitud": -33.2333,
        "longitud": -54.3833,
        "conectores": "CCS2, Type 2",
        "potencia_kw": 50.0,
        "tipo_carga": "DC Rápida"
    }
]

def seed_chargers():
    print(f"=== Sincronizando Red Nacional de Cargadores UTE Mueve ({len(RED_NACIONAL_CARGADORES)} estaciones) ===")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM charging_stations;")
    count = 0

    for st in RED_NACIONAL_CARGADORES:
        cursor.execute("""
        INSERT INTO charging_stations (
            id, operador, nombre, direccion, departamento, latitud, longitud,
            conectores, potencia_kw, tipo_carga
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            st["id"], st["operador"], st["nombre"], st["direccion"],
            st["departamento"], st["latitud"], st["longitud"],
            st["conectores"], st["potencia_kw"], st["tipo_carga"]
        ))
        count += 1

    conn.commit()
    conn.close()
    print(f"[Éxito] {count} estaciones de carga georreferenciadas en SQLite.")

    # Re-exportar a JSON y JS
    from export_to_json import export_db_to_json
    export_db_to_json()

if __name__ == "__main__":
    seed_chargers()
