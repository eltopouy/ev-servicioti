# -*- coding: utf-8 -*-
"""
Enriquecedor Exhaustivo de Especificaciones Técnicas de Batería y Año de Origen
Proyecto: EV Uruguay (https://ev.servicioti.com.uy)
Autor: Andrés Franchi Ugartemendía (ServicioTI)

Agrega a la base de datos de cada uno de los 97 vehículos:
- Tipo de batería (LFP, NCM, Ternaria, Iones de Litio, Gel Sellado)
- Fabricante de celdas (BYD FinDreams Blade, CATL, LG Energy Solution, Panasonic, etc.)
- Química exacta (LiFePO4, NMC 811, NMC 622, etc.)
- Sistema de refrigeración y gestión térmica
- Arquitectura de voltaje (400V, 800V, 72V, etc.)
- Año de fabricación / lanzamiento del modelo en origen
"""
import sqlite3
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ev_uruguay.db"

BATTERY_AND_YEAR_RULES = {
    # BYD
    "byd-seagull": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 estructural Blade Battery",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida activa integrada con bomba de calor",
        "voltaje": "307.2V (Arquitectura e-Platform 3.0)",
        "anio": 2023
    },
    "byd-dolphin": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 estructural Blade Battery",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida activa con climatización térmica por bomba de calor",
        "voltaje": "332.8V - 403.2V (e-Platform 3.0)",
        "anio": 2021
    },
    "byd-yuan-pro": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas Blade de alta seguridad",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida inteligente con precalentamiento",
        "voltaje": "384V (e-Platform 3.0)",
        "anio": 2021
    },
    "byd-yuan-plus": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 Cell-to-Body (CTB) Blade",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida activa con bomba de calor reversible",
        "voltaje": "403.2V (e-Platform 3.0)",
        "anio": 2022
    },
    "byd-song-plus": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas Blade",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida activa con intercambiador térmico",
        "voltaje": "400V nominal",
        "anio": 2020
    },
    "byd-han": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 Blade Battery de alta potencia",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida de doble circuito con refrigeración directa",
        "voltaje": "569.6V (Alta tensión deportiva)",
        "anio": 2020
    },
    "byd-tang": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas Blade",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida activa dual para SUV 7 plazas",
        "voltaje": "600V nominal",
        "anio": 2022
    },
    "byd-seal": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 Cell-to-Body (CTB) de integración estructural",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida inteligente con bomba de calor y gestión de -30°C a 60°C",
        "voltaje": "550.4V - 800V High Voltage",
        "anio": 2022
    },
    "byd-e2": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas Blade",
        "fabricante": "BYD FinDreams Battery (Blade)",
        "refrigeracion": "Líquida activa",
        "voltaje": "350V",
        "anio": 2019
    },
    "byd-t3": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas prismáticas para trabajo comercial pesado",
        "fabricante": "BYD FinDreams Battery",
        "refrigeracion": "Líquida de alta resistencia térmica",
        "voltaje": "384V",
        "anio": 2020
    },
    # Farizon
    "farizon-v6e": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas prismáticas de ciclo profundo (+3000 ciclos)",
        "fabricante": "EVE Energy / CATL",
        "refrigeracion": "Líquida activa con monitoreo térmico en tiempo real",
        "voltaje": "380V comercial",
        "anio": 2022
    },
    "farizon-supervan": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 arquitectura modular GMA con celdas de alta densidad",
        "fabricante": "CATL / Geely Farizon Power",
        "refrigeracion": "Líquida inteligente con precalentamiento y carga rápida CCS2",
        "voltaje": "400V - 500V DC",
        "anio": 2024
    },
    "farizon-h8e": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 paquete de tracción para camión urbano 6 Toneladas",
        "fabricante": "CATL Commercial Division",
        "refrigeracion": "Líquida reforzada para servicio severo y pendientes pronunciadas",
        "voltaje": "540V DC",
        "anio": 2022
    },
    "farizon-h9e": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 paquete industrial para camión pesado 8 Toneladas",
        "fabricante": "CATL Heavy Duty Battery Systems",
        "refrigeracion": "Líquida dual de alto caudal con aislamiento IP68",
        "voltaje": "540V - 600V DC",
        "anio": 2023
    },
    # Tesla
    "tesla-model-3-rwd": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 prismática (permite carga diaria habitual al 100%)",
        "fabricante": "CATL (Contemporary Amperex Technology)",
        "refrigeracion": "Líquida patentada Tesla Octovalve con bomba de calor",
        "voltaje": "400V nominal",
        "anio": 2023
    },
    "tesla-model-3-long-range": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Ternaria",
        "quimica": "NMC 811 celdas cilíndricas 2170 de alta densidad",
        "fabricante": "LG Energy Solution / Panasonic",
        "refrigeracion": "Líquida patentada Tesla Octovalve con preacondicionamiento térmico",
        "voltaje": "400V nominal",
        "anio": 2023
    },
    "tesla-model-3-performance": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Ternaria de Alto Rendimiento",
        "quimica": "NMC celdas cilíndricas 2170 optimizadas para alta descarga (Ludicrous)",
        "fabricante": "Panasonic / LG Energy Solution",
        "refrigeracion": "Líquida de competición con radiador dual y Octovalve",
        "voltaje": "400V",
        "anio": 2024
    },
    "tesla-model-y-rwd": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 prismática (carga diaria al 100% sin degradación prematura)",
        "fabricante": "CATL (Contemporary Amperex Technology)",
        "refrigeracion": "Líquida patentada Tesla Octovalve con bomba de calor",
        "voltaje": "400V nominal",
        "anio": 2022
    },
    "tesla-model-y-long-range": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Ternaria",
        "quimica": "NMC 811 celdas cilíndricas 2170",
        "fabricante": "LG Energy Solution",
        "refrigeracion": "Líquida con bomba de calor Octovalve",
        "voltaje": "400V nominal",
        "anio": 2021
    },
    "tesla-model-y-performance": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Ternaria de Alta Potencia",
        "quimica": "NMC 811 celdas 2170 de entrega inmediata",
        "fabricante": "LG Energy Solution / Panasonic",
        "refrigeracion": "Líquida de alta disipación térmica",
        "voltaje": "400V nominal",
        "anio": 2021
    },
    # Volvo
    "volvo-ex30-core": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 de química estable y económica",
        "fabricante": "CATL (Plataforma Geely SEA)",
        "refrigeracion": "Líquida con preacondicionamiento",
        "voltaje": "400V",
        "anio": 2023
    },
    "volvo-ex30": {
        "tipo": "NMC (Níquel Manganeso Cobalto) Extended Range",
        "quimica": "NMC celdas prismáticas de alta densidad energética",
        "fabricante": "CALB / CATL",
        "refrigeracion": "Líquida activa con bomba de calor CleanZone",
        "voltaje": "400V",
        "anio": 2023
    },
    "volvo-xc40-recharge": {
        "tipo": "NMC (Níquel Manganeso Cobalto)",
        "quimica": "NMC 811 celdas en módulo estanco",
        "fabricante": "LG Energy Solution / CATL",
        "refrigeracion": "Líquida con bomba de calor",
        "voltaje": "400V",
        "anio": 2020
    },
    "volvo-c40-recharge": {
        "tipo": "NMC (Níquel Manganeso Cobalto)",
        "quimica": "NMC 811 celdas modulares",
        "fabricante": "LG Energy Solution / CATL",
        "refrigeracion": "Líquida con bomba de calor",
        "voltaje": "400V",
        "anio": 2021
    },
    # Chevrolet
    "chevrolet-equinox-ev": {
        "tipo": "NCMA (Níquel Cobalto Manganeso Aluminio) Ultium",
        "quimica": "NCMA de bajo cobalto con química avanzada de alta energía",
        "fabricante": "Ultium Cells LLC (General Motors & LG Energy Solution)",
        "refrigeracion": "Líquida modular patentada Ultium con placas térmicas planas",
        "voltaje": "400V arquitectura Ultium",
        "anio": 2024
    },
    "chevrolet-blazer-ev": {
        "tipo": "NCMA (Níquel Cobalto Manganeso Aluminio) Ultium",
        "quimica": "NCMA celdas tipo pouch de gran formato",
        "fabricante": "Ultium Cells LLC (General Motors & LG Energy Solution)",
        "refrigeracion": "Líquida activa Ultium con gestión térmica inteligente",
        "voltaje": "400V (permite recarga DC hasta 190 kW)",
        "anio": 2024
    },
    "chevrolet-bolt-euv": {
        "tipo": "NCM (Níquel Cobalto Manganeso)",
        "quimica": "NMC 622 celdas tipo bolsa",
        "fabricante": "LG Energy Solution",
        "refrigeracion": "Líquida con etilenglicol",
        "voltaje": "350V",
        "anio": 2021
    },
    "chevrolet-spark-euv": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas compactas",
        "fabricante": "SAIC-GM-Wuling",
        "refrigeracion": "Gestión térmica por líquido",
        "voltaje": "320V",
        "anio": 2023
    },
    # Geely
    "geely-geometry-c": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Ternaria",
        "quimica": "NMC 523 celdas prismáticas CATL",
        "fabricante": "CATL (Contemporary Amperex Technology)",
        "refrigeracion": "Líquida con sistema ITCS 3.0",
        "voltaje": "380V",
        "anio": 2021
    },
    "geely-geometry-e": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas seguras",
        "fabricante": "Gotion High-Tech / CATL",
        "refrigeracion": "Líquida activa",
        "voltaje": "320V",
        "anio": 2022
    },
    "geely-ex5": {
        "tipo": "Short Blade LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas Short Blade de nueva generación",
        "fabricante": "Geely Aegis / SVOLT",
        "refrigeracion": "Líquida con bomba de calor y protección contra impactos",
        "voltaje": "400V arquitectura GEA",
        "anio": 2024
    },
    # Renault
    "renault-kwid-e-tech": {
        "tipo": "LFP / Iones de Litio Ternario Compacto",
        "quimica": "NMC celdas modulares compactas",
        "fabricante": "Svolt Energy / Sunwoda",
        "refrigeracion": "Refrigeración por aire forzado con ventilador térmico",
        "voltaje": "240V",
        "anio": 2022
    },
    "renault-megane-e-tech": {
        "tipo": "NMC (Níquel Manganeso Cobalto) Ultraplana",
        "quimica": "NMC 811 celdas LG de tan solo 11 cm de espesor",
        "fabricante": "LG Energy Solution (Plataforma CMF-EV)",
        "refrigeracion": "Líquida con circuito ultrafino integrado",
        "voltaje": "400V nominal",
        "anio": 2022
    },
    # Nissan
    "nissan-leaf": {
        "tipo": "Iones de Litio Manganeso",
        "quimica": "LMO/NMC celdas laminadas",
        "fabricante": "Envision AESC",
        "refrigeracion": "Refrigeración pasiva por aire",
        "voltaje": "350V",
        "anio": 2018
    },
    "nissan-ariya": {
        "tipo": "NMC (Níquel Manganeso Cobalto)",
        "quimica": "NMC prismática de alta capacidad",
        "fabricante": "CATL / Prime Planet Energy",
        "refrigeracion": "Líquida con preacondicionamiento térmico",
        "voltaje": "352V - 400V",
        "anio": 2022
    },
    # Hyundai & Kia (800V E-GMP)
    "hyundai-ioniq-5": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Arquitectura 800V",
        "quimica": "NMC 811 celdas tipo bolsa E-GMP",
        "fabricante": "SK On / LG Energy Solution",
        "refrigeracion": "Líquida con aceite dieléctrico en circuito de alta disipación",
        "voltaje": "800V Ultra-High Voltage (10% a 80% en 18 min)",
        "anio": 2021
    },
    "hyundai-kona-ev": {
        "tipo": "NCM (Níquel Cobalto Manganeso)",
        "quimica": "NMC 622 celdas prismáticas",
        "fabricante": "CATL / LG Energy Solution",
        "refrigeracion": "Líquida con bomba de calor y calentador de batería",
        "voltaje": "392V",
        "anio": 2023
    },
    "kia-ev6": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Arquitectura 800V",
        "quimica": "NMC 811 celdas E-GMP",
        "fabricante": "SK On",
        "refrigeracion": "Líquida avanzada con bomba de calor",
        "voltaje": "800V Ultra-High Voltage (permite carga DC a 240 kW)",
        "anio": 2021
    },
    "kia-ev9": {
        "tipo": "NCM (Níquel Cobalto Manganeso) 99.8 kWh 800V",
        "quimica": "NMC 9/0.5/0.5 de 4ta generación",
        "fabricante": "SK On / Hyundai Mobis",
        "refrigeracion": "Líquida de caudal variable con gestión inteligente",
        "voltaje": "800V Ultra-High Voltage",
        "anio": 2023
    },
    # BMW
    "bmw-ix1": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Gen5",
        "quimica": "NMC 811 prismática BMW eDrive de quinta generación",
        "fabricante": "CATL / Samsung SDI",
        "refrigeracion": "Líquida con climatización integral del habitáculo y batería",
        "voltaje": "286V - 400V",
        "anio": 2022
    },
    "bmw-i4": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Gen5",
        "quimica": "NMC 811 de alta densidad volumétrica (110 mm de altura)",
        "fabricante": "CATL / Samsung SDI",
        "refrigeracion": "Líquida con preacondicionamiento térmico para carga rápida",
        "voltaje": "400V nominal",
        "anio": 2021
    },
    # Audi
    "audi-q4-e-tron": {
        "tipo": "NMC (Níquel Manganeso Cobalto) Plataforma MEB",
        "quimica": "NMC 712 / 811 celdas tipo bolsa",
        "fabricante": "LG Energy Solution / CATL",
        "refrigeracion": "Líquida con placa base de disipación de aluminio",
        "voltaje": "400V",
        "anio": 2021
    },
    # Mercedes-Benz
    "mercedes-eqa": {
        "tipo": "NCM (Níquel Cobalto Manganeso) Mercedes-EQ",
        "quimica": "NMC celdas en paquete de doble nivel",
        "fabricante": "Accumotive / CATL",
        "refrigeracion": "Líquida con refrigerante de circuito cerrado",
        "voltaje": "420V",
        "anio": 2021
    },
    # Zeekr
    "zeekr-001": {
        "tipo": "Qilin NCM / Golden Battery LFP Arquitectura 800V",
        "quimica": "CATL Qilin CTP 3.0 / LFP estructural",
        "fabricante": "CATL / VREMT (Geely Group)",
        "refrigeracion": "Líquida de superficie completa entre celdas (x4 disipación)",
        "voltaje": "800V Ultra-High Voltage",
        "anio": 2021
    },
    "zeekr-x": {
        "tipo": "NMC (Níquel Manganeso Cobalto) Plataforma SEA",
        "quimica": "NMC 66 kWh celdas prismáticas",
        "fabricante": "CATL / CALB",
        "refrigeracion": "Líquida con bomba de calor y gestión climática extrema",
        "voltaje": "400V",
        "anio": 2023
    },
    # Chery & Omoda
    "chery-eq1": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas compactas urbanas",
        "fabricante": "Guoxuan High-Tech / CATL",
        "refrigeracion": "Líquida",
        "voltaje": "320V",
        "anio": 2017
    },
    "omoda-e5": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas prismáticas de alta estabilidad",
        "fabricante": "CATL (Contemporary Amperex Technology)",
        "refrigeracion": "Líquida con bomba de calor",
        "voltaje": "400V",
        "anio": 2023
    },
    # GWM ORA
    "gwm-ora-03": {
        "tipo": "LFP / NCM (según versión 48 kWh / 63 kWh)",
        "quimica": "LiFePO4 / NMC celdas SVOLT",
        "fabricante": "SVOLT Energy Technology (GWM Group)",
        "refrigeracion": "Líquida inteligente",
        "voltaje": "400V",
        "anio": 2021
    },
    # JAC
    "jac-e-js1": {
        "tipo": "LFP (Fosfato de Hierro y Litio) Célula Segura",
        "quimica": "LiFePO4 celdas en panal de abeja (Honeycomb)",
        "fabricante": "Guoxuan High-Tech (Volkswagen-Gotion)",
        "refrigeracion": "Líquida con gestión térmica integrada",
        "voltaje": "330V",
        "anio": 2021
    },
    "jac-e-js4": {
        "tipo": "LFP (Fosfato de Hierro y Litio)",
        "quimica": "LiFePO4 celdas prismáticas",
        "fabricante": "Guoxuan High-Tech / CATL",
        "refrigeracion": "Líquida activa",
        "voltaje": "380V",
        "anio": 2021
    },
    # Motos y Scooters
    "niu-nqi-gt": {
        "tipo": "Iones de Litio 18650 Extraíbles (Pack Dual)",
        "quimica": "NMC celdas cilíndricas 18650 de alta descarga",
        "fabricante": "Panasonic / EVE Energy",
        "refrigeracion": "Pasiva en carcasa de aluminio estanca IP67",
        "voltaje": "60V nominal (Dual Pack = 120V combinable)",
        "anio": 2020
    },
    "super-soco-tc-max": {
        "tipo": "Iones de Litio de Alta Capacidad Extraíble",
        "quimica": "NMC celdas en módulo cilíndrico",
        "fabricante": "ATL (Amperex Technology Limited)",
        "refrigeracion": "Disipación pasiva por carcasa de aleación",
        "voltaje": "72V 45Ah",
        "anio": 2020
    },
    "sunra-robo-s": {
        "tipo": "Litio-Ion Extraíble Dual (2 x 72V 20Ah)",
        "quimica": "Celdas de litio de ciclo profundo",
        "fabricante": "Sunra Micro Power",
        "refrigeracion": "Aire / disipación sellada",
        "voltaje": "72V",
        "anio": 2021
    },
    "yadea-g5-pro": {
        "tipo": "Iones de Litio Panasonic 18650 Extraíble",
        "quimica": "NMC celdas cilíndricas de grado automotriz",
        "fabricante": "Panasonic",
        "refrigeracion": "Carcasa sellada de magnesio y aluminio",
        "voltaje": "60V 32Ah",
        "anio": 2020
    },
    # E-Bikes
    "xiaomi-himo-z20": {
        "tipo": "Iones de Litio Oculta en Cuadro Extraíble con Llave",
        "quimica": "Celdas cilíndricas de litio 18650",
        "fabricante": "Shanghai Himo Electric / EVE Energy",
        "refrigeracion": "Pasiva protegida dentro del tubo principal de aluminio",
        "voltaje": "36V 10Ah (360 Wh con BMS inteligente)",
        "anio": 2020
    },
    "voltbike-classica": {
        "tipo": "Batería de Litio Extraíble con Cerradura de Seguridad",
        "quimica": "Celdas de ion de litio de alta densidad",
        "fabricante": "VoltBike UY / DLG Power",
        "refrigeracion": "Pasiva montada sobre portaequipajes trasero",
        "voltaje": "36V 10.4Ah (374 Wh)",
        "anio": 2022
    },
    "voltbike-flex-foldable": {
        "tipo": "Batería de Litio Extraíble Integrada en Cuadro Plegable",
        "quimica": "Celdas de ion de litio 18650",
        "fabricante": "VoltBike UY / Samsung SDI celdas",
        "refrigeracion": "Pasiva estanca en bisagra de cuadro",
        "voltaje": "36V 10Ah (360 Wh)",
        "anio": 2022
    },
    "voltbike-pioneer": {
        "tipo": "Batería de Litio Fat Bike de Gran Capacidad",
        "quimica": "Celdas de ion de litio 18650 para alta descarga",
        "fabricante": "VoltBike UY / LG Energy Solution celdas",
        "refrigeracion": "Pasiva en tubo diagonal con indicador LED de nivel",
        "voltaje": "48V 14Ah (672 Wh)",
        "anio": 2023
    },
    "specialized-turbo-vado-4": {
        "tipo": "Specialized U2 Custom Li-ion Integrada",
        "quimica": "Celdas de litio de grado premium con conectividad ANT+/BLE",
        "fabricante": "Specialized Bicycles / BMZ Group",
        "refrigeracion": "Pasiva estanca IPX6 en tubo diagonal",
        "voltaje": "36V (710 Wh)",
        "anio": 2022
    },
    "trek-allant-plus-7": {
        "tipo": "Bosch PowerTube Li-ion Integrada (RIB System)",
        "quimica": "Celdas de litio automotriz de alta durabilidad Bosch",
        "fabricante": "Robert Bosch GmbH",
        "refrigeracion": "Pasiva protegida contra polvo y agua IP54",
        "voltaje": "36V (500 Wh / 625 Wh)",
        "anio": 2021
    },
    "decathlon-riverside-500e": {
        "tipo": "Litio-Ion Extraíble sobre Tubo Diagonal",
        "quimica": "Celdas LG / Samsung 18650",
        "fabricante": "Decathlon B'Twin Power",
        "refrigeracion": "Pasiva",
        "voltaje": "36V (418 Wh)",
        "anio": 2021
    }
}

def obtener_regla(vid, marca, modelo, tipo):
    vid_l = vid.lower()
    marca_l = marca.lower()
    modelo_l = modelo.lower()

    for k, v in BATTERY_AND_YEAR_RULES.items():
        if k in vid_l:
            return v

    # Reglas generales por marca / química
    if "byd" in marca_l:
        return {
            "tipo": "LFP (Fosfato de Hierro y Litio) Blade Battery",
            "quimica": "LiFePO4 celdas Blade estructurales",
            "fabricante": "BYD FinDreams Battery (Blade)",
            "refrigeracion": "Líquida activa inteligente con bomba de calor",
            "voltaje": "400V (e-Platform 3.0)",
            "anio": 2022
        }
    elif "farizon" in marca_l:
        return {
            "tipo": "LFP (Fosfato de Hierro y Litio) Comercial",
            "quimica": "LiFePO4 prismática de alta durabilidad (+3000 ciclos)",
            "fabricante": "CATL / EVE Energy",
            "refrigeracion": "Líquida activa reforzada para servicio pesado",
            "voltaje": "400V - 540V DC",
            "anio": 2023
        }
    elif "tesla" in marca_l:
        return {
            "tipo": "LFP / NCM Ternaria (según variante RWD o AWD)",
            "quimica": "CATL LiFePO4 (RWD) / LG-Panasonic NMC 2170 (AWD)",
            "fabricante": "CATL / LG Energy Solution / Panasonic",
            "refrigeracion": "Líquida patentada Tesla Octovalve con bomba de calor",
            "voltaje": "400V nominal",
            "anio": 2023
        }
    elif "volvo" in marca_l:
        return {
            "tipo": "NMC / LFP (según versión Core o Plus/Ultra)",
            "quimica": "NMC 811 celdas de alta densidad CATL/CALB",
            "fabricante": "CATL / CALB / LG Energy Solution",
            "refrigeracion": "Líquida con gestión térmica CleanZone",
            "voltaje": "400V",
            "anio": 2023
        }
    elif "chevrolet" in marca_l:
        return {
            "tipo": "NCMA (Níquel Cobalto Manganeso Aluminio) Ultium",
            "quimica": "NCMA celdas tipo pouch de bajo contenido en cobalto",
            "fabricante": "Ultium Cells LLC (General Motors & LG)",
            "refrigeracion": "Líquida modular patentada Ultium",
            "voltaje": "400V",
            "anio": 2023
        }
    elif "geely" in marca_l:
        return {
            "tipo": "Short Blade LFP / NCM Ternaria",
            "quimica": "LiFePO4 / NMC celdas seguras",
            "fabricante": "SVOLT / CATL",
            "refrigeracion": "Líquida activa",
            "voltaje": "400V",
            "anio": 2023
        }
    elif "audi" in marca_l or "bmw" in marca_l or "mercedes" in marca_l:
        return {
            "tipo": "NCM (Níquel Cobalto Manganeso) Grado Premium",
            "quimica": "NMC 811 celdas prismáticas de alta capacidad",
            "fabricante": "CATL / Samsung SDI / LG Energy Solution",
            "refrigeracion": "Líquida de alto caudal con climatización reversible",
            "voltaje": "400V - 800V",
            "anio": 2022
        }
    elif "hyundai" in marca_l or "kia" in marca_l:
        return {
            "tipo": "NCM (Níquel Cobalto Manganeso) Plataforma E-GMP",
            "quimica": "NMC 811 celdas pouch de alta densidad",
            "fabricante": "SK On / LG Energy Solution",
            "refrigeracion": "Líquida avanzada con gestión térmica activa",
            "voltaje": "800V Ultra-High Voltage",
            "anio": 2022
        }
    elif tipo == "bicicleta":
        return {
            "tipo": "Iones de Litio Extraíble con Cerradura de Seguridad",
            "quimica": "Celdas cilíndricas 18650 / 21700 de litio",
            "fabricante": "Celdas de grado automotriz Samsung / LG / DLG",
            "refrigeracion": "Disipación pasiva protegida en cuadro estanco",
            "voltaje": "36V - 48V",
            "anio": 2022
        }
    elif tipo == "moto":
        return {
            "tipo": "Iones de Litio / Grafeno Extraíble",
            "quimica": "NMC / LFP de alta descarga",
            "fabricante": "Panasonic / EVE Energy / Sunra",
            "refrigeracion": "Disipación pasiva estanca IP67",
            "voltaje": "60V - 72V",
            "anio": 2021
        }
    elif tipo == "triciclo":
        return {
            "tipo": "Plomo-Ácido Gel Sellado / Litio LFP de Tracción",
            "quimica": "Gel Silicio / LiFePO4 de ciclo profundo para carga pesada",
            "fabricante": "Chilwee / Tianneng / EVE",
            "refrigeracion": "Pasiva en compartimento reforzado de carga",
            "voltaje": "60V - 72V",
            "anio": 2022
        }
    else:
        return {
            "tipo": "LFP / NCM (Fosfato de Hierro y Litio o Ternaria)",
            "quimica": "LiFePO4 / NMC celdas automotrices",
            "fabricante": "CATL / Gotion / BYD",
            "refrigeracion": "Líquida activa",
            "voltaje": "400V nominal",
            "anio": 2022
        }

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Asegurar columnas nuevas en la tabla vehicles
    cursor.execute("PRAGMA table_info(vehicles)")
    columnas_actuales = [c[1] for c in cursor.fetchall()]

    nuevas_columnas = [
        ("bateria_tipo", "TEXT"),
        ("bateria_quimica", "TEXT"),
        ("bateria_fabricante", "TEXT"),
        ("bateria_refrigeracion", "TEXT"),
        ("bateria_voltaje", "TEXT"),
        ("anio_origen", "INTEGER")
    ]

    for col_name, col_type in nuevas_columnas:
        if col_name not in columnas_actuales:
            cursor.execute(f"ALTER TABLE vehicles ADD COLUMN {col_name} {col_type}")
            print(f"Columna añadida: {col_name} ({col_type})")

    # 2. Consultar todos los vehículos y enriquecer datos
    cursor.execute("SELECT id, marca, modelo, version, tipo, especificaciones_json FROM vehicles")
    vehiculos = cursor.fetchall()

    print(f"\nEnriqueciendo datos técnicos para {len(vehiculos)} vehículos...")

    for vid, marca, modelo, version, tipo, specs_json_str in vehiculos:
        regla = obtener_regla(vid, marca, modelo, tipo)
        
        # Parsear especificaciones_json existentes y enriquecerlas
        try:
            specs = json.loads(specs_json_str or "{}")
        except Exception:
            specs = {}

        specs["tipo_bateria"] = regla["tipo"]
        specs["quimica_bateria"] = regla["quimica"]
        specs["fabricante_bateria"] = regla["fabricante"]
        specs["refrigeracion_bateria"] = regla["refrigeracion"]
        specs["voltaje_arquitectura"] = regla["voltaje"]
        specs["anio_origen"] = regla["anio"]

        nuevo_specs_json = json.dumps(specs, ensure_ascii=False)

        cursor.execute("""
            UPDATE vehicles
            SET bateria_tipo = ?,
                bateria_quimica = ?,
                bateria_fabricante = ?,
                bateria_refrigeracion = ?,
                bateria_voltaje = ?,
                anio_origen = ?,
                especificaciones_json = ?
            WHERE id = ?
        """, (
            regla["tipo"],
            regla["quimica"],
            regla["fabricante"],
            regla["refrigeracion"],
            regla["voltaje"],
            regla["anio"],
            nuevo_specs_json,
            vid
        ))

    conn.commit()
    conn.close()
    print("[OK] Base de datos enriquecida al 100% con química, fabricante de batería y año de origen.")

if __name__ == "__main__":
    main()
