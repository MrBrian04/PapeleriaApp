import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
from utils.formatters import formatear_pesos, formatear_numero
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

    def _formatear_entrada_precio(self, event, entry):
        """Formatea el valor de entrada mientras se escribe."""
        # Obtener el valor actual
        valor = entry.get().replace(".", "")
        # Formatear el número
        valor_formateado = formatear_numero(valor)
        # Actualizar el campo
        entry.delete(0, tk.END)
        entry.insert(0, valor_formateado)

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
        self.precio_entry.bind('<KeyRelease>', lambda e: self._formatear_entrada_precio(e, self.precio_entry))
        
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
        self.precio_venta_entry.bind('<KeyRelease>', lambda e: self._formatear_entrada_precio(e, self.precio_venta_entry))
        
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
        scrollbar = ttk.Scrollbar(frame_tabla_scroll, orient=tk.VERTICAL, command=self.historial.yview)
        self.historial.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        frame_tabla_scroll.pack(fill=tk.BOTH, expand=True)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

    def _configurar_layout(self):
        """Configura el layout de la interfaz."""
        # Frame principal
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame de entrada
        self.frame_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.titulo_formulario.pack()
        
        # Frame de botones derecha
        self.frame_botones_derecha.pack(side=tk.RIGHT, fill=tk.Y)

    def calcular_precio_unitario(self):
        """Calcula el precio unitario basado en el precio total y la cantidad."""
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

    def agregar_producto(self):
        """Agrega un nuevo producto."""
        try:
            # Obtener valores de los campos y eliminar puntos
            nombre = self.nombre_entry.get()
            precio_total = float(self.precio_entry.get().replace(".", ""))
            cantidad = int(self.cantidad_entry.get())
            precio_venta = float(self.precio_venta_entry.get().replace(".", ""))
            
            # Agregar el producto
            self.controller.agregar_producto(nombre, precio_total, cantidad, precio_venta)
            
            # Limpiar campos y actualizar historial
            self.limpiar_entradas()
            self.mostrar_historial()
            
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
        except ValidacionError as e:
            messagebox.showerror("Error de validación", str(e))
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar el producto: {str(e)}")

    def limpiar_entradas(self):
        """Limpia todos los campos de entrada."""
        self.nombre_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_venta_entry.delete(0, tk.END)
        self.label_precio_unitario.config(text="Precio unitario: -")

    def mostrar_historial(self):
        """Muestra el historial de productos en la tabla."""
        # Limpiar tabla
        for item in self.historial.get_children():
            self.historial.delete(item)
        
        # Obtener productos y mostrarlos
        productos = self.controller.obtener_productos()
        for idx, producto in enumerate(productos):
            self.historial.insert("", tk.END, values=(
                idx,  # Usar el índice como ID
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
        """Abre una ventana para buscar productos."""
        ventana = self._crear_ventana_emergente("Buscar Producto", "400x200")
        
        # Frame para la búsqueda
        frame_busqueda = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_busqueda.pack(fill=tk.BOTH, expand=True)
        
        # Campo de búsqueda
        tk.Label(
            frame_busqueda,
            text="Ingrese el nombre del producto:",
            font=("Arial", 10),
            bg="#ffffff"
        ).pack(pady=(0, 10))
        
        entry_busqueda = tk.Entry(frame_busqueda, font=("Arial", 10), width=30)
        entry_busqueda.pack(pady=(0, 20))
        
        # Frame para resultados
        frame_resultados = tk.Frame(frame_busqueda, bg="#ffffff")
        frame_resultados.pack(fill=tk.BOTH, expand=True)
        
        def realizar_busqueda():
            # Limpiar resultados anteriores
            for widget in frame_resultados.winfo_children():
                widget.destroy()
            
            # Realizar búsqueda
            nombre = entry_busqueda.get()
            productos = self.controller.buscar_productos(nombre)
            
            if not productos:
                tk.Label(
                    frame_resultados,
                    text="No se encontraron productos",
                    font=("Arial", 10),
                    bg="#ffffff",
                    fg="#666666"
                ).pack()
                return
            
            # Mostrar resultados
            for producto in productos:
                frame_producto = tk.Frame(frame_resultados, bg="#ffffff", pady=5)
                frame_producto.pack(fill=tk.X)
                
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
                
                tk.Label(
                    frame_producto,
                    text=f"Fecha: {producto.fecha}",
                    font=("Arial", 10),
                    bg="#ffffff"
                ).pack(anchor="w")
                
                # Separador
                ttk.Separator(frame_resultados, orient="horizontal").pack(fill=tk.X, pady=5)
        
        # Botón buscar
        tk.Button(
            frame_busqueda,
            text="Buscar",
            command=realizar_busqueda,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            width=20,
            pady=5,
            bd=0,
            cursor="hand2"
        ).pack(pady=10)

    def editar_producto(self):
        """Abre una ventana para editar un producto."""
        # Obtener el ID del producto a editar
        id_producto = simpledialog.askinteger("Editar Producto", "Ingrese el ID del producto a editar:")
        if id_producto is None:
            return
        
        # Obtener el producto
        producto = self.controller.obtener_producto(id_producto)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        # Crear ventana de edición
        ventana = self._crear_ventana_emergente("Editar Producto", "400x300")
        
        # Frame para el formulario
        frame_formulario = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_formulario.pack(fill=tk.BOTH, expand=True)
        
        # Campos de edición
        tk.Label(frame_formulario, text="Nombre:", bg="#ffffff").pack(anchor="w")
        entry_nombre = tk.Entry(frame_formulario, width=30)
        entry_nombre.insert(0, producto.nombre)
        entry_nombre.pack(pady=(0, 10))
        
        tk.Label(frame_formulario, text="Precio total:", bg="#ffffff").pack(anchor="w")
        entry_precio = tk.Entry(frame_formulario, width=30)
        entry_precio.insert(0, str(producto.precio_total))
        entry_precio.pack(pady=(0, 10))
        
        tk.Label(frame_formulario, text="Cantidad:", bg="#ffffff").pack(anchor="w")
        entry_cantidad = tk.Entry(frame_formulario, width=30)
        entry_cantidad.insert(0, str(producto.cantidad))
        entry_cantidad.pack(pady=(0, 10))
        
        tk.Label(frame_formulario, text="Precio de venta:", bg="#ffffff").pack(anchor="w")
        entry_precio_venta = tk.Entry(frame_formulario, width=30)
        entry_precio_venta.insert(0, str(producto.precio_venta_usuario))
        entry_precio_venta.pack(pady=(0, 10))
        
        def guardar():
            try:
                # Obtener valores
                nombre = entry_nombre.get()
                precio_total = float(entry_precio.get())
                cantidad = int(entry_cantidad.get())
                precio_venta = float(entry_precio_venta.get())
                
                # Actualizar producto
                self.controller.actualizar_producto(id_producto, nombre, precio_total, cantidad, precio_venta)
                
                # Cerrar ventana y actualizar historial
                ventana.destroy()
                self.mostrar_historial()
                
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            except ValidacionError as e:
                messagebox.showerror("Error de validación", str(e))
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar el producto: {str(e)}")
        
        # Botón guardar
        tk.Button(
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
        ).pack(pady=10)

    def eliminar_producto(self):
        """Abre una ventana para eliminar un producto."""
        # Obtener el ID del producto a eliminar
        id_producto = simpledialog.askinteger("Eliminar Producto", "Ingrese el ID del producto a eliminar:")
        if id_producto is None:
            return
        
        # Obtener el producto
        producto = self.controller.obtener_producto(id_producto)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        # Crear ventana de confirmación
        ventana = self._crear_ventana_emergente("Confirmar Eliminación", "400x200")
        
        # Frame para la confirmación
        frame_confirmacion = tk.Frame(ventana, bg="#ffffff", padx=20, pady=20)
        frame_confirmacion.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje de confirmación
        tk.Label(
            frame_confirmacion,
            text=f"¿Está seguro de eliminar el producto '{producto.nombre}'?",
            font=("Arial", 10),
            bg="#ffffff",
            wraplength=350
        ).pack(pady=(0, 20))
        
        def confirmar_eliminacion():
            try:
                # Eliminar producto
                self.controller.eliminar_producto(id_producto)
                
                # Cerrar ventana y actualizar historial
                ventana.destroy()
                self.mostrar_historial()
                
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el producto: {str(e)}")
        
        # Botones de confirmación
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
        
        tk.Button(
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
        ).pack(side=tk.RIGHT, padx=5)

    def calcular_total_inversion_dia(self):
        """Calcula el total invertido en el día actual."""
        total = self.controller.calcular_total_inversion_dia()
        messagebox.showinfo("Total Invertido", f"El total invertido hoy es: {formatear_pesos(total)}")

    def calcular_ganancia_total_dia(self):
        """Calcula la ganancia total del día actual."""
        ganancia = self.controller.calcular_ganancia_total_dia()
        messagebox.showinfo("Ganancia Total", f"La ganancia total de hoy es: {formatear_pesos(ganancia)}")

    def _crear_ventana_emergente(self, titulo, geometria):
        """Crea una ventana emergente con el título y geometría especificados."""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(geometria)
        ventana.configure(bg="#ffffff")
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        return ventana 