import cv2
import numpy as np

def verificar_presenca_componente(img, pontos_poligono, limite_presenca=5.0):
    mascara = np.zeros(img.shape[:2], dtype=np.uint8)

    cv2.fillPoly(mascara, [np.int32(pontos_poligono)], 255)


    x, y, w, h = cv2.boundingRect(np.int32(pontos_poligono))

    if w == 0 or h == 0 or x < 0 or y < 0:
        return False, 0.0
    
    recorte_img = img[y:y+h, x:x+w]
    recorte_mascara = mascara[y:y+h, x:x+w]

    gray = cv2.cvtColor(recorte_img, cv2.COLOR_BGR2GRAY)
    bordas = cv2.Canny(gray, 50, 150)
    bordas_mascaradas = cv2.bitwise_and(bordas, bordas, mask=recorte_mascara)

    total_pixel_caixa = cv2.countNonZero(recorte_mascara)
    total_pixel_borda = cv2.countNonZero(bordas_mascaradas)

    if total_pixel_caixa == 0:
        return False, 0.0
    
    desidade_bordas = (total_pixel_borda/total_pixel_caixa) * 100
    esta_presente = desidade_bordas > limite_presenca

    return esta_presente, desidade_bordas
