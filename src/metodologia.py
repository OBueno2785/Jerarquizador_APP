# -*- coding: utf-8 -*-
"""Parámetros de la metodología de priorización de APP del Gobierno Nacional.

Fuente: Resolución Directoral N° 002-2026-EF/68.01 y sus Anexos 1 a 6
(MEF - DGPPIP, 08/07/2026).
"""

PESO_BLOQUE_FIJO = 0.85
PESO_BLOQUE_OPCIONAL = 0.15
PERCENTIL_CORTE = 70

INDICADORES = {
    1: {"nombre": "Inclusión del proyecto en el portafolio priorizado del PNI vigente",
        "criterio": "Inclusión en el Plan Nacional de Infraestructura",
        "dimension": "Sostenibilidad institucional",
        "peso": 0.07, "bloque": "fijo", "escala": (0, 1),
         "escala_txt": "0 o 1", "fuente": "Documento oficial del Plan Nacional de Infraestructura"},
    2: {"nombre": "Capacidad preliminar del proyecto para generar ingresos para asumir compromisos",
        "criterio": "Capacidad de generar ingresos",
        "dimension": "Sostenibilidad económica y financiera",
        "peso": 0.16, "bloque": "fijo", "escala": (1, 3),
         "escala_txt": "1 a 3", "fuente": "Estudios y toda información disponible al momento de la evaluación"},
    3: {"nombre": "Nivel de pobreza en el ámbito del proyecto",
        "criterio": "Impacto socioeconómico",
        "dimension": "Sostenibilidad social",
        "peso": 0.09, "bloque": "fijo", "escala": (1, 6),
         "escala_txt": "1 a 6", "fuente": "INEI · Mapa de pobreza monetaria provincial, 2018"},
    4: {"nombre": "Población directamente beneficiada por el proyecto",
        "criterio": "Impacto socioeconómico",
        "dimension": "Sostenibilidad social",
        "peso": 0.10, "bloque": "fijo", "escala": (1, 10),
         "escala_txt": "1 a 10", "fuente": "Estudios y toda información disponible al momento de la evaluación"},
    5: {"nombre": "Monto de inversión del proyecto",
        "criterio": "Proyectos con enfoque territorial",
        "dimension": "Sostenibilidad económica y financiera",
        "peso": 0.12, "bloque": "fijo", "escala": (1, 7),
         "escala_txt": "1 a 7", "fuente": "Estudios y toda información disponible al momento de la evaluación"},
    6: {"nombre": "Impulso territorial del proyecto",
        "criterio": "Proyectos con enfoque territorial",
        "dimension": "Sostenibilidad económica y financiera",
        "peso": 0.09, "bloque": "fijo", "escala": None,
         "escala_txt": "variable según macrozona", "fuente": "Tabla 11 y tabla 9 del PNI 2026-2031 · Anexo 4 del Lineamiento"},
    7: {"nombre": "Nivel de transferencia de riesgos al sector privado",
        "criterio": "Capacidad de transferencia de riesgos",
        "dimension": "Sostenibilidad económica y financiera",
        "peso": 0.12, "bloque": "fijo", "escala": (1, 3),
         "escala_txt": "1 a 3", "fuente": "Estudios y toda información disponible al momento de la evaluación"},
    8: {"nombre": "Nivel de avance de los estudios de ingeniería del proyecto",
        "criterio": "Nivel de avance de estudios",
        "dimension": "Sostenibilidad institucional",
        "peso": 0.10, "bloque": "fijo", "escala": (1, 4),
         "escala_txt": "1 a 4", "fuente": "Estudios disponibles al momento de la evaluación"},
    9: {"nombre": "Proporción del proyecto frente a la brecha de infraestructura",
        "criterio": "Cierre de brechas de infraestructura y/o servicios públicos",
        "dimension": "Sostenibilidad económica y financiera",
        "peso": 0.075, "bloque": "opcional", "escala": (1, 8),
         "escala_txt": "1 a 8", "fuente": "PNIC 2019 o actualizaciones posteriores"},
    10: {"nombre": "Declaración de viabilidad del proyecto",
         "criterio": "Viabilidad del proyecto",
         "dimension": "Sostenibilidad institucional",
         "peso": 0.075, "bloque": "opcional", "escala": (1, 2),
         "escala_txt": "1 a 2", "fuente": "Consulta pública del Banco de Inversiones del MEF"},
}

ESCALA_IND2 = [("Cofinanciada total", 1), ("Cofinanciada parcial", 2), ("Autofinanciada", 3)]

# Rangos de tasa de pobreza monetaria provincial (INEI 2018; P10/P25/P50/P75/P90)
RANGOS_IND3 = [(12.00, 1), (21.91, 2), (33.06, 3), (43.81, 4), (50.31, 5), (float("inf"), 6)]

RANGOS_IND4 = [(1000, 1), (8000, 2), (13000, 3), (27000, 4), (62000, 5),
               (120000, 6), (290000, 7), (500000, 8), (1200000, 9), (float("inf"), 10)]

# CTI o CTP expresado en UIT
RANGOS_IND5 = [(7000, 1), (10000, 2), (15000, 3), (40000, 4), (80000, 5),
               (300000, 6), (float("inf"), 7)]

ESCALA_IND7 = [("Baja o nula", 1), ("Mediana", 2), ("Alta", 3)]

ESCALA_IND8_ING = [("Visualización", 1), ("Ingeniería conceptual", 2),
                   ("Ingeniería básica", 3), ("Ingeniería básica extendida", 4)]
ESCALA_IND8_OYM = [("Sin documentación técnica necesaria", 1),
                   ("Con documentación técnica necesaria", 4)]

RANGOS_IND9 = [(0.05, 1), (0.10, 2), (0.25, 3), (0.50, 4), (1.00, 5),
               (3.00, 6), (5.00, 7), (float("inf"), 8)]

ESCALA_IND10 = [("Sin declaratoria de viabilidad vigente", 1),
                ("Con declaratoria de viabilidad vigente", 2)]

ACTIVIDADES = ["AGRICOLA", "PECUARIO", "MINERO", "PESCA", "TURISMO",
               "LOGISTICO", "ENERGETICO", "FORESTAL", "MANUFACTURA", "INFRA_SOCIAL"]

# Anexo 5: actividades con potencial consolidado por macrozona (PNI 2026-2031, tabla 11)
ANEXO5 = {
    "MN":  [1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
    "MS":  [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    "MC":  [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    "MLC": [0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
}
MACROZONAS = {"MN": "Macrozona Norte", "MS": "Macrozona Sur",
              "MC": "Macrozona Centro", "MLC": "Macrozona Lima-Callao"}

# Rango fijo de normalización del indicador 6 (ficha del Anexo 2)
RANGO_IND6 = {"MN": (6, 12), "MS": (5, 10), "MC": (4, 8), "MLC": (5, 10)}

# Anexo 6: asignación de departamentos por macrozona
ANEXO6 = {
    "MN": ["TUMBES", "PIURA", "LAMBAYEQUE", "LA LIBERTAD", "CAJAMARCA", "AMAZONAS",
           "SAN MARTIN", "LORETO"],
    "MC": ["ANCASH", "HUANUCO", "UCAYALI", "PASCO", "JUNIN"],
    "MLC": ["LIMA", "CALLAO"],
    "MS": ["ICA", "HUANCAVELICA", "AYACUCHO", "AREQUIPA", "MOQUEGUA", "TACNA",
           "CUSCO", "APURIMAC", "MADRE DE DIOS", "PUNO"],
}

# Anexo 4: matriz de contribución sector/subsector x actividad (2 = directo, 1 = indirecto)
ANEXO4 = {
    ("Agua y Saneamiento", "Urbano"):                  [1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
    ("Agua y Saneamiento", "Rural"):                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Electricidad", "Generación"):                    [1, 1, 2, 1, 1, 1, 2, 1, 2, 2],
    ("Electricidad", "Transmisión y Sub-Transmisión"): [1, 1, 2, 1, 1, 1, 2, 1, 2, 2],
    ("Electricidad", "Distribución"):                  [1, 1, 1, 1, 1, 1, 2, 1, 2, 2],
    ("Comunicaciones", "Móvil"):                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Comunicaciones", "Banda ancha"):                 [1, 1, 1, 1, 1, 2, 1, 1, 2, 2],
    ("Transportes", "Ferrocarriles/líneas de metro"):  [1, 1, 2, 1, 1, 2, 1, 1, 2, 2],
    ("Transportes", "Carreteras"):                     [2, 2, 2, 2, 2, 2, 1, 2, 2, 2],
    ("Transportes", "Aeropuertos"):                    [1, 1, 1, 1, 2, 2, 1, 1, 1, 1],
    ("Transportes", "Puertos"):                        [1, 1, 2, 2, 1, 2, 1, 1, 2, 1],
    ("Transportes", "Vías Navegables"):                [1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
    ("Educación", "Inicial"):                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Educación", "Primaria"):                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Educación", "Secundaria"):                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Salud", "Primer nivel de atención"):             [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Salud", "Segundo nivel de atención"):            [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Salud", "Tercer nivel de atención"):             [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Agricultura y Riego", "Infraestructura de Riego"): [2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ("Producción", "Parques Industriales"):            [1, 1, 1, 1, 1, 2, 1, 1, 2, 1],
    ("Hidrocarburos", "Almacenamiento"):               [1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    ("Hidrocarburos", "Transporte"):                   [1, 1, 1, 1, 1, 2, 2, 1, 1, 1],
    ("Ambiente", "Limpieza Pública"):                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Ambiente", "Residuos Sólidos"):                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Turismo", "Turismo"):                            [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    ("Cultura", "Cultura"):                            [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    ("General", "Otros"):                              [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    ("Defensa", "Defensa"):                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
}

# Mapeo de la "Cartera" de ProInversión al par sector/subsector del Anexo 4
CARTERA_A_ANEXO4 = {
    "Vial": ("Transportes", "Carreteras"),
    "Puertos": ("Transportes", "Puertos"),
    "Aeropuertos": ("Transportes", "Aeropuertos"),
    "Ferroviario": ("Transportes", "Ferrocarriles/líneas de metro"),
    "Vías Navegables": ("Transportes", "Vías Navegables"),
    "Agua y saneamiento": ("Agua y Saneamiento", "Urbano"),
    "Salud": ("Salud", "Segundo nivel de atención"),
    "Educación": ("Educación", "Secundaria"),
    "Irrigación": ("Agricultura y Riego", "Infraestructura de Riego"),
    "Teleféricos": ("Turismo", "Turismo"),
    "Hidrocarburos": ("Hidrocarburos", "Transporte"),
    "Tecnología": ("General", "Otros"),
    "Generación eléctrica": ("Electricidad", "Generación"),
    "Transmisión eléctrica": ("Electricidad", "Transmisión y Sub-Transmisión"),
    "Telecomunicaciones": ("Comunicaciones", "Banda ancha"),
    "Inmuebles estatales": ("General", "Otros"),
    "Inmuebles": ("General", "Otros"),
}

# Nombres para presentación (las claves internas van sin tilde y en mayúsculas)
DEPARTAMENTOS_NOMBRE = {
    "TUMBES": "Tumbes", "PIURA": "Piura", "LAMBAYEQUE": "Lambayeque",
    "LA LIBERTAD": "La Libertad", "CAJAMARCA": "Cajamarca", "AMAZONAS": "Amazonas",
    "SAN MARTIN": "San Martín", "LORETO": "Loreto", "ANCASH": "Áncash",
    "HUANUCO": "Huánuco", "UCAYALI": "Ucayali", "PASCO": "Pasco", "JUNIN": "Junín",
    "LIMA": "Lima", "CALLAO": "Callao", "ICA": "Ica", "HUANCAVELICA": "Huancavelica",
    "AYACUCHO": "Ayacucho", "AREQUIPA": "Arequipa", "MOQUEGUA": "Moquegua",
    "TACNA": "Tacna", "CUSCO": "Cusco", "APURIMAC": "Apurímac",
    "MADRE DE DIOS": "Madre de Dios", "PUNO": "Puno",
}

ACTIVIDADES_NOMBRE = {
    "AGRICOLA": "Agrícola", "PECUARIO": "Pecuario", "MINERO": "Minero", "PESCA": "Pesca",
    "TURISMO": "Turismo", "LOGISTICO": "Logístico", "ENERGETICO": "Energético",
    "FORESTAL": "Forestal", "MANUFACTURA": "Manufactura", "INFRA_SOCIAL": "Infraestructura social",
}

UIT_2026 = 5500.0  # DS 301-2025-EF


def puntaje_por_rango(valor, rangos):
    """Puntaje interno según una tabla de rangos [(límite_superior, puntaje)]."""
    if valor is None:
        return None
    for limite, puntaje in rangos:
        if valor <= limite:
            return puntaje
    return rangos[-1][1]


def normalizar(puntaje, minimo, maximo):
    """Normalización de rango fijo: v = (P - Pmin) / (Pmax - Pmin)."""
    if puntaje is None:
        return None
    if maximo == minimo:
        return 0.0
    return (float(puntaje) - minimo) / (maximo - minimo)


def puntaje_ind6(macrozona, contribucion):
    """Impulso territorial: suma de C_i (macrozona) x S_i (sector) sobre las 10 actividades."""
    return sum(c * s for c, s in zip(ANEXO5[macrozona], contribucion))
