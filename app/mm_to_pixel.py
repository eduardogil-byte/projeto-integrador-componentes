from typing import List, Dict, Tuple
import cv2
import numpy as np

def obter_limites(componentes: List[Dict]) -> Tuple[float, float, float, float]:
    xs = [c["x_mm"] for c in componentes]
    ys = [c["y_mm"] for c in componentes]
    return min(xs), max(xs), min(ys), max(ys)

def calcular_escala(
    min_x: float,
    max_x: float,
    min_y: float,
    max_y: float,
    img_w: int,
    img_h: int,
    margem_px: int = 30,
) -> float:
    area_w = img_w - 2 * margem_px
    area_h = img_h - 2 * margem_px

    span_x = max_x - min_x
    span_y = max_y - min_y

    if span_x <= 0 or span_y <= 0:
        raise ValueError("Span inválido nas coordenadas do CSV.")

    escala_x = area_w / span_x
    escala_y = area_h / span_y

    return min(escala_x, escala_y)

def mm_para_pixel(
    x_mm: float,
    y_mm: float,
    min_x: float,
    max_x: float,
    min_y: float,
    max_y: float,
    img_w: int,
    img_h: int,
    margem_px: int = 30,
) -> Tuple[int, int]:
    escala = calcular_escala(min_x, max_x, min_y, max_y, img_w, img_h, margem_px)

    x_px = margem_px + (x_mm - min_x) * escala
    y_px = margem_px + (max_y - y_mm) * escala

    return int(round(x_px)), int(round(y_px))

def mm_para_pixel_perspectiva(x_mm: float, y_mm: float, matriz_transformacao) -> tuple[int,int]:
    pontos_mm = np.float32([[[x_mm,y_mm]]])

    pontos_foto = cv2.perspectiveTransform(pontos_mm, matriz_transformacao)

    x_px = int(round(pontos_foto[0][0][0]))
    y_px = int(round(pontos_foto[0][0][1]))

    return x_px, y_px

