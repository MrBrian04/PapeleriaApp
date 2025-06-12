import json
import os
from models.producto import Producto

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

    def agregar_producto(self, producto):
        """Agrega un nuevo producto."""
        self.productos.append(producto)
        self.guardar_productos()

    def editar_producto(self, indice, producto):
        """Edita un producto existente."""
        if 0 <= indice < len(self.productos):
            self.productos[indice] = producto
            self.guardar_productos()
            return True
        return False

    def eliminar_producto(self, indice):
        """Elimina un producto."""
        if 0 <= indice < len(self.productos):
            self.productos.pop(indice)
            self.guardar_productos()
            return True
        return False

    def buscar_productos(self, criterio):
        """Busca productos por nombre o fecha."""
        criterio = criterio.lower()
        return [
            (i, p) for i, p in enumerate(self.productos)
            if criterio in p.nombre.lower() or criterio == p.fecha
        ]

    def obtener_total_inversion_dia(self, fecha):
        """Calcula el total invertido en un día específico."""
        return sum(p.precio_total for p in self.productos if p.fecha == fecha)

    def obtener_ganancia_total_dia(self, fecha):
        """Calcula la ganancia total de un día específico."""
        return sum(p.ganancia_total for p in self.productos if p.fecha == fecha) 