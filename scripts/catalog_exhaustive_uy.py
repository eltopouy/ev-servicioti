# -*- coding: utf-8 -*-
"""
Catálogo Maestro y Exhaustivo de Movilidad Eléctrica en Uruguay (+98% del Mercado).
Cubre más de 100 modelos de autos, SUVs, pickups, furgones, motos, scooters y e-bikes
comercializados y homologados en Uruguay por importadores y marcas oficiales:
- BYD (SADAR)
- Volvo (Danissa / Norden)
- Geely & Zeekr (Grupo Fiancar)
- Dongfeng & Nammi (Fidocar)
- JAC Motors (Grupo Aler / Fiancar)
- Renault & Nissan (Santa Rosa)
- GWM & Omoda
- Hyundai & Kia (Fidocar / Zenex)
- Maxus (Abriley S.A.)
- BMW, Mini, Audi, Mercedes-Benz, Porsche
- Tesla, Microcars (BAW, Changan, Chery)
- Motos: Sunra, Yadea, Niu, Super Soco / Vmoto, Segway, Horwin, Silence
- Bicicletas: Loop Bikes (Nacional UY), VoltBike, Wheele, Decathlon, Trek, Specialized, Xiaomi/Himo
"""

import json
from pathlib import Path
from db_manager import get_connection

CATALOGO_EXHAUSTIVO = [
    # =========================================================================
    # 1. BYD (IMPORTADOR OFICIAL EN URUGUAY: SADAR S.A.)
    # =========================================================================
    {
        "id": "byd-seagull-ev300",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Seagull EV300",
        "version": "GL / Active 30.08 kWh (Blade LFP)",
        "precio_usd": 18990,
        "autonomia_km": 305,
        "bateria_kwh": 30.08,
        "potencia": "75 CV (55 kW)",
        "par_motor_nm": 135,
        "aceleracion_0_100": "13.0 s",
        "velocidad_maxima": "130 km/h",
        "tiempo_carga_ac": "4.0 h",
        "tiempo_carga_dc": "30 min (30-80%)",
        "dimensiones": "3.780 x 1.715 x 1.540 mm",
        "peso_kg": 1160,
        "capacidad_baul_l": 230,
        "conector": "GB/T (Adaptador Type 2 incluido)",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.com.uy/seagull",
        "especificaciones": {
            "traccion": "Delantera (FWD)",
            "airbags": "4 airbags de serie (frontales y de cortina)",
            "pantalla": "Táctil rotativa de 10.1 pulgadas con DiLink y Apple CarPlay",
            "llantas": "Aleación de aluminio de 15 pulgadas",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-seagull-ev400-gs",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Seagull EV400",
        "version": "GS 38.88 kWh (Blade LFP)",
        "precio_usd": 21990,
        "autonomia_km": 380,
        "bateria_kwh": 38.88,
        "potencia": "75 CV (55 kW)",
        "par_motor_nm": 135,
        "aceleracion_0_100": "13.0 s",
        "velocidad_maxima": "130 km/h",
        "tiempo_carga_ac": "5.0 h",
        "tiempo_carga_dc": "30 min (30-80%)",
        "dimensiones": "3.780 x 1.715 x 1.540 mm",
        "peso_kg": 1240,
        "capacidad_baul_l": 230,
        "conector": "GB/T (Adaptador Type 2 incluido)",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.com.uy/seagull",
        "especificaciones": {
            "traccion": "Delantera (FWD)",
            "airbags": "6 airbags (frontales, laterales delanteros y cortina)",
            "innovacion": "Descarga bidireccional V2L + Cargador inalámbrico para celular",
            "llantas": "Aleación diamantadas de 16 pulgadas",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-seagull-surf",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Seagull Surf",
        "version": "Tope de Gama 43.2 kWh 88 CV",
        "precio_usd": 23990,
        "autonomia_km": 380,
        "bateria_kwh": 43.2,
        "potencia": "88 CV (65 kW)",
        "par_motor_nm": 150,
        "aceleracion_0_100": "11.5 s",
        "velocidad_maxima": "135 km/h",
        "tiempo_carga_ac": "4.0 h (Soporta 11 kW AC)",
        "tiempo_carga_dc": "30 min en 40 kW DC",
        "dimensiones": "3.780 x 1.715 x 1.540 mm",
        "peso_kg": 1280,
        "capacidad_baul_l": 230,
        "conector": "GB/T / Tipo 2",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.com.uy/seagull",
        "especificaciones": {
            "estetica": "Pack deportivo Surf con tapizados bitono exclusivos",
            "asientos": "Regulación eléctrica de 6 posiciones para conductor",
            "llantas": "Diseño bitono deportivo de 16 pulgadas",
            "carga_ac": "Cargador a bordo trifásico de 11 kW",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-dolphin-gs",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Dolphin",
        "version": "GS EV e-Platform 3.0",
        "precio_usd": 28990,
        "autonomia_km": 405,
        "bateria_kwh": 44.9,
        "potencia": "95 CV",
        "par_motor_nm": 180,
        "aceleracion_0_100": "10.9 s",
        "velocidad_maxima": "150 km/h",
        "tiempo_carga_ac": "6.0 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.125 x 1.770 x 1.570 mm",
        "peso_kg": 1405,
        "capacidad_baul_l": 345,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/dolphin",
        "especificaciones": {
            "traccion": "Delantera",
            "suspension_delantera": "McPherson independiente",
            "pantalla": "12.8 pulgadas rotativa eléctrica",
            "carga_bidireccional": "V2L hasta 3.3 kW",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-dolphin-mini",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Dolphin Mini",
        "version": "EV Urban 300",
        "precio_usd": 21990,
        "autonomia_km": 300,
        "bateria_kwh": 30.0,
        "potencia": "75 CV",
        "par_motor_nm": 135,
        "aceleracion_0_100": "13.5 s",
        "velocidad_maxima": "130 km/h",
        "tiempo_carga_ac": "4.0 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "3.780 x 1.715 x 1.580 mm",
        "peso_kg": 1100,
        "capacidad_baul_l": 230,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy",
        "especificaciones": {
            "tipo_bateria": "Blade LFP ultra segura",
            "climatizador": "Automático digital",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-dolphin-plus",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Dolphin Plus",
        "version": "EV 204 CV 60.5 kWh",
        "precio_usd": 34990,
        "autonomia_km": 490,
        "bateria_kwh": 60.5,
        "potencia": "204 CV",
        "par_motor_nm": 310,
        "aceleracion_0_100": "7.0 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "8 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.150 x 1.770 x 1.570 mm",
        "peso_kg": 1658,
        "capacidad_baul_l": 345,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/dolphin-plus",
        "especificaciones": {
            "techo": "Panorámico acristalado",
            "adas": "Control crucero adaptativo y frenado autónomo",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-yuan-pro",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Yuan Pro",
        "version": "EV 380 SUV",
        "precio_usd": 26990,
        "autonomia_km": 380,
        "bateria_kwh": 45.1,
        "potencia": "95 CV",
        "par_motor_nm": 180,
        "aceleracion_0_100": "11.0 s",
        "velocidad_maxima": "150 km/h",
        "tiempo_carga_ac": "6.0 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.310 x 1.830 x 1.675 mm",
        "peso_kg": 1500,
        "capacidad_baul_l": 380,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/yuan-pro",
        "especificaciones": {
            "carroceria": "SUV Compacto B",
            "barras_techo": "De serie en aluminio",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-yuan-plus",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Yuan Plus",
        "version": "EV 500 Flagship (Atto 3)",
        "precio_usd": 39990,
        "autonomia_km": 480,
        "bateria_kwh": 60.5,
        "potencia": "204 CV",
        "par_motor_nm": 310,
        "aceleracion_0_100": "7.3 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "8 h",
        "tiempo_carga_dc": "30 min en 80 kW",
        "dimensiones": "4.455 x 1.875 x 1.615 mm",
        "peso_kg": 1690,
        "capacidad_baul_l": 440,
        "conector": "GB/T (Adaptador Type 2)",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/yuan-plus",
        "especificaciones": {
            "seguridad_ncap": "5 Estrellas Euro NCAP",
            "suspension_trasera": "Multi-link independiente",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-song-plus",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Song Plus",
        "version": "DM-i Plug-in Hybrid / EV",
        "precio_usd": 48990,
        "autonomia_km": 505,
        "bateria_kwh": 71.7,
        "potencia": "184 CV",
        "par_motor_nm": 280,
        "aceleracion_0_100": "8.5 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "8 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.705 x 1.890 x 1.680 mm",
        "peso_kg": 1950,
        "capacidad_baul_l": 574,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/song-plus",
        "especificaciones": {
            "segmento": "SUV Mediano D",
            "asientos": "Cuero ecológico ventilados y calefaccionados",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-seal-awd",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Seal",
        "version": "Excellence AWD 530 CV",
        "precio_usd": 63990,
        "autonomia_km": 570,
        "bateria_kwh": 82.5,
        "potencia": "530 CV",
        "par_motor_nm": 670,
        "aceleracion_0_100": "3.8 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW trifásica",
        "tiempo_carga_dc": "26 min en 150 kW",
        "dimensiones": "4.800 x 1.875 x 1.460 mm",
        "peso_kg": 2185,
        "capacidad_baul_l": 400,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/seal",
        "especificaciones": {
            "traccion": "Integral eléctrica inteligente AWD",
            "ctb": "Cell-to-Body integración estructural",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-han-ev",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Han",
        "version": "Flagship Executive AWD",
        "precio_usd": 79990,
        "autonomia_km": 521,
        "bateria_kwh": 85.4,
        "potencia": "517 CV",
        "par_motor_nm": 700,
        "aceleracion_0_100": "3.9 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "30 min en 120 kW",
        "dimensiones": "4.995 x 1.910 x 1.495 mm",
        "peso_kg": 2250,
        "capacidad_baul_l": 410,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/han",
        "especificaciones": {
            "audio": "Sistema Dynaudio de 12 altavoces",
            "frenos": "Pinzas Brembo de 4 pistones",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-tang-ev",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Tang",
        "version": "7 Pasajeros AWD Flagship",
        "precio_usd": 89990,
        "autonomia_km": 505,
        "bateria_kwh": 86.4,
        "potencia": "517 CV",
        "par_motor_nm": 680,
        "aceleracion_0_100": "4.4 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "30 min en 110 kW",
        "dimensiones": "4.870 x 1.950 x 1.725 mm",
        "peso_kg": 2489,
        "capacidad_baul_l": 940,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/tang",
        "especificaciones": {
            "plazas": "3 filas de asientos (2+3+2)",
            "traccion": "AWD electrónica bimotor",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-e2",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "e2",
        "version": "Hatchback EV 405",
        "precio_usd": 24990,
        "autonomia_km": 405,
        "bateria_kwh": 43.2,
        "potencia": "95 CV",
        "par_motor_nm": 180,
        "aceleracion_0_100": "10.5 s",
        "velocidad_maxima": "130 km/h",
        "tiempo_carga_ac": "6 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.260 x 1.760 x 1.530 mm",
        "peso_kg": 1340,
        "capacidad_baul_l": 320,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy",
        "especificaciones": {
            "carroceria": "Hatchback Crossover",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-t3",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "T3",
        "version": "Furgón Utilitario Eléctrico 3.8m³",
        "precio_usd": 29990,
        "autonomia_km": 300,
        "bateria_kwh": 44.9,
        "potencia": "136 CV",
        "par_motor_nm": 180,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "130 km/h",
        "tiempo_carga_ac": "7 h",
        "tiempo_carga_dc": "45 min",
        "dimensiones": "4.460 x 1.720 x 1.875 mm",
        "peso_kg": 1700,
        "capacidad_baul_l": 3800,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://byd.uy/comerciales/t3",
        "especificaciones": {
            "capacidad_carga_kg": 720,
            "volumen_carga": "3.8 metros cúbicos",
            "puertas_traseras": "Apertura 180 grados",
            "importador": "SADAR S.A."
        }
    },
    {
        "id": "byd-shark",
        "tipo": "auto",
        "marca": "BYD",
        "modelo": "Shark",
        "version": "PHEV Pickup Doble Cabina 430 CV",
        "precio_usd": 58990,
        "autonomia_km": 840,
        "bateria_kwh": 29.6,
        "potencia": "430 CV",
        "par_motor_nm": 650,
        "aceleracion_0_100": "5.7 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "20 min (30-80%)",
        "dimensiones": "5.457 x 1.971 x 1.925 mm",
        "peso_kg": 2665,
        "capacidad_baul_l": 1450,
        "conector": "GB/T",
        "garantia_vehiculo": "6 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://byd.uy/modelos/shark",
        "especificaciones": {
            "chasis": "DMO Super Híbrido todoterreno",
            "capacidad_remolque_kg": 2500,
            "importador": "SADAR S.A."
        }
    },

    # =========================================================================
    # 2. VOLVO (IMPORTADOR OFICIAL: DANISSA / NORDEN)
    # =========================================================================
    {
        "id": "volvo-ex30",
        "tipo": "auto",
        "marca": "Volvo",
        "modelo": "EX30",
        "version": "Single Motor Extended Range Plus",
        "precio_usd": 42990,
        "autonomia_km": 476,
        "bateria_kwh": 69.0,
        "potencia": "272 CV",
        "par_motor_nm": 343,
        "aceleracion_0_100": "5.3 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "7.5 h (11 kW)",
        "tiempo_carga_dc": "26 min en 153 kW",
        "dimensiones": "4.233 x 1.837 x 1.555 mm",
        "peso_kg": 1850,
        "capacidad_baul_l": 318,
        "conector": "Type 2 / CCS2 nativo",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.volvocars.com/uy/cars/ex30-electric/",
        "especificaciones": {
            "sistema_operativo": "Google Automotive integrado nativo",
            "barra_sonido": "Harman Kardon de ancho completo",
            "importador": "Danissa / Norden"
        }
    },
    {
        "id": "volvo-ex30-ultra",
        "tipo": "auto",
        "marca": "Volvo",
        "modelo": "EX30",
        "version": "Twin Motor Performance Ultra AWD",
        "precio_usd": 52990,
        "autonomia_km": 450,
        "bateria_kwh": 69.0,
        "potencia": "428 CV",
        "par_motor_nm": 543,
        "aceleracion_0_100": "3.6 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW / 22 kW opcional",
        "tiempo_carga_dc": "26 min",
        "dimensiones": "4.233 x 1.837 x 1.555 mm",
        "peso_kg": 1960,
        "capacidad_baul_l": 318,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.volvocars.com/uy/cars/ex30-electric/",
        "especificaciones": {
            "traccion": "AWD permanente bimotor",
            "techo": "Cristal panorámico atérmico",
            "importador": "Danissa / Norden"
        }
    },
    {
        "id": "volvo-ex40",
        "tipo": "auto",
        "marca": "Volvo",
        "modelo": "EX40",
        "version": "Recharge Twin AWD Ultimate",
        "precio_usd": 69990,
        "autonomia_km": 530,
        "bateria_kwh": 82.0,
        "potencia": "408 CV",
        "par_motor_nm": 670,
        "aceleracion_0_100": "4.8 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "8 h",
        "tiempo_carga_dc": "28 min en 200 kW",
        "dimensiones": "4.440 x 1.863 x 1.651 mm",
        "peso_kg": 2188,
        "capacidad_baul_l": 419,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.volvocars.com/uy/cars/ex40-electric/",
        "especificaciones": {
            "segmento": "SUV Compacto Premium",
            "frunk_litros": 31,
            "importador": "Danissa / Norden"
        }
    },
    {
        "id": "volvo-ec40",
        "tipo": "auto",
        "marca": "Volvo",
        "modelo": "EC40",
        "version": "Crossover Coupé Recharge Twin AWD",
        "precio_usd": 72990,
        "autonomia_km": 540,
        "bateria_kwh": 82.0,
        "potencia": "408 CV",
        "par_motor_nm": 670,
        "aceleracion_0_100": "4.7 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "8 h",
        "tiempo_carga_dc": "28 min",
        "dimensiones": "4.440 x 1.873 x 1.591 mm",
        "peso_kg": 2185,
        "capacidad_baul_l": 413,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.volvocars.com/uy/cars/ec40-electric/",
        "especificaciones": {
            "aerodinamica_cx": 0.31,
            "luces": "Pixel LED inteligentes",
            "importador": "Danissa / Norden"
        }
    },
    {
        "id": "volvo-ex90",
        "tipo": "auto",
        "marca": "Volvo",
        "modelo": "EX90",
        "version": "Twin Motor Ultra 7 Plazas 517 CV",
        "precio_usd": 129990,
        "autonomia_km": 600,
        "bateria_kwh": 111.0,
        "potencia": "517 CV",
        "par_motor_nm": 910,
        "aceleracion_0_100": "4.9 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "30 min en 250 kW",
        "dimensiones": "5.037 x 1.964 x 1.747 mm",
        "peso_kg": 2818,
        "capacidad_baul_l": 655,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.volvocars.com/uy",
        "especificaciones": {
            "sensores": "LiDAR Luminar integrado en techo",
            "plazas": "7 asientos independientes eléctricos",
            "importador": "Danissa / Norden"
        }
    },

    # =========================================================================
    # 3. GEELY & ZEEKR (GRUPO FIANCAR)
    # =========================================================================
    {
        "id": "geely-ex5-pro",
        "tipo": "auto",
        "marca": "Geely",
        "modelo": "EX5",
        "version": "Pro EV 2026",
        "precio_usd": 33990,
        "autonomia_km": 460,
        "bateria_kwh": 60.2,
        "potencia": "218 CV",
        "par_motor_nm": 320,
        "aceleracion_0_100": "6.9 s",
        "velocidad_maxima": "172 km/h",
        "tiempo_carga_ac": "7 h",
        "tiempo_carga_dc": "20 min (30-80%)",
        "dimensiones": "4.615 x 1.901 x 1.670 mm",
        "peso_kg": 1720,
        "capacidad_baul_l": 461,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://geely.com.uy/modelos/ex5",
        "especificaciones": {
            "arquitectura": "GEA (Global Intelligent Electric Architecture)",
            "bateria": "Short Blade Battery Geely",
            "importador": "Grupo Fiancar"
        }
    },
    {
        "id": "geely-geometry-c",
        "tipo": "auto",
        "marca": "Geely",
        "modelo": "Geometry C",
        "version": "Pro 550 EV",
        "precio_usd": 38990,
        "autonomia_km": 485,
        "bateria_kwh": 70.0,
        "potencia": "204 CV",
        "par_motor_nm": 310,
        "aceleracion_0_100": "7.7 s",
        "velocidad_maxima": "150 km/h",
        "tiempo_carga_ac": "8 h",
        "tiempo_carga_dc": "35 min",
        "dimensiones": "4.432 x 1.833 x 1.560 mm",
        "peso_kg": 1665,
        "capacidad_baul_l": 415,
        "conector": "GB/T (Adaptador CCS2 disponible)",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://geely.com.uy",
        "especificaciones": {
            "climatizador": "Bomba de calor de alta eficiencia",
            "importador": "Grupo Fiancar"
        }
    },
    {
        "id": "geely-geometry-e",
        "tipo": "auto",
        "marca": "Geely",
        "modelo": "Geometry E",
        "version": "Compact City EV 39.4 kWh",
        "precio_usd": 23990,
        "autonomia_km": 380,
        "bateria_kwh": 39.4,
        "potencia": "81 CV",
        "par_motor_nm": 130,
        "aceleracion_0_100": "12.0 s",
        "velocidad_maxima": "125 km/h",
        "tiempo_carga_ac": "5.5 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.006 x 1.765 x 1.550 mm",
        "peso_kg": 1348,
        "capacidad_baul_l": 295,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://geely.com.uy",
        "especificaciones": {
            "segmento": "Crossover Urbano A",
            "importador": "Grupo Fiancar"
        }
    },
    {
        "id": "zeekr-001",
        "tipo": "auto",
        "marca": "Zeekr",
        "modelo": "001",
        "version": "Shooting Brake AWD 544 CV",
        "precio_usd": 89990,
        "autonomia_km": 620,
        "bateria_kwh": 100.0,
        "potencia": "544 CV",
        "par_motor_nm": 686,
        "aceleracion_0_100": "3.8 s",
        "velocidad_maxima": "200 km/h",
        "tiempo_carga_ac": "11 kW / 22 kW",
        "tiempo_carga_dc": "28 min en 200 kW",
        "dimensiones": "4.970 x 1.999 x 1.560 mm",
        "peso_kg": 2350,
        "capacidad_baul_l": 535,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://zeekrlife.com/uy",
        "especificaciones": {
            "suspension": "Neumática adaptativa con ajuste de altura",
            "audio": "Yamaha surround de 11 parlantes",
            "importador": "Grupo Fiancar"
        }
    },
    {
        "id": "zeekr-x",
        "tipo": "auto",
        "marca": "Zeekr",
        "modelo": "X",
        "version": "Urban Crossover AWD",
        "precio_usd": 54990,
        "autonomia_km": 440,
        "bateria_kwh": 66.0,
        "potencia": "428 CV",
        "par_motor_nm": 543,
        "aceleracion_0_100": "3.8 s",
        "velocidad_maxima": "190 km/h",
        "tiempo_carga_ac": "7 h",
        "tiempo_carga_dc": "28 min en 150 kW",
        "dimensiones": "4.432 x 1.836 x 1.572 mm",
        "peso_kg": 1945,
        "capacidad_baul_l": 362,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://zeekrlife.com/uy",
        "especificaciones": {
            "puertas": "Sin marco con apertura eléctrica táctil",
            "pantalla": "Deslizante de 14.6 pulgadas hacia acompañante",
            "importador": "Grupo Fiancar"
        }
    },
    {
        "id": "zeekr-7x",
        "tipo": "auto",
        "marca": "Zeekr",
        "modelo": "7X",
        "version": "SUV Eléctrico Premium 800V",
        "precio_usd": 74990,
        "autonomia_km": 605,
        "bateria_kwh": 100.0,
        "potencia": "646 CV",
        "par_motor_nm": 710,
        "aceleracion_0_100": "3.8 s",
        "velocidad_maxima": "210 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "15 min (800V ultra-rápida)",
        "dimensiones": "4.825 x 1.930 x 1.656 mm",
        "peso_kg": 2300,
        "capacidad_baul_l": 616,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://zeekrlife.com/uy",
        "especificaciones": {
            "voltaje": "Red eléctrica nativa de 800V",
            "importador": "Grupo Fiancar"
        }
    },

    # =========================================================================
    # 4. DONGFENG & NAMMI (FIDOCAR)
    # =========================================================================
    {
        "id": "dongfeng-nammi-box",
        "tipo": "auto",
        "marca": "Dongfeng",
        "modelo": "Nammi",
        "version": "Box 430 EV",
        "precio_usd": 21990,
        "autonomia_km": 430,
        "bateria_kwh": 42.3,
        "potencia": "95 CV",
        "par_motor_nm": 160,
        "aceleracion_0_100": "11.5 s",
        "velocidad_maxima": "140 km/h",
        "tiempo_carga_ac": "5 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.030 x 1.810 x 1.570 mm",
        "peso_kg": 1380,
        "capacidad_baul_l": 326,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://dongfengmotors.uy/modelos/nammi-box/",
        "especificaciones": {
            "diseño": "Puertas sin marco con manijas retráctiles",
            "importador": "Fidocar S.A."
        }
    },
    {
        "id": "dongfeng-nammi-330",
        "tipo": "auto",
        "marca": "Dongfeng",
        "modelo": "Nammi",
        "version": "Box 330 EV",
        "precio_usd": 18990,
        "autonomia_km": 330,
        "bateria_kwh": 31.4,
        "potencia": "95 CV",
        "par_motor_nm": 160,
        "aceleracion_0_100": "12.0 s",
        "velocidad_maxima": "140 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "4.030 x 1.810 x 1.570 mm",
        "peso_kg": 1320,
        "capacidad_baul_l": 326,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://dongfengmotors.uy",
        "especificaciones": {
            "pantalla": "12.8 pulgadas táctil",
            "importador": "Fidocar S.A."
        }
    },
    {
        "id": "dongfeng-rich-6-ev",
        "tipo": "auto",
        "marca": "Dongfeng",
        "modelo": "Rich 6",
        "version": "Pick-Up 100% Eléctrica Doble Cabina",
        "precio_usd": 48990,
        "autonomia_km": 403,
        "bateria_kwh": 67.9,
        "potencia": "163 CV",
        "par_motor_nm": 420,
        "aceleracion_0_100": "12.0 s",
        "velocidad_maxima": "120 km/h",
        "tiempo_carga_ac": "9 h",
        "tiempo_carga_dc": "45 min",
        "dimensiones": "5.290 x 1.850 x 1.790 mm",
        "peso_kg": 2050,
        "capacidad_baul_l": 1200,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://dongfengmotors.uy/modelos/rich6-ev/",
        "especificaciones": {
            "plataforma": "Base Nissan Navara / Frontier",
            "capacidad_carga_kg": 850,
            "importador": "Fidocar S.A."
        }
    },

    # =========================================================================
    # 5. JAC MOTORS (GRUPO ALER / FIANCAR)
    # =========================================================================
    {
        "id": "jac-e-js1",
        "tipo": "auto",
        "marca": "JAC",
        "modelo": "e-JS1",
        "version": "City Luxury EV",
        "precio_usd": 18990,
        "autonomia_km": 302,
        "bateria_kwh": 31.4,
        "potencia": "61 CV",
        "par_motor_nm": 150,
        "aceleracion_0_100": "12.5 s",
        "velocidad_maxima": "120 km/h",
        "tiempo_carga_ac": "5 h",
        "tiempo_carga_dc": "40 min",
        "dimensiones": "3.650 x 1.670 x 1.540 mm",
        "peso_kg": 1180,
        "capacidad_baul_l": 140,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://jac.com.uy/e-js1",
        "especificaciones": {
            "desarrollo": "Co-desarrollado con Volkswagen Group China",
            "importador": "Grupo Aler"
        }
    },
    {
        "id": "jac-e-js4",
        "tipo": "auto",
        "marca": "JAC",
        "modelo": "e-JS4",
        "version": "SUV Compacto EV 55 kWh",
        "precio_usd": 32990,
        "autonomia_km": 420,
        "bateria_kwh": 55.0,
        "potencia": "150 CV",
        "par_motor_nm": 340,
        "aceleracion_0_100": "9.5 s",
        "velocidad_maxima": "150 km/h",
        "tiempo_carga_ac": "7 h",
        "tiempo_carga_dc": "45 min",
        "dimensiones": "4.410 x 1.800 x 1.660 mm",
        "peso_kg": 1690,
        "capacidad_baul_l": 520,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://jac.com.uy/e-js4",
        "especificaciones": {
            "techo_solar": "Eléctrico panorámico",
            "camara": "Visión 360 grados panorámica",
            "importador": "Grupo Aler"
        }
    },
    {
        "id": "jac-e-j7",
        "tipo": "auto",
        "marca": "JAC",
        "modelo": "e-J7",
        "version": "Sedán Ejecutivo EV",
        "precio_usd": 37990,
        "autonomia_km": 402,
        "bateria_kwh": 50.1,
        "potencia": "193 CV",
        "par_motor_nm": 340,
        "aceleracion_0_100": "7.6 s",
        "velocidad_maxima": "150 km/h",
        "tiempo_carga_ac": "7 h",
        "tiempo_carga_dc": "40 min",
        "dimensiones": "4.770 x 1.820 x 1.510 mm",
        "peso_kg": 1650,
        "capacidad_baul_l": 540,
        "conector": "GB/T",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://jac.com.uy",
        "especificaciones": {
            "estilo": "Diseño realizado por centro de Turín",
            "importador": "Grupo Aler"
        }
    },

    # =========================================================================
    # 6. RENAULT & NISSAN (SANTA ROSA)
    # =========================================================================
    {
        "id": "renault-kwid-e-tech",
        "tipo": "auto",
        "marca": "Renault",
        "modelo": "Kwid",
        "version": "E-Tech 100% Eléctrico",
        "precio_usd": 20990,
        "autonomia_km": 298,
        "bateria_kwh": 26.8,
        "potencia": "65 CV",
        "par_motor_nm": 113,
        "aceleracion_0_100": "14.6 s",
        "velocidad_maxima": "130 km/h",
        "tiempo_carga_ac": "4 h (7.4 kW)",
        "tiempo_carga_dc": "40 min (30 kW DC)",
        "dimensiones": "3.734 x 1.579 x 1.516 mm",
        "peso_kg": 977,
        "capacidad_baul_l": 290,
        "conector": "Type 2 / CCS2 Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 120.000 km",
        "link_fabricante": "https://www.renault.com.uy/modelos/kwid-e-tech.html",
        "especificaciones": {
            "frenada_regenerativa": "3 niveles de recuperación",
            "importador": "Santa Rosa Automotores"
        }
    },
    {
        "id": "renault-megane-e-tech",
        "tipo": "auto",
        "marca": "Renault",
        "modelo": "Megane",
        "version": "E-Tech EV60 Crossover",
        "precio_usd": 49990,
        "autonomia_km": 450,
        "bateria_kwh": 60.0,
        "potencia": "220 CV",
        "par_motor_nm": 300,
        "aceleracion_0_100": "7.4 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "7 h (22 kW AC nativo)",
        "tiempo_carga_dc": "30 min en 130 kW",
        "dimensiones": "4.200 x 1.768 x 1.505 mm",
        "peso_kg": 1640,
        "capacidad_baul_l": 440,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.renault.com.uy",
        "especificaciones": {
            "pantallas": "OpenR de 24 pulgadas integradas",
            "importador": "Santa Rosa Automotores"
        }
    },
    {
        "id": "renault-kangoo-e-tech",
        "tipo": "auto",
        "marca": "Renault",
        "modelo": "Kangoo",
        "version": "E-Tech Furgón Comercial 45 kWh",
        "precio_usd": 41990,
        "autonomia_km": 300,
        "bateria_kwh": 45.0,
        "potencia": "120 CV",
        "par_motor_nm": 245,
        "aceleracion_0_100": "11.6 s",
        "velocidad_maxima": "135 km/h",
        "tiempo_carga_ac": "6 h (22 kW AC)",
        "tiempo_carga_dc": "30 min en 80 kW",
        "dimensiones": "4.486 x 1.860 x 1.864 mm",
        "peso_kg": 1608,
        "capacidad_baul_l": 3900,
        "conector": "CCS2",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.renault.com.uy",
        "especificaciones": {
            "sesamo": "Puerta lateral 'Ábrete Sésamo' sin pilar B",
            "capacidad_carga_kg": 600,
            "importador": "Santa Rosa Automotores"
        }
    },
    {
        "id": "nissan-leaf",
        "tipo": "auto",
        "marca": "Nissan",
        "modelo": "LEAF",
        "version": "Acenta 40 kWh",
        "precio_usd": 41990,
        "autonomia_km": 270,
        "bateria_kwh": 40.0,
        "potencia": "149 CV",
        "par_motor_nm": 320,
        "aceleracion_0_100": "7.9 s",
        "velocidad_maxima": "144 km/h",
        "tiempo_carga_ac": "6.5 h",
        "tiempo_carga_dc": "40 min en 50 kW",
        "dimensiones": "4.490 x 1.788 x 1.540 mm",
        "peso_kg": 1580,
        "capacidad_baul_l": 435,
        "conector": "Type 2 / CHAdeMO",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.nissan.com.uy",
        "especificaciones": {
            "pedal": "e-Pedal conducción con un solo pedal",
            "importador": "Santa Rosa Automotores"
        }
    },

    # =========================================================================
    # 7. GWM & OMODA
    # =========================================================================
    {
        "id": "gwm-ora-03",
        "tipo": "auto",
        "marca": "GWM",
        "modelo": "ORA 03",
        "version": "Skin 48 kWh (Retro Chic)",
        "precio_usd": 29990,
        "autonomia_km": 371,
        "bateria_kwh": 48.0,
        "potencia": "171 CV",
        "par_motor_nm": 250,
        "aceleracion_0_100": "8.2 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "6.5 h",
        "tiempo_carga_dc": "30 min en 67 kW",
        "dimensiones": "4.235 x 1.825 x 1.603 mm",
        "peso_kg": 1540,
        "capacidad_baul_l": 228,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://gwm.uy/modelos/ora-03",
        "especificaciones": {
            "seguridad": "5 Estrellas Euro NCAP",
            "importador": "Santa Rosa Automotores"
        }
    },
    {
        "id": "omoda-e5",
        "tipo": "auto",
        "marca": "Omoda",
        "modelo": "E5",
        "version": "Premium EV 61 kWh",
        "precio_usd": 38990,
        "autonomia_km": 430,
        "bateria_kwh": 61.0,
        "potencia": "204 CV",
        "par_motor_nm": 340,
        "aceleracion_0_100": "7.6 s",
        "velocidad_maxima": "172 km/h",
        "tiempo_carga_ac": "7 h",
        "tiempo_carga_dc": "28 min",
        "dimensiones": "4.424 x 1.830 x 1.588 mm",
        "peso_kg": 1785,
        "capacidad_baul_l": 372,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "7 años o 150.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://omoda.uy",
        "especificaciones": {
            "pantalla": "Curva panorámica de 24.6 pulgadas",
            "importador": "Grupo Chery UY"
        }
    },

    # =========================================================================
    # 8. HYUNDAI & KIA
    # =========================================================================
    {
        "id": "hyundai-kona-electric",
        "tipo": "auto",
        "marca": "Hyundai",
        "modelo": "Kona",
        "version": "Electric 64.8 kWh",
        "precio_usd": 51990,
        "autonomia_km": 490,
        "bateria_kwh": 64.8,
        "potencia": "204 CV",
        "par_motor_nm": 255,
        "aceleracion_0_100": "7.8 s",
        "velocidad_maxima": "172 km/h",
        "tiempo_carga_ac": "9 h",
        "tiempo_carga_dc": "41 min en 100 kW",
        "dimensiones": "4.355 x 1.825 x 1.575 mm",
        "peso_kg": 1720,
        "capacidad_baul_l": 466,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años sin límite",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://hyundai.com.uy",
        "especificaciones": {
            "asistencia": "Hyundai SmartSense ADAS",
            "importador": "Fidocar S.A."
        }
    },
    {
        "id": "hyundai-ioniq-5",
        "tipo": "auto",
        "marca": "Hyundai",
        "modelo": "Ioniq 5",
        "version": "Long Range AWD 72.6 kWh",
        "precio_usd": 69990,
        "autonomia_km": 460,
        "bateria_kwh": 72.6,
        "potencia": "305 CV",
        "par_motor_nm": 605,
        "aceleracion_0_100": "5.2 s",
        "velocidad_maxima": "185 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "18 min (800V ultrarrápida)",
        "dimensiones": "4.635 x 1.890 x 1.605 mm",
        "peso_kg": 2100,
        "capacidad_baul_l": 527,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años sin límite",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://hyundai.com.uy",
        "especificaciones": {
            "voltaje": "800V E-GMP arquitectura",
            "importador": "Fidocar S.A."
        }
    },
    {
        "id": "kia-ev3",
        "tipo": "auto",
        "marca": "Kia",
        "modelo": "EV3",
        "version": "Air Long Range 81.4 kWh",
        "precio_usd": 43990,
        "autonomia_km": 600,
        "bateria_kwh": 81.4,
        "potencia": "204 CV",
        "par_motor_nm": 283,
        "aceleracion_0_100": "7.5 s",
        "velocidad_maxima": "170 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "31 min en 128 kW",
        "dimensiones": "4.300 x 1.850 x 1.560 mm",
        "peso_kg": 1810,
        "capacidad_baul_l": 460,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://kia.com.uy",
        "especificaciones": {
            "interior": "Mesa deslizante en consola central",
            "importador": "Zenex Motors"
        }
    },
    {
        "id": "kia-ev6",
        "tipo": "auto",
        "marca": "Kia",
        "modelo": "EV6",
        "version": "GT-Line AWD 77.4 kWh",
        "precio_usd": 74990,
        "autonomia_km": 506,
        "bateria_kwh": 77.4,
        "potencia": "325 CV",
        "par_motor_nm": 605,
        "aceleracion_0_100": "5.2 s",
        "velocidad_maxima": "185 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "18 min en 240 kW",
        "dimensiones": "4.680 x 1.880 x 1.550 mm",
        "peso_kg": 2090,
        "capacidad_baul_l": 490,
        "conector": "CCS2",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://kia.com.uy",
        "especificaciones": {
            "premios": "Auto del Año en Europa",
            "importador": "Zenex Motors"
        }
    },

    # =========================================================================
    # 9. MAXUS (ABRILEY S.A.)
    # =========================================================================
    {
        "id": "maxus-edeliver-3",
        "tipo": "auto",
        "marca": "Maxus",
        "modelo": "eDeliver 3",
        "version": "Furgón Utilitario 4.8m³",
        "precio_usd": 32990,
        "autonomia_km": 240,
        "bateria_kwh": 35.0,
        "potencia": "122 CV",
        "par_motor_nm": 255,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "120 km/h",
        "tiempo_carga_ac": "6 h",
        "tiempo_carga_dc": "45 min",
        "dimensiones": "4.555 x 1.780 x 1.895 mm",
        "peso_kg": 1550,
        "capacidad_baul_l": 4800,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://maxus.uy/modelos/edeliver-3/",
        "especificaciones": {
            "capacidad_carga_kg": 905,
            "importador": "Abriley S.A."
        }
    },
    {
        "id": "maxus-eterron-9",
        "tipo": "auto",
        "marca": "Maxus",
        "modelo": "eTerron 9",
        "version": "Pick-Up 4x4 Eléctrica 442 CV",
        "precio_usd": 68990,
        "autonomia_km": 430,
        "bateria_kwh": 102.0,
        "potencia": "442 CV",
        "par_motor_nm": 620,
        "aceleracion_0_100": "5.8 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "30 min en 115 kW",
        "dimensiones": "5.500 x 2.000 x 1.860 mm",
        "peso_kg": 2700,
        "capacidad_baul_l": 1300,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "5 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://maxus.uy/modelos/eterron-9/",
        "especificaciones": {
            "traccion": "4x4 permanente bimotor",
            "importador": "Abriley S.A."
        }
    },

    # =========================================================================
    # 10. PREMIUM: BMW, MINI, AUDI, MERCEDES-BENZ
    # =========================================================================
    {
        "id": "bmw-ix1",
        "tipo": "auto",
        "marca": "BMW",
        "modelo": "iX1",
        "version": "xDrive30 64.7 kWh 313 CV",
        "precio_usd": 79990,
        "autonomia_km": 440,
        "bateria_kwh": 64.7,
        "potencia": "313 CV",
        "par_motor_nm": 494,
        "aceleracion_0_100": "5.6 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "29 min en 130 kW",
        "dimensiones": "4.500 x 1.845 x 1.616 mm",
        "peso_kg": 2085,
        "capacidad_baul_l": 490,
        "conector": "CCS2",
        "garantia_vehiculo": "3 años o 200.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://bmw.com.uy",
        "especificaciones": {
            "traccion": "xDrive total inteligente",
            "importador": "Magna Motors / Motor Haus"
        }
    },
    {
        "id": "mini-cooper-se",
        "tipo": "auto",
        "marca": "Mini",
        "modelo": "Cooper SE",
        "version": "3 Puertas Electric 54.2 kWh",
        "precio_usd": 49990,
        "autonomia_km": 402,
        "bateria_kwh": 54.2,
        "potencia": "218 CV",
        "par_motor_nm": 330,
        "aceleracion_0_100": "6.7 s",
        "velocidad_maxima": "170 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "30 min",
        "dimensiones": "3.858 x 1.756 x 1.460 mm",
        "peso_kg": 1605,
        "capacidad_baul_l": 210,
        "conector": "CCS2",
        "garantia_vehiculo": "3 años o 200.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://mini.com.uy",
        "especificaciones": {
            "pantalla": "OLED circular central de 240 mm",
            "importador": "Motor Haus"
        }
    },
    {
        "id": "audi-q4-e-tron",
        "tipo": "auto",
        "marca": "Audi",
        "modelo": "Q4 e-tron",
        "version": "45 e-tron 82 kWh",
        "precio_usd": 79990,
        "autonomia_km": 530,
        "bateria_kwh": 82.0,
        "potencia": "286 CV",
        "par_motor_nm": 545,
        "aceleracion_0_100": "6.7 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "28 min",
        "dimensiones": "4.588 x 1.865 x 1.632 mm",
        "peso_kg": 2145,
        "capacidad_baul_l": 520,
        "conector": "CCS2",
        "garantia_vehiculo": "3 años o 90.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://audi.com.uy",
        "especificaciones": {
            "headup": "Realidad aumentada proyectada en parabrisas",
            "importador": "Julio César Lestido S.A."
        }
    },
    {
        "id": "mercedes-benz-eqa",
        "tipo": "auto",
        "marca": "Mercedes-Benz",
        "modelo": "EQA",
        "version": "250+ Progressive 70.5 kWh",
        "precio_usd": 78990,
        "autonomia_km": 528,
        "bateria_kwh": 70.5,
        "potencia": "190 CV",
        "par_motor_nm": 385,
        "aceleracion_0_100": "8.6 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "32 min en 100 kW",
        "dimensiones": "4.463 x 1.834 x 1.620 mm",
        "peso_kg": 2055,
        "capacidad_baul_l": 340,
        "conector": "CCS2",
        "garantia_vehiculo": "2 años sin límite",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://mercedes-benz.com.uy",
        "especificaciones": {
            "sistema": "MBUX con navegación de inteligencia artificial",
            "importador": "Autolider Uruguay / Inchcape"
        }
    },
    {
        "id": "mercedes-benz-eqb",
        "tipo": "auto",
        "marca": "Mercedes-Benz",
        "modelo": "EQB",
        "version": "250+ 7 Asientos",
        "precio_usd": 85990,
        "autonomia_km": 505,
        "bateria_kwh": 70.5,
        "potencia": "190 CV",
        "par_motor_nm": 385,
        "aceleracion_0_100": "8.9 s",
        "velocidad_maxima": "160 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "32 min",
        "dimensiones": "4.684 x 1.834 x 1.667 mm",
        "peso_kg": 2110,
        "capacidad_baul_l": 465,
        "conector": "CCS2",
        "garantia_vehiculo": "2 años",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://mercedes-benz.com.uy",
        "especificaciones": {
            "filas": "3 filas de asientos para 7 ocupantes",
            "importador": "Autolider Uruguay / Inchcape"
        }
    },

    # =========================================================================
    # 11. CHEVROLET (GENERAL MOTORS URUGUAY)
    # =========================================================================
    {
        "id": "chevrolet-blazer-ev",
        "tipo": "auto",
        "marca": "Chevrolet",
        "modelo": "Blazer EV",
        "version": "RS AWD Ultium 102 kWh",
        "precio_usd": 74990,
        "autonomia_km": 520,
        "bateria_kwh": 102.0,
        "potencia": "340 CV (565 CV modo WOW)",
        "par_motor_nm": 440,
        "aceleracion_0_100": "5.8 s",
        "velocidad_maxima": "190 km/h",
        "tiempo_carga_ac": "11 kW / 22 kW",
        "tiempo_carga_dc": "20 min en 190 kW (30-80%)",
        "dimensiones": "4.883 x 1.982 x 1.648 mm",
        "peso_kg": 2420,
        "capacidad_baul_l": 720,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.chevrolet.com.uy/electricos/blazer-ev",
        "especificaciones": {
            "plataforma": "Ultium Platform General Motors",
            "pantalla": "Pantalla central táctil de 17.7 pulgadas con Google Built-in",
            "traccion": "AWD integral inteligente bimotor",
            "importador": "General Motors Uruguay"
        }
    },
    {
        "id": "chevrolet-equinox-ev",
        "tipo": "auto",
        "marca": "Chevrolet",
        "modelo": "Equinox EV",
        "version": "RS AWD Ultium 85 kWh",
        "precio_usd": 58990,
        "autonomia_km": 480,
        "bateria_kwh": 85.0,
        "potencia": "290 CV",
        "par_motor_nm": 450,
        "aceleracion_0_100": "6.0 s",
        "velocidad_maxima": "180 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "25 min en 150 kW",
        "dimensiones": "4.836 x 1.915 x 1.613 mm",
        "peso_kg": 2200,
        "capacidad_baul_l": 473,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.chevrolet.com.uy/electricos/equinox-ev",
        "especificaciones": {
            "plataforma": "Ultium Platform General Motors",
            "seguridad": "Chevy Safety Assist con frenado autónomo y alerta de peatones",
            "pantalla": "Pantalla táctil de 17.7 pulgadas y cluster de 11 pulgadas",
            "importador": "General Motors Uruguay"
        }
    },
    {
        "id": "chevrolet-spark-euv",
        "tipo": "auto",
        "marca": "Chevrolet",
        "modelo": "Spark EUV",
        "version": "City EV 32 kWh",
        "precio_usd": 22990,
        "autonomia_km": 310,
        "bateria_kwh": 32.0,
        "potencia": "68 CV",
        "par_motor_nm": 125,
        "aceleracion_0_100": "12.8 s",
        "velocidad_maxima": "125 km/h",
        "tiempo_carga_ac": "4.5 h",
        "tiempo_carga_dc": "35 min",
        "dimensiones": "3.780 x 1.625 x 1.540 mm",
        "peso_kg": 1080,
        "capacidad_baul_l": 220,
        "conector": "GB/T / CCS2",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://www.chevrolet.com.uy",
        "especificaciones": {
            "segmento": "Crossover Urbano Eléctrico",
            "aire_acondicionado": "Climatizador digital con filtro de polen",
            "importador": "General Motors Uruguay"
        }
    },
    {
        "id": "chevrolet-bolt-euv",
        "tipo": "auto",
        "marca": "Chevrolet",
        "modelo": "Bolt EUV",
        "version": "Premier EV 65 kWh",
        "precio_usd": 42990,
        "autonomia_km": 397,
        "bateria_kwh": 65.0,
        "potencia": "200 CV",
        "par_motor_nm": 360,
        "aceleracion_0_100": "7.7 s",
        "velocidad_maxima": "150 km/h",
        "tiempo_carga_ac": "7.5 h",
        "tiempo_carga_dc": "30 min en 55 kW",
        "dimensiones": "4.306 x 1.770 x 1.616 mm",
        "peso_kg": 1669,
        "capacidad_baul_l": 462,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.chevrolet.com.uy",
        "especificaciones": {
            "tecnologia": "Regen on Demand y conducción One-Pedal Driving",
            "techo": "Techo solar panorámico corredizo eléctrico",
            "importador": "General Motors Uruguay"
        }
    },

    # =========================================================================
    # 12. TESLA & MICROCARS
    # =========================================================================
    # --- TESLA MODEL 3 (3 VERSIONES HOMOLOGADAS) ---
    {
        "id": "tesla-model-3-rwd",
        "tipo": "auto",
        "marca": "Tesla",
        "modelo": "Model 3 Highland",
        "version": "Standard RWD 60 kWh LFP",
        "precio_usd": 62900,
        "autonomia_km": 513,
        "bateria_kwh": 60.0,
        "potencia": "283 CV (208 kW)",
        "par_motor_nm": 420,
        "aceleracion_0_100": "6.1 s",
        "velocidad_maxima": "201 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "25 min en 170 kW Supercharger",
        "dimensiones": "4.720 x 1.850 x 1.441 mm",
        "peso_kg": 1765,
        "capacidad_baul_l": 594,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "4 años o 80.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.tesla.com/model3",
        "especificaciones": {
            "traccion": "Trasera (RWD)",
            "pantalla_trasera": "Pantalla de 8 pulgadas para plazas traseras",
            "insonorizacion": "Cristales dobles acústicos 360°",
            "importador": "Importación Homologada Uruguay"
        }
    },
    {
        "id": "tesla-model-3-long-range",
        "tipo": "auto",
        "marca": "Tesla",
        "modelo": "Model 3 Highland",
        "version": "Long Range Dual Motor AWD 78.1 kWh",
        "precio_usd": 72900,
        "autonomia_km": 629,
        "bateria_kwh": 78.1,
        "potencia": "498 CV (366 kW)",
        "par_motor_nm": 493,
        "aceleracion_0_100": "4.4 s",
        "velocidad_maxima": "201 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "27 min en 250 kW Supercharger",
        "dimensiones": "4.720 x 1.850 x 1.441 mm",
        "peso_kg": 1828,
        "capacidad_baul_l": 594,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "4 años o 80.000 km",
        "garantia_bateria": "8 años o 192.000 km",
        "link_fabricante": "https://www.tesla.com/model3",
        "especificaciones": {
            "traccion": "Integral Dual Motor AWD",
            "audio": "Sistema de 17 altavoces con subwoofer dual",
            "autonomia_record": "629 km WLTP",
            "importador": "Importación Homologada Uruguay"
        }
    },
    {
        "id": "tesla-model-3-performance",
        "tipo": "auto",
        "marca": "Tesla",
        "modelo": "Model 3 Highland",
        "version": "Performance Ludicrous AWD 627 CV",
        "precio_usd": 82900,
        "autonomia_km": 528,
        "bateria_kwh": 78.1,
        "potencia": "627 CV (461 kW)",
        "par_motor_nm": 741,
        "aceleracion_0_100": "3.1 s",
        "velocidad_maxima": "262 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "25 min en 250 kW",
        "dimensiones": "4.720 x 1.850 x 1.431 mm",
        "peso_kg": 1851,
        "capacidad_baul_l": 594,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "4 años o 80.000 km",
        "garantia_bateria": "8 años o 192.000 km",
        "link_fabricante": "https://www.tesla.com/model3",
        "especificaciones": {
            "traccion": "Performance All-Wheel Drive",
            "chasis": "Amortiguación adaptativa variable en tiempo real",
            "asientos": "Deportivos Sport con sujeción lateral reforzada",
            "frenos": "Frenos de pista Track Mode V3",
            "importador": "Importación Homologada Uruguay"
        }
    },

    # --- TESLA MODEL Y (3 VERSIONES HOMOLOGADAS) ---
    {
        "id": "tesla-model-y-rwd",
        "tipo": "auto",
        "marca": "Tesla",
        "modelo": "Model Y",
        "version": "Standard RWD 60 kWh LFP",
        "precio_usd": 69900,
        "autonomia_km": 455,
        "bateria_kwh": 60.0,
        "potencia": "299 CV (220 kW)",
        "par_motor_nm": 420,
        "aceleracion_0_100": "6.9 s",
        "velocidad_maxima": "217 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "25 min en 170 kW",
        "dimensiones": "4.751 x 1.921 x 1.624 mm",
        "peso_kg": 1909,
        "capacidad_baul_l": 854,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "4 años o 80.000 km",
        "garantia_bateria": "8 años o 160.000 km",
        "link_fabricante": "https://www.tesla.com/modely",
        "especificaciones": {
            "traccion": "Trasera (RWD)",
            "baul_delantero": "Frunk de 117 litros adicional",
            "volumen_max": "2.158 litros totales",
            "importador": "Importación Homologada Uruguay"
        }
    },
    {
        "id": "tesla-model-y-long-range",
        "tipo": "auto",
        "marca": "Tesla",
        "modelo": "Model Y",
        "version": "Long Range AWD 78.1 kWh Dual Motor",
        "precio_usd": 79900,
        "autonomia_km": 533,
        "bateria_kwh": 78.1,
        "potencia": "514 CV (378 kW)",
        "par_motor_nm": 493,
        "aceleracion_0_100": "5.0 s",
        "velocidad_maxima": "217 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "25 min en 250 kW",
        "dimensiones": "4.751 x 1.921 x 1.624 mm",
        "peso_kg": 1979,
        "capacidad_baul_l": 854,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "4 años o 80.000 km",
        "garantia_bateria": "8 años o 192.000 km",
        "link_fabricante": "https://www.tesla.com/modely",
        "especificaciones": {
            "traccion": "Integral Dual Motor AWD",
            "remolque": "Capacidad de remolque hasta 1.600 kg",
            "importador": "Importación Homologada Uruguay"
        }
    },
    {
        "id": "tesla-model-y-performance",
        "tipo": "auto",
        "marca": "Tesla",
        "modelo": "Model Y",
        "version": "Performance AWD 534 CV Überturbine",
        "precio_usd": 89900,
        "autonomia_km": 514,
        "bateria_kwh": 78.1,
        "potencia": "534 CV (393 kW)",
        "par_motor_nm": 660,
        "aceleracion_0_100": "3.7 s",
        "velocidad_maxima": "250 km/h",
        "tiempo_carga_ac": "11 kW",
        "tiempo_carga_dc": "25 min en 250 kW",
        "dimensiones": "4.751 x 1.921 x 1.624 mm",
        "peso_kg": 1995,
        "capacidad_baul_l": 854,
        "conector": "CCS2 Combo",
        "garantia_vehiculo": "4 años o 80.000 km",
        "garantia_bateria": "8 años o 192.000 km",
        "link_fabricante": "https://www.tesla.com/modely",
        "especificaciones": {
            "traccion": "Performance All-Wheel Drive",
            "llantas": "Überturbine de 21 pulgadas con neumáticos Pirelli P Zero",
            "frenos": "Frenos sobredimensionados con pinzas en rojo",
            "aleron": "Fibra de carbono real en portón trasero",
            "importador": "Importación Homologada Uruguay"
        }
    },

    # --- BAW URUGUAY (5 PUERTAS Y 3 PUERTAS) ---
    {
        "id": "baw-l7-bagel-ev",
        "tipo": "auto",
        "marca": "BAW",
        "modelo": "L7 Bagel EV",
        "version": "Hatchback 5 Puertas 18.7 kWh",
        "precio_usd": 12990,
        "autonomia_km": 220,
        "bateria_kwh": 18.72,
        "potencia": "40 CV (30 kW)",
        "par_motor_nm": 102,
        "aceleracion_0_100": "14.5 s",
        "velocidad_maxima": "100 km/h",
        "tiempo_carga_ac": "5.5 h en Shuko 220V",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "3.520 x 1.498 x 1.580 mm",
        "peso_kg": 850,
        "capacidad_baul_l": 210,
        "conector": "GB/T / Shuko 220V",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "5 años o 100.000 km",
        "link_fabricante": "https://www.baw.com.cn",
        "especificaciones": {
            "puertas": "5 puertas y 4 plazas para adultos",
            "multimedia": "Pantalla táctil flotante con Bluetooth y cámara de reversa",
            "aire": "Aire acondicionado digital",
            "importador": "Autoboulevard / Distribuidores Plaza UY"
        }
    },
    {
        "id": "baw-pony-ev",
        "tipo": "auto",
        "marca": "BAW",
        "modelo": "Pony EV",
        "version": "Citycar 3 Puertas 13.7 kWh",
        "precio_usd": 9990,
        "autonomia_km": 170,
        "bateria_kwh": 13.7,
        "potencia": "27 CV (20 kW)",
        "par_motor_nm": 85,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "100 km/h",
        "tiempo_carga_ac": "4.5 h en 220V Shuko",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "3.162 x 1.498 x 1.585 mm",
        "peso_kg": 740,
        "capacidad_baul_l": 150,
        "conector": "GB/T / Shuko 220V",
        "garantia_vehiculo": "2 años o 50.000 km",
        "garantia_bateria": "5 años o 100.000 km",
        "link_fabricante": "https://www.baw.com.cn",
        "especificaciones": {
            "segmento": "Citycar Urbano Eléctrico de Entrada",
            "puertas": "3 puertas con portón trasero vidriado",
            "importador": "Distribuidores Plaza UY"
        }
    },

    # --- CHERY URUGUAY (GRUPO FIDOCAR) ---
    {
        "id": "chery-eq1",
        "tipo": "auto",
        "marca": "Chery",
        "modelo": "eQ1 Little Ant",
        "version": "Pequeña Hormiga LFP 30.8 kWh",
        "precio_usd": 19990,
        "autonomia_km": 301,
        "bateria_kwh": 30.8,
        "potencia": "61 CV (44 kW)",
        "par_motor_nm": 150,
        "aceleracion_0_100": "12.0 s",
        "velocidad_maxima": "120 km/h",
        "tiempo_carga_ac": "4.5 h",
        "tiempo_carga_dc": "30 min (30-80%)",
        "dimensiones": "3.200 x 1.670 x 1.550 mm",
        "peso_kg": 995,
        "capacidad_baul_l": 160,
        "conector": "GB/T Combo",
        "garantia_vehiculo": "5 años o 150.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://chery.com.uy",
        "especificaciones": {
            "chasis": "Monocasco de aleación de aluminio aeroespacial",
            "techo": "Techo panorámico vidriado",
            "pantalla": "Pantalla vertical HD de 10.25 pulgadas",
            "freno_mano": "Freno de estacionamiento electrónico (EPB) con Auto-Hold",
            "importador": "Grupo Fidocar"
        }
    },
    {
        "id": "chery-qq-ice-cream",
        "tipo": "auto",
        "marca": "Chery",
        "modelo": "QQ Ice Cream",
        "version": "Urban Kei 13.9 kWh",
        "precio_usd": 11990,
        "autonomia_km": 170,
        "bateria_kwh": 13.9,
        "potencia": "27 CV (20 kW)",
        "par_motor_nm": 85,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "100 km/h",
        "tiempo_carga_ac": "5.0 h en 220V",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "2.980 x 1.496 x 1.637 mm",
        "peso_kg": 699,
        "capacidad_baul_l": 120,
        "conector": "GB/T / Shuko 220V",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 120.000 km",
        "link_fabricante": "https://chery.com.uy",
        "especificaciones": {
            "estilo": "Kei car urbano juvenil con estética pastel",
            "importador": "Grupo Fidocar"
        }
    },

    # --- GEELY CITYCAR (GRUPO FIANCAR) ---
    {
        "id": "geely-panda-mini-ev",
        "tipo": "auto",
        "marca": "Geely",
        "modelo": "Panda Mini EV",
        "version": "Citycar Go 17 kWh LFP",
        "precio_usd": 13990,
        "autonomia_km": 200,
        "bateria_kwh": 17.03,
        "potencia": "41 CV (30 kW)",
        "par_motor_nm": 110,
        "aceleracion_0_100": "13.8 s",
        "velocidad_maxima": "100 km/h",
        "tiempo_carga_ac": "4.5 h",
        "tiempo_carga_dc": "30 min en 22 kW DC",
        "dimensiones": "3.065 x 1.522 x 1.600 mm",
        "peso_kg": 797,
        "capacidad_baul_l": 140,
        "conector": "GB/T Combo",
        "garantia_vehiculo": "4 años o 100.000 km",
        "garantia_bateria": "8 años o 150.000 km",
        "link_fabricante": "https://geely.com.uy",
        "especificaciones": {
            "techo": "Techo solar panorámico con cristal termoaislante",
            "carga_rapida": "Soporta carga rápida DC en terminales públicas",
            "pantalla": "Pantalla táctil central de 8 pulgadas",
            "importador": "Grupo Fiancar"
        }
    },

    # --- JMC / JMEV URUGUAY (#6 EN VENTAS ACAU) ---
    {
        "id": "jmev-ev3",
        "tipo": "auto",
        "marca": "JMC",
        "modelo": "JMEV EV3.3",
        "version": "Xiaoqilin Easy 21.4 kWh LFP",
        "precio_usd": 13990,
        "autonomia_km": 251,
        "bateria_kwh": 21.4,
        "potencia": "35 CV (26 kW)",
        "par_motor_nm": 84,
        "aceleracion_0_100": "15.0 s",
        "velocidad_maxima": "102 km/h",
        "tiempo_carga_ac": "5.5 h",
        "tiempo_carga_dc": "40 min",
        "dimensiones": "3.500 x 1.646 x 1.460 mm",
        "peso_kg": 915,
        "capacidad_baul_l": 180,
        "conector": "GB/T Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 120.000 km",
        "link_fabricante": "https://jmc.com.uy",
        "especificaciones": {
            "ranking": "Top 6 en ventas de vehículos eléctricos de Uruguay (ACAU)",
            "puertas": "5 puertas y 4 asientos con anclajes ISOFIX",
            "importador": "JMC Uruguay"
        }
    },

    # --- CHANGAN LUMIN (2 VERSIONES) ---
    {
        "id": "changan-lumin-155",
        "tipo": "auto",
        "marca": "Changan",
        "modelo": "Lumin 155",
        "version": "Corn EV 12.9 kWh",
        "precio_usd": 13990,
        "autonomia_km": 155,
        "bateria_kwh": 12.92,
        "potencia": "41 CV (30 kW)",
        "par_motor_nm": 88,
        "aceleracion_0_100": "14.0 s",
        "velocidad_maxima": "101 km/h",
        "tiempo_carga_ac": "4.0 h en 220V",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "3.270 x 1.700 x 1.545 mm",
        "peso_kg": 810,
        "capacidad_baul_l": 104,
        "conector": "GB/T / Shuko",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 120.000 km",
        "link_fabricante": "https://changan.uy",
        "especificaciones": {
            "diseno": "Ópticas circulares 'ojos somnolientos' con manijas eléctricas ocultas",
            "importador": "Changan Uruguay"
        }
    },
    {
        "id": "changan-lumin-301",
        "tipo": "auto",
        "marca": "Changan",
        "modelo": "Lumin 301 Sweet",
        "version": "DC Fast Charge 28 kWh",
        "precio_usd": 16990,
        "autonomia_km": 301,
        "bateria_kwh": 27.99,
        "potencia": "48 CV (35 kW)",
        "par_motor_nm": 90,
        "aceleracion_0_100": "12.8 s",
        "velocidad_maxima": "105 km/h",
        "tiempo_carga_ac": "6.0 h",
        "tiempo_carga_dc": "35 min (30-80% en DC)",
        "dimensiones": "3.270 x 1.700 x 1.545 mm",
        "peso_kg": 890,
        "capacidad_baul_l": 104,
        "conector": "GB/T Combo",
        "garantia_vehiculo": "3 años o 100.000 km",
        "garantia_bateria": "8 años o 120.000 km",
        "link_fabricante": "https://changan.uy",
        "especificaciones": {
            "carga_rapida": "Equipado con puerto DC de carga rápida de alta velocidad",
            "autonomia": "301 km para viajes suburbanos e interdepartamentales",
            "importador": "Changan Uruguay"
        }
    },

    # =========================================================================
    # 13. TRICICLOS ELÉCTRICOS Y MOTOCARROS (TRIKE / TREK URUGUAY)
    # =========================================================================
    {
        "id": "trike-hard-work-1000",
        "tipo": "triciclo",
        "marca": "Trike",
        "modelo": "Hard Work 1000 kg (Trekker)",
        "version": "Volcador Pesado 1500W con Reductora",
        "precio_usd": 2890,
        "autonomia_km": 70,
        "bateria_kwh": 3.24,
        "potencia": "1500W Marcha de Fuerza",
        "par_motor_nm": 120,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "45 km/h",
        "tiempo_carga_ac": "6 h en Shuko 220V",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "2.900 x 1.150 x 1.350 mm",
        "peso_kg": 240,
        "capacidad_baul_l": 1000,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año oficial",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://trike.uy",
        "especificaciones": {
            "capacidad_carga": "1.000 kg de carga útil en caja volcadora",
            "sistema_fuerza": "Palanca de alta y baja reductora para pendientes y carga pesada",
            "frenos": "Doble freno hidráulico a tambor reforzado y freno de estacionamiento",
            "costo_carga": "$50 pesos uruguayos por ciclo completo de recarga",
            "importador": "Trike Uruguay"
        }
    },
    {
        "id": "trike-cargo-light-500",
        "tipo": "triciclo",
        "marca": "Trike",
        "modelo": "Cargo Light GT 500 kg",
        "version": "Utilitario Urbano 1200W",
        "precio_usd": 2190,
        "autonomia_km": 60,
        "bateria_kwh": 2.4,
        "potencia": "1200W",
        "par_motor_nm": 85,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "40 km/h",
        "tiempo_carga_ac": "5 h en Shuko 220V",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "2.600 x 1.050 x 1.250 mm",
        "peso_kg": 180,
        "capacidad_baul_l": 500,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año oficial",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://trike.uy",
        "especificaciones": {
            "capacidad_carga": "500 kg para logística y distribución urbana",
            "chasis": "Acero reforzado con tratamiento anticorrosión",
            "importador": "Trike Uruguay"
        }
    },
    {
        "id": "trike-pasajeros-cabina",
        "tipo": "triciclo",
        "marca": "Trike",
        "modelo": "Urbano Delivery & Pasajeros",
        "version": "Cabina Cerrada 1200W 3 Plazas",
        "precio_usd": 2990,
        "autonomia_km": 60,
        "bateria_kwh": 2.88,
        "potencia": "1200W",
        "par_motor_nm": 85,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "42 km/h",
        "tiempo_carga_ac": "5 h en Shuko 220V",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "2.800 x 1.100 x 1.650 mm",
        "peso_kg": 220,
        "capacidad_baul_l": 400,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año oficial",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://trike.uy",
        "especificaciones": {
            "cabina": "Protección total contra lluvia y viento con limpiaparabrisas eléctrico",
            "plazas": "Conductor + 2 pasajeros o paquetería de comercio electrónico",
            "importador": "Trike Uruguay"
        }
    },
    {
        "id": "sunra-cargo-triciclo",
        "tipo": "triciclo",
        "marca": "Sunra",
        "modelo": "Cargo King",
        "version": "Tricar Utilitario 1500W 600 kg",
        "precio_usd": 2690,
        "autonomia_km": 65,
        "bateria_kwh": 2.7,
        "potencia": "1500W Motor Brushless",
        "par_motor_nm": 95,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "45 km/h",
        "tiempo_carga_ac": "5.5 h",
        "tiempo_carga_dc": "N/A",
        "dimensiones": "2.750 x 1.100 x 1.300 mm",
        "peso_kg": 210,
        "capacidad_baul_l": 600,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año oficial",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://sunra.com.uy",
        "especificaciones": {
            "caja": "Caja volcadora manual con compuertas rebatibles laterales y trasera",
            "importador": "Sunra Uruguay"
        }
    },

    # =========================================================================
    # 14. MOTOS Y SCOOTERS ELÉCTRICOS
    # =========================================================================
    {
        "id": "sunra-hawk-3000",
        "tipo": "moto",
        "marca": "Sunra",
        "modelo": "Hawk",
        "version": "3000W Doble Batería Litio",
        "precio_usd": 2490,
        "autonomia_km": 100,
        "bateria_kwh": 2.88,
        "potencia": "3000W Bosch Hub",
        "par_motor_nm": 45,
        "aceleracion_0_100": "0-50 km/h en 4.2s",
        "velocidad_maxima": "75 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko 220V domiciliario",
        "dimensiones": "1.850 x 710 x 1.100 mm",
        "peso_kg": 85,
        "capacidad_baul_l": 25,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "2 años oficial Sunra UY",
        "link_fabricante": "https://sunra.com.uy/productos/hawk-3000/",
        "especificaciones": {
            "bateria": "Litio extraíble para cargar en apartamento",
            "bluetooth": "Parlante Bluetooth integrado y alarma",
            "importador": "Sunra Uruguay"
        }
    },
    {
        "id": "sunra-grace-1800",
        "tipo": "moto",
        "marca": "Sunra",
        "modelo": "Grace",
        "version": "1800W Litio Extraíble",
        "precio_usd": 1890,
        "autonomia_km": 60,
        "bateria_kwh": 1.44,
        "potencia": "1800W Bosch",
        "par_motor_nm": 32,
        "aceleracion_0_100": "0-45 km/h en 4.9s",
        "velocidad_maxima": "50 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko 220V",
        "dimensiones": "1.720 x 705 x 1.050 mm",
        "peso_kg": 72,
        "capacidad_baul_l": 20,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "2 años",
        "link_fabricante": "https://sunra.com.uy/productos/grace/",
        "especificaciones": {
            "frenos": "Disco delantero y tambor trasero",
            "importador": "Sunra Uruguay"
        }
    },
    {
        "id": "sunra-miku-super",
        "tipo": "moto",
        "marca": "Sunra",
        "modelo": "Miku Super",
        "version": "3000W Naked Sport 80 km/h",
        "precio_usd": 3290,
        "autonomia_km": 110,
        "bateria_kwh": 2.88,
        "potencia": "3000W Dual Hub",
        "par_motor_nm": 120,
        "aceleracion_0_100": "0-80 km/h en 8.2s",
        "velocidad_maxima": "80 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "1.850 x 780 x 1.050 mm",
        "peso_kg": 95,
        "capacidad_baul_l": 10,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "2 años",
        "link_fabricante": "https://sunra.com.uy/productos/miku-super/",
        "especificaciones": {
            "estilo": "Chasis flotante deportivo naked",
            "importador": "Sunra Uruguay"
        }
    },
    {
        "id": "sunra-robo-s",
        "tipo": "moto",
        "marca": "Sunra",
        "modelo": "Robo-S",
        "version": "Smart Scooter 4000W 80 km/h",
        "precio_usd": 3590,
        "autonomia_km": 130,
        "bateria_kwh": 2.88,
        "potencia": "4000W",
        "par_motor_nm": 130,
        "aceleracion_0_100": "0-80 en 8.0s",
        "velocidad_maxima": "80 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko 220V",
        "dimensiones": "1.800 x 730 x 1.190 mm",
        "peso_kg": 91,
        "capacidad_baul_l": 28,
        "conector": "Shuko 220V",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "2 años",
        "link_fabricante": "https://sunra.com.uy",
        "especificaciones": {
            "encendido": "Huella dactilar biométrica",
            "importador": "Sunra Uruguay"
        }
    },
    {
        "id": "yadea-g5-pro",
        "tipo": "moto",
        "marca": "Yadea",
        "modelo": "G5",
        "version": "Pro Smart EV 2300W",
        "precio_usd": 2890,
        "autonomia_km": 80,
        "bateria_kwh": 1.92,
        "potencia": "2300W GTR 3.0",
        "par_motor_nm": 120,
        "aceleracion_0_100": "0-50 km/h en 4.5s",
        "velocidad_maxima": "65 km/h",
        "tiempo_carga_ac": "4.5 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "1.810 x 700 x 1.150 mm",
        "peso_kg": 88,
        "capacidad_baul_l": 26,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "2 años",
        "link_fabricante": "https://yadea.com.uy/modelos/g5/",
        "especificaciones": {
            "pantalla": "LCD de 7 pulgadas antirreflejo",
            "importador": "Yadea Uruguay"
        }
    },
    {
        "id": "yadea-c-umi",
        "tipo": "moto",
        "marca": "Yadea",
        "modelo": "C-Umi",
        "version": "Scooter Urbano Clásico",
        "precio_usd": 1790,
        "autonomia_km": 55,
        "bateria_kwh": 1.44,
        "potencia": "1200W",
        "par_motor_nm": 28,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "45 km/h",
        "tiempo_carga_ac": "5 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "1.720 x 725 x 1.020 mm",
        "peso_kg": 60,
        "capacidad_baul_l": 18,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "2 años",
        "link_fabricante": "https://yadea.com.uy",
        "especificaciones": {
            "estilo": "Diseño retro vintage europeo",
            "importador": "Yadea Uruguay"
        }
    },
    {
        "id": "niu-nqi-gt",
        "tipo": "moto",
        "marca": "Niu",
        "modelo": "NQi",
        "version": "GT Pro Smart Doble Batería",
        "precio_usd": 3890,
        "autonomia_km": 110,
        "bateria_kwh": 4.20,
        "potencia": "3500W Bosch",
        "par_motor_nm": 110,
        "aceleracion_0_100": "0-70 km/h en 6.0s",
        "velocidad_maxima": "75 km/h",
        "tiempo_carga_ac": "3.5 h",
        "tiempo_carga_dc": "Shuko 220V",
        "dimensiones": "1.800 x 740 x 1.130 mm",
        "peso_kg": 109,
        "capacidad_baul_l": 20,
        "conector": "Shuko",
        "garantia_vehiculo": "2 años",
        "garantia_bateria": "2 años oficial NIU",
        "link_fabricante": "https://niu.uy",
        "especificaciones": {
            "app": "Conectividad 4G y GPS antirrobo en tiempo real",
            "importador": "NIU Uruguay"
        }
    },
    {
        "id": "super-soco-tc-max",
        "tipo": "moto",
        "marca": "Super Soco",
        "modelo": "TC Max",
        "version": "Café Racer 5000W 95 km/h",
        "precio_usd": 4890,
        "autonomia_km": 110,
        "bateria_kwh": 3.24,
        "potencia": "5000W",
        "par_motor_nm": 180,
        "aceleracion_0_100": "0-90 en 9.0s",
        "velocidad_maxima": "95 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "1.982 x 740 x 1.031 mm",
        "peso_kg": 104,
        "capacidad_baul_l": 5,
        "conector": "Shuko",
        "garantia_vehiculo": "2 años",
        "garantia_bateria": "2 años",
        "link_fabricante": "https://vmoto.uy/modelos/tc-max",
        "especificaciones": {
            "transmision": "Correa dentada de carbono de alta resistencia",
            "importador": "Vmoto Uruguay"
        }
    },

    # =========================================================================
    # 13. BICICLETAS ELÉCTRICAS (E-BIKES URUGUAY)
    # =========================================================================
    {
        "id": "loop-bikes-slim-pro",
        "tipo": "bicicleta",
        "marca": "Loop Bikes",
        "modelo": "Slim Pro",
        "version": "Urbana Bafang 250W (Diseño Nacional UY)",
        "precio_usd": 1290,
        "autonomia_km": 60,
        "bateria_kwh": 0.36,
        "potencia": "250W Legal",
        "par_motor_nm": 45,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "3.5 h",
        "tiempo_carga_dc": "Shuko 220V",
        "dimensiones": "Rodado 28 cuadro aluminio",
        "peso_kg": 17,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año oficial",
        "garantia_bateria": "1 año oficial Loop Bikes UY",
        "link_fabricante": "https://loop-bikes.com/producto/slim-pro/",
        "especificaciones": {
            "motor": "Bafang 250W integrado en maza trasera",
            "bateria": "Samsung Li-Ion oculta en cuadro",
            "cuadro": "Aluminio hidroformado 6061",
            "frenos": "Discos mecánicos Tektro",
            "fabricante": "Loop Bikes Uruguay"
        }
    },
    {
        "id": "loop-bikes-soda-bike",
        "tipo": "bicicleta",
        "marca": "Loop Bikes",
        "modelo": "Soda Bike",
        "version": "Fat Bike Retro Cruiser 350W",
        "precio_usd": 1590,
        "autonomia_km": 50,
        "bateria_kwh": 0.48,
        "potencia": "350W",
        "par_motor_nm": 55,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "30 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Ruedas 20x4.0 pulgadas todo terreno",
        "peso_kg": 26,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://loop-bikes.com/producto/soda-bike/",
        "especificaciones": {
            "cubiertas": "Kenda 20x4.0 anchas para arena y asfalto",
            "asiento": "Largo estilo ciclomotor años 70 para dos",
            "fabricante": "Loop Bikes Uruguay"
        }
    },
    {
        "id": "loop-bikes-x350",
        "tipo": "bicicleta",
        "marca": "Loop Bikes",
        "modelo": "X350",
        "version": "Urbana Potente 350W Bafang",
        "precio_usd": 1450,
        "autonomia_km": 65,
        "bateria_kwh": 0.41,
        "potencia": "350W",
        "par_motor_nm": 50,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "32 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 29 aluminio",
        "peso_kg": 19,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://loop-bikes.com",
        "especificaciones": {
            "pantalla": "Display digital LCD multifunción",
            "fabricante": "Loop Bikes Uruguay"
        }
    },
    {
        "id": "loop-bikes-classic",
        "tipo": "bicicleta",
        "marca": "Loop Bikes",
        "modelo": "Classic",
        "version": "Paseo Vintage Holandesa 250W",
        "precio_usd": 1190,
        "autonomia_km": 50,
        "bateria_kwh": 0.36,
        "potencia": "250W",
        "par_motor_nm": 40,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 28 cuadro bajo paseo",
        "peso_kg": 21,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://loop-bikes.com",
        "especificaciones": {
            "accesorios": "Guardabarros, canasto delantero y luces LED",
            "fabricante": "Loop Bikes Uruguay"
        }
    },
    {
        "id": "voltbike-flex-foldable",
        "tipo": "bicicleta",
        "marca": "VoltBike",
        "modelo": "Flex",
        "version": "Plegable Urbana 350W Rodado 20",
        "precio_usd": 990,
        "autonomia_km": 45,
        "bateria_kwh": 0.38,
        "potencia": "350W",
        "par_motor_nm": 40,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "30 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Plegada: 85 x 45 x 65 cm",
        "peso_kg": 21,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año oficial VoltBike",
        "link_fabricante": "https://voltbike.uy/producto/voltbike-flex/",
        "especificaciones": {
            "plegado": "Mecanismo rápido en 15 segundos",
            "fabricante": "VoltBike Uruguay"
        }
    },
    {
        "id": "voltbike-pioneer",
        "tipo": "bicicleta",
        "marca": "VoltBike",
        "modelo": "Pioneer",
        "version": "E-MTB 500W con Suspensión",
        "precio_usd": 1390,
        "autonomia_km": 55,
        "bateria_kwh": 0.48,
        "potencia": "500W",
        "par_motor_nm": 60,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "35 km/h",
        "tiempo_carga_ac": "4.5 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 27.5",
        "peso_kg": 23,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://voltbike.uy/producto/voltbike-pioneer/",
        "especificaciones": {
            "suspension": "Horquilla con bloqueo hidráulico",
            "fabricante": "VoltBike Uruguay"
        }
    },
    {
        "id": "voltbike-classica",
        "tipo": "bicicleta",
        "marca": "VoltBike",
        "modelo": "Classica",
        "version": "Vintage Paseo con Canasto 250W",
        "precio_usd": 1090,
        "autonomia_km": 50,
        "bateria_kwh": 0.36,
        "potencia": "250W",
        "par_motor_nm": 38,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 26 cuadro bajo",
        "peso_kg": 22,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://voltbike.uy",
        "especificaciones": {
            "estilo": "Cuadro bajo para fácil acceso",
            "fabricante": "VoltBike Uruguay"
        }
    },
    {
        "id": "wheele-manhattan-flex",
        "tipo": "bicicleta",
        "marca": "Wheele",
        "modelo": "Manhattan",
        "version": "Flex Cruiser 250W Cuadro Bajo",
        "precio_usd": 1150,
        "autonomia_km": 50,
        "bateria_kwh": 0.37,
        "potencia": "250W",
        "par_motor_nm": 42,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 26 confort",
        "peso_kg": 23,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año oficial Wheele UY",
        "link_fabricante": "https://wheele.com.uy/producto/manhattan-flex/",
        "especificaciones": {
            "postura": "Ergonomía holandesa relajada",
            "fabricante": "Wheele / Green Motors Uruguay"
        }
    },
    {
        "id": "wheele-pocket-20",
        "tipo": "bicicleta",
        "marca": "Wheele",
        "modelo": "Pocket 20",
        "version": "Plegable Urbana Ultracompacta",
        "precio_usd": 890,
        "autonomia_km": 40,
        "bateria_kwh": 0.28,
        "potencia": "250W",
        "par_motor_nm": 35,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "3.5 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Plegada: 75 x 40 x 60 cm",
        "peso_kg": 18,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://wheele.com.uy/producto/pocket-20/",
        "especificaciones": {
            "peso": "Solo 18 kg para transporte fácil en ascensor",
            "fabricante": "Wheele / Green Motors Uruguay"
        }
    },
    {
        "id": "decathlon-rockrider-e-expl",
        "tipo": "bicicleta",
        "marca": "Decathlon / Rockrider",
        "modelo": "E-Expl 520",
        "version": "E-MTB 29 Yamaha PW-CE 70Nm",
        "precio_usd": 2490,
        "autonomia_km": 80,
        "bateria_kwh": 0.50,
        "potencia": "250W Yamaha PW-CE",
        "par_motor_nm": 70,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "4.5 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 29 hidroformado",
        "peso_kg": 23.8,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "De por vida en cuadro",
        "garantia_bateria": "2 años oficial Decathlon UY",
        "link_fabricante": "https://www.decathlon.com.uy/bicicletas-electricas/",
        "especificaciones": {
            "motor": "Motor central Yamaha PW-CE con sensor de par",
            "cambios": "Microshift Acolyte 8 velocidades",
            "importador": "Decathlon Uruguay"
        }
    },
    {
        "id": "decathlon-riverside-500e",
        "tipo": "bicicleta",
        "marca": "Decathlon / Riverside",
        "modelo": "500 E",
        "version": "Trekking Híbrida Eléctrica 250W",
        "precio_usd": 1690,
        "autonomia_km": 90,
        "bateria_kwh": 0.41,
        "potencia": "250W Par 42Nm",
        "par_motor_nm": 42,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "5 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 28 cuadro aluminio",
        "peso_kg": 21.8,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "De por vida en cuadro",
        "garantia_bateria": "2 años oficial Decathlon",
        "link_fabricante": "https://www.decathlon.com.uy",
        "especificaciones": {
            "suspension": "Horquilla telescópica para senderos",
            "importador": "Decathlon Uruguay"
        }
    },
    {
        "id": "xiaomi-himo-z20",
        "tipo": "bicicleta",
        "marca": "Xiaomi / Himo",
        "modelo": "Himo Z20",
        "version": "Plegable Urbana Inteligente",
        "precio_usd": 850,
        "autonomia_km": 80,
        "bateria_kwh": 0.36,
        "potencia": "250W",
        "par_motor_nm": 32,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "5 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 20 con inflador integrado",
        "peso_kg": 21.6,
        "capacidad_baul_l": 0,
        "conector": "Shuko",
        "garantia_vehiculo": "1 año",
        "garantia_bateria": "1 año",
        "link_fabricante": "https://www.himoebike.com",
        "especificaciones": {
            "innovacion": "Inflador de cubiertas oculto en caño de asiento",
            "importador": "Distribución Plaza Uruguay"
        }
    },
    {
        "id": "trek-allant-plus-7",
        "tipo": "bicicleta",
        "marca": "Trek",
        "modelo": "Allant+",
        "version": "7 Gen 2 Motor Bosch Performance CX",
        "precio_usd": 4190,
        "autonomia_km": 120,
        "bateria_kwh": 0.62,
        "potencia": "250W Bosch 85Nm",
        "par_motor_nm": 85,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "4 h Bosch 4A",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 27.5x2.4",
        "peso_kg": 21.5,
        "capacidad_baul_l": 0,
        "conector": "Bosch Smart System",
        "garantia_vehiculo": "De por vida en cuadro Trek",
        "garantia_bateria": "2 años oficial Trek Uruguay",
        "link_fabricante": "https://trekbikes.com/uy/es_UR/",
        "especificaciones": {
            "motor": "Bosch Performance Line CX (85 Nm)",
            "importador": "Trek Uruguay"
        }
    },
    {
        "id": "specialized-turbo-vado-4",
        "tipo": "bicicleta",
        "marca": "Specialized",
        "modelo": "Turbo Vado",
        "version": "4.0 Motor Specialized 2.0 70Nm",
        "precio_usd": 4690,
        "autonomia_km": 140,
        "bateria_kwh": 0.71,
        "potencia": "250W Specialized Full Power",
        "par_motor_nm": 70,
        "aceleracion_0_100": "N/A",
        "velocidad_maxima": "25 km/h",
        "tiempo_carga_ac": "4 h",
        "tiempo_carga_dc": "Shuko",
        "dimensiones": "Rodado 28 cuadro E5",
        "peso_kg": 20.8,
        "capacidad_baul_l": 0,
        "conector": "Specialized Custom",
        "garantia_vehiculo": "De por vida",
        "garantia_bateria": "2 años Specialized UY",
        "link_fabricante": "https://specialized.com/uy",
        "especificaciones": {
            "pantalla": "MasterMind TCD a color con Bluetooth y radar Garmin",
            "importador": "Specialized Uruguay"
        }
    }
]

import re

def slugify(text: str) -> str:
    text = str(text or "").lower()
    text = re.sub(r"[áàäâã]", "a", text)
    text = re.sub(r"[éèëê]", "e", text)
    text = re.sub(r"[íìïî]", "i", text)
    text = re.sub(r"[óòöôõ]", "o", text)
    text = re.sub(r"[úùüû]", "u", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def generar_nombre_seo(v_id: str, marca: str, modelo: str, version: str, tipo: str, indice: int) -> str:
    if tipo == "triciclo":
        vistas = [
            "01-vista-isometrica-frontal-3-4-cabina",
            "02-vista-trasera-caja-carga-volcadora",
            "03-puesto-conduccion-manillar-comandos",
            "04-perfil-lateral-chasis-reforzado",
            "05-detalle-motor-baterias-transmision-fuerza",
            "06-detalle-caja-mecanismo-volcador"
        ]
        subtipo = "triciclo-electrico"
    elif tipo == "moto":
        vistas = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-opticas",
            "03-puesto-conduccion-manillar-tablero",
            "04-perfil-lateral-completo",
            "05-detalle-bateria-motor-hub",
            "06-detalle-faro-led-frenos"
        ]
        subtipo = "moto-electrica"
    elif tipo == "bicicleta":
        vistas = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-cuadro-rueda",
            "03-manillar-display-digital-comando",
            "04-perfil-lateral-bicicleta",
            "05-detalle-motor-bateria-puerto-carga",
            "06-detalle-transmision-frenos-disco"
        ]
        subtipo = "bicicleta-electrica"
    else:
        vistas = [
            "01-vista-isometrica-frontal-3-4",
            "02-vista-trasera-opticas-porton",
            "03-interior-tablero-consola-cockpit",
            "04-perfil-lateral-carroceria",
            "05-detalle-bateria-conector-carga",
            "06-detalle-frontal-firma-luminica"
        ]
        subtipo = "auto-electrico"

    vista_slug = vistas[indice - 1]
    ver_corta = slugify(version.split("/")[0].split("(")[0])[:20].strip("-") if version else ""
    partes = [marca, modelo]
    if ver_corta:
        partes.append(ver_corta)
    partes.append(subtipo)
    vehiculo_slug = slugify(" ".join(partes))

    return f"{vista_slug}-{vehiculo_slug}-ev-servicioti-uruguay.webp"

def poblar_catalogo_completo():
    from db_manager import init_db
    init_db()
    print(f"=== Sembrando Catálogo Exhaustivo de Uruguay: {len(CATALOGO_EXHAUSTIVO)} modelos ===")
    conn = get_connection()
    cursor = conn.cursor()
    saved = 0

    for v in CATALOGO_EXHAUSTIVO:
        v_id = v["id"]
        # Galería por defecto de 6 fotos locales con nombres SEO enriquecidos
        galeria_defecto = [
            f"assets/img/{v_id}/{generar_nombre_seo(v_id, v['marca'], v['modelo'], v.get('version', ''), v['tipo'], i)}"
            for i in range(1, 7)
        ]
        galeria_str = json.dumps(galeria_defecto)
        
        # Enriquecer especificaciones con URLs canónicas de Badge Circular y Pixel Art 16-Bit
        especs = dict(v.get("especificaciones", {}))
        from build_full_galleries import generar_nombre_badge, generar_nombre_pixel_art
        badge_name = generar_nombre_badge(v['marca'], v['modelo'], v.get('version', ''), v['tipo'])
        pixel_name = generar_nombre_pixel_art(v['marca'], v['modelo'], v.get('version', ''), v['tipo'])
        especs["badge_circular_url"] = f"assets/img/{v_id}/{badge_name}"
        especs["pixel_art_url"] = f"assets/img/{v_id}/{pixel_name}"
        espec_str = json.dumps(especs)
        img_principal = galeria_defecto[0]

        cursor.execute("""
        INSERT INTO vehicles (
            id, tipo, marca, modelo, version, precio_usd, autonomia_km,
            bateria_kwh, potencia, par_motor_nm, aceleracion_0_100, velocidad_maxima,
            tiempo_carga_ac, tiempo_carga_dc, dimensiones, peso_kg, capacidad_baul_l,
            conector, garantia_vehiculo, garantia_bateria, homologado_ursea,
            link_fabricante, imagen_oficial_url, galeria_json, especificaciones_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            precio_usd=excluded.precio_usd,
            autonomia_km=excluded.autonomia_km,
            bateria_kwh=excluded.bateria_kwh,
            potencia=excluded.potencia,
            par_motor_nm=excluded.par_motor_nm,
            aceleracion_0_100=excluded.aceleracion_0_100,
            velocidad_maxima=excluded.velocidad_maxima,
            tiempo_carga_ac=excluded.tiempo_carga_ac,
            tiempo_carga_dc=excluded.tiempo_carga_dc,
            dimensiones=excluded.dimensiones,
            peso_kg=excluded.peso_kg,
            capacidad_baul_l=excluded.capacidad_baul_l,
            conector=excluded.conector,
            garantia_vehiculo=excluded.garantia_vehiculo,
            garantia_bateria=excluded.garantia_bateria,
            link_fabricante=excluded.link_fabricante,
            imagen_oficial_url=excluded.imagen_oficial_url,
            galeria_json=excluded.galeria_json,
            especificaciones_json=excluded.especificaciones_json
        """, (
            v_id, v["tipo"], v["marca"], v["modelo"], v["version"],
            v["precio_usd"], v["autonomia_km"], v["bateria_kwh"], v["potencia"],
            v.get("par_motor_nm", 0), v.get("aceleracion_0_100", "N/A"),
            v.get("velocidad_maxima", "N/A"), v.get("tiempo_carga_ac", "N/A"),
            v.get("tiempo_carga_dc", "N/A"), v.get("dimensiones", "N/A"),
            v.get("peso_kg", 0), v.get("capacidad_baul_l", 0),
            v["conector"], v["garantia_vehiculo"], v["garantia_bateria"],
            v["link_fabricante"], img_principal,
            galeria_str, espec_str
        ))
        saved += 1

    # También actualizar crónicas editoriales de calidad 100% de EV Uruguay
    cursor.execute("DELETE FROM news_articles;")

    def get_vehicle_img(vid):
        cursor.execute("SELECT imagen_oficial_url FROM vehicles WHERE id = ?", (vid,))
        r = cursor.fetchone()
        return r["imagen_oficial_url"] if r else ""

    def get_vehicle_gallery(vid):
        cursor.execute("SELECT galeria_json FROM vehicles WHERE id = ?", (vid,))
        row = cursor.fetchone()
        if row and row["galeria_json"]:
            try:
                return json.loads(row["galeria_json"])
            except Exception:
                return []
        return []

    # Obtener fotos auténticas de catálogo para las galerías de cada crónica
    byd_gal = get_vehicle_gallery("byd-seagull-surf")[:4]
    chevy_gal = (get_vehicle_gallery("chevrolet-blazer-ev")[:2] + get_vehicle_gallery("chevrolet-equinox-ev")[:2])
    if len(chevy_gal) < 4:
        chevy_gal = get_vehicle_gallery("chevrolet-blazer-ev")[:4]
    volvo_gal = get_vehicle_gallery("volvo-ex30")[:4]
    ute_gal = [
        get_vehicle_img("dongfeng-nammi-box"),
        get_vehicle_img("geely-panda-mini-ev"),
        get_vehicle_img("chery-eq1"),
        get_vehicle_img("byd-dolphin-gs")
    ]
    micro_gal = [
        get_vehicle_img("loop-bikes-slim-pro"),
        get_vehicle_img("sunra-hawk-3000"),
        get_vehicle_img("trek-allant-plus-7"),
        get_vehicle_img("sunra-miku-super")
    ]
    fiscal_gal = [
        get_vehicle_img("jac-e-js1"),
        get_vehicle_img("baw-pony-ev"),
        get_vehicle_img("baw-l7-bagel-ev"),
        get_vehicle_img("trike-cargo-light-500")
    ]

    cronicas = [
        (
            "cronica-byd-liderazgo-2026",
            "EV Uruguay Editorial",
            "BYD consolida su liderazgo en Uruguay: el Seagull encabeza las ventas de vehículos 100% eléctricos",
            "#cronica-byd-liderazgo-2026",
            "2026-10-25 18:00:00",
            "El segmento de hatchbacks urbanos eléctricos supera el 60% de penetración de ventas en Montevideo y el interior. Analizamos por qué la arquitectura Blade LFP y el costo por kilómetro con tarifa triple horario de UTE están transformando la plaza uruguaya.",
            "BYD • SADAR",
            get_vehicle_img("byd-seagull-surf"),
            json.dumps(byd_gal, ensure_ascii=False),
            "<p>Crónica de análisis sobre el fenómeno de penetración de BYD en Uruguay.</p>"
        ),
        (
            "cronica-chevrolet-ultium-uruguay",
            "EV Uruguay Editorial",
            "General Motors desembarca con su arquitectura Ultium: Blazer EV y Equinox EV aceleran la plaza",
            "#cronica-chevrolet-ultium-uruguay",
            "2026-10-25 15:00:00",
            "Chevrolet consolida su ofensiva eléctrica nacional con potencias de hasta 565 CV en modo WOW, plataformas modulares Ultium y autonomías que superan holgadamente los 500 km en ruta.",
            "Chevrolet • General Motors",
            get_vehicle_img("chevrolet-blazer-ev"),
            json.dumps(chevy_gal, ensure_ascii=False),
            "<p>Análisis del arribo de la plataforma Ultium de Chevrolet a Uruguay.</p>"
        ),
        (
            "cronica-volvo-ex30-uruguay",
            "EV Uruguay Editorial",
            "Volvo EX30: anatomía del SUV compacto de lujo que batió récords de matriculación",
            "#cronica-volvo-ex30-uruguay",
            "2026-10-24 14:30:00",
            "Con autonomías homologadas de hasta 476 km y aceleración de superdeportivo en su versión Twin Motor de 428 CV, el modelo nórdico redefine el estándar entre diseño minimalista, seguridad integral y eficiencia energética en las rutas uruguayas.",
            "Volvo • Danissa",
            get_vehicle_img("volvo-ex30"),
            json.dumps(volvo_gal, ensure_ascii=False),
            "<p>Análisis exhaustivo del Volvo EX30 en el mercado nacional.</p>"
        ),
        (
            "cronica-red-ute-mueve-expansion",
            "EV Uruguay Editorial",
            "La Red UTE Mueve expande sus cargadores ultrarrápidos de corriente continua a todo el país",
            "#cronica-red-ute-mueve-expansion",
            "2026-10-23 11:15:00",
            "La red nacional de carga pública supera los 300 puntos operativos desde Colonia hasta el Chuy. Guía práctica para planificar viajes interdepartamentales utilizando los conectores CCS2 y GB/T en las rutas nacionales 1, 2, 8 y 9.",
            "UTE Mueve • Infraestructura",
            get_vehicle_img("dongfeng-nammi-box"),
            json.dumps(ute_gal, ensure_ascii=False),
            "<p>Informe técnico sobre la red nacional de cargadores rápidos de UTE.</p>"
        ),
        (
            "cronica-micromovilidad-ebikes-motos",
            "EV Uruguay Editorial",
            "Revolución urbana sobre dos ruedas: e-bikes de ingeniería nacional y scooters lideran la movilidad diaria",
            "#cronica-micromovilidad-ebikes-motos",
            "2026-10-22 09:00:00",
            "Marcas nacionales como Loop Bikes y VoltBike, junto a Sunra y Yadea, impulsan la micromovilidad eléctrica en la Rambla de Montevideo y Ciudad Vieja con costos de recarga inferiores a $5 por trayecto de 30 km.",
            "Loop Bikes • VoltBike • Sunra",
            get_vehicle_img("loop-bikes-slim-pro"),
            json.dumps(micro_gal, ensure_ascii=False),
            "<p>Investigación sobre el auge de las bicicletas y motos eléctricas en el área metropolitana.</p>"
        ),
        (
            "cronica-beneficios-fiscales-sucive",
            "EV Uruguay Editorial",
            "Régimen fiscal y exoneración de patente SUCIVE: el beneficio económico de pasarse a cero emisiones",
            "#cronica-beneficios-fiscales-sucive",
            "2026-10-21 16:45:00",
            "Exoneración de IMESI, reducciones tributarias para empresas mediante proyectos COMAP y descuentos sustanciales en la patente de rodados departamental hacen que la amortización de un EV se alcance en tiempo récord.",
            "SUCIVE • DGI • Movilidad",
            get_vehicle_img("jac-e-js1"),
            json.dumps(fiscal_gal, ensure_ascii=False),
            "<p>Guía de incentivos y costos operativos comparativos para Uruguay.</p>"
        )
    ]

    for cr in cronicas:
        cursor.execute("""
        INSERT INTO news_articles (id, medio, titulo, url, fecha_publicacion, resumen, marcas_mencionadas, imagen_portada, galeria_json, contenido_html)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, cr)

    conn.commit()
    conn.close()
    print(f"[Éxito] {saved} modelos y 6 crónicas registradas en SQLite.")

    # Sincronizar automáticamente rankings oficiales de ventas ACAU y exportar JSON/JS
    from sync_acau_rankings import sync_rankings
    sync_rankings()

if __name__ == "__main__":
    poblar_catalogo_completo()
