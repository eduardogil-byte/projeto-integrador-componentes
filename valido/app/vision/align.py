import cv2

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


