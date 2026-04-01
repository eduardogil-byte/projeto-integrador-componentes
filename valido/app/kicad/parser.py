import csv
from typing import List, Dict
from app.kicad.filters import deve_ignorar


def carregar_componentes(caminho_csv: str) -> List[Dict]:
    componentes = []

    with open(caminho_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if deve_ignorar(row):
                continue

            try:
                comp = {
                    "ref": row["Ref"].strip().replace('"', ""),
                    "val": row["Val"].strip().replace('"', ""),
                    "package": row["Package"].strip().replace('"', ""),
                    "x_mm": float(row["PosX"]),
                    "y_mm": float(row["PosY"]),
                    "rot": float(row["Rot"]),
                    "side": row["Side"].strip().lower().replace('"', ""),
                }
                componentes.append(comp)
            except Exception as e:
                print(f"[WARN] Linha ignorada: {row} | erro: {e}")

    return componentes


def carregar_pontos_parafusos(caminho_csv: str) -> List[List]:
    pontos = []

    with open(caminho_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["Ref"].startswith("UNK_HOLE_"):

                try:
                    x = float(row["PosX"])
                    y = float(row["PosY"])
                    pontos.append([x, y])

                except Exception as e:
                    print(f"[WARN] Erro ao converter coordenadas do furo: {e}")
                """ try:
                    comp = {
                        "ref": row["Ref"].strip().replace('"',""),
                        "x_mm": float(row["PosX"]),
                        "y_mm": float(row["PosY"]),
                    }
                except Exception as e:
                    print(f"[WARN] Linha ignorada: {row} | erro: {e}") """
                

    return pontos