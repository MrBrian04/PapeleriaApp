import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
from utils.formatters import formatear_pesos, formatear_numero
from utils.validators import ValidacionError
import tkinter.filedialog as filedialog
import openpyxl

class MainWindow:
    def __init__(self, root, controller):
        """
        Inicializa la ventana principal de la aplicación.
        Configura la interfaz, widgets y muestra el historial de productos.
        """
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

    def _formatear_entrada_precio(self, event, entry):
        """
        Formatea el valor de entrada mientras se escribe, agregando puntos cada 3 dígitos.
        Útil para mostrar precios en formato colombiano.
        """
        # Obtener el valor actual
        valor = entry.get().replace(".", "")
        # Formatear el número
        valor_formateado = formatear_numero(valor)
        # Actualizar el campo
        entry.delete(0, tk.END)
        entry.insert(0, valor_formateado)

    def _configurar_estilos(self):
        """
        Configura los estilos visuales de la aplicación (colores, fuentes, botones, etc).
        """
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
        """
        Crea y organiza todos los widgets principales de la interfaz.
        (Elimino el botón de tema claro/oscuro, solo tema claro)
        """
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg="#f0f2f5")
        # Frame de entrada con borde y sombra
        self.frame_entrada = tk.Frame(self.frame_principal, bg="#ffffff", bd=1, relief="solid")
        # Campos de entrada
        self._crear_campos_entrada()
        # Botones
        self._crear_botones()
        # Tabla de historial
        self._crear_tabla_historial()

    def _crear_campos_entrada(self):
        """
        Crea los campos de entrada para registrar un producto y gestiona la navegación con Enter.
        Ahora incluye validaciones visuales: resalta campos con error y muestra mensajes claros.
        """
        frame_campos = tk.Frame(self.frame_entrada, bg="#ffffff", padx=20, pady=10)
        frame_campos.grid_columnconfigure(0, weight=0)
        frame_campos.grid_columnconfigure(1, weight=0)
        frame_campos.grid_columnconfigure(2, weight=0)
        self.titulo_formulario = tk.Label(
            frame_campos,
            text="Registro de Producto",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        self.titulo_formulario.grid(row=0, column=0, columnspan=3, pady=10, sticky="")
        label_style = {"font": ("Arial", 10), "bg": "#ffffff", "pady": 5}
        entry_style = {"font": ("Arial", 10), "width": 25}
        # Labels e inputs
        # Nombre
        tk.Label(frame_campos, text="Nombre del producto:", **label_style).grid(row=2, column=0, sticky="e", pady=1)
        self.nombre_entry = tk.Entry(frame_campos, **entry_style)
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=1)
        self.nombre_error = tk.Label(frame_campos, text="", font=("Arial", 8), fg="#F44336", bg="#ffffff")
        self.nombre_error.grid(row=3, column=1, sticky="w")
        # Precio total
        tk.Label(frame_campos, text="Precio total ($):", **label_style).grid(row=4, column=0, sticky="e", pady=1)
        self.precio_entry = tk.Entry(frame_campos, **entry_style)
        self.precio_entry.grid(row=4, column=1, padx=10, pady=1)
        self.precio_entry.bind('<KeyRelease>', lambda e: self._formatear_entrada_precio(e, self.precio_entry))
        self.precio_error = tk.Label(frame_campos, text="", font=("Arial", 8), fg="#F44336", bg="#ffffff")
        self.precio_error.grid(row=5, column=1, sticky="w")
        # Cantidad
        tk.Label(frame_campos, text="Cantidad:", **label_style).grid(row=6, column=0, sticky="e", pady=1)
        self.cantidad_entry = tk.Entry(frame_campos, **entry_style)
        self.cantidad_entry.grid(row=6, column=1, padx=10, pady=1)
        self.cantidad_error = tk.Label(frame_campos, text="", font=("Arial", 8), fg="#F44336", bg="#ffffff")
        self.cantidad_error.grid(row=7, column=1, sticky="w")
        # Label para precio unitario al lado de cantidad
        self.label_precio_unitario = tk.Label(
            frame_campos,
            text="Precio unitario: -",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#2196F3"
        )
        self.label_precio_unitario.grid(row=6, column=2, padx=(10,0), pady=1)
        # Evento para calcular precio unitario y pasar foco
        def calcular_precio_unitario_y_saltar(event=None):
            try:
                precio_total = float(self.precio_entry.get().replace(".", ""))
                cantidad = int(self.cantidad_entry.get())
                if cantidad <= 0:
                    self.label_precio_unitario.config(text="Cantidad > 0")
                    return
                precio_unitario = precio_total / cantidad
                from utils.formatters import formatear_pesos
                self.label_precio_unitario.config(text=f"Precio unitario: {formatear_pesos(precio_unitario)}")
                self.precio_venta_entry.focus_set()
            except ValueError:
                self.label_precio_unitario.config(text="Precio unitario: -")
        self.cantidad_entry.bind('<Return>', calcular_precio_unitario_y_saltar)
        # Precio de venta
        tk.Label(frame_campos, text="Precio de venta ($):", **label_style).grid(row=8, column=0, sticky="e", pady=1)
        self.precio_venta_entry = tk.Entry(frame_campos, **entry_style)
        self.precio_venta_entry.grid(row=8, column=1, padx=10, pady=1)
        self.precio_venta_entry.bind('<KeyRelease>', lambda e: self._formatear_entrada_precio(e, self.precio_venta_entry))
        self.precio_venta_error = tk.Label(frame_campos, text="", font=("Arial", 8), fg="#F44336", bg="#ffffff")
        self.precio_venta_error.grid(row=9, column=1, sticky="w")
        # Botón agregar
        self.boton_agregar = tk.Button(
            frame_campos,
            text="Agregar Producto",
            command=self.agregar_producto,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2",
            relief="flat",
            highlightthickness=0
        )
        # Eliminar cualquier grid_columnconfigure(1, weight=1) agregado para el botón
        # Restaurar el grid del botón a su forma original
        self.boton_agregar.grid(row=10, column=1, columnspan=1, pady=(3, 0), sticky="n")
        self.frame_campos = frame_campos
        self.nombre_entry.bind('<Return>', lambda e: self.precio_entry.focus_set())
        self.precio_entry.bind('<Return>', lambda e: self.cantidad_entry.focus_set())
        self.cantidad_entry.bind('<Return>', calcular_precio_unitario_y_saltar)
        self.precio_venta_entry.bind('<Return>', lambda e: self.agregar_producto())

    def _crear_botones(self):
        """
        Crea los botones de acción (buscar, editar, eliminar, totales) en la interfaz.
        Ahora muestra los atajos de teclado al lado izquierdo de cada botón.
        Ajusta el alto de los botones para que sean un poco más compactos y no se corte el último botón.
        """
        self.atajos = {
            'Buscar producto': 'Ctrl+B',
            'Editar producto': 'Ctrl+E',
            'Eliminar producto': 'Ctrl+D',
            'Total Invertido del Día': 'Ctrl+I',
            'Ganancia Total del Día': 'Ctrl+G',
            'Agregar Producto': 'Ctrl+N',
            'Exportar a Excel': 'Ctrl+X',
        }
        self.atajos_funciones = {
            '<Control-b>': self.buscar_producto,
            '<Control-e>': self.editar_producto,
            '<Control-d>': self.eliminar_producto,
            '<Control-i>': self.calcular_total_inversion_dia,
            '<Control-g>': self.calcular_ganancia_total_dia,
            '<Control-n>': lambda: self.nombre_entry.focus_set(),
            '<Control-x>': self.exportar_excel,
        }
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
        # Botones de acción con atajos
        botones_derecha = [
            ("🔍 Buscar producto", self.buscar_producto, "#2196F3"),
            ("✏️ Editar producto", self.editar_producto, "#FF9800"),
            ("🗑️ Eliminar producto", self.eliminar_producto, "#F44336"),
            ("💰 Total Invertido del Día", self.calcular_total_inversion_dia, "#9C27B0"),
            ("📈 Ganancia Total del Día", self.calcular_ganancia_total_dia, "#4CAF50"),
            ("➕ Agregar Producto", self.agregar_producto, "#4CAF50"),
            ("📤 Exportar a Excel", self.exportar_excel, "#607d8b"),
        ]
        frame_grid = tk.Frame(self.frame_botones_derecha, bg="#f0f2f5")
        frame_grid.pack(fill=tk.Y, expand=False)
        for i, (texto, comando, color) in enumerate(botones_derecha):
            atajo = self.atajos.get(texto.replace('🔍 ','').replace('✏️ ','').replace('🗑️ ','').replace('💰 ','').replace('📈 ','').replace('➕ ','').replace('📤 ',''), "")
            label_atajo = tk.Label(
                frame_grid,
                text=atajo,
                font=("Arial", 9, "bold"),
                bg="#f0f2f5",
                fg="#888888",
                width=13,
                anchor="w"
            )
            label_atajo.grid(row=i, column=0, sticky="ew", padx=(0, 4), pady=3)
            boton = tk.Button(
                frame_grid,
                text=texto,
                command=comando,
                bg=color,
                fg="white",
                font=("Arial", 10),
                width=22,  # ancho suficiente para todo el texto
                pady=6,    # sutilmente más compacto
                bd=0,
                cursor="hand2",
                anchor="center"
            )
            boton.grid(row=i, column=1, sticky="w", padx=(0, 0), pady=3)
        frame_grid.grid_columnconfigure(1, weight=0)
        for atajo, funcion in self.atajos_funciones.items():
            self.root.bind(atajo, lambda e, f=funcion: f())

    def _crear_tabla_historial(self):
        """
        Crea la tabla donde se muestra el historial de productos registrados.
        """
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
        
        # Configurar el estilo para el resaltado
        self.historial.tag_configure('resaltado', background='#FFEB3B')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla_scroll, orient=tk.VERTICAL, command=self.historial.yview)
        self.historial.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        frame_tabla_scroll.pack(fill=tk.BOTH, expand=True)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

    def _configurar_layout(self):
        """
        Organiza el layout general de la ventana principal.
        """
        # Frame principal
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame de entrada (ahora usando grid para frame_campos)
        self.frame_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        # Posicionar frame_campos dentro de frame_entrada usando grid
        self.frame_campos.grid(row=0, column=0, sticky="nsew") # Asegurarse de que frame_campos se referencie correctamente
        self.frame_entrada.grid_rowconfigure(0, weight=1)
        self.frame_entrada.grid_columnconfigure(0, weight=1)
        
        # Frame de botones derecha
        self.frame_botones_derecha.pack(side=tk.RIGHT, fill=tk.Y)

    def calcular_precio_unitario(self):
        """
        Calcula y muestra el precio unitario basado en el precio total y la cantidad ingresada.
        """
        try:
            precio_total = float(self.precio_entry.get().replace(".", ""))
            cantidad = int(self.cantidad_entry.get())
            
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            precio_unitario = precio_total / cantidad
            self.label_precio_unitario.config(text=f"Precio unitario: {formatear_pesos(precio_unitario)}")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")

    def mostrar_errores_registro(self, errores):
        """
        Muestra los mensajes de error y resalta los campos con error en el registro de producto.
        """
        # Limpiar estilos previos
        for entry, label in [
            (self.nombre_entry, self.nombre_error),
            (self.precio_entry, self.precio_error),
            (self.cantidad_entry, self.cantidad_error),
            (self.precio_venta_entry, self.precio_venta_error)
        ]:
            entry.config(highlightthickness=0)
            label.config(text="")
        # Mostrar errores
        for campo, mensaje in errores.items():
            entry = getattr(self, f"{campo}_entry")
            label = getattr(self, f"{campo}_error")
            entry.config(highlightbackground="#F44336", highlightcolor="#F44336", highlightthickness=2)
            label.config(text=mensaje)

    def limpiar_errores_registro(self):
        """
        Limpia los mensajes y estilos de error en el registro de producto.
        """
        for entry, label in [
            (self.nombre_entry, self.nombre_error),
            (self.precio_entry, self.precio_error),
            (self.cantidad_entry, self.cantidad_error),
            (self.precio_venta_entry, self.precio_venta_error)
        ]:
            entry.config(highlightthickness=0)
            label.config(text="")

    def agregar_producto(self):
        """
        Agrega un nuevo producto al historial y actualiza la vista.
        Valida los datos y muestra errores si es necesario.
        """
        self.limpiar_errores_registro()
        errores = {}
        nombre = self.nombre_entry.get().strip()
        precio_total = self.precio_entry.get().replace(".", "")
        cantidad = self.cantidad_entry.get().strip()
        precio_venta = self.precio_venta_entry.get().replace(".", "")
        if not nombre:
            errores["nombre"] = "El nombre es obligatorio."
        if not precio_total or not precio_total.isdigit() or float(precio_total) <= 0:
            errores["precio"] = "Precio total inválido."
        if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
            errores["cantidad"] = "Cantidad inválida."
        if not precio_venta or not precio_venta.isdigit() or float(precio_venta) <= 0:
            errores["precio_venta"] = "Precio de venta inválido."
        if errores:
            self.mostrar_errores_registro(errores)
            return
        try:
            self.controller.agregar_producto(
                nombre,
                float(precio_total),
                int(cantidad),
                float(precio_venta)
            )
            self.limpiar_entradas()
            self.mostrar_historial()
        except ValidacionError as e:
            self.mostrar_errores_registro({"nombre": str(e)})
        except Exception as e:
            self.mostrar_errores_registro({"nombre": f"Error: {str(e)}"})

    def limpiar_entradas(self):
        """
        Limpia todos los campos de entrada del formulario de registro.
        """
        self.nombre_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_venta_entry.delete(0, tk.END)
        self.label_precio_unitario.config(text="Precio unitario: -")

    def mostrar_historial(self):
        """
        Muestra el historial de productos en la tabla principal.
        """
        # Limpiar tabla
        for item in self.historial.get_children():
            self.historial.delete(item)
        
        # Obtener productos y mostrarlos
        productos = self.controller.obtener_productos()
        for idx, producto in enumerate(productos):
            self.historial.insert("", tk.END, values=(
                idx + 1,  # ID comienza en 1
                producto.nombre,
                formatear_pesos(producto.precio_total),
                producto.cantidad,
                formatear_pesos(producto.precio_unitario),
                formatear_pesos(producto.precio_venta_usuario),
                formatear_pesos(producto.ganancia_unitaria),
                formatear_pesos(producto.ganancia_total),
                producto.fecha
            ))

    def buscar_producto(self):
        """
        Abre una ventana para buscar productos por ID, nombre o fecha.
        Permite buscar y resaltar productos en el historial.
        """
        ventana = self._crear_ventana_emergente("Buscar Producto", "500x350")
        def on_closing():
            for item in self.historial.get_children():
                self.historial.item(item, tags=())
            ventana.destroy()
        ventana.protocol("WM_DELETE_WINDOW", on_closing)
        frame_principal = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        frame_botones_inferior = tk.Frame(frame_principal, bg="#ffffff")
        frame_botones_inferior.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        boton_buscar = tk.Button(
            frame_botones_inferior,
            text="Buscar",
            command=lambda: realizar_busqueda(), 
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        boton_buscar.pack(side=tk.LEFT, padx=5)
        tk.Button(
            frame_botones_inferior,
            text="Cerrar",
            command=on_closing,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=5)
        frame_busqueda = tk.Frame(frame_principal, bg="#ffffff")
        frame_busqueda.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))
        frame_opciones = tk.Frame(frame_busqueda, bg="#ffffff")
        frame_opciones.pack(fill=tk.X, pady=(0, 10))
        tipo_busqueda = tk.StringVar(value="id")
        tk.Radiobutton(
            frame_opciones,
            text="Buscar por ID",
            variable=tipo_busqueda,
            value="id",
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(
            frame_opciones,
            text="Buscar por nombre",
            variable=tipo_busqueda,
            value="nombre",
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(
            frame_opciones,
            text="Buscar por fecha",
            variable=tipo_busqueda,
            value="fecha",
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=10)
        tk.Label(
            frame_busqueda,
            text="Ingrese el término de búsqueda:",
            font=("Arial", 10),
            bg="#ffffff"
        ).pack(pady=(0, 10))
        entry_busqueda = tk.Entry(frame_busqueda, font=("Arial", 10), width=30)
        entry_busqueda.pack(pady=(0, 20))
        frame_resultados = tk.Frame(frame_principal, bg="#ffffff")
        frame_resultados.pack(fill=tk.BOTH, expand=True)
        def realizar_busqueda(event=None):
            for widget in frame_resultados.winfo_children():
                widget.destroy()
            termino = entry_busqueda.get()
            tipo = tipo_busqueda.get()
            if tipo == "id":
                try:
                    id_busqueda = int(termino) - 1
                    productos = [self.controller.obtener_producto(id_busqueda)] if self.controller.obtener_producto(id_busqueda) else []
                    self.resaltar_producto_en_historial(id_busqueda)
                except ValueError:
                    productos = []
            elif tipo == "fecha":
                productos = self.controller.buscar_productos_por_fecha(termino)
                for idx, p in enumerate(self.controller.obtener_productos()):
                    if p.fecha == termino:
                        self.resaltar_producto_en_historial(idx)
            else:
                productos = self.controller.buscar_productos(termino)
                for idx, p in enumerate(self.controller.obtener_productos()):
                    if termino.lower() in p.nombre.lower():
                        self.resaltar_producto_en_historial(idx)
            if not productos:
                tk.Label(
                    frame_resultados,
                    text="No se encontraron productos",
                    font=("Arial", 10),
                    bg="#ffffff",
                    fg="#666666"
                ).pack()
                return
            for idx, producto in enumerate(productos):
                frame_producto = tk.Frame(frame_resultados, bg="#ffffff", pady=5)
                frame_producto.pack(fill=tk.X)
                tk.Label(
                    frame_producto,
                    text=f"ID: {idx + 1}",
                    font=("Arial", 10, "bold"),
                    bg="#ffffff"
                ).pack(anchor="w")
                tk.Label(
                    frame_producto,
                    text=f"Nombre: {producto.nombre}",
                    font=("Arial", 10, "bold"),
                    bg="#ffffff"
                ).pack(anchor="w")
                tk.Label(
                    frame_producto,
                    text=f"Precio total: {formatear_pesos(producto.precio_total)}",
                    font=("Arial", 10),
                    bg="#ffffff"
                ).pack(anchor="w")
                tk.Label(
                    frame_producto,
                    text=f"Cantidad: {producto.cantidad}",
                    font=("Arial", 10),
                    bg="#ffffff"
                ).pack(anchor="w")
                tk.Label(
                    frame_producto,
                    text=f"Precio unitario: {formatear_pesos(producto.precio_unitario)}",
                    font=("Arial", 10),
                    bg="#ffffff"
                ).pack(anchor="w")
                tk.Label(
                    frame_producto,
                    text=f"Precio venta: {formatear_pesos(producto.precio_venta_usuario)}",
                    font=("Arial", 10),
                    bg="#ffffff"
                ).pack(anchor="w")
                tk.Label(
                    frame_producto,
                    text=f"Ganancia unitaria: {formatear_pesos(producto.ganancia_unitaria)}",
                    font=("Arial", 10),
                    bg="#ffffff"
                ).pack(anchor="w")
                tk.Label(
                    frame_producto,
                    text=f"Ganancia total: {formatear_pesos(producto.ganancia_total)}",
                    font=("Arial", 10),
                    bg="#ffffff"
                ).pack(anchor="w")
        entry_busqueda.bind('<Return>', realizar_busqueda)
        ventana.bind('<Return>', realizar_busqueda)
        entry_busqueda.focus_set()

    def resaltar_producto_en_historial(self, id_producto):
        """
        Resalta un producto en la tabla de historial según su ID.
        """
        # Primero, quitar el resaltado de todos los items
        for item in self.historial.get_children():
            self.historial.item(item, tags=())
        # Luego, resaltar el producto encontrado solo si está en rango
        items = self.historial.get_children()
        if id_producto is not None and 0 <= id_producto < len(items):
            item = items[id_producto]
            self.historial.item(item, tags=('resaltado',))
            self.historial.see(item)  # Hacer scroll hasta el item resaltado

    def editar_producto(self):
        """
        Abre una ventana para ingresar el ID del producto a editar.
        Navegación y confirmación con Enter.
        """
        # --- NUEVA VENTANA PERSONALIZADA PARA INGRESAR ID ---
        ventana_id = self._crear_ventana_emergente("Editar Producto", "400x200")
        frame_id = tk.Frame(ventana_id, bg="#ffffff", padx=20, pady=20)
        frame_id.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame_id,
            text="Ingrese el ID del producto a editar:",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#FF9800"
        ).pack(pady=(0, 10))

        entry_id = tk.Entry(frame_id, font=("Arial", 12), width=10, justify="center")
        entry_id.pack(pady=(0, 20))
        entry_id.focus_set()

        label_error = tk.Label(frame_id, text="", font=("Arial", 10), fg="#F44336", bg="#ffffff")
        label_error.pack()

        def continuar(event=None):
            valor = entry_id.get()
            if not valor.isdigit() or int(valor) <= 0:
                label_error.config(text="Ingrese un ID válido (número mayor a 0)")
                return
            id_producto = int(valor) - 1
        producto = self.controller.obtener_producto(id_producto)
        if not producto:
                label_error.config(text="Producto no encontrado")
            return
            ventana_id.destroy()
            self._ventana_editar_producto(id_producto, producto)

        frame_botones = tk.Frame(frame_id, bg="#ffffff")
        frame_botones.pack(pady=10)
        tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana_id.destroy,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            frame_botones,
            text="Continuar",
            command=continuar,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=5)
        ventana_id.bind('<Return>', continuar)
        entry_id.focus_set()

    def _ventana_editar_producto(self, id_producto, producto):
        """
        Ventana de edición de producto. Permite navegar entre campos con Enter y guardar solo cuando el foco está en el botón Guardar.
        """
        ventana = self._crear_ventana_emergente("Editar Producto", "400x350")
        frame_formulario = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_formulario.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame_formulario, text="Nombre:", bg="#ffffff").pack(anchor="w")
        entry_nombre = tk.Entry(frame_formulario, width=30)
        entry_nombre.insert(0, producto.nombre)
        entry_nombre.pack(pady=(0, 10))
        tk.Label(frame_formulario, text="Precio total:", bg="#ffffff").pack(anchor="w")
        entry_precio = tk.Entry(frame_formulario, width=30)
        entry_precio.insert(0, formatear_numero(str(int(producto.precio_total))))
        entry_precio.pack(pady=(0, 10))
        entry_precio.bind('<KeyRelease>', lambda e: self._formatear_entrada_precio(e, entry_precio))
        tk.Label(frame_formulario, text="Cantidad:", bg="#ffffff").pack(anchor="w")
        entry_cantidad = tk.Entry(frame_formulario, width=30)
        entry_cantidad.insert(0, str(producto.cantidad))
        entry_cantidad.pack(pady=(0, 10))
        tk.Label(frame_formulario, text="Precio de venta:", bg="#ffffff").pack(anchor="w")
        entry_precio_venta = tk.Entry(frame_formulario, width=30)
        entry_precio_venta.insert(0, formatear_numero(str(int(producto.precio_venta_usuario))))
        entry_precio_venta.pack(pady=(0, 10))
        entry_precio_venta.bind('<KeyRelease>', lambda e: self._formatear_entrada_precio(e, entry_precio_venta))
        def guardar(event=None):
            try:
                nombre = entry_nombre.get()
                precio_total = float(entry_precio.get().replace(".", ""))
                cantidad = int(entry_cantidad.get())
                precio_venta = float(entry_precio_venta.get().replace(".", ""))
                self.controller.actualizar_producto(id_producto, nombre, precio_total, cantidad, precio_venta)
                ventana.destroy()
                self.mostrar_historial()
            except ValidacionError as e:
                messagebox.showerror("Error de validación", str(e))
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar el producto: {str(e)}")
        boton_guardar = tk.Button(
            frame_formulario,
            text="Guardar",
            command=guardar,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=20,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        boton_guardar.pack(pady=10)
        # Navegación por Enter
        entry_nombre.bind('<Return>', lambda e: entry_precio.focus_set())
        entry_precio.bind('<Return>', lambda e: entry_cantidad.focus_set())
        entry_cantidad.bind('<Return>', lambda e: entry_precio_venta.focus_set())
        entry_precio_venta.bind('<Return>', lambda e: boton_guardar.focus_set())
        boton_guardar.bind('<Return>', guardar)
        entry_nombre.focus_set()

    def eliminar_producto(self):
        """
        Abre una ventana para ingresar el ID del producto a eliminar.
        Navegación y confirmación con Enter.
        """
        # --- NUEVA VENTANA PERSONALIZADA PARA INGRESAR ID ---
        ventana_id = self._crear_ventana_emergente("Eliminar Producto", "400x200")
        frame_id = tk.Frame(ventana_id, bg="#ffffff", padx=20, pady=20)
        frame_id.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame_id,
            text="Ingrese el ID del producto a eliminar:",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#F44336"
        ).pack(pady=(0, 10))

        entry_id = tk.Entry(frame_id, font=("Arial", 12), width=10, justify="center")
        entry_id.pack(pady=(0, 20))
        entry_id.focus_set()

        label_error = tk.Label(frame_id, text="", font=("Arial", 10), fg="#F44336", bg="#ffffff")
        label_error.pack()

        def continuar(event=None):
            valor = entry_id.get()
            if not valor.isdigit() or int(valor) <= 0:
                label_error.config(text="Ingrese un ID válido (número mayor a 0)")
                return
            id_producto = int(valor) - 1
        producto = self.controller.obtener_producto(id_producto)
        if not producto:
                label_error.config(text="Producto no encontrado")
            return
            ventana_id.destroy()
            self._confirmar_eliminacion(id_producto, producto)

        frame_botones = tk.Frame(frame_id, bg="#ffffff")
        frame_botones.pack(pady=10)
        tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana_id.destroy,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            frame_botones,
            text="Continuar",
            command=continuar,
            bg="#F44336",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=5)
        ventana_id.bind('<Return>', continuar)
        entry_id.focus_set()

    def _confirmar_eliminacion(self, id_producto, producto):
        """
        Ventana de confirmación para eliminar un producto. Permite confirmar con Enter.
        """
        ventana = self._crear_ventana_emergente("Confirmar Eliminación", "400x200")
        frame_confirmacion = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_confirmacion.pack(fill=tk.BOTH, expand=True)
        tk.Label(
            frame_confirmacion,
            text=f"¿Está seguro de eliminar el producto '{producto.nombre}'?",
            font=("Arial", 10),
            bg="#ffffff",
            wraplength=350
        ).pack(pady=(0, 20))
        def confirmar_eliminacion(event=None):
            try:
                self.controller.eliminar_producto(id_producto)
                ventana.destroy()
                self.mostrar_historial()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el producto: {str(e)}")
        frame_botones = tk.Frame(frame_confirmacion, bg="#ffffff")
        frame_botones.pack(fill=tk.X, pady=10)
        tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana.destroy,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        boton_eliminar = tk.Button(
            frame_botones,
            text="Eliminar",
            command=confirmar_eliminacion,
            bg="#F44336",
            fg="white",
            font=("Arial", 10),
            width=15,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        boton_eliminar.pack(side=tk.RIGHT, padx=5)
        ventana.bind('<Return>', confirmar_eliminacion)
        ventana.focus_set()

    def calcular_total_inversion_dia(self):
        """
        Muestra una ventana informativa con el total invertido en el día actual.
        Se puede cerrar con Enter.
        """
        total = self.controller.calcular_total_inversion_dia()
        ventana = self._crear_ventana_emergente("Total Invertido", "400x300")
        frame_principal = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        tk.Label(
            frame_principal,
            text="💰 Total Invertido del Día",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#2196F3"
        ).pack(pady=(0, 20))
        tk.Label(
            frame_principal,
            text=formatear_pesos(total),
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#4CAF50"
        ).pack(pady=20)
        tk.Label(
            frame_principal,
            text="Este es el total de inversión realizada hoy",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#666666"
        ).pack(pady=10)
        boton_cerrar = tk.Button(
            frame_principal,
            text="Cerrar",
            command=ventana.destroy,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=20,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        boton_cerrar.pack(pady=20)
        # Permitir cerrar con Enter
        ventana.bind('<Return>', lambda event: ventana.destroy())
        boton_cerrar.focus_set()

    def calcular_ganancia_total_dia(self):
        """
        Muestra una ventana informativa con la ganancia total del día actual.
        Se puede cerrar con Enter.
        """
        ganancia = self.controller.calcular_ganancia_total_dia()
        ventana = self._crear_ventana_emergente("Ganancia Total", "400x300")
        frame_principal = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        tk.Label(
            frame_principal,
            text="📈 Ganancia Total del Día",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#4CAF50"
        ).pack(pady=(0, 20))
        tk.Label(
            frame_principal,
            text=formatear_pesos(ganancia),
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#4CAF50"
        ).pack(pady=20)
        tk.Label(
            frame_principal,
            text="Este es el total de ganancia obtenida hoy",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#666666"
        ).pack(pady=10)
        boton_cerrar = tk.Button(
            frame_principal,
            text="Cerrar",
            command=ventana.destroy,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            width=20,
            pady=5,
            bd=0,
            cursor="hand2"
        )
        boton_cerrar.pack(pady=20)
        # Permitir cerrar con Enter
        ventana.bind('<Return>', lambda event: ventana.destroy())
        boton_cerrar.focus_set()

    def exportar_excel(self):
        """
        Exporta el historial de productos a un archivo Excel (.xlsx), permitiendo elegir la ubicación.
        """
        productos = self.controller.obtener_productos()
        if not productos:
            messagebox.showinfo("Exportar a Excel", "No hay productos para exportar.")
            return
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar historial como Excel"
        )
        if not archivo:
            return
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Historial"
        columnas = [
            "ID", "Nombre", "Precio Total", "Cantidad", "Precio Unitario",
            "Precio Venta", "Ganancia U.", "Ganancia Total", "Fecha"
        ]
        ws.append(columnas)
        for idx, p in enumerate(productos):
            ws.append([
                idx + 1,
                p.nombre,
                p.precio_total,
                p.cantidad,
                p.precio_unitario,
                p.precio_venta_usuario,
                p.ganancia_unitaria,
                p.ganancia_total,
                p.fecha
            ])
        wb.save(archivo)
        messagebox.showinfo("Exportar a Excel", f"Historial exportado exitosamente a:\n{archivo}")

    def _crear_ventana_emergente(self, titulo, geometria):
        """
        Crea una ventana emergente personalizada con el título y tamaño especificados.
        """
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(geometria)
        ventana.configure(bg="#ffffff")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar la ventana
        ventana.update_idletasks()
        width = ventana.winfo_width()
        height = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (ventana.winfo_screenheight() // 2) - (height // 2)
        ventana.geometry(f'{width}x{height}+{x}+{y}')
        
        return ventana 