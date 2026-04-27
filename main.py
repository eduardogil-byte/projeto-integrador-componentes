# from app.core.pipeline import run_overlay_referencia
# from app.pipeline_2 import run_overlay_referencia
# if __name__ == "__main__":
#     run_overlay_referencia(
#         caminho_img="./data/arduino.jpeg",
#         caminho_csv="./data/bom_footprints.csv",
#         caminho_saida="./output/overlay_ref2.png",
#     )


from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from app.pipeline_2 import run_overlay_referencia
from projeto_kicad.main_kicad import gerar_csv_do_projeto

# Inicializa o aplicativo FastAPI
app = FastAPI(title="API de Inspeção AOI", version="1.0")

from fastapi.staticfiles import StaticFiles

app.mount("/output", StaticFiles(directory="output"), name="output")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que qualquer página web acesse sua API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PASTA_CSVS = "./data/csvs"
PASTA_PROJETOS = "./data/projetos"

# Garante que as pastas existam
os.makedirs("./data", exist_ok=True)
os.makedirs("./output", exist_ok=True)
os.makedirs(PASTA_CSVS, exist_ok=True)

# =========================================================
# ROTA: Receber projeto e GERAR CSV a partir do .kicad_pcb
# =========================================================
@app.post("/novo-projeto/")
async def novo_projeto(
    nome_projeto: str = Form(...),
    arquivo_projeto: UploadFile = File(...)
):
    """
    Recebe um arquivo de projeto (.zip ou .kicad_pcb), salva no servidor,
    extrai os dados geométricos e gera o CSV gabarito dinamicamente.
    """
    try:
        # Pega a extensão e formata o nome do projeto
        extensao = arquivo_projeto.filename.split('.')[-1].lower()
        nome_formatado = nome_projeto.strip().replace(" ", "_")
        nome_arquivo = f"{nome_formatado}.{extensao}"
        caminho_salvo = os.path.join(PASTA_PROJETOS, nome_arquivo)

        # 1. Salva o arquivo ZIP ou PCB original no servidor
        with open(caminho_salvo, "wb") as buffer:
            shutil.copyfileobj(arquivo_projeto.file, buffer)

        # 2. Define onde o CSV gerado deverá ser salvo
        nome_csv_saida = f"{nome_formatado}.csv"
        caminho_csv_saida = os.path.join(PASTA_CSVS, nome_csv_saida)
        
        # 3. Chama o seu código main_kicad.py para processar!
        gerar_csv_do_projeto(
            caminho_arquivo_entrada=caminho_salvo,
            caminho_csv_saida=caminho_csv_saida
        )

        return {"mensagem": f"Projeto processado com sucesso! O gabarito '{nome_csv_saida}' já está disponível."}
 
    except Exception as e:
        return {"erro": f"Falha ao gerar o projeto: {str(e)}"}


@app.get("/projetos-csv/")
async def listar_csvs():
    """
    Lê a pasta de CSVs e retorna uma lista com os nomes dos arquivos.
    """
    try:
        # Lista apenas os arquivos que terminam com '.csv'
        arquivos = [f for f in os.listdir(PASTA_CSVS) if f.endswith('.csv')]
        return {"csvs": arquivos}
    except Exception as e:
        return {"erro": f"Falha ao listar CSVs: {str(e)}"}


@app.post("/inspecionar-placa/")
async def inspecionar_placa(imagem: UploadFile = File(...), projeto_csv: str = Form(...)):
    """
    Recebe a foto de uma placa, processa o alinhamento 
    e devolve a imagem com as marcações dos componentes.
    """
    
    # 1. Salvar a imagem recebida temporariamente
    caminho_img_temp = f"./data/temp_{imagem.filename}"
    with open(caminho_img_temp, "wb") as buffer:
        shutil.copyfileobj(imagem.file, buffer)
        
    # 2. Definir caminhos do gabarito e da saída
    caminho_csv = os.path.join(PASTA_CSVS, projeto_csv)

    if not os.path.exists(caminho_csv):
        return {"erro": f"O arquivo de gabarito '{projeto_csv}' não foi encontrado no servidor."}

    nome_base = projeto_csv.replace(".csv", "")
    caminho_pcb = os.path.join(PASTA_PROJETOS, f"{nome_base}.kicad_pcb")

    if not os.path.exists(caminho_pcb):
        return {"erro": f"O arquivo KiCad '{nome_base}.kicad_pcb' não foi encontrado na pasta de projetos."}

    nome_saida = f"{uuid.uuid4()}.png"
    caminho_saida = f"./output/{nome_saida}"
    
    try:
        # 3. Rodar o seu pipeline! A mágica acontece aqui.
        run_overlay_referencia(
            caminho_img=caminho_img_temp,
            caminho_csv=caminho_csv,
            caminho_pcb=caminho_pcb,
            caminho_saida=caminho_saida
        )
        

        # print("Arquivo \existe?", os.path.exists(caminho_saida))

        # 4. Retornar a imagem final para quem fez a requisição
        return {"url": caminho_saida.replace("./", "http://127.0.0.1:8000/")}
        
    except Exception as e:
        return {"erro": f"Falha ao processar a imagem: {str(e)}"}
        
    finally:
        # (Opcional) Limpar a imagem original temporária para não lotar o HD
        if os.path.exists(caminho_img_temp):
            os.remove(caminho_img_temp)

# Manter essa parte permite rodar o servidor direto pelo Python, se preferir
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)