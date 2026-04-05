import cv2
import numpy as np

def verificar_presenca_componente(img, pontos_poligono, limite_presenca=7.0):
    centro = np.mean(pontos_poligono, axis=0)

    pontos_encolhidos = []
    for pt in pontos_poligono:
        vetor_direcao = pt - centro
        
        novo_pt = centro+(vetor_direcao*0.6)
        pontos_encolhidos.append(novo_pt)

    pontos_encolhidos = np.int32(pontos_encolhidos)

    mascara = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mascara, [np.int32(pontos_encolhidos)], 255)

    x, y, w, h = cv2.boundingRect(np.int32(pontos_encolhidos))
    if w == 0 or h == 0 or x < 0 or y < 0:
        return False, 0.0
    
    recorte_img = img[y:y+h, x:x+w]
    recorte_mascara = mascara[y:y+h, x:x+w]

    gray = cv2.cvtColor(recorte_img, cv2.COLOR_BGR2GRAY)

    # # gray_eq = cv2.equalizeHist(gray)

    # gray_blur = cv2.GaussianBlur(gray, (3,3), 0)

    # mediana = np.median(gray_blur)

    # sigma = 0.33
    # lower = int(max(0, (1.0 - sigma) * mediana))
    # upper = int(min(255, (1.0 + sigma) * mediana))

    # # brilho_medio = cv2.mean(gray, mask=recorte_mascara)[0]
    # # LIMITE_ESCURIDAO = 100

    # bordas = cv2.Canny(gray, lower, upper)

    # bordas_mascaradas = cv2.bitwise_and(bordas, bordas, mask=recorte_mascara)


    # total_pixel_caixa = cv2.countNonZero(recorte_mascara)
    # total_pixel_borda = cv2.countNonZero(bordas_mascaradas)

    # if total_pixel_caixa == 0:
    #     return False, 0.0
    
    # densidade_bordas = (total_pixel_borda/total_pixel_caixa) * 100

    # esta_presente = densidade_bordas > limite_presenca

    _, stddev = cv2.meanStdDev(gray, mask=recorte_mascara)

    nivel_textura = stddev[0][0]

    esta_presente = nivel_textura > limite_presenca

    return esta_presente, nivel_textura  



def verificar_presenca_componente_desvio_padrao(img, pontos_poligono, limite_presenca=12.0):
    
    pontos_poligono = np.array(pontos_poligono, dtype=np.float32)
    centro = np.mean(pontos_poligono, axis=0)

    pontos_encolhidos = centro + (pontos_poligono - centro) * 0.6
    pontos_encolhidos = np.int32(pontos_encolhidos)
    
    x, y, w, h = cv2.boundingRect(np.int32(pontos_encolhidos))

    altura_img, largura_img = img.shape[:2]
    if w <= 0 or h <=0 or x < 0 or y < 0 or (x+w) > largura_img or (y+h) > altura_img:
        return False, 0.0
    
    recorte_img = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(recorte_img, cv2.COLOR_BGR2GRAY)

    recorte_mascara = np.zeros((h, w), dtype=np.uint8)

    pontos_deslocados = pontos_encolhidos - [x, y]
    cv2.fillPoly(recorte_mascara, [pontos_deslocados], 255)

    _, stddev = cv2.meanStdDev(gray, mask=recorte_mascara)

    nivel_textura = stddev[0][0] if stddev is not None else 0.0

    esta_presente = nivel_textura > limite_presenca

    return esta_presente, nivel_textura  


def verificar_presenca_componente_desvio_padrao_sem_reflexo(img, pontos_poligono, limite_presenca=12.0):
    
    pontos_poligono = np.array(pontos_poligono, dtype=np.float32)
    centro = np.mean(pontos_poligono, axis=0)

    pontos_encolhidos = centro + (pontos_poligono - centro) * 0.35
    pontos_encolhidos = np.int32(pontos_encolhidos)
    
    x, y, w, h = cv2.boundingRect(np.int32(pontos_encolhidos))

    altura_img, largura_img = img.shape[:2]
    if w <= 0 or h <=0 or x < 0 or y < 0 or (x+w) > largura_img or (y+h) > altura_img:
        return False, 0.0
    
    recorte_img = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(recorte_img, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 3)

    recorte_mascara = np.zeros((h, w), dtype=np.uint8)

    pontos_deslocados = pontos_encolhidos - [x, y]
    cv2.fillPoly(recorte_mascara, [pontos_deslocados], 255)

    _, stddev = cv2.meanStdDev(gray, mask=recorte_mascara)

    nivel_textura = stddev[0][0] if stddev is not None else 0.0

    esta_presente = nivel_textura > limite_presenca

    return esta_presente, nivel_textura  
