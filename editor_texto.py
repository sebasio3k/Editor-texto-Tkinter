import tkinter as tk
from tkmacosx import Button
from tkinter.filedialog import askopenfile, asksaveasfilename


class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Editor de Texto')
        # Configuración de ventana
        self.geometry('+450+200')
        self.rowconfigure(0, minsize=600, weight=1)
        self.columnconfigure(1, minsize=600, weight=1)
        # Atributo de campo de texto
        self.campo_texto = tk.Text(self, wrap=tk.WORD, font=('arial', 12))
        # Atributo de archivo
        self.archivo = None
        # Atributo para saber si está abierto un archivo
        self.archivo_abierto = False
        # Creación de componentes
        self._crear_componentes()
        self._crear_menu()

    def _crear_componentes(self):
        # Frame de botones
        frame_botones = tk.Frame(self, relief=tk.RAISED, bd=2)
        boton_abrir = Button(frame_botones, text='Abrir', cursor='hand2', command=self._abrir_archivo)
        boton_guardar = Button(frame_botones, text='Guardar', command=self._guardar)
        boton_guardar_como = Button(frame_botones, text='Guardar como...', command=self._guardar_como)

        boton_abrir.grid(row=0, column=0, sticky='we', padx=5, pady=5)
        boton_guardar.grid(row=1, column=0, sticky='we', padx=5, pady=5)
        boton_guardar_como.grid(row=2, column=0, sticky='we', padx=5, pady=5)
        frame_botones.grid(row=0, column=0, sticky='ns')

        # Campo de texto
        self.campo_texto.grid(row=0, column=1, sticky='nsew')

    def _crear_menu(self):
        # Creamos el menú de la app
        menu_app = tk.Menu(self)
        self.config(menu=menu_app)

        # Opciones del menú
        # Archivo
        menu_archivo = tk.Menu(menu_app, tearoff=False)
        menu_app.add_cascade(label='Archivo', menu=menu_archivo)
        # Opciones de archivo
        menu_archivo.add_command(label='Abrir', command=self._abrir_archivo)
        menu_archivo.add_command(label='Guardar', command=self._guardar)
        menu_archivo.add_command(label='Guardar como...', command=self._guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label='Salir', command=self.quit)

    def _abrir_archivo(self):
        # Abrimos el archivo para edición (leer, describe)
        self.archivo_abierto = askopenfile(mode='r+')
        # Eliminamos el texto anterior de la caja de texto
        self.campo_texto.delete(1.0, tk.END)
        # Revisar si hay un archivo
        if not self.archivo_abierto:
            return
        # Abrir el archivo en modo lectura/escritura como un recurso
        with open(self.archivo_abierto.name, 'r+', encoding='utf-8') as self.archivo:
            # Leer el contenido del archivo
            texto = self.archivo.read()
            # Insertar el contenido del archivo en el campo de texto
            self.campo_texto.insert(1.0, texto)
            # Modificar el título de la aplicación con el nombre del archivo
            self.title(f'*Editor Texto - {self.archivo.name}')

    def _guardar(self):
        # Si ya se abrió previamente un archivo, lo sobreescribimos
        if self.archivo_abierto:
            # Se guarda el archivo (modo escritura)
            with open(self.archivo_abierto.name, 'w', encoding='utf-8') as self.archvo:
                # Leemos el contenido de la caja de texto
                texto = self.campo_texto.get(1.0, tk.END)
                # Escribir el texto en el archivo
                self.archvo.write(texto)
                # Cambiar el nombre del título de la app
                self.title(f'Editor Texto - {self.archivo.name}')
        else:
            self._guardar_como()

    def _guardar_como(self):
        # Se guarda el archivo actual como un nuevo archivo
        self.archvo = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
        )
        if not self.archvo:
            # Si no se abre correctamente, regresamos el control
            return
        # Abrimos el archivo en modo escritura
        with open(self.archvo, 'w') as archivo:
            # Leer el contenido de la caja de texto
            texto = self.campo_texto.get(1.0, tk.END)
            # Escribir el contenido al nuevo archivo
            archivo.write(texto)
            # Cambiar el nombre del archivo
            self.title(f'Editor Texto - {archivo.name}')
            # Indicar que ya se ha abierto un archivo
            self.archivo_abierto = archivo


if __name__ == '__main__':
    editor_texto = Editor()
    editor_texto.mainloop()
