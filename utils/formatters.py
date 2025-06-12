def formatear_pesos(valor):
    """Formatea un valor numérico a formato de pesos."""
    return f"${valor:,.2f}"

def formatear_numero(valor):
    """Formatea un número agregando puntos cada 3 dígitos."""
    if valor is None or valor == "":
        return ""
    # Eliminar puntos existentes y convertir a string
    valor_str = str(valor).replace(".", "")
    # Formatear con puntos cada 3 dígitos
    partes = []
    for i in range(len(valor_str), 0, -3):
        inicio = max(0, i - 3)
        partes.insert(0, valor_str[inicio:i])
    return ".".join(partes) 