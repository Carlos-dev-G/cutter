import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from util.list import Utilidades  # Importación de utilidades personalizadas


class CutterApp(ctk.CTk):
    """Aplicación de GUI para gestionar videos y carpetas."""

    def __init__(self):
        """Inicializa la aplicación, sus variables y la interfaz."""
        super().__init__()
        self.path_archivos = None  # Ruta de la carpeta de videos
        self.valor_borrar = ctk.BooleanVar(
            value=False
        )  # Borrar videos al cortar
        self.valor_carpetas = ctk.BooleanVar(
            value=False
        )  # Crear carpeta por video
        self.valor_videos = ctk.IntVar(value=0)  # Contador de videos
        self.utilidades = Utilidades()  # Instancia de Utilidades

        self.configure_interface()
        self.create_ui()

    def configure_interface(self):
        """Configura las propiedades básicas de la ventana."""
        for i in range(3):
            self.columnconfigure(i, minsize=100)

        self.title("CUTTER")
        self.resizable(False, False)
        ctk.set_default_color_theme("dark-blue")

    def create_ui(self):
        """Crea y organiza los elementos de la interfaz de usuario."""
        # Sección 1 (fila 1)
        self.visualizador_path = ctk.CTkEntry(
            self,
            placeholder_text="Carpeta de videos no seleccionada",
            state="readonly",
        )
        self.visualizador_path.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10
        )

        self.button_path = ctk.CTkButton(
            self, text="Abrir", command=self.select_path
        )
        self.button_path.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.switch_borrar = ctk.CTkSwitch(
            self, text="Borrar videos al cortar", variable=self.valor_borrar
        )
        self.switch_borrar.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10
        )

        self.switch_carpetas = ctk.CTkSwitch(
            self, text="Carpeta por video", variable=self.valor_carpetas
        )
        self.switch_carpetas.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10
        )

        self.inputs_segundos = ctk.CTkEntry(
            self, placeholder_text="Intervalo Segundos"
        )
        self.inputs_segundos.grid(
            row=1, column=2, sticky="nsew", padx=10, pady=10
        )

        # Sección 2 (fila 2)
        self.videos_label = ctk.CTkLabel(self, text="Videos")
        self.videos_label.grid(row=2, column=0)

        self.visualizador_videos_cantidad = ctk.CTkEntry(
            self,
            textvariable=self.valor_videos,
            state="readonly",
            placeholder_text="No hay videos",
        )
        self.visualizador_videos_cantidad.grid(
            row=2, column=1, padx=0, pady=10
        )

        self.reload_button = ctk.CTkButton(
            self, text="Reload", command=self.update_video_count
        )
        self.reload_button.grid(
            row=2, column=2, sticky="nsew", padx=10, pady=10
        )

        # Sección 3 (fila 3)
        frame = ctk.CTkFrame(self)
        frame.grid(
            row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10
        )

        self.logs = ttk.Treeview(
            frame, columns=("Video", "Estado"), show="headings"
        )
        self.logs.heading("Video", text="Video")
        self.logs.heading("Estado", text="Estado")

        self.scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.logs.yview
        )
        self.logs.configure(yscrollcommand=self.scrollbar.set)

        self.logs.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Sección 4 (fila 4)
        self.iniciar_button = ctk.CTkButton(
            self, text="Iniciar", command=self.iniciar
        )
        self.iniciar_button.grid(
            row=4, column=2, sticky="nsew", padx=10, pady=10
        )

    def select_path(self):
        """Abre un cuadro de diálogo para seleccionar la carpeta de videos."""
        self.path_archivos = filedialog.askdirectory()
        if self.path_archivos:
            self.visualizador_path.configure(state="normal")
            self.visualizador_path.delete(0, ctk.END)
            self.visualizador_path.insert(0, self.path_archivos)
            self.visualizador_path.configure(state="readonly")
            self.update_video_count()
        else:
            messagebox.showwarning(
                "Directorios", "No seleccionó ningún directorio"
            )

    def update_video_count(self):
        """Actualiza la cantidad de videos en la carpeta seleccionada."""
        if self.path_archivos:
            self.limpiar()
            video_count = self.utilidades.listar_videos(
                self.insertar, self.path_archivos
            )
            self.valor_videos.set(video_count if video_count > 0 else 0)
            if video_count == 0:
                self.aler("No hay ningún video en el directorio especificado")
        else:
            self.valor_videos.set(0)

    def limpiar(self):
        """Limpia el TreeView antes de añadir nuevos datos."""
        for item in self.logs.get_children():
            self.logs.delete(item)

    def insertar(self, datos: tuple):
        """Inserta nuevos datos en el TreeView."""
        self.logs.insert("", "end", values=datos)

    def actualizar(self, video: str, estado: str):
        """Actualiza el estado de un video en el TreeView."""
        for item in self.logs.get_children():
            nombre, _ = self.logs.item(item, "values")
            if nombre == video:
                self.logs.item(item=item, values=(nombre, estado))

    def aler(self, msg: str):
        """Muestra un mensaje informativo."""
        messagebox.showinfo("CUTTER", msg)

    def iniciar(self):
        """Inicia el procesamiento de videos."""
        valor_borrar = self.valor_borrar.get()
        valor_carpetas = self.valor_carpetas.get()
        try:
            seconds_value = float(self.inputs_segundos.get())
        except ValueError:
            seconds_value = 1

        self.utilidades.iniciar(
            [self.actualizar, self.aler],
            valor_borrar,
            valor_carpetas,
            seconds_value,
        )


# Iniciar la aplicación
if __name__ == "__main__":
    app = CutterApp()
    app.mainloop()