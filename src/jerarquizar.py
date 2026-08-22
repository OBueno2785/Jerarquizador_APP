# -*- coding: utf-8 -*-
"""Motor de jerarquización de potenciales proyectos APP del Gobierno Nacional.

Implementa la metodología multicriterio de la RD 002-2026-EF/68.01:
calificación por escala interna -> normalización de rango fijo -> ponderación
-> ranking sectorial -> línea de corte en el percentil 70.
"""
import argparse
import csv
import json
import os

import metodologia as M

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDAS = os.path.join(RAIZ, "salidas")

FIJOS = [1, 2, 3, 4, 5, 6, 7, 8]


def calificar(p):
    """Asigna el puntaje interno de cada indicador y el origen del dato.

    origen: 'auto'      -> derivado de fuente oficial sin supuestos adicionales
            'proxy'     -> derivado con un supuesto documentado (revisable)
            'pendiente' -> requiere información que el portafolio público no expone
    """
    c = {}

    c[1] = {"p": 1 if p["pni"] else 0, "origen": "auto",
            "nota": p["pni"] or "No identificado en el portafolio priorizado del PNI 2026-2031"}

    if p["modalidad"] == "Autofinanciada":
        c[2] = {"p": 3, "origen": "auto", "nota": "Autofinanciada"}
    else:
        c[2] = {"p": 1, "origen": "auto",
                "nota": "Cofinanciada; elevar a 2 si se acredita cofinanciamiento parcial"}

    if p["tasa_pobreza"] is not None:
        c[3] = {"p": M.puntaje_por_rango(p["tasa_pobreza"], M.RANGOS_IND3), "origen": "proxy",
                "nota": "Tasa provincial máxima del ámbito: %.2f%% (INEI 2018)" % p["tasa_pobreza"]}
    else:
        c[3] = {"p": 1, "origen": "pendiente", "nota": "Sin provincia identificada"}

    if p["poblacion_ambito"]:
        c[4] = {"p": M.puntaje_por_rango(p["poblacion_ambito"], M.RANGOS_IND4), "origen": "proxy",
                "nota": "Población del ámbito: %s hab. (INEI 2020). Reemplazar por beneficiarios "
                        "directos del estudio" % f"{p['poblacion_ambito']:,}".replace(",", " ")}
    else:
        c[4] = {"p": 1, "origen": "pendiente", "nota": "Sin población de referencia"}

    if p["cti_uit"]:
        c[5] = {"p": M.puntaje_por_rango(p["cti_uit"], M.RANGOS_IND5), "origen": "auto",
                "nota": "CTI/CTP = %s UIT (UIT 2026 = S/ %.0f)"
                        % (f"{p['cti_uit']:,.0f}".replace(",", " "), M.UIT_2026)}
    else:
        c[5] = {"p": 1, "origen": "pendiente", "nota": "Monto de inversión no publicado"}

    c[6] = {"p": None, "origen": "auto", "nota": ""}  # se calcula en normalizar_ind6

    if p["modalidad"] == "Autofinanciada":
        c[7] = {"p": 3, "origen": "proxy", "nota": "Autofinanciada: demanda y financiamiento al privado"}
    else:
        c[7] = {"p": 2, "origen": "proxy", "nota": "Cofinanciada: transferencia media (supuesto)"}

    if p["es_oym"]:
        c[8] = {"p": 4 if p["fase"] == "Estructuración" else 1, "origen": "proxy",
                "nota": "Proyecto de O&M: escala de documentación técnica (1 o 4)"}
    else:
        c[8] = {"p": 3 if p["fase"] == "Estructuración" else 2, "origen": "proxy",
                "nota": "Supuesto por fase: Estructuración = ingeniería básica, "
                        "Formulación = ingeniería conceptual"}

    c[9] = {"p": 1, "origen": "pendiente", "nota": "Requiere brecha sectorial del PNIC 2019"}
    c[10] = {"p": 1, "origen": "pendiente", "nota": "Requiere consulta al Banco de Inversiones"}
    return c


def normalizados(p, c):
    """Valor normalizado 0-1 de cada indicador."""
    v = {}
    for i in [1, 2, 3, 4, 5, 7, 8, 9, 10]:
        lo, hi = M.INDICADORES[i]["escala"]
        v[i] = M.normalizar(c[i]["p"], lo, hi)

    contribucion = p["anexo4"]["contribucion"]
    detalle = []
    vals = []
    for mz in p["macrozonas"] or ["MLC"]:
        bruto = M.puntaje_ind6(mz, contribucion)
        lo, hi = M.RANGO_IND6[mz]
        vals.append(M.normalizar(bruto, lo, hi))
        detalle.append("%s: %d/%d-%d" % (mz, bruto, lo, hi))
    v[6] = sum(vals) / len(vals)
    c[6]["p"] = round(sum(vals) / len(vals) * 100) / 100
    c[6]["nota"] = "Anexo 4 (%s / %s) x Anexo 5 -> %s" % (
        p["anexo4"]["sector"], p["anexo4"]["subsector"], "; ".join(detalle))
    return v


def pesos_base(opcionales):
    """Pesos de los indicadores aplicados. Sin opcionales, el 15% se redistribuye
    proporcionalmente entre los ocho fijos para preservar la escala 0-1."""
    w = {i: M.INDICADORES[i]["peso"] for i in FIJOS}
    if opcionales:
        cada = M.PESO_BLOQUE_OPCIONAL / len(opcionales)
        for i in opcionales:
            w[i] = cada
    else:
        for i in FIJOS:
            w[i] = w[i] / M.PESO_BLOQUE_FIJO
    return w


def reponderar_sector(w, valores, opcionales):
    """Regla del numeral 2.2: un indicador obligatorio con el mismo valor para todos
    los proyectos del sector no se aplica y su peso se redistribuye uniformemente
    entre los demás obligatorios."""
    constantes = [i for i in FIJOS if len({round(v[i], 6) for v in valores}) == 1]
    if not constantes or len(constantes) == len(FIJOS):
        return dict(w), []
    w2 = dict(w)
    liberado = sum(w2.pop(i) for i in constantes)
    restantes = [i for i in FIJOS if i not in constantes]
    for i in restantes:
        w2[i] += liberado / len(restantes)
    for i in opcionales:
        w2.setdefault(i, w[i])
    return w2, constantes


def percentil(datos, q):
    """Percentil por interpolación lineal (equivalente a numpy.percentile)."""
    d = sorted(datos)
    if len(d) == 1:
        return d[0]
    k = (len(d) - 1) * q / 100.0
    f, cl = int(k), min(int(k) + 1, len(d) - 1)
    return d[f] + (d[cl] - d[f]) * (k - f)


def jerarquizar(proyectos, opcionales=(), campo_sector="sector"):
    w0 = pesos_base(list(opcionales))
    aplicados = FIJOS + list(opcionales)

    for p in proyectos:
        p["_calif"] = calificar(p)
        p["_norm"] = normalizados(p, p["_calif"])

    sectores = {}
    for p in proyectos:
        sectores.setdefault(p[campo_sector], []).append(p)

    resultado = []
    for sector, grupo in sorted(sectores.items()):
        w, constantes = reponderar_sector(w0, [p["_norm"] for p in grupo], list(opcionales))
        for p in grupo:
            p["_pesos"] = w
            p["_excluidos"] = constantes
            p["_puntaje"] = sum(w[i] * p["_norm"][i] for i in aplicados if i in w)
        grupo.sort(key=lambda x: -x["_puntaje"])
        corte = percentil([p["_puntaje"] for p in grupo], M.PERCENTIL_CORTE)
        for n, p in enumerate(grupo, 1):
            p["_rank_sector"] = n
            p["_corte_sector"] = corte
            p["_seleccionado"] = p["_puntaje"] >= corte
        resultado.extend(grupo)

    resultado.sort(key=lambda x: -x["_puntaje"])
    for n, p in enumerate(resultado, 1):
        p["_rank_global"] = n
    return resultado


def exportar(res, campo_sector="sector"):
    os.makedirs(SALIDAS, exist_ok=True)
    ruta = os.path.join(SALIDAS, "ranking.csv")
    with open(ruta, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh, delimiter=";")
        wr.writerow(["Rank global", "Rank sector", "Sector", "Proyecto", "Fase", "Modalidad",
                     "Ambito", "Monto US$ MM", "Puntaje total", "Corte P70 sector",
                     "Seleccionado"] + ["Ind %d (pt)" % i for i in range(1, 11)]
                    + ["Ind %d (norm)" % i for i in range(1, 11)])
        for p in res:
            wr.writerow([p["_rank_global"], p["_rank_sector"], p[campo_sector], p["nombre_corto"],
                         p["fase"], p["modalidad"], p["ambito"], p["monto_usd_mm"] or "",
                         round(p["_puntaje"], 4), round(p["_corte_sector"], 4),
                         "Si" if p["_seleccionado"] else "No"]
                        + [p["_calif"][i]["p"] for i in range(1, 11)]
                        + [round(p["_norm"][i], 4) for i in range(1, 11)])
    return ruta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--opcionales", default="", help="indicadores opcionales a aplicar: 9, 10 o 9,10")
    ap.add_argument("--sector", default="sector", choices=["sector", "cartera"],
                    help="nivel del ranking sectorial")
    args = ap.parse_args()
    opcionales = [int(x) for x in args.opcionales.split(",") if x.strip()]

    proyectos = json.load(open(os.path.join(SALIDAS, "proyectos.json"), encoding="utf-8"))
    res = jerarquizar(proyectos, opcionales, args.sector)

    grupos = {}
    for p in res:
        grupos.setdefault(p[args.sector], []).append(p)
    for sector, grupo in sorted(grupos.items()):
        grupo.sort(key=lambda x: x["_rank_sector"])
        aviso = "  [ATENCION: menos de 4 proyectos, ranking poco discriminante]" if len(grupo) < 4 else ""
        print("\n=== %s  (%d proyectos | corte P70 = %.4f | indicadores no aplicados: %s)%s"
              % (sector, len(grupo), grupo[0]["_corte_sector"],
                 grupo[0]["_excluidos"] or "ninguno", aviso))
        for p in grupo:
            print("  %s %2d. %-52s %.4f  %s" % (
                ">>" if p["_seleccionado"] else "  ", p["_rank_sector"], p["nombre_corto"][:52],
                p["_puntaje"], p["fase"][:5]))

    ruta = exportar(res, args.sector)
    sel = [p for p in res if p["_seleccionado"]]
    print("\nSeleccionados sobre la linea de corte: %d de %d  (US$ %.0f MM)"
          % (len(sel), len(res), sum(p["monto_usd_mm"] or 0 for p in sel)))
    print("CSV:", ruta)


if __name__ == "__main__":
    main()
