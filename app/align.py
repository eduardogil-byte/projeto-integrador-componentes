import cv2
import numpy as np
from app.parser import ordernar_pontos

pontos_foto = []
img_display = None

def capturar_cliques(event, x, y, flags, param):
    global pontos_foto 
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pontos_foto) < 4:
            pontos_foto.append([x,y])
            cv2.circle(img_display, (x,y), 5, (0, 255,0), -1)
            cv2.imshow("Clique nos 4 furos", img_display)
            print(f"Ponto {len(pontos_foto)} capturado: ({x}, {y})")


def align(img):
    global img_display
    img_display = img.copy()

    cv2.imshow("Clique nos 4 furos", img_display)
    cv2.setMouseCallback("Clique nos 4 furos", capturar_cliques)

    while len(pontos_foto) < 4:
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    return pontos_foto


def carregar_imagem(caminho: str):
    img = cv2.imread(caminho)
    if img is None:
        raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")
    return img