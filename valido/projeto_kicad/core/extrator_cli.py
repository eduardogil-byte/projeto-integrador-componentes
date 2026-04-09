import subprocess
import csv
import os

def extrair_bom_csv(caminho_sch):
    pasta_base = os.path.dirname(caminho_sch)
    caminho_csv = os.path.join(pasta_base, "bom_temp.csv")

    comando = [
        "kicad-cli", 
        "sch",
        "export",
        "bom", 
        "--output", caminho_csv,
        caminho_sch
    ]


    try:
        subprocess.run(comando, check=True, capture_output=True, text=True)

        componentes = []

        with open(caminho_csv, mode="r", encoding="utf-8-sig") as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)

            for linha in leitor:
                ref = linha.get('Reference', '').strip()
                val = linha.get('Value', '').strip()

                if ref:
                    componentes.append({
                        'ref': ref,
                        'valor': val,
                        'dados_extras': linha
                    })
        
        return componentes

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro na execução do kicad-cli: {e.stderr}")

    except FileNotFoundError:
        raise RuntimeError("O executável 'kicad-cli' não foi encontrado no sistema.")
    
    