IGNORAR_PREFIXOS = (
    "TP_",
    # "UNK_HOLE_",
)

IGNORAR_REFS = {
    "FRAME1",
    "ORIGIN0",
}

IGNORAR_PACKAGES = {
    "FRAME",
    "TP-SP",
}

IGNORAR_VALORES = {
    "DNP",
}


def deve_ignorar(row: dict) -> bool:
    ref = row.get("Ref", "").strip().replace('"', "")
    val = row.get("Val", "").strip().replace('"', "")
    package = row.get("Package", "").strip().replace('"', "")
    side = row.get("Side", "").strip().lower().replace('"', "")

    if side != "top":
        return True

    if ref in IGNORAR_REFS:
        return True

    if any(ref.startswith(prefix) for prefix in IGNORAR_PREFIXOS):
        return True

    if package in IGNORAR_PACKAGES:
        return True

    if val in IGNORAR_VALORES:
        return True

    return False