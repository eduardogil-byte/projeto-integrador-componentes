# Sem os pontos nos imports!
from utils.gerenciador_arquivos import descompactar_zip, buscar_arquivos_kicad, limpar_pasta_temporaria
from core.extrator_cli import extrair_bom_csv
from core.extrator_pcbnew import extrair_dados_geometria

def run():
    # Facilita a leitura separar as variáveis
    arquivo_zip = "projeto-integrador-componentes/valido/projeto_kicad/A000073-cad-files.zip"
    pasta_temp = "projeto-integrador-componentes/valido/projeto_kicad/temp_uploads"

    try:
        print("1. Descompactando o ZIP...")
        pasta_destino = descompactar_zip(
            caminho_zip=arquivo_zip,
            pasta_destino=pasta_temp
        )

        print("2. Buscando arquivos do KiCad...")
        caminho_sch, caminho_pcb = buscar_arquivos_kicad(pasta_destino)
        print(f"   -> Esquemático encontrado: {caminho_sch}")

        print("3. Extraindo BOM com kicad-cli...")
        lista_componentes = extrair_bom_csv(caminho_pcb)
        
        # Mostra o resultado na tela para provar que funcionou
        print(f"\nSUCESSO! Foram encontrados {len(lista_componentes)} componentes.")
        print("Aqui estão os 5 primeiros:")
        for componente in lista_componentes[:5]:
            print(f" - {componente['ref']}: {componente['valor']}")

        print("Testando o extrator_pcbnew")
        dados_footprints = extrair_dados_geometria(caminho_pcb)
        print("Mostrando 5 primeiros do extrator_pcbnew")
        for dado in dados_footprints[:5]:
            print(dado)


    except Exception as e:
        print(f"\nERRO: {e}")
        
    finally:
        # Se quiser testar a limpeza, é só descomentar a linha abaixo:
        # limpar_pasta_temporaria(pasta_temp)
        print("\nFim da execução.")

# Essa estrutura é o padrão Python para rodar um script de teste
if __name__ == "__main__":
    run()