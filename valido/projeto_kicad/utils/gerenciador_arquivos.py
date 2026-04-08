import os
import zipfile
import shutil
from pathlib import Path

def descompactar_zip(caminho_zip, pasta_destino):
    os.makedirs(pasta_destino, exist_ok=True)

    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        zip_ref.extractall(pasta_destino)

    return pasta_destino