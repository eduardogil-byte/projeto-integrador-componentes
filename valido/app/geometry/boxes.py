""" PACKAGE_SIZES_MM = {
    "C0603-ROUND": (1.6, 0.8),
    "R0603-ROUND": (1.6, 0.8),
    "0805": (2.0, 1.25),
    "CHIP-LED0805": (2.0, 1.25),
    "SOT-23": (3.0, 1.5),
    "SOT23-DBV": (3.0, 1.5),
    "SOT223": (6.5, 3.5),
    "MSOP08": (3.0, 3.0),
    "ATMEL_QFN32": (5.0, 5.0),
    "MLF32": (5.0, 5.0),
    "CAY16": (2.0, 1.25),
    "SMB": (4.6, 3.6),
    "MINIMELF": (3.6, 1.6),
    "PANASONIC_D": (6.3, 6.3),
    "TS42": (6.0, 3.5),
    "2X03": (7.5, 5.0),
    "2X02": (5.0, 5.0),
    "1X14-CUSTOM": (35.0, 2.5),
    "1X18-CUSTOM": (45.0, 2.5),
    "POWERSUPPLY_DC-21MM": (14.0, 9.0),
    "PN61729": (14.0, 12.0),
    "QS": (7.0, 3.0),
    "RESONATOR": (7.0, 3.0),
    "L1812": (4.6, 3.2),
    "CT_CN0603": (1.6, 0.8),
    "SJ": (2.0, 1.0),
}


def obter_tamanho_package_mm(package: str):
    return PACKAGE_SIZES_MM.get(package, (3.0, 3.0))
 """


PACKAGE_SIZES_MM = {
    # ==========================================
    # 1. PASSIVOS SMD (Padrão EIA Imperial)
    # Usado para Resistores, Capacitores, Indutores, LEDs
    # ==========================================
    "0201": (0.6, 0.3),
    "0402": (1.0, 0.5),
    "0603": (1.6, 0.8),
    "C0603-ROUND": (1.6, 0.8), # Variação do seu KiCad
    "R0603-ROUND": (1.6, 0.8), # Variação do seu KiCad
    "CT_CN0603": (1.6, 0.8),   # Variação do seu KiCad
    "0805": (2.0, 1.25),
    "CHIP-LED0805": (2.0, 1.25),
    "1206": (3.2, 1.6),
    "1210": (3.2, 2.5),
    "1812": (4.5, 3.2),
    "L1812": (4.5, 3.2),       # Variação do seu KiCad
    "2010": (5.0, 2.5),
    "2512": (6.3, 3.2),

    # ==========================================
    # 2. DIODOS E CAPACITORES DE TÂNTALO
    # ==========================================
    "MINIMELF": (3.5, 1.5),    # SOD-80 / LL34
    "MELF": (5.8, 2.4),
    "SMA": (4.3, 2.6),         # DO-214AC
    "SMB": (4.6, 3.6),         # DO-214AA
    "SMC": (6.9, 5.9),         # DO-214AB
    "SOD-123": (2.7, 1.6),
    "SOD-323": (1.7, 1.25),
    "SOD-523": (1.2, 0.8),
    "EIA-3216": (3.2, 1.6),    # Tântalo Tamanho A
    "EIA-3528": (3.5, 2.8),    # Tântalo Tamanho B
    "PANASONIC_D": (6.6, 6.6), # Cap. Eletrolítico SMD (Base 6.6x6.6, Corpo Dia 6.3)

    # ==========================================
    # 3. TRANSISTORES E REGULADORES DE TENSÃO
    # ==========================================
    "SOT-23": (2.9, 1.3),      # Corpo principal
    "SOT23-DBV": (2.9, 1.6),   # Variação
    "SOT-89": (4.5, 2.5),
    "SOT223": (6.5, 3.5),
    "TO-252": (6.5, 6.1),      # DPAK
    "TO-263": (10.2, 9.0),     # D2PAK

    # ==========================================
    # 4. CIRCUITOS INTEGRADOS (CIs / Chips)
    # ==========================================
    "SOIC-8": (4.9, 3.9),
    "SOIC-14": (8.65, 3.9),
    "SOIC-16": (9.9, 3.9),
    "TSSOP-8": (3.0, 4.4),
    "TSSOP-14": (5.0, 4.4),
    "MSOP08": (3.0, 3.0),
    "ATMEL_QFN32": (5.0, 5.0), # QFN de 32 pinos (Arduino)
    "MLF32": (5.0, 5.0),       # Sinônimo de QFN32
    "LQFP-32": (7.0, 7.0),     # Muito comum em microcontroladores
    "LQFP-48": (7.0, 7.0),
    "LQFP-64": (10.0, 10.0),

    # ==========================================
    # 5. COMPONENTES THROUGH-HOLE (PTH) E DIVERSOS
    # ==========================================
    "TO-92": (4.8, 3.8),       # Transistor clássico em pé
    "TO-220": (10.0, 4.5),     # Regulador clássico em pé
    "DIP-8": (9.8, 6.4),
    "DIP-14": (19.2, 6.4),
    "DIP-28": (35.6, 7.6),     # ATMEGA328P PTH Clássico
    
    # ==========================================
    # 6. CONECTORES E PEÇAS ESPECÍFICAS DO SEU PROJETO
    # ==========================================
    "CAY16": (3.2, 1.6),       # Resistor Array (1206 footprint)
    "TS42": (6.0, 3.5),        # Tactile Switch
    "2X02": (5.08, 5.08),      # Header 2x2 (Pitch 2.54mm)
    "2X03": (7.62, 5.08),      # Header 2x3 (ICSP Arduino - Pitch 2.54mm)
    "1X14-CUSTOM": (35.56, 2.54),
    "1X18-CUSTOM": (45.72, 2.54),
    "POWERSUPPLY_DC-21MM": (14.0, 9.0), # Jack P4 (Barrel Jack)
    "PN61729": (14.0, 12.0),   # Conector USB-B
    "QS": (7.0, 3.0),          # Cristal Oscilador
    "RESONATOR": (7.0, 3.0),   # Ressonador Cerâmico
    "SJ": (2.0, 1.0),          # Solder Jumper (Ponte de solda)
}

def obter_tamanho_package_mm(package: str):
    # Se o package não estiver no dicionário, retorna 3.0x3.0 como "tamanho de emergência"
    return PACKAGE_SIZES_MM.get(package, (3.0, 3.0))