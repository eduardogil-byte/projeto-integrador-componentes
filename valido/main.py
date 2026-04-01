# from app.core.pipeline import run_overlay_referencia
from app.core.pipeline_2 import run_overlay_referencia

if __name__ == "__main__":
    run_overlay_referencia(
        caminho_img="arduino_uno_r3_smd_teste.jpeg",
        caminho_csv="valido/data/top.csv",
        caminho_saida="valido/output/overlay_ref2.png",
    )