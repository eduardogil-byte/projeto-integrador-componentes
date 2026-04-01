import cv2


def carregar_imagem(caminho: str):
    img = cv2.imread(caminho)
    if img is None:
        raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho}")
    return img