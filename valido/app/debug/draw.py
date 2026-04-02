import cv2
from app.geometry.boxes import obter_tamanho_package_mm
from app.geometry.mm_to_pixel import calcular_escala
from app.vision.analyze import verificar_presenca_componente
import numpy as np


def desenhar_ponto_e_label(img, x_px, y_px, texto):
    cv2.circle(img, (x_px, y_px), 4, (0, 255, 0), -1)
    cv2.putText(
        img,
        texto,
        (x_px + 6, y_px - 6),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (0, 255, 0),
        1,
        cv2.LINE_AA,
    )


def desenhar_caixa_aproximada(
    img,
    comp,
    x_px,
    y_px,
    min_x,
    max_x,
    min_y,
    max_y,
    img_w,
    img_h,
    margem_px=30,
):
    escala = calcular_escala(min_x, max_x, min_y, max_y, img_w, img_h, margem_px)
    w_mm, h_mm = obter_tamanho_package_mm(comp["package"])

    w_px = max(8, int(round(w_mm * escala)))
    h_px = max(8, int(round(h_mm * escala)))

    x1 = x_px - w_px // 2
    y1 = y_px - h_px // 2
    x2 = x_px + w_px // 2
    y2 = y_px + h_px // 2

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)



def desenhar_caixa_aproximada_matriz(img, comp, matriz_transformacao, padding_px=12):
    w_mm, h_mm = obter_tamanho_package_mm(comp["package"])
    x_mm = comp["x_mm"]
    y_mm = comp["y_mm"]
    rot = comp["rot"]

    img_copy = img.copy()

    if abs(rot) % 180 == 90:
        w_mm, h_mm = h_mm, w_mm


    cantos_mm = np.float32([[
        [x_mm - w_mm / 2, y_mm - h_mm / 2],
        [x_mm + w_mm / 2, y_mm - h_mm / 2],
        [x_mm + w_mm / 2, y_mm + h_mm / 2],
        [x_mm - w_mm / 2, y_mm + h_mm / 2]
    ]])


    cantos_px = cv2.perspectiveTransform(cantos_mm, matriz_transformacao)
    
    # cantos_px = np.int32(cantos_px)
    # print(cantos_px)

    # cv2.polylines(img, [cantos_px], isClosed=True, color=(0, 255, 0), thickness=2)

    # nova logica para colocar padding
    pontos = cantos_px[0]

    centro_px = np.mean(pontos, axis=0)

    pontos_com_padding = []
    for pt in pontos:
        vetor_direcao = pt - centro_px

        distancia = np.linalg.norm(vetor_direcao)

        if distancia > padding_px:
            vetor_movimento = (vetor_direcao / distancia) * padding_px
            novo_pt = pt+vetor_movimento
        else:
            novo_pt = pt
        
        pontos_com_padding.append(novo_pt)

    cantos_finais_px = np.int32([pontos_com_padding])

    esta_presente, score = verificar_presenca_componente(img_copy, cantos_finais_px)
    
    color = (0,255,0) if esta_presente else (0,0,255)

    cv2.polylines(img, cantos_finais_px, isClosed=True, color=color, thickness=2)






    """ ponto_mm = np.float32([[[w_mm, h_mm]]])

    pontos_foto = cv2.perspectiveTransform(ponto_mm, matriz_transformacao)

    w_px = int(round(pontos_foto[0][0][0]))
    h_px = int(round(pontos_foto[0][0][1]))

    x1 = x_px - w_px // 2
    y1 = y_px - h_px // 2
    x2 = x_px + w_px // 2
    y2 = y_px + h_px // 2

    cv2.rectangle(img, (x1,y1), (x2, y2), (0, 255, 0), 1) """