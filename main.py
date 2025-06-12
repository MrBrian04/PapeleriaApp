import tkinter as tk
from controllers.producto_controller import ProductoController
from views.main_window import MainWindow

def main():
    root = tk.Tk()
    controller = ProductoController()
    app = MainWindow(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
