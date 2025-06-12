def formatear_pesos(valor):
    """Formatea un valor numérico a formato de moneda."""
    return "${:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".") 