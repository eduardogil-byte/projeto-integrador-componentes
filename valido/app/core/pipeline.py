import os
import cv2
import numpy as np
from app.kicad.parser import carregar_componentes, carregar_pontos_parafusos
from app.geometry.mm_to_pixel import obter_limites, mm_para_pixel, mm_para_pixel_perspectiva
from app.vision.io import carregar_imagem
from app.debug.draw import desenhar_ponto_e_label, desenhar_caixa_aproximada

from app.vision.align import align

def run_overlay_referencia(
    caminho_img: str,
    caminho_csv: str,
    caminho_saida: str,
):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    img = carregar_imagem(caminho_img)
    componentes = carregar_componentes(caminho_csv)

    # pontos_parafuso = align(img)

    print(f"[INFO] Componentes válidos: {len(componentes)}")

    min_x, max_x, min_y, max_y = obter_limites(componentes)
    h, w = img.shape[:2]

    for comp in componentes:
        x_px, y_px = mm_para_pixel(
            comp["x_mm"],
            comp["y_mm"],
            min_x,
            max_x,
            min_y,
            max_y,
            w,
            h,
            margem_px=30,
        )

        desenhar_caixa_aproximada(
            img,
            comp,
            x_px,
            y_px,
            min_x,
            max_x,
            min_y,
            max_y,
            w,
            h,
            margem_px=30,
        )
        desenhar_ponto_e_label(img, x_px, y_px, comp["ref"])

    cv2.imwrite(caminho_saida, img)
    print(f"[OK] Overlay salvo em: {caminho_saida}")