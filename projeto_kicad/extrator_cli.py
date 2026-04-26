import subprocess
import pcbnew
import csv
import os

def extrair_bom_csv(caminho_pcb):
    pasta_base = os.path.dirname(caminho_pcb)
    caminho = "projeto_kicad/output"
    caminho_csv = os.path.join(caminho, "bom_temp.csv")

    comando = [
        r"C:\Users\486973624\AppData\Local\Programs\KiCad\9.0\bin\kicad-cli.exe", 
        "pcb",
        "export",
        "pos",
        "--format", "csv",
        "--units", "mm",
        "--output", caminho_csv,
        caminho_pcb
    ]


    try:
        subprocess.run(comando, check=True, capture_output=True, text=True)

        componentes = []

        with open(caminho_csv, mode="r", encoding="utf-8-sig") as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)

            for linha in leitor:
                ref = linha.get('Ref', '').strip()
                val = linha.get('Val', '').strip()

                if ref:
                    componentes.append({
                        'ref': ref,
                        'valor': val,
                        'posX': linha.get('PosX'),
                        'posY': linha.get('PosY'),
                        'lado': linha.get('Side'),
                        'dados_extras': linha
                    })
        
        return componentes

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro na execução do kicad-cli: {e.stderr}")

    except FileNotFoundError:
        raise RuntimeError("O executável 'kicad-cli' não foi encontrado no sistema.")
    
    

def extrair_dados_geometria(caminho_pcb):
    if not os.path.exists(caminho_pcb):
        raise FileNotFoundError(f"Arquivo de placa não encontrado: {caminho_pcb}")
    
    try:
        board = pcbnew.LoadBoard(caminho_pcb)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar a placa com pcbnew: {e}")
    

    dados_footprints = []

    for footprint in board.GetFootprints():
        if "FRAME" in footprint.GetReference():
            continue
        ref = footprint.GetReference()

        pos = footprint.GetPosition()
        pos_x = pos.x / 1000000.0
        pos_y = -(pos.y / 1000000.0)

        # Rotação e Lado
        rotacao = footprint.GetOrientationDegrees()
        lado = "top" if footprint.GetLayer() == pcbnew.F_Cu else "bottom"

        package = str(footprint.GetFPID().GetLibItemName())

        # 3. A NOVA MÁGICA: Obtendo o tamanho APENAS pelos Pads (Ilhas de solda)
        # Isso ignora os textos que deixavam as caixas gigantes.
        pads = footprint.Pads()
        
        if pads:
            # Pega as medidas do primeiro pad como ponto de partida
            primeiro_pad_bbox = pads[0].GetBoundingBox()
            min_x = primeiro_pad_bbox.GetLeft()
            max_x = primeiro_pad_bbox.GetRight()
            min_y = primeiro_pad_bbox.GetTop()
            max_y = primeiro_pad_bbox.GetBottom()
            
            # Itera sobre os outros pads para expandir a caixa apenas se necessário
            for pad in pads[1:]:
                p_bbox = pad.GetBoundingBox()
                min_x = min(min_x, p_bbox.GetLeft())
                max_x = max(max_x, p_bbox.GetRight())
                min_y = min(min_y, p_bbox.GetTop())
                max_y = max(max_y, p_bbox.GetBottom())
                
            largura = (max_x - min_x) / 1000000.0
            altura = (max_y - min_y) / 1000000.0
        else:
            # Fallback: Se a peça não tiver pads, usa a caixa inteira
            bbox = footprint.GetBoundingBox()
            largura = bbox.GetWidth() / 1000000.0
            altura = bbox.GetHeight() / 1000000.0

        dados_footprints.append({
            'Ref': ref,
            "Package": package,
            'PosX': round(pos_x, 4),
            'PosY': round(pos_y, 4),
            'width_mm': round(largura, 4),
            'height_mm': round(altura, 4),
            'Rot': rotacao,
            'Side': lado
        })

    return dados_footprints

def salvar_geometria_csv(dados, caminho_saida):
    """
    Recebe a lista de dicionários e salva em um arquivo CSV.
    """
    if not dados:
        print("Nenhum dado para salvar.")
        return

    # Extrai os nomes das colunas a partir das chaves do primeiro dicionário
    colunas = dados[0].keys()

    try:
        # 'utf-8-sig' é excelente para que o Excel no Windows abra o arquivo com acentos corretos
        with open(caminho_saida, mode='w', encoding='utf-8-sig', newline='') as arquivo_csv:
            escritor = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            
            # Escreve o cabeçalho
            escritor.writeheader()
            
            # Escreve todas as linhas
            escritor.writerows(dados)
            
        print(f"Sucesso! Arquivo salvo em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")
