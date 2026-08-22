# -*- coding: utf-8 -*-
"""Inyecta los datos y parámetros en la plantilla y genera app/index.html."""
import datetime
import io
import json
import os

import metodologia as M

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INF = 1e18


def limpiar(rangos):
    return [[INF if lim == float("inf") else lim, pt] for lim, pt in rangos]


def main():
    proyectos = json.load(open(os.path.join(RAIZ, "salidas", "proyectos.json"), encoding="utf-8"))
    for p in proyectos:
        p.pop("provincias_ambito_full", None)

    parametros = {
        "indicadores": {str(i): {"nombre": d["nombre"], "criterio": d["criterio"],
                                 "dimension": d["dimension"], "bloque": d["bloque"]}
                        for i, d in M.INDICADORES.items()},
        "pesos": {str(i): d["peso"] for i, d in M.INDICADORES.items()},
        "escalas": {str(i): (d["escala"] or [0, 1]) for i, d in M.INDICADORES.items()},
        "rangos": {"3": limpiar(M.RANGOS_IND3), "4": limpiar(M.RANGOS_IND4),
                   "5": limpiar(M.RANGOS_IND5), "9": limpiar(M.RANGOS_IND9)},
        "escala2": [[t, v] for t, v in M.ESCALA_IND2],
        "escala7": [["Capacidad " + t.lower() + " de transferencia de riesgos", v]
                    for t, v in M.ESCALA_IND7],
        "escala8ing": [[t, v] for t, v in M.ESCALA_IND8_ING],
        "escala8oym": [[t, v] for t, v in M.ESCALA_IND8_OYM],
        "escala10": [[t, v] for t, v in M.ESCALA_IND10],
        "anexo5": M.ANEXO5,
        "rango6": {k: list(v) for k, v in M.RANGO_IND6.items()},
        "macrozonas": M.MACROZONAS,
        "actividades": M.ACTIVIDADES,
        "uit": M.UIT_2026,
        "fecha_datos": datetime.date.today().strftime("%d/%m/%Y"),
    }

    datos = json.dumps({"parametros": parametros, "proyectos": proyectos},
                       ensure_ascii=False, separators=(",", ":"))

    plantilla = io.open(os.path.join(RAIZ, "app", "plantilla.html"), encoding="utf-8").read()
    html = plantilla.replace("/*__DATOS__*/", datos)
    destino = os.path.join(RAIZ, "app", "index.html")
    io.open(destino, "w", encoding="utf-8").write(html)
    print("escrito:", destino, "%.0f KB" % (len(html.encode("utf-8")) / 1024))


if __name__ == "__main__":
    main()
