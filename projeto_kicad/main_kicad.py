import os
import subprocess
import shutil
from projeto_kicad.gerenciador_arquivos import descompactar_zip, buscar_arquivos_kicad, limpar_pasta_temporaria



def run():
    # Facilita a leitura separar as variáveis
    arquivo_zip = "./projeto_kicad/A000073-cad-files.zip"
    pasta_temp = "./projeto_kicad/temp_uploads"

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
        # lista_componentes = extrair_bom_csv(caminho_pcb)
        
        # Mostra o resultado na tela para provar que funcionou
        # print(f"\nSUCESSO! Foram encontrados {len(lista_componentes)} componentes.")
        # print("Aqui estão os 5 primeiros:")
        # for componente in lista_componentes[:5]:
        #     print(f" - {componente['ref']}: {componente['valor']}")

        print("Testando o extrator_pcbnew")
        dados_footprints = extrair_dados_geometria(caminho_pcb)
        print("Mostrando 5 primeiros do extrator_pcbnew")
        for dado in dados_footprints[:5]:
            print(dado)

        limpar_pasta_temporaria(pasta_temp)
        
        salvar_geometria_csv(dados_footprints, "./data/bom_footprints.csv")

    except Exception as e:
        print(f"\nERRO: {e}")
        
    finally:
        # Se quiser testar a limpeza, é só descomentar a linha abaixo:
        # limpar_pasta_temporaria(pasta_temp)
        print("\nFim da execução.")


KICAD_PYTHON_EXE = r"c:\Users\486973624\AppData\Local\Programs\KiCad\9.0\bin\python.exe"

def gerar_csv_do_projeto(caminho_arquivo_entrada, caminho_csv_saida):
    pasta_temp = "./data/temp_uploads"
    # Pegamos o nome base do CSV (ex: "Placa_V1.csv" vira "Placa_V1") para salvar o PCB com o mesmo nome
    nome_base = os.path.basename(caminho_csv_saida).replace(".csv", "")
    caminho_pcb_final = f"./data/projetos/{nome_base}.kicad_pcb"
    
    try:
        caminho_pcb = None
        
        # 1. Lida com a extração se for um arquivo ZIP
        if caminho_arquivo_entrada.endswith(".zip"):
            pasta_destino = descompactar_zip(caminho_arquivo_entrada, pasta_temp)
            _, caminho_pcb = buscar_arquivos_kicad(pasta_destino)
            
            if not caminho_pcb:
                raise ValueError("Nenhum arquivo .kicad_pcb encontrado no ZIP.")
            
            # COPIA o .kicad_pcb extraído para a pasta projetos com o nome correto!
            shutil.copy(caminho_pcb, caminho_pcb_final)
            caminho_pcb = caminho_pcb_final
                
        # 2. Se for o PCB direto
        elif caminho_arquivo_entrada.endswith(".kicad_pcb"):
            caminho_pcb = caminho_arquivo_entrada
            # Se já é um pcb solto, o FastAPI já salvou ele na pasta projetos com o nome certo, 
            # então não precisamos copiar de novo.
            
        else:
            raise ValueError("Envie um .zip ou .kicad_pcb.")

        # 3. CHAMA O WORKER DO KICAD VIA SUBPROCESS
        print("Chamando o Python do KiCad em background...")
        
        # ATENÇÃO AQUI: Apontamos para o worker_kicad.py dentro da pasta projeto_kicad!
        caminho_worker = "./projeto_kicad/worker_kicad.py"
        
        comando = [
            KICAD_PYTHON_EXE, 
            os.path.abspath(caminho_worker), 
            os.path.abspath(caminho_pcb), 
            os.path.abspath(caminho_csv_saida)
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            raise RuntimeError(f"Erro no KiCad Worker:\n{resultado.stderr}\n{resultado.stdout}")
            
        print("CSV gerado com sucesso via Subprocesso!")
        return True

    finally:
        if os.path.exists(pasta_temp):
            limpar_pasta_temporaria(pasta_temp)

# Essa estrutura é o padrão Python para rodar um script de teste
if __name__ == "__main__":
    run()