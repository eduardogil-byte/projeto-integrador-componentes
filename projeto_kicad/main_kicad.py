import os
import subprocess
from projeto_kicad.gerenciador_arquivos import (
    descompactar_zip,
    limpar_pasta_temporaria,
    localizar_arquivo_projeto
)

KICAD_PYTHON_EXE = r"c:\Users\486973624\AppData\Local\Programs\KiCad\10.0\bin\python.exe"
KICAD_CLI_EXE = r"c:\Users\486973624\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"

def validar_pcb(caminho):
    if not os.path.exists(caminho):
        raise RuntimeError("PCB não foi gerado")

    if os.path.getsize(caminho) < 100:  # arquivo muito pequeno = inválido
        raise RuntimeError("PCB gerado está vazio ou corrompido")


def converter_para_kicad_cli(caminho_origem, caminho_pcb_final):
    ext = os.path.splitext(caminho_origem)[1].lower()

    if ext == ".kicad_pcb":
        return caminho_origem

    if ext == ".brd":
        formato = "eagle"
    elif ext == ".pcbdoc":
        formato = "altium"
    else:
        raise ValueError(f"Formato não suportado: {ext}")

    os.makedirs(os.path.dirname(caminho_pcb_final), exist_ok=True)

    comando = [
        KICAD_CLI_EXE,
        "pcb", "import",
        "--format", formato,
        "--output", caminho_pcb_final,
        caminho_origem
    ]

    resultado = subprocess.run(comando, capture_output=True, text=True)

    print("STDOUT:", resultado.stdout)
    print("STDERR:", resultado.stderr)
    print("RETURN CODE:", resultado.returncode)


    return caminho_pcb_final


def gerar_csv_do_projeto(caminho_arquivo_entrada, caminho_csv_saida):
    pasta_temp = os.path.abspath("./data/temp_raw")
    nome_base = os.path.basename(caminho_csv_saida).replace(".csv", "")
    caminho_pcb_final = os.path.abspath(f"./data/projetos/{nome_base}.kicad_pcb")

    try:
        if caminho_arquivo_entrada.endswith(".zip"):
            descompactar_zip(caminho_arquivo_entrada, pasta_temp)
            caminho_origem = localizar_arquivo_projeto(pasta_temp)
        else:
            caminho_origem = caminho_arquivo_entrada

        if not caminho_origem:
            raise ValueError("Nenhum arquivo de CAD compatível foi encontrado.")

        print(f"Origem encontrada: {caminho_origem}")

        caminho_pcb_final = converter_para_kicad_cli(caminho_origem, caminho_pcb_final)
        validar_pcb(caminho_pcb_final)


        print(f"PCB convertido em: {caminho_pcb_final}")

        caminho_worker = os.path.abspath("./projeto_kicad/worker_kicad.py")
        comando = [
            KICAD_PYTHON_EXE,
            caminho_worker,
            os.path.abspath(caminho_pcb_final),
            os.path.abspath(caminho_pcb_final),
            os.path.abspath(caminho_csv_saida)
        ]

        resultado = subprocess.run(comando, capture_output=True, text=True)

        if resultado.returncode != 0:
            raise RuntimeError(f"Erro no worker de extração:\n{resultado.stdout}\n{resultado.stderr}")

        return True

    finally:
        if os.path.exists(pasta_temp):
            limpar_pasta_temporaria(pasta_temp)