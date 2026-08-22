# -*- coding: utf-8 -*-
"""Construye el dataset de proyectos APP a partir del portafolio de ProInversión
y de las fuentes oficiales referenciadas por la RD 002-2026-EF/68.01.

Salida: salidas/proyectos.json
"""
import json
import os
import re
import unicodedata

import metodologia as M

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RAIZ, "data")
SALIDAS = os.path.join(RAIZ, "salidas")

# Proyectos del portafolio priorizado del PNI 2026-2031 (DS 039-2026-EF, tablas 24 a 27)
# identificados dentro del portafolio APP de ProInversión.
PNI_2026_2031 = {
    "PTAR Trujillo": "PTAR Trujillo y Chepén (Tabla 24, N.° 5)",
    "Nuevos terminales Portuarios de Loreto": "Nuevo TP Loreto - Saramiriza e Iquitos (Tabla 24, N.° 18)",
    "Vía de Evitamiento de Cusco": "Vía de Evitamiento de la Ciudad Cusco (Tabla 25, N.° 3)",
    "Terminal Internacional de Chimbote": "TP Internacional Chimbote (Tabla 26, N.° 4)",
    "Nuevo Terminal Portuario Pucallpa": "TP Pucallpa (Tabla 26, N.° 5)",
    "Tercer Grupo de Aeropuertos": "Tercer Grupo de Aeropuertos (Tabla 26, N.° 7)",
    "PTAR Huancayo": "PTAR Huancayo (Tabla 26, N.° 8)",
    "Majes Siguas - II Etapa": "Majes Siguas II, Arequipa (Tabla 25, N.° 2 - modalidad G2G)",
    "Proyecto Chavimochic - Tercera Etapa": "Chavimochic III (Tabla 24, N.° 2 - modalidad G2G)",
}

POBLACION_NACIONAL = 32625948  # INEI, proyección 2020 (suma departamental)


def sinacento(s):
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").upper().strip()


DEPTO_A_MACROZONA = {}
for mz, deptos in M.ANEXO6.items():
    for d in deptos:
        DEPTO_A_MACROZONA[sinacento(d)] = mz
DEPTO_A_MACROZONA["PROVINCIA CONSTITUCIONAL DEL CALLAO"] = "MLC"


def parse_ambito(ambito):
    """Devuelve la lista de departamentos normalizados del ámbito del proyecto."""
    if not ambito:
        return []
    partes = [sinacento(p) for p in re.split(r"[,/]", ambito) if p.strip()]
    out = []
    for p in partes:
        if "AMBITO NACIONAL" in p:
            out.append("AMBITO NACIONAL")
        elif p in DEPTO_A_MACROZONA:
            out.append(p)
        else:
            out.append(p)
    return out


def macrozonas_de(deptos):
    if "AMBITO NACIONAL" in deptos:
        return ["MN", "MC", "MLC", "MS"]
    mz = []
    for d in deptos:
        m = DEPTO_A_MACROZONA.get(d)
        if m and m not in mz:
            mz.append(m)
    return mz


def cargar_portafolio():
    proyectos = []
    for archivo, fase in [("portafolio_formulacion.json", "Formulación"),
                          ("portafolio_estructuracion.json", "Estructuración")]:
        with open(os.path.join(DATA, archivo), encoding="utf-8") as fh:
            for p in json.load(fh)["Data"]:
                p["_fase"] = fase
                proyectos.append(p)
    return proyectos


def main():
    pobreza = json.load(open(os.path.join(DATA, "pobreza_provincial_2018.json"), encoding="utf-8"))
    poblacion = json.load(open(os.path.join(DATA, "poblacion_departamental_2020.json"), encoding="utf-8"))
    poblacion = {sinacento(k): v for k, v in poblacion.items()}

    prov_por_depto = {}
    for ubigeo, r in pobreza.items():
        prov_por_depto.setdefault(sinacento(r["dep"]), []).append(
            {"ubigeo": ubigeo, "provincia": r["prov"], "tasa": r["tasa"]})

    salida = []
    for p in cargar_portafolio():
        deptos = parse_ambito(p["Ambito"])
        mzs = macrozonas_de(deptos)
        cartera = p["Cartera"]
        clave4 = M.CARTERA_A_ANEXO4.get(cartera, ("General", "Otros"))
        contribucion = M.ANEXO4[clave4]

        # --- Indicador 3: pobreza provincial (proxy: máxima provincial del ámbito)
        provincias = []
        for d in deptos:
            provincias.extend(prov_por_depto.get(d, []))
        if "AMBITO NACIONAL" in deptos:
            provincias = [x for v in prov_por_depto.values() for x in v]
        tasa = max((x["tasa"] for x in provincias), default=None)

        # --- Indicador 4: población beneficiada (proxy: población del ámbito)
        if "AMBITO NACIONAL" in deptos:
            pob = POBLACION_NACIONAL
        else:
            pob = sum(poblacion.get(d, 0) for d in deptos) or None

        # --- Indicador 5: CTI/CTP en UIT
        monto_usd = p.get("MontoInversionSIGV") or 0
        try:
            tc = float(p.get("TipoCambio") or 3.40)
        except ValueError:
            tc = 3.40
        cti_soles = monto_usd * 1e6 * tc
        uit = cti_soles / M.UIT_2026 if monto_usd else None

        es_oym = "Operación y Mantenimiento" in (p.get("ModalidadContractual") or "") \
            or sinacento(p["NombreCorto"]).startswith("O&M") \
            or "OPERACION Y MANTENIMIENTO" in sinacento(p["NombreCorto"])

        salida.append({
            "id": p["Id"],
            "slug": p["Slug"],
            "nombre": p["Nombre"],
            "nombre_corto": p["NombreCorto"],
            "sector": p["Sector"],
            "cartera": cartera,
            "fase": p["_fase"],
            "modalidad": p["Modalidad"],
            "iniciativa": p["Iniciativa"],
            "titular": p["Titular"],
            "ambito": p["Ambito"],
            "departamentos": deptos,
            "macrozonas": mzs,
            "macrozona": mzs[0] if len(mzs) == 1 else None,
            "green_brownfield": p["GreenBrownfield"],
            "modalidad_contractual": p["ModalidadContractual"],
            "plazo_anios": p["AnhoConcesion"],
            "monto_usd_mm": monto_usd or None,
            "tipo_cambio": tc,
            "cti_uit": round(uit, 1) if uit else None,
            "anexo4": {"sector": clave4[0], "subsector": clave4[1], "contribucion": contribucion},
            "ficha_pdf": p["FichaPDF"],
            "url": "https://www.investinperu.pe/portafolio-app/detalle/?" + p["Slug"],
            "enunciado": re.sub(r"<[^>]+>", " ", p.get("Enunciado_PrimerParrafo") or "").strip(),
            "es_oym": es_oym,
            "pni": PNI_2026_2031.get(p["NombreCorto"]),
            "tasa_pobreza": tasa,
            "poblacion_ambito": pob,
            "provincias_ambito": sorted(provincias, key=lambda x: -x["tasa"]),
        })

    os.makedirs(SALIDAS, exist_ok=True)
    with open(os.path.join(SALIDAS, "proyectos.json"), "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=1)
    print("proyectos:", len(salida))
    print("en PNI:", sum(1 for x in salida if x["pni"]))
    print("sin monto:", sum(1 for x in salida if not x["monto_usd_mm"]))
    print("sin macrozona única:", sum(1 for x in salida if not x["macrozona"]))


if __name__ == "__main__":
    main()
