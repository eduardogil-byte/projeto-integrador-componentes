import os
import cv2
import numpy as np
from app.kicad.parser import carregar_componentes, carregar_pontos_parafusos
from app.geometry.mm_to_pixel import obter_limites, mm_para_pixel, mm_para_pixel_perspectiva
from app.vision.io import carregar_imagem
from app.debug.draw import desenhar_ponto_e_label, desenhar_caixa_aproximada_matriz

from app.vision.align import align

def run_overlay_referencia(
    caminho_img: str,
    caminho_csv: str,
    caminho_saida: str,
):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    img = carregar_imagem(caminho_img)
    componentes = carregar_componentes(caminho_csv)

    pontos_parafuso_img = align(img)

    print(f"[INFO] Componentes válidos: {len(componentes)}")

    carregar_pontos_p = carregar_pontos_parafusos(caminho_csv)

    pontos_csv_mm = np.float32(carregar_pontos_p)

    ponto_foto_px = np.float32(pontos_parafuso_img)

    print(f"ponto parafuso: {len(ponto_foto_px)}")
    print(f"ponto parafuso: {len(carregar_pontos_p)}")

    matriz = cv2.getPerspectiveTransform(pontos_csv_mm, ponto_foto_px)

    img_copy = img.copy()

    for comp in componentes:
        x_px, y_px = mm_para_pixel_perspectiva(comp["x_mm"], comp["y_mm"], matriz)

        # desenhar_caixa_aproximada_matriz(img_copy, x_px, y_px, comp["package"], matriz)

        desenhar_caixa_aproximada_matriz(img_copy, comp, matriz)

        desenhar_ponto_e_label(img_copy, x_px, y_px, comp["ref"])


    cv2.imwrite(caminho_saida, img_copy)
    print(f"[OK] Overlay salvo em: {caminho_saida}")
