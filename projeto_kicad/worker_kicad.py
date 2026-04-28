import sys
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
if diretorio_atual not in sys.path:
    sys.path.append(diretorio_atual)

import pcbnew
from extrator_cli import extrair_dados_geometria, salvar_geometria_csv

def main():
    if len(sys.argv) < 4:
        print("Uso: worker_kicad.py <caminho_pcb> <destino_pcb_ou_igual> <destino_csv>")
        sys.exit(1)

    caminho_pcb = sys.argv[1]
    caminho_csv_saida = sys.argv[3]

    try:
        dados_footprints = extrair_dados_geometria(caminho_pcb)
        salvar_geometria_csv(dados_footprints, caminho_csv_saida)
        print("SUCESSO_TOTAL")
        sys.exit(0)

    except Exception as e:
        import traceback
        print(f"ERRO_WORKER: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()