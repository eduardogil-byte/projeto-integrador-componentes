# from app.core.pipeline import run_overlay_referencia
# from app.pipeline_2 import run_overlay_referencia
# if __name__ == "__main__":
#     run_overlay_referencia(
#         caminho_img="./data/arduino.jpeg",
#         caminho_csv="./data/bom_footprints.csv",
#         caminho_saida="./output/overlay_ref2.png",
#     )


from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from app.pipeline_2 import run_overlay_referencia

# Inicializa o aplicativo FastAPI
app = FastAPI(title="API de Inspeção AOI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que qualquer página web acesse sua API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Garante que as pastas existam
os.makedirs("./data", exist_ok=True)
os.makedirs("./output", exist_ok=True)

@app.post("/inspecionar-placa/")
async def inspecionar_placa(imagem: UploadFile = File(...)):
    """
    Recebe a foto de uma placa, processa o alinhamento 
    e devolve a imagem com as marcações dos componentes.
    """
    
    # 1. Salvar a imagem recebida temporariamente
    caminho_img_temp = f"./data/temp_{imagem.filename}"
    with open(caminho_img_temp, "wb") as buffer:
        shutil.copyfileobj(imagem.file, buffer)
        
    # 2. Definir caminhos do gabarito e da saída
    caminho_csv = "./data/bom_footprints.csv"  # O seu CSV gabarito
    caminho_saida = f"./output/processada_{imagem.filename}"
    
    try:
        # 3. Rodar o seu pipeline! A mágica acontece aqui.
        run_overlay_referencia(
            caminho_img=caminho_img_temp,
            caminho_csv=caminho_csv,
            caminho_saida=caminho_saida
        )
        
        # 4. Retornar a imagem final para quem fez a requisição
        return FileResponse(caminho_saida, media_type="image/jpeg")
        
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