import os
import zipfile
import shutil
from pathlib import Path

def descompactar_zip(caminho_zip, pasta_destino):
    os.makedirs(pasta_destino, exist_ok=True)

    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        zip_ref.extractall(pasta_destino)

    return pasta_destino

from pathlib import Path

def localizar_arquivo_projeto(pasta_extraida):
    prioridades = [".kicad_pcb", ".pcbdoc", ".brd"]
    encontrados = {ext: None for ext in prioridades}

    for arquivo in Path(pasta_extraida).rglob("*"):
        ext = arquivo.suffix.lower()
        if ext in encontrados and encontrados[ext] is None:
            encontrados[ext] = str(arquivo)

    for ext in prioridades:
        if encontrados[ext]:
            return encontrados[ext]

    return None

def limpar_pasta_temporaria(pasta):
    if os.path.exists(pasta):
        shutil.rmtree(pasta)