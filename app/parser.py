import csv
from typing import List, Dict
import numpy as np


def carregar_componentes(caminho_csv: str) -> List[Dict]:
    componentes = []

    with open(caminho_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # if deve_ignorar(row):
            #     continue
            
            try:
                comp = {
                    "ref": row["ref"].strip().replace('"', ""),
                    # "val": row["Val"].strip().replace('"', ""),
                    "package": row["package"].strip().replace('"', ""),
                    "x_mm": float(row["pos_x"]),
                    "y_mm": float(row["pos_y"]),
                    "w_mm": float(row["largura_mm"]),
                    "h_mm": float(row["altura_mm"]),
                    "rot": float(row["rotacao"]),
                    "side": row["lado"].strip().lower().replace('"', ""),
                }
                componentes.append(comp)
            except Exception as e:
                print(f"[WARN] Linha ignorada: {row} | erro: {e}")

    return componentes


def carregar_pontos_parafusos(caminho_csv: str) -> List[List]:
    pontos = []

    with open(caminho_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["ref"].startswith("UNK_HOLE_"):

                try:
                    x = float(row["pos_x"])
                    y = float(row["pos_y"])
                    pontos.append([x, y])

                except Exception as e:
                    print(f"[WARN] Erro ao converter coordenadas do furo: {e}")
                
    return pontos

def ordernar_pontos(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect






IGNORAR_PREFIXOS = (
    "TP_",
    # "UNK_HOLE_",
)

IGNORAR_REFS = {
    "FRAME1",
    "ORIGIN0",
}

IGNORAR_PACKAGES = {
    "FRAME",
    "TP-SP",
}

IGNORAR_VALORES = {
    "DNP",
}


def deve_ignorar(row: dict) -> bool:
    ref = row.get("Ref", "").strip().replace('"', "")
    val = row.get("Val", "").strip().replace('"', "")
    package = row.get("Package", "").strip().replace('"', "")
    side = row.get("Side", "").strip().lower().replace('"', "")

    if side != "top":
        return True

    if ref in IGNORAR_REFS:
        return True

    if any(ref.startswith(prefix) for prefix in IGNORAR_PREFIXOS):
        return True

    if package in IGNORAR_PACKAGES:
        return True

    if val in IGNORAR_VALORES:
        return True

    return False