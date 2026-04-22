import pcbnew
import os

def extrair_dados_geometria(caminho_pcb):
    if not os.path.exists(caminho_pcb):
        raise FileNotFoundError(f"Arquivo de placa não encontrado: {caminho_pcb}")
    
    try:
        board = pcbnew.LoadBoard(caminho_pcb)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar a placa com pcbnew: {e}")
    

    dados_footprints = []

    for footprint in board.GetFootprints():
        ref = footprint.GetReference()

        pos = footprint.GetPosition()
        pos_x = pos.x / 1000000.0
        pos_y = pos.y / 1000000.0

        # Rotação e Lado
        rotacao = footprint.GetOrientationDegrees()
        lado = "top" if footprint.GetLayer() == pcbnew.F_Cu else "bottom"

        package = str(footprint.GetFPID().GetLibItemName())

        # 3. A MÁGICA: Obtendo o tamanho real (Bounding Box)
        # O Bounding Box engloba todo o desenho do footprint (pads, silk, courtyard)
        bbox = footprint.GetBoundingBox()
        largura = bbox.GetWidth() / 1000000.0
        altura = bbox.GetHeight() / 1000000.0

        dados_footprints.append({
            'ref': ref,
            "package": package,
            'pos_x': round(pos_x, 4),
            'pos_y': round(pos_y, 4),
            'largura_mm': round(largura, 4),
            'altura_mm': round(altura, 4),
            'rotacao': rotacao,
            'lado': lado
        })

    return dados_footprints
