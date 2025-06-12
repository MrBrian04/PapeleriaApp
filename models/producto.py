import datetime
from utils.validators import validar_producto

class Producto:
    def __init__(self, nombre, precio_total, cantidad, precio_venta_usuario, fecha=None):
        """
        Inicializa un nuevo producto.
        
        Args:
            nombre (str): Nombre del producto
            precio_total (float): Precio total del producto
            cantidad (int): Cantidad del producto
            precio_venta_usuario (float): Precio de venta al usuario
            fecha (str, optional): Fecha del producto. Por defecto es la fecha actual
        """
        validar_producto(nombre, precio_total, cantidad, precio_venta_usuario)
        
        self.nombre = nombre
        self.precio_total = precio_total
        self.cantidad = cantidad
        self.precio_venta_usuario = precio_venta_usuario
        self.fecha = fecha or datetime.date.today().isoformat()
        self.precio_unitario = self.calcular_precio_unitario()
        self.ganancia_unitaria = self.calcular_ganancia_unitaria()
        self.ganancia_total = self.calcular_ganancia_total()

    def calcular_precio_unitario(self):
        """Calcula el precio unitario del producto."""
        return self.precio_total / self.cantidad if self.cantidad else 0

    def calcular_ganancia_unitaria(self):
        """Calcula la ganancia unitaria del producto."""
        return self.precio_venta_usuario - self.precio_unitario

    def calcular_ganancia_total(self):
        """Calcula la ganancia total del producto."""
        return self.ganancia_unitaria * self.cantidad

    def to_dict(self):
        """Convierte el producto a un diccionario para almacenamiento."""
        return {
            'nombre': self.nombre,
            'precio_total': self.precio_total,
            'cantidad': self.cantidad,
            'precio_venta_usuario': self.precio_venta_usuario,
            'fecha': self.fecha
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un producto desde un diccionario."""
        return cls(
            nombre=data['nombre'],
            precio_total=data['precio_total'],
            cantidad=data['cantidad'],
            precio_venta_usuario=data['precio_venta_usuario'],
            fecha=data['fecha']
        ) 