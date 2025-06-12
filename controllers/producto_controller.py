import json
import os
from models.producto import Producto
import datetime

class ProductoController:
    def __init__(self):
        self.productos = []
        self.archivo_db = "db/productos.json"
        self.cargar_productos()

    def cargar_productos(self):
        """Carga los productos desde el archivo JSON."""
        try:
            if not os.path.exists("db"):
                os.makedirs("db")
            
            if os.path.exists(self.archivo_db):
                with open(self.archivo_db, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.productos = [Producto.from_dict(p) for p in datos]
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            self.productos = []

    def guardar_productos(self):
        """Guarda los productos en el archivo JSON."""
        try:
            if not os.path.exists("db"):
                os.makedirs("db")
            
            with open(self.archivo_db, 'w', encoding='utf-8') as f:
                json.dump([p.to_dict() for p in self.productos], f, indent=4)
        except Exception as e:
            print(f"Error al guardar productos: {e}")

    def obtener_productos(self):
        """Retorna la lista de todos los productos."""
        return self.productos

    def agregar_producto(self, nombre, precio_total, cantidad, precio_venta_usuario):
        """Agrega un nuevo producto."""
        producto = Producto(nombre, precio_total, cantidad, precio_venta_usuario)
        self.productos.append(producto)
        self.guardar_productos()
        return producto

    def obtener_producto(self, id_producto):
        """Obtiene un producto por su ID."""
        try:
            return self.productos[id_producto]
        except IndexError:
            return None

    def actualizar_producto(self, id_producto, nombre, precio_total, cantidad, precio_venta_usuario):
        """Actualiza un producto existente."""
        if 0 <= id_producto < len(self.productos):
            producto = Producto(nombre, precio_total, cantidad, precio_venta_usuario)
            self.productos[id_producto] = producto
            self.guardar_productos()
            return True
        return False

    def eliminar_producto(self, id_producto):
        """Elimina un producto."""
        if 0 <= id_producto < len(self.productos):
            self.productos.pop(id_producto)
            self.guardar_productos()
            return True
        return False

    def buscar_productos(self, criterio):
        """Busca productos por nombre o fecha."""
        criterio = criterio.lower()
        return [
            p for p in self.productos
            if criterio in p.nombre.lower() or criterio == p.fecha
        ]

    def calcular_total_inversion_dia(self):
        """Calcula el total invertido en el día actual."""
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        return sum(p.precio_total for p in self.productos if p.fecha == fecha_actual)

    def calcular_ganancia_total_dia(self):
        """Calcula la ganancia total del día actual."""
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        return sum(p.ganancia_total for p in self.productos if p.fecha == fecha_actual)

    def obtener_total_inversion_dia(self, fecha):
        """Calcula el total invertido en un día específico."""
        return sum(p.precio_total for p in self.productos if p.fecha == fecha)

    def obtener_ganancia_total_dia(self, fecha):
        """Calcula la ganancia total de un día específico."""
        return sum(p.ganancia_total for p in self.productos if p.fecha == fecha) 