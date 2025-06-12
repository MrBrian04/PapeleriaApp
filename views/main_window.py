import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
from utils.formatters import formatear_pesos
from utils.validators import ValidacionError

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("PapeleriaApp")
        self.root.configure(bg="#f0f2f5")
        
        # Configurar el tamaño mínimo de la ventana
        self.root.minsize(1000, 600)
        
        # Configurar el estilo
        self._configurar_estilos()
        
        self._crear_widgets()
        self._configurar_layout()
        self.mostrar_historial()

    def _configurar_estilos(self):
        """Configura los estilos de la aplicación."""
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        style.configure("TLabel", background="#f0f2f5", font=("Arial", 10))
        style.configure("TEntry", padding=5)
        style.configure("Treeview", 
                       background="#ffffff",
                       fieldbackground="#ffffff",
                       rowheight=25)
        style.configure("Treeview.Heading", 
                       font=("Arial", 10, "bold"),
                       padding=5)

    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg="#f0f2f5")
        
        # Frame de entrada con borde y sombra
        self.frame_entrada = tk.Frame(self.frame_principal, bg="#ffffff", bd=1, relief="solid")
        
        # Título del formulario
        self.titulo_formulario = tk.Label(
            self.frame_entrada,
            text="Registro de Producto",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        
        # Campos de entrada
        self._crear_campos_entrada()
        
        # Botones
        self._crear_botones()
        
        # Tabla de historial
        self._crear_tabla_historial()

    def _crear_campos_entrada(self):
        """Crea los campos de entrada de datos."""
        # Frame para los campos
        frame_campos = tk.Frame(self.frame_entrada, bg="#ffffff", padx=20, pady=10)
        
        # Estilo común para las etiquetas
        label_style = {"font": ("Arial", 10), "bg": "#ffffff", "pady": 5}
        entry_style = {"font": ("Arial", 10), "width": 25}
        
        # Nombre
        tk.Label(frame_campos, text="Nombre del producto:", **label_style).grid(row=0, column=0, sticky="e", pady=5)
        self.nombre_entry = tk.Entry(frame_campos, **entry_style)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Precio total
        tk.Label(frame_campos, text="Precio total ($):", **label_style).grid(row=1, column=0, sticky="e", pady=5)
        self.precio_entry = tk.Entry(frame_campos, **entry_style)
        self.precio_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Cantidad y botón calcular en la misma fila
        tk.Label(frame_campos, text="Cantidad:", **label_style).grid(row=2, column=0, sticky="e", pady=5)
        self.cantidad_entry = tk.Entry(frame_campos, **entry_style)
        self.cantidad_entry.grid(row=2, column=1, padx=10, pady=5)
        
        self.boton_calcular = tk.Button(
            frame_campos,
            text="Calcular Precio Unitario",
            command=self.calcular_precio_unitario,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=20,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        self.boton_calcular.grid(row=2, column=2, padx=(10,0), pady=5)
        
        # Label para precio unitario (debajo del botón calcular)
        self.label_precio_unitario = tk.Label(
            frame_campos,
            text="Precio unitario: -",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2196F3"
        )
        self.label_precio_unitario.grid(row=3, column=2, pady=5)
        
        # Precio de venta
        tk.Label(frame_campos, text="Precio de venta ($):", **label_style).grid(row=4, column=0, sticky="e", pady=5)
        self.precio_venta_entry = tk.Entry(frame_campos, **entry_style)
        self.precio_venta_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Botón agregar (centrado)
        self.boton_agregar = tk.Button(
            frame_campos,
            text="Agregar Producto",
            command=self.agregar_producto,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=20,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        self.boton_agregar.grid(row=5, column=0, columnspan=3, pady=10)
        
        frame_campos.pack(fill="both", expand=True)
        self.frame_campos = frame_campos

    def _crear_botones(self):
        """Crea los botones de la interfaz."""
        # Frame para botones de la derecha
        self.frame_botones_derecha = tk.Frame(self.frame_principal, bg="#f0f2f5", padx=10)
        
        # Título de acciones
        tk.Label(
            self.frame_botones_derecha,
            text="Acciones",
            font=("Arial", 12, "bold"),
            bg="#f0f2f5",
            pady=10
        ).pack()
        
        # Botones de acción
        botones_derecha = [
            ("🔍 Buscar producto", self.buscar_producto, "#2196F3"),
            ("✏️ Editar producto", self.editar_producto, "#FF9800"),
            ("🗑️ Eliminar producto", self.eliminar_producto, "#F44336"),
            ("💰 Total Invertido del Día", self.calcular_total_inversion_dia, "#9C27B0"),
            ("📈 Ganancia Total del Día", self.calcular_ganancia_total_dia, "#4CAF50")
        ]
        
        for texto, comando, color in botones_derecha:
            tk.Button(
                self.frame_botones_derecha,
                text=texto,
                command=comando,
                bg=color,
                fg="white",
                font=("Arial", 10),
                width=25,
                pady=8,
                bd=0,
                cursor="hand2"
            ).pack(fill=tk.X, pady=5)

    def _crear_tabla_historial(self):
        """Crea la tabla de historial."""
        # Frame para la tabla
        frame_tabla = tk.Frame(self.frame_principal, bg="#f0f2f5")
        
        # Título de la aplicación
        tk.Label(
            frame_tabla,
            text="PapeleriaApp",
            font=("Arial", 16, "bold"),
            bg="#f0f2f5",
            pady=10
        ).pack()
        
        # Frame para la tabla y scrollbar
        frame_tabla_scroll = tk.Frame(frame_tabla, bg="#f0f2f5")
        
        columnas = (
            "ID", "Nombre", "Precio Total", "Cantidad", "Precio Unitario",
            "Precio Venta", "Ganancia U.", "Ganancia Total", "Fecha"
        )
        
        self.historial = ttk.Treeview(frame_tabla_scroll, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        for col in columnas:
            self.historial.heading(col, text=col)
            self.historial.column(col, anchor=tk.CENTER, width=110)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla_scroll, orient="vertical", command=self.historial.yview)
        self.historial.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        frame_tabla_scroll.pack(fill=tk.BOTH, expand=True, padx=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _configurar_layout(self):
        """Configura el layout de los widgets."""
        # Empaquetar el frame principal
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Empaquetar el frame de entrada
        self.frame_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Empaquetar los botones de la derecha
        self.frame_botones_derecha.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

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
        ventana = self._crear_ventana_emergente("Buscar Producto", "300x150")
        
        # Frame para el contenido
        frame_contenido = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_contenido.pack(fill="both", expand=True)
        
        # Etiqueta y campo de búsqueda
        tk.Label(
            frame_contenido,
            text="Ingrese nombre o fecha (YYYY-MM-DD):",
            font=("Arial", 10),
            bg="#ffffff"
        ).pack(pady=(0, 10))
        
        entry_busqueda = tk.Entry(frame_contenido, font=("Arial", 10), width=25)
        entry_busqueda.pack(pady=5)
        entry_busqueda.focus()
        
        def realizar_busqueda():
            criterio = entry_busqueda.get()
            if criterio:
                self.mostrar_historial()
                resultados = self.controller.buscar_productos(criterio)
                
                for item in self.historial.get_children():
                    valores = self.historial.item(item, "values")
                    if any(str(idx + 1) == valores[0] for idx, _ in resultados):
                        self.historial.item(item, tags=("resaltado",))
                    else:
                        self.historial.item(item, tags=())
                
                ventana.destroy()
        
        # Frame para botones
        frame_botones = tk.Frame(frame_contenido, bg="#ffffff")
        frame_botones.pack(pady=10)
        
        # Botones con estilo
        tk.Button(
            frame_botones,
            text="Buscar",
            command=realizar_busqueda,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=10,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana.destroy,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10),
            width=10,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Configurar tecla Enter para buscar
        entry_busqueda.bind('<Return>', lambda e: realizar_busqueda())

    def editar_producto(self):
        """Edita un producto existente."""
        try:
            id_producto = int(simpledialog.askstring("Editar", "Ingrese el ID del producto a editar:"))
            if not (1 <= id_producto <= len(self.controller.productos)):
                messagebox.showerror("Error", "Producto no encontrado.")
                return
            
            producto = self.controller.productos[id_producto - 1]
            ventana = self._crear_ventana_emergente(f"Editar Producto ID {id_producto}", "400x300")
            
            # Frame para el contenido
            frame_contenido = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
            frame_contenido.pack(fill="both", expand=True)
            
            # Estilo común
            label_style = {"font": ("Arial", 10), "bg": "#ffffff", "pady": 5}
            entry_style = {"font": ("Arial", 10), "width": 25}
            
            # Campos de edición
            tk.Label(frame_contenido, text="Nombre:", **label_style).grid(row=0, column=0, sticky="e", pady=5)
            entry_nombre = tk.Entry(frame_contenido, **entry_style)
            entry_nombre.insert(0, producto.nombre)
            entry_nombre.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(frame_contenido, text="Precio total ($):", **label_style).grid(row=1, column=0, sticky="e", pady=5)
            entry_precio = tk.Entry(frame_contenido, **entry_style)
            entry_precio.insert(0, str(producto.precio_total))
            entry_precio.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(frame_contenido, text="Cantidad:", **label_style).grid(row=2, column=0, sticky="e", pady=5)
            entry_cantidad = tk.Entry(frame_contenido, **entry_style)
            entry_cantidad.insert(0, str(producto.cantidad))
            entry_cantidad.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(frame_contenido, text="Precio venta ($):", **label_style).grid(row=3, column=0, sticky="e", pady=5)
            entry_precio_venta = tk.Entry(frame_contenido, **entry_style)
            entry_precio_venta.insert(0, str(producto.precio_venta_usuario))
            entry_precio_venta.grid(row=3, column=1, padx=10, pady=5)
            
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
            
            # Frame para botones
            frame_botones = tk.Frame(frame_contenido, bg="#ffffff", pady=20)
            frame_botones.grid(row=4, column=0, columnspan=2)
            
            # Botones con estilo
            tk.Button(
                frame_botones,
                text="Guardar",
                command=guardar,
                bg="#4CAF50",
                fg="white",
                font=("Arial", 10),
                width=15,
                pady=5,
                bd=0,
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                frame_botones,
                text="Cancelar",
                command=ventana.destroy,
                bg="#F44336",
                fg="white",
                font=("Arial", 10),
                width=15,
                pady=5,
                bd=0,
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
            
        except (ValueError, TypeError):
            return

    def eliminar_producto(self):
        """Elimina un producto."""
        try:
            id_producto = int(simpledialog.askstring("Eliminar", "Ingrese el ID del producto a eliminar:"))
            if not (1 <= id_producto <= len(self.controller.productos)):
                messagebox.showerror("Error", "Producto no encontrado.")
                return
                
            # Crear ventana de confirmación
            ventana = self._crear_ventana_emergente("Confirmar Eliminación", "300x150")
            
            # Frame para el contenido
            frame_contenido = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
            frame_contenido.pack(fill="both", expand=True)
            
            # Mensaje de confirmación
            tk.Label(
                frame_contenido,
                text="¿Está seguro que desea eliminar este producto?",
                font=("Arial", 10),
                bg="#ffffff",
                wraplength=250
            ).pack(pady=10)
            
            # Frame para botones
            frame_botones = tk.Frame(frame_contenido, bg="#ffffff")
            frame_botones.pack(pady=10)
            
            def confirmar_eliminacion():
                if self.controller.eliminar_producto(id_producto - 1):
                    self.mostrar_historial()
                    ventana.destroy()
            
            # Botones con estilo
            tk.Button(
                frame_botones,
                text="Eliminar",
                command=confirmar_eliminacion,
                bg="#F44336",
                fg="white",
                font=("Arial", 10),
                width=10,
                pady=5,
                bd=0,
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                frame_botones,
                text="Cancelar",
                command=ventana.destroy,
                bg="#9E9E9E",
                fg="white",
                font=("Arial", 10),
                width=10,
                pady=5,
                bd=0,
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=5)
            
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

    def _crear_ventana_emergente(self, titulo, geometria):
        """Crea una ventana emergente con estilo consistente."""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(geometria)
        ventana.configure(bg="#ffffff")
        ventana.resizable(False, False)
        
        # Centrar la ventana
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        # Hacer la ventana modal
        ventana.transient(self.root)
        ventana.grab_set()
        
        return ventana 