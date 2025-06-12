import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
from utils.formatters import formatear_pesos
from utils.validators import ValidacionError

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Control de Productos")
        self.root.configure(bg="#f4f6f8")
        
        self._crear_widgets()
        self._configurar_layout()
        self.mostrar_historial()

    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame de entrada
        self.frame_entrada = tk.Frame(self.root, bg="#f4f6f8")
        
        # Campos de entrada
        self._crear_campos_entrada()
        
        # Botones
        self._crear_botones()
        
        # Tabla de historial
        self._crear_tabla_historial()

    def _crear_campos_entrada(self):
        """Crea los campos de entrada de datos."""
        # Nombre
        tk.Label(self.frame_entrada, text="Nombre del producto:", bg="#f4f6f8").grid(row=0, column=0, sticky="e")
        self.nombre_entry = tk.Entry(self.frame_entrada)
        self.nombre_entry.grid(row=0, column=1)
        
        # Precio total
        tk.Label(self.frame_entrada, text="Precio total:", bg="#f4f6f8").grid(row=1, column=0, sticky="e")
        self.precio_entry = tk.Entry(self.frame_entrada)
        self.precio_entry.grid(row=1, column=1)
        
        # Cantidad
        tk.Label(self.frame_entrada, text="Cantidad:", bg="#f4f6f8").grid(row=2, column=0, sticky="e")
        self.cantidad_entry = tk.Entry(self.frame_entrada)
        self.cantidad_entry.grid(row=2, column=1)
        
        # Precio de venta
        tk.Label(self.frame_entrada, text="Precio de venta:", bg="#f4f6f8").grid(row=3, column=0, sticky="e")
        self.precio_venta_entry = tk.Entry(self.frame_entrada)
        self.precio_venta_entry.grid(row=3, column=1)
        
        # Label para precio unitario
        self.label_precio_unitario = tk.Label(self.frame_entrada, text="Precio unitario: -", bg="#f4f6f8")
        self.label_precio_unitario.grid(row=4, column=0, columnspan=2)

    def _crear_botones(self):
        """Crea los botones de la interfaz."""
        # Botones principales
        self.boton_calcular = tk.Button(
            self.frame_entrada,
            text="Calcular Precio Unitario",
            command=self.calcular_precio_unitario,
            bg="#cfe2f3"
        )
        self.boton_calcular.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.boton_agregar = tk.Button(
            self.frame_entrada,
            text="Agregar producto",
            command=self.agregar_producto,
            bg="#b6d7a8"
        )
        self.boton_agregar.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Frame para botones de la derecha
        self.frame_botones_derecha = tk.Frame(self.root, bg="#f4f6f8")
        
        botones_derecha = [
            ("Buscar producto", self.buscar_producto),
            ("Editar producto", self.editar_producto),
            ("Eliminar producto", self.eliminar_producto),
            ("Total Invertido del Día", self.calcular_total_inversion_dia),
            ("Ganancia Total del Día", self.calcular_ganancia_total_dia)
        ]
        
        for texto, comando in botones_derecha:
            tk.Button(
                self.frame_botones_derecha,
                text=texto,
                command=comando,
                bg="#ddd"
            ).pack(fill=tk.X, pady=2)

    def _crear_tabla_historial(self):
        """Crea la tabla de historial."""
        columnas = (
            "ID", "Nombre", "Precio Total", "Cantidad", "Precio Unitario",
            "Precio Venta", "Ganancia U.", "Ganancia Total", "Fecha"
        )
        
        self.historial = ttk.Treeview(self.root, columns=columnas, show="headings", height=15)
        
        for col in columnas:
            self.historial.heading(col, text=col)
            self.historial.column(col, anchor=tk.CENTER, width=110)
        
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.historial.yview)
        self.historial.configure(yscrollcommand=scrollbar.set)
        
        self.historial.tag_configure("resaltado", background="#fff2b2")

    def _configurar_layout(self):
        """Configura el layout de los widgets."""
        self.frame_entrada.pack(pady=10)
        self.frame_botones_derecha.pack(side=tk.RIGHT, padx=10, pady=10, anchor="n")
        self.historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.historial.yview_moveto(0)

    def calcular_precio_unitario(self):
        """Calcula y muestra el precio unitario."""
        try:
            precio_total = float(self.precio_entry.get())
            cantidad = int(self.cantidad_entry.get())
            if cantidad == 0:
                raise ValueError("La cantidad no puede ser 0")
            precio_unitario = precio_total / cantidad
            self.label_precio_unitario.config(text=f"Precio unitario: {formatear_pesos(precio_unitario)}")
        except ValueError as e:
            messagebox.showerror("Error", str(e) or "Por favor ingresa valores válidos en Precio total y Cantidad.")

    def agregar_producto(self):
        """Agrega un nuevo producto."""
        try:
            nombre = self.nombre_entry.get()
            precio_total = float(self.precio_entry.get())
            cantidad = int(self.cantidad_entry.get())
            precio_venta = float(self.precio_venta_entry.get())
            
            from models.producto import Producto
            producto = Producto(nombre, precio_total, cantidad, precio_venta)
            self.controller.agregar_producto(producto)
            
            self.limpiar_entradas()
            self.label_precio_unitario.config(text="Precio unitario: -")
            self.mostrar_historial()
            
        except ValidacionError as e:
            messagebox.showerror("Error de Validación", str(e))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")

    def limpiar_entradas(self):
        """Limpia los campos de entrada."""
        self.nombre_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_venta_entry.delete(0, tk.END)

    def mostrar_historial(self):
        """Muestra el historial de productos."""
        self.historial.delete(*self.historial.get_children())
        for idx, p in enumerate(self.controller.productos, start=1):
            self.historial.insert("", tk.END, values=(
                idx, p.nombre, formatear_pesos(p.precio_total), p.cantidad,
                formatear_pesos(p.precio_unitario), formatear_pesos(p.precio_venta_usuario),
                formatear_pesos(p.ganancia_unitaria), formatear_pesos(p.ganancia_total),
                p.fecha
            ))

    def buscar_producto(self):
        """Busca productos por nombre o fecha."""
        criterio = simpledialog.askstring("Buscar", "Ingrese nombre o fecha (YYYY-MM-DD):")
        if not criterio:
            return
        
        self.mostrar_historial()
        resultados = self.controller.buscar_productos(criterio)
        
        for item in self.historial.get_children():
            valores = self.historial.item(item, "values")
            if any(str(idx + 1) == valores[0] for idx, _ in resultados):
                self.historial.item(item, tags=("resaltado",))
            else:
                self.historial.item(item, tags=())

    def editar_producto(self):
        """Edita un producto existente."""
        try:
            id_producto = int(simpledialog.askstring("Editar", "Ingrese el ID del producto a editar:"))
            if not (1 <= id_producto <= len(self.controller.productos)):
                messagebox.showerror("Error", "Producto no encontrado.")
                return
            
            producto = self.controller.productos[id_producto - 1]
            ventana = tk.Toplevel(self.root)
            ventana.title(f"Editar Producto ID {id_producto}")
            
            # Campos de edición
            tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
            entry_nombre = tk.Entry(ventana)
            entry_nombre.insert(0, producto.nombre)
            entry_nombre.grid(row=0, column=1)
            
            tk.Label(ventana, text="Precio total:").grid(row=1, column=0)
            entry_precio = tk.Entry(ventana)
            entry_precio.insert(0, str(producto.precio_total))
            entry_precio.grid(row=1, column=1)
            
            tk.Label(ventana, text="Cantidad:").grid(row=2, column=0)
            entry_cantidad = tk.Entry(ventana)
            entry_cantidad.insert(0, str(producto.cantidad))
            entry_cantidad.grid(row=2, column=1)
            
            tk.Label(ventana, text="Precio venta:").grid(row=3, column=0)
            entry_precio_venta = tk.Entry(ventana)
            entry_precio_venta.insert(0, str(producto.precio_venta_usuario))
            entry_precio_venta.grid(row=3, column=1)
            
            def guardar():
                try:
                    from models.producto import Producto
                    nuevo_producto = Producto(
                        entry_nombre.get(),
                        float(entry_precio.get()),
                        int(entry_cantidad.get()),
                        float(entry_precio_venta.get()),
                        producto.fecha
                    )
                    if self.controller.editar_producto(id_producto - 1, nuevo_producto):
                        self.mostrar_historial()
                        ventana.destroy()
                except (ValueError, ValidacionError) as e:
                    messagebox.showerror("Error", str(e))
            
            tk.Button(ventana, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=5)
            
        except (ValueError, TypeError):
            return

    def eliminar_producto(self):
        """Elimina un producto."""
        try:
            id_producto = int(simpledialog.askstring("Eliminar", "Ingrese el ID del producto a eliminar:"))
            if self.controller.eliminar_producto(id_producto - 1):
                self.mostrar_historial()
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        except (ValueError, TypeError):
            return

    def calcular_total_inversion_dia(self):
        """Calcula el total invertido del día."""
        hoy = datetime.date.today().isoformat()
        total = self.controller.obtener_total_inversion_dia(hoy)
        messagebox.showinfo("Total Invertido", f"Inversión total del día: {formatear_pesos(total)}")

    def calcular_ganancia_total_dia(self):
        """Calcula la ganancia total del día."""
        hoy = datetime.date.today().isoformat()
        total = self.controller.obtener_ganancia_total_dia(hoy)
        messagebox.showinfo("Ganancia Total", f"Ganancia total del día: {formatear_pesos(total)}") 