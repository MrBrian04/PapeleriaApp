class ValidacionError(Exception):
    """Excepción personalizada para errores de validación."""
    pass

def validar_producto(nombre, precio_total, cantidad, precio_venta):
    """
    Valida los datos de un producto.
    
    Args:
        nombre (str): Nombre del producto
        precio_total (float): Precio total del producto
        cantidad (int): Cantidad del producto
        precio_venta (float): Precio de venta del producto
    
    Raises:
        ValidacionError: Si algún dato no es válido
    """
    if not nombre or not nombre.strip():
        raise ValidacionError("El nombre del producto no puede estar vacío")
    
    if precio_total < 0:
        raise ValidacionError("El precio total no puede ser negativo")
    
    if cantidad <= 0:
        raise ValidacionError("La cantidad debe ser mayor a 0")
    
    if precio_venta < 0:
        raise ValidacionError("El precio de venta no puede ser negativo")
    
    if precio_venta < precio_total / cantidad:
        raise ValidacionError("El precio de venta no puede ser menor al precio unitario") 