from datetime import datetime

class Controller:
    def buscar_productos_por_fecha(self, fecha):
        """Busca productos por fecha."""
        try:
            # Convertir la fecha de entrada a datetime
            fecha_busqueda = datetime.strptime(fecha, "%Y-%m-%d").date()
            return [p for p in self.productos if p.fecha == fecha_busqueda.strftime("%Y-%m-%d")]
        except ValueError:
            return [] 