import subprocess
import csv
import os

def extrair_bom_csv(caminho_pcb):
    pasta_base = os.path.dirname(caminho_pcb)
    caminho_csv = os.path.join(pasta_base, "bom_temp.csv")

    comando = [
        r"C:\Users\486973624\AppData\Local\Programs\KiCad\9.0\bin\kicad-cli.exe", 
        "pcb",
        "export",
        "pos",
        "--format", "csv",
        "--units", "mm",
        "--output", caminho_csv,
        caminho_pcb
    ]


    try:
        subprocess.run(comando, check=True, capture_output=True, text=True)

        componentes = []

        with open(caminho_csv, mode="r", encoding="utf-8-sig") as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)

            for linha in leitor:
                ref = linha.get('Ref', '').strip()
                val = linha.get('Val', '').strip()

                if ref:
                    componentes.append({
                        'ref': ref,
                        'valor': val,
                        'posX': linha.get('PosX'),
                        'posY': linha.get('PosY'),
                        'lado': linha.get('Side'),
                        'dados_extras': linha
                    })
        
        return componentes

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro na execução do kicad-cli: {e.stderr}")

    except FileNotFoundError:
        raise RuntimeError("O executável 'kicad-cli' não foi encontrado no sistema.")
    
    