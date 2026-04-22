import cv2
import numpy as np
from app.kicad.parser import ordernar_pontos

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

# apagar tudo para baixo
""" def align_auto(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 7)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, 
                               param1=50, param2=25, minRadius=8, maxRadius=30)

    if circles is not None:
        circles = np.round(circles[0, :].astype("int"))
        pontos_encontrados = []

        for (x, y, r) in circles:
            pontos_encontrados.append([x,y])

        pontos_encontrados = np.array(pontos_encontrados)

        if len(pontos_encontrados) >= 4:
            pontos_finais = pontos_encontrados[:4]

            pontos_ordenados = ordernar_pontos(pontos_finais)

            img_debug = img.copy()
            cores = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]

            for i, (x, y) in enumerate(pontos_ordenados):
                cv2.circle(img_debug, (int(x), int(y)), 8, cores[i], -1)
                cv2.putText(img_debug, str(i), (int(x)-15, int(y)-15), cv2.FONT_HERSHEY_SIMPLEX, 1, cores[i], 2)

            cv2.imshow("Furos Encontrados (0=TL, 1=TR, 2=BR, 3=BL)", img_debug)
            cv2.imwrite("valido/output/teste_align_auto.png", img_debug)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            return pontos_ordenados.tolist()
        else:
            print(f"Erro: Encontrou apenas {len(pontos_encontrados)} furos. Precisamos de 4.")
            return None
    else:
        print("Erro: Nenhum furo encontrado! Verifique minRadius e maxRadius.")
        return None


def align_auto_binario(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 3)

    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imshow("Debug: ", cv2.resize(thresh, (800, 800)))

    cv2.imwrite("valido/output/teste_thresh.png", thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 400<area<3000:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0: continue

            circularidade = (4 * np.pi * area) / (perimeter * perimeter)

            if circularidade > 0.85:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    candidates.append([cX, cY])
    
    if len(candidates) != 4:
        img_error = img.copy()
        for cand in candidates:
            cv2.circle(img_error, (cand[0], cand[1]), 10, (0,0,255), -1)
        cv2.imshow("Debug: Achou %d formas erradas" % len(candidates), img_error)
        cv2.waitKey(0)

        print(f"Erro Crítico: O algoritmo detectou {len(candidates)} furos. Precisamos de 4 exatos.")
        print("Calibre os ranges de Area ou Circularidade no código.")
        return None
    
    candidates = np.array(candidates, dtype="float32")

    pontos_ordenados = ordernar_pontos(candidates)

    img_debug = img.copy()
    cores = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]

    for i, pt in enumerate(pontos_ordenados):
        cX, cY = int(pt[0]), int(pt[1])
        cv2.circle(img_debug, (cX, cY), 8, cores[i], -1)
        cv2.putText(img_debug, str(i), (cX-15, cY-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cores[i], 2)

    cv2.imshow("Furos Encontrados (0=TL, 1=TR, 2=BR, 3=BL)", img_debug)
    cv2.imwrite("valido/output/teste_align_auto.png", img_debug)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return pontos_ordenados.tolist()



def align_auto_canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 40, 120)

    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    cv2.imshow("Debug: ", cv2.resize(edges_dilated, (800, 800)))

    cv2.imwrite("valido/output/teste_thresh.png", edges_dilated)

    contours, _ = cv2.findContours(edges_dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 600 < area < 3000:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0: continue

            circularidade = (4 * np.pi * area) / (perimeter * perimeter)

            if circularidade > 0.85:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    cor_central = gray[cY, cX]

                    if cor_central > 220:

                        ja_existe = False
                        for cand in candidates:
                            dist = np.sqrt((cX - cand[0])**2 + (cY - cand[1])**2)
                            if dist < 20:
                                ja_existe = True
                                break
                        if not ja_existe:
                            candidates.append([cX, cY])
    
    if len(candidates) != 4:
        img_error = img.copy()
        for cand in candidates:
            cv2.circle(img_error, (cand[0], cand[1]), 10, (0,0,255), -1)
        cv2.imshow("Debug: Achou %d formas erradas" % len(candidates), img_error)
        cv2.waitKey(0)
        cv2.imwrite("valido/output/teste_align_auto_canny.png", img_error)
        print(f"Erro Crítico: O algoritmo detectou {len(candidates)} furos. Precisamos de 4 exatos.")
        print("Calibre os ranges de Area ou Circularidade no código.")
        return None
    
    candidates = np.array(candidates, dtype="float32")

    pontos_ordenados = ordernar_pontos(candidates)

    img_debug = img.copy()
    cores = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]

    for i, pt in enumerate(pontos_ordenados):
        cX, cY = int(pt[0]), int(pt[1])
        cv2.circle(img_debug, (cX, cY), 8, cores[i], -1)
        cv2.putText(img_debug, str(i), (cX-15, cY-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cores[i], 2)

    cv2.imshow("Furos Encontrados (0=TL, 1=TR, 2=BR, 3=BL)", img_debug)
    cv2.imwrite("valido/output/teste_align_auto.png", img_debug)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return pontos_ordenados.tolist()


# teste!!!
def align_todos_circulos(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1. Blur Gaussiano leve para remover ruídos de alta frequência
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # 2. CANNY EDGE DETECTION: ALTA SENSIBILIDADE
    edges = cv2.Canny(blurred, 20, 60)

    # 3. Dilatação leve: Para emendar qualquer linha falhada do círculo
    kernel = np.ones((3,3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    # DEBUG VISUAL: Janela para ver as bordas geométricas detectadas
    cv2.imshow("Debug: Bordas Canny (Alta Sensibilidade)", cv2.resize(edges_dilated, (800, 800)))

    # 4. Achar os contornos nas linhas geométricas
    contours, _ = cv2.findContours(edges_dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 10: continue # Ignora ruídos ínfimos

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0: continue

        circularidade = (4 * np.pi * area) / (perimeter * perimeter)

        if circularidade > 0.5: 
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                # C. FILTRO ANTI-DUPLICATAS CORRIGIDO
                ja_existe = False
                for cand in candidates:
                    # Agora pegamos o X e Y corretamente de dentro do dicionário!
                    cand_X, cand_Y = cand['centro']
                    
                    dist = np.sqrt((cX - cand_X)**2 + (cY - cand_Y)**2)
                    if dist < 5: 
                        ja_existe = True
                        break
                        
                if not ja_existe:
                    # Guardamos o dicionário
                    candidates.append({
                        'centro': (cX, cY),
                        'area': area,
                        'circularidade': circularidade
                    })
    
    # D. DEBUG VISUAL E RESULTADO
    img_debug = img.copy()
    print(f"Total de formas circulares detectadas: {len(candidates)}")

    for i, cand in enumerate(candidates):
        cX, cY = cand['centro']
        area = cand['area']
        circ = cand['circularidade']

        # Desenha o centro com uma cor fixa (verde)
        cv2.circle(img_debug, (cX, cY), 5, (0, 255, 0), -1)

    cv2.imshow("Todos os Círculos Detectados", img_debug)
    cv2.imwrite("valido/output/teste_detectar_todos_os_circulos.png", img_debug)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return candidates """