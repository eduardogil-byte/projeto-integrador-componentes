# worker_kicad.py
import sys
import os

# Tenta importar o pcbnew (isso só vai funcionar no Python do KiCad)
try:
    import pcbnew
except ImportError:
    print("ERRO: Este script precisa ser executado pelo Python do KiCad.")
    sys.exit(1)

# Importa as suas funções de extração (que usam o pcbnew)
from projeto_kicad.extrator_cli import extrair_dados_geometria, salvar_geometria_csv

def main():
    # O sys.argv pega os argumentos passados pelo terminal
    if len(sys.argv) < 3:
        print("Uso: python worker_kicad.py <caminho_pcb> <caminho_csv_saida>")
        sys.exit(1)

    caminho_pcb = sys.argv[1]
    caminho_csv = sys.argv[2]

    try:
        print(f"Extraindo geometria de: {caminho_pcb}")
        dados_footprints = extrair_dados_geometria(caminho_pcb)
        
        print(f"Salvando CSV em: {caminho_csv}")
        salvar_geometria_csv(dados_footprints, caminho_csv)
        
        print("SUCESSO")
        sys.exit(0)
    except Exception as e:
        print(f"ERRO INTERNO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()