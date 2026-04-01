import cv2
import numpy as np

# Variável global para guardar os cliques do mouse
pontos_foto = []

# Função que o OpenCV chama toda vez que o mouse interagir com a janela
def capturar_cliques(event, x, y, flags, param):
    global pontos_foto
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pontos_foto) < 4:
            pontos_foto.append([x, y])
            # Desenha um bolinha verde onde você clicou
            cv2.circle(img_display, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Clique nos 4 furos", img_display)
            print(f"Ponto {len(pontos_foto)} capturado: ({x}, {y})")

# 1. Carregar a imagem (Coloque o nome da sua foto aqui)
caminho_imagem = r"arduino_uno_r3_smd_teste.jpeg" # <--- MUDE ISSO SE NECESSÁRIO
img_original = cv2.imread(caminho_imagem)

# Se a foto do celular for de 12 Megapixels, ela não vai caber na tela.
# Vamos reduzi-la pela metade apenas para facilitar o clique (opcional)
img_display = cv2.resize(img_original, (0,0), fx=0.5, fy=0.5) 

# 2. Configurar a janela e o mouse
cv2.imshow("Clique nos 4 furos", img_display)
cv2.setMouseCallback("Clique nos 4 furos", capturar_cliques)

print("==== INSTRUÇÕES ====")
print("Clique no centro dos 4 furos na imagem, EXATAMENTE nesta ordem:")
print("1. Furo Superior Esquerdo (Perto do J2 / UNK_HOLE_2)")
print("2. Furo Superior Direito (Perto do ICSP0 / UNK_HOLE_0)")
print("3. Furo Inferior Direito (Perto do J1 / UNK_HOLE_1)")
print("4. Furo Inferior Esquerdo (Perto do X1 / UNK_HOLE_3)")
print("Pressione qualquer tecla após dar os 4 cliques para alinhar...")

# Fica esperando o usuário clicar e apertar uma tecla
cv2.waitKey(0)
cv2.destroyAllWindows()

# 3. O Alinhamento Matemático (Transformação)
if len(pontos_foto) == 4:
    # Se diminuímos a imagem para exibir, precisamos multiplicar os pontos por 2
    # para bater com o tamanho real da imagem original
    pontos_foto_np = np.float32(pontos_foto) * 2.0 

    # --- LÓGICA DO SEU CSV ---
    # Coordenadas em MM do seu arquivo:
    # Sup_Esq: H2 (129.45, -80.87)
    # Sup_Dir: H0 (180.25, -96.11)
    # Inf_Dir: H1 (180.25, -124.05)
    # Inf_Esq: H3 (128.18, -129.13)
    
    # Para alinhar com seu código atual, usamos o min_x e max_y para ancorar
    min_x = 128.18  
    max_y = -80.87  
    
    escala = 20.0 # 20 pixels para cada 1 mm (Garante uma imagem em alta resolução)
    margem = 50   # 50 pixels de borda
    
    # Aplicando a SUA fórmula: margem_px + (x_mm - min_x) * escala
    def calc_px(x_mm, y_mm):
        x_px = margem + (x_mm - min_x) * escala
        y_px = margem + (max_y - y_mm) * escala # (Lembrando que inverte o Y)
        return [x_px, y_px]

    # Gerando os pontos de destino (onde os furos DEVEM ir na imagem final)
    pt_sup_esq = calc_px(129.45, -80.87)
    pt_sup_dir = calc_px(180.25, -96.11)
    pt_inf_dir = calc_px(180.25, -124.05)
    pt_inf_esq = calc_px(128.18, -129.13)

    pontos_csv = np.float32([pt_sup_esq, pt_sup_dir, pt_inf_dir, pt_inf_esq])

    # 4. A MÁGICA: Calcula a matriz de endireitamento e aplica na imagem original
    matriz_perspectiva = cv2.getPerspectiveTransform(pontos_foto_np, pontos_csv)
    
    # Calcula tamanho final da imagem baseada nos pontos extremos
    largura_final = int(margem*2 + (185.0 - min_x) * escala)
    altura_final = int(margem*2 + (max_y - (-135.0)) * escala)

    img_alinhada = cv2.warpPerspective(img_original, matriz_perspectiva, (largura_final, altura_final))

    # 5. Salva e mostra o resultado
    cv2.imwrite("placa_alinhada.png", img_alinhada)
    print("Sucesso! Imagem endireitada salva como 'placa_alinhada.png'.")
    
    # Mostra a foto final em um tamanho que cabe na tela
    cv2.imshow("Resultado Final", cv2.resize(img_alinhada, (0,0), fx=0.4, fy=0.4))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print(f"Erro: Você clicou em {len(pontos_foto)} pontos. Eram necessários 4. Rode novamente.")