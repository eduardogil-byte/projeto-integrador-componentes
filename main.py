# from app.core.pipeline import run_overlay_referencia
from app.pipeline_2 import run_overlay_referencia

if __name__ == "__main__":
    run_overlay_referencia(
        caminho_img="./arduino_uno_r3_smd_teste_falta.jpeg",
        caminho_csv="./valido/projeto_kicad/output/bom_footprints.csv",
        caminho_saida="valido/output/overlay_ref2.png",
    )