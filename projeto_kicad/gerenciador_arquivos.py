import os
import zipfile
import shutil
from pathlib import Path

def descompactar_zip(caminho_zip, pasta_destino):
    os.makedirs(pasta_destino, exist_ok=True)

    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        zip_ref.extractall(pasta_destino)

    return pasta_destino

def buscar_arquivos_kicad(pasta_extraida):
    caminho_sch = None
    caminho_pcb = None

    for arquivo in Path(pasta_extraida).rglob('*'):
        if arquivo.suffix == '.kicad_sch':
            caminho_sch = str(arquivo)
        if arquivo.suffix == '.kicad_pcb':
            novo_caminho = f"./data/projetos/{arquivo.name}"
            shutil.move(str(arquivo), str(novo_caminho))
            caminho_pcb = str(novo_caminho)

    if not caminho_pcb:
        raise FileNotFoundError("Erro: O arquivo .zip deve conter pelo menos um .kicad_pcb.")
    
    return caminho_sch, caminho_pcb

def limpar_pasta_temporaria(pasta_para_deletar, caminho_zip_original=None):
    
    if os.path.exists(pasta_para_deletar):
        shutil.rmtree(pasta_para_deletar)

    if caminho_zip_original and os.path.exists(caminho_zip_original):
        os.remove(caminho_zip_original)