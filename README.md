# PapeleriaApp

Aplicación de escritorio para la gestión de productos, ventas e inversiones en una papelería.

## Características principales
- Registro, edición y eliminación de productos.
- Cálculo automático de inversión y ganancia diaria.
- Navegación rápida entre campos usando Enter.
- Ventanas informativas y de confirmación con diseño coherente.
- Almacenamiento de datos en archivo JSON.

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/MrBrian04/PapeleriaApp.git
   ```
2. Asegúrate de tener Python 3 instalado.
3. Instala las dependencias si es necesario (Tkinter viene con Python estándar).
4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Uso
- Selecciona el campo de nombre con el mouse y navega el formulario con Enter.
- Los botones de la derecha permiten buscar, editar, eliminar productos y ver totales.
- Las ventanas informativas y de confirmación pueden cerrarse o confirmarse con Enter.

## Estructura del proyecto
- `main.py`: Punto de entrada de la aplicación.
- `controllers/`: Lógica de negocio (controlador de productos).
- `models/`: Definición del modelo de producto.
- `views/`: Interfaz gráfica y ventanas.
- `db/`: Almacenamiento de productos en JSON.
- `utils/`: Validaciones y formateadores auxiliares.

## Autor
- MrBrian04

---
¡Contribuciones y sugerencias son bienvenidas! 