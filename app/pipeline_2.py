import os
import cv2
import numpy as np

from app.parser import carregar_componentes
from app.mm_to_pixel import mm_para_pixel_perspectiva
from app.align import carregar_imagem, detectar_contorno_pcb
from app.draw import desenhar_ponto_e_label, desenhar_caixa_aproximada_matriz
from app.pcb_parser import carregar_edgecuts_pcb, extrair_bbox_edgecuts_para_csv_original


def run_overlay_referencia(
    caminho_img: str,
    caminho_csv: str,
    caminho_pcb: str,
    caminho_saida: str,
):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    img = carregar_imagem(caminho_img)
    componentes = carregar_componentes(caminho_csv)

    pontos_img = detectar_contorno_pcb(img)

    pontos_edge = carregar_edgecuts_pcb(caminho_pcb)
    pontos_csv_mm = extrair_bbox_edgecuts_para_csv_original(pontos_edge)

    # pontos_csv_mm = np.array([
    #     [173.67, -29.46],  # Superior Esquerdo
    #     [242.25, -29.46],  # Superior Direito
    #     [242.25, -82.80],  # Inferior Direito
    #     [173.67, -82.80]   # Inferior Esquerdo
    # ], dtype=np.float32)

    matriz = cv2.getPerspectiveTransform(
        np.float32(pontos_csv_mm),
        np.float32(pontos_img)
    )

    print(len(componentes))
    for comp in componentes[:5]:
        print(comp)

    DEBUG = True

    if DEBUG:
        print("PONTOS IMG:", pontos_img)
        print("PONTOS EDGE/CSV:", pontos_csv_mm)
        print("MATRIZ:", matriz)

    img_copy = img.copy()

    for comp in componentes:
        x_px, y_px = mm_para_pixel_perspectiva(
            comp["x_mm"],
            comp["y_mm"],
            matriz
        )

        desenhar_caixa_aproximada_matriz(img_copy, comp, matriz)
        desenhar_ponto_e_label(img_copy, x_px, y_px, comp["ref"])

    cv2.imwrite(caminho_saida, img_copy)
    print(f"[OK] Overlay salvo em: {caminho_saida}")