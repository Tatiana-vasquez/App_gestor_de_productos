from tkinter import ttk
from tkinter import *

import sqlite3


class Producto():
    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App gestor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap("recursos/icon.ico")

        # creacion del contenedor Frame ppal
        frame = LabelFrame(self.ventana, text='Registrar un nuevo Producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre:  ")
        self.etiqueta_nombre.grid(row=1, column=0)
        # entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # label Precio
        self.etiqueta_precio = Label(frame, text="Precio:  ")
        self.etiqueta_precio.grid(row=2, column=0)
        # entry Nombre
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Boton de Anadir Producto
        self.boton_anadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto)
        self.boton_anadir.grid(row=3, columnspan=2, sticky=W + E)

        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=3, column=0, sticky=W + E)

        # Tabla productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", hightlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=10, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading("#0", text="Nombre", anchor="center")
        self.tabla.heading("#1", text="Precio", anchor="center")

        # botones de Eliminar y editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        boton_eliminar = ttk.Button(text="Eliminar", style='my.TButton', command=self.del_producto)
        boton_eliminar.grid(row=5, column=0, sticky=W + E)
        boton_editar = ttk.Button(text="Editar", style='my.TButton', command=self.edit_producto)
        boton_editar.grid(row=5, column=1, sticky=W + E)

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registro_tabla = self.tabla.get_children()
        for fila in registro_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=fila[2])

    def validacion_nombre(self):
        nombre_introducido_por_ususario = self.nombre.get()
        return len(nombre_introducido_por_ususario) != 0

    def validacion_precio(self):
        precio_introducido_por_ususario = self.precio.get()
        return len(precio_introducido_por_ususario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio():
            query = "INSERT INTO producto VALUES(NULL, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")

            print(self.nombre.get())
            print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        else:
            print("El precio y el nombre son obligatorios")
            self.mensaje["text"] = "El precio y el nombre son obligatorios"

        self.get_productos()

    def del_producto(self):
        # debaug, depurar
        print(self.tabla.item(self.tabla.selection())["values"])
        print(self.tabla.item(self.tabla.selection()))
        nombre = self.tabla.item(self.tabla.selection())["text"]
        print(self.tabla.item(self.tabla.selection())["values"][0])
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.get_productos()

    def edit_producto(self):
        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return
        nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]

        # Ventana nueva(editar producto)
        self.ventana_editar = Toplevel()  # crear una ventana por delante de la ppal
        self.ventana_editar.title = "Editar producto"
        self.ventana_editar.resizable(1, 1)  # dimensiones de la ventana
        self.ventana_editar.wm_iconbitmap("recursos/icon.ico")

        titulo = Label(self.ventana_editar, text="Edicion de Productos", font=('Calibri', 30, 'bold'))
        titulo.grid(column=0, row=0)

        # creacion del contenedor Frame de la ventana de editar producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el Siguiente Producto")
        # frame_ep: Frame editar producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # label nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre Antiguo")
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)
        # entry nombre antiguo(texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),
                                          state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre Nuevo")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry nombre nuevo(texto que si se puede modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # para q el foco del raton vaya a este entry al inicio

        # label precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio Antiguo: ")
        self.etiqueta_precio_antiguo.grid(row=4, column=0)
        # entry Precio antiguo(texto que no se puede modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state="readonly")
        self.input_precio_antiguo.grid(row=4, column=1)

        # label precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio Nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # entry precio nuevo (texto q no se puede modificar)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)

        # Boton para actualizar producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                           command=lambda:
        self.actualizar_productos(self.input_precio_nuevo.get(),
        self.input_precio_antiguo.get(),
        self.input_precio_nuevo.get(),
        self.input_precio_antiguo.get()))
        self.boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio):
        producto_modificado = False
        query = "UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?"
        if nuevo_nombre != "" and nuevo_precio != "":
            # si el usuario escribe nuevo nombre y nuevo precio, se cambian ambos
            parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre != "" and nuevo_precio == "":
            # si el usuario deja vacio el nuevo precio, se mantiene el precio anterior
            parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre == "" and nuevo_precio != "":
            # si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        if producto_modificado:
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje["text"] = 'El producto {} ha sido actualizado con exito'.format(antiguo_nombre)
            self.get_productos()
        else:
            self.ventana_editar.destroy()
            self.mensaje['text'] = "El producto {} NO ha sido actualizado".format(antiguo_nombre)


if __name__ == "__main__":
    root = Tk()  # instancia de la ventana principal
    app = Producto(root)
    root.mainloop()
