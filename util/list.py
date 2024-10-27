from typing import Callable
import threading
from pathlib import Path
import random
import string
import cv2


def generar_letras_aleatorias(cantidad):
    letras_aleatorias = "".join(
        random.choices(string.ascii_letters, k=cantidad)
    )
    return letras_aleatorias


class Utilidades:
    """Clase para gestionar videos y su procesamiento en un directorio."""

    __slots__ = ["videos", "contador", "_path"]

    def __init__(self) -> None:
        """Inicializa la lista de videos y el contador."""
        self.videos = []  # Lista para almacenar los nombres de videos
        self.contador: int = 0  # Contador de videos
        self._path = None

    def listar_videos(
        self, logs_callback: Callable, path: str = Path.cwd()
    ) -> int:
        """
        Lista y cuenta archivos de video en el directorio especificado.

        Args:
            path (str): Ruta del directorio donde buscar videos.
                        Por defecto, utiliza el directorio actual.

        Returns:
            int: Número total de archivos de video encontrados.
        """
        extensiones = (".mp4",)  # Extensiones válidas para archivos de video
        self.videos.clear()  # Limpiar lista de videos para evitar duplicados
        self.contador = 0  # Reiniciar el contador
        self._path = Path(path)
        for archivo in self._path.iterdir():
            if (
                archivo.suffix in extensiones
            ):  # Verificar si el archivo es un video
                logs_callback((archivo.name, "Pendiente"))
                self.contador += 1
                self.videos.append(archivo.name)

        return self.contador

    def iniciar(
        self,
        callbakcs: list,
        dele_vid: bool,
        vid_folder: bool,
        interval: int,
    ) -> None:
        """Inicia el proceso de extracción de frames en un hilo separado."""
        proceso = threading.Thread(
            target=self.iniciar_sec_proces,
            args=(callbakcs, dele_vid, vid_folder, interval),
        )
        proceso.start()

    def iniciar_sec_proces(
        self,
        callbakcs: list,
        dele_vid: bool,
        vid_folder: bool,
        interval: int,
    ) -> None:
        """Proceso secundario para extraer frames de los videos listados."""
        for video in self.videos:

            # callback
            callbakcs[0](f"{video}", " Iniciando ")

            video_path = Path(self._path) / video

            # Verificar si se debe crear carpeta específica
            if vid_folder:
                carpeta = self._path / Path(video).stem
                carpeta.mkdir(parents=True, exist_ok=True)
            else:
                carpeta = self._path

            # Cargar el video
            cap = cv2.VideoCapture(str(video_path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frames_interval = int(fps * interval)

            success, frame = cap.read()
            frame_count = 0

            callbakcs[0](f"{video}", " Procesando ")

            while success:
                # Guardar frame en el intervalo especificado
                if frame_count % frames_interval == 0:
                    frame_name = (
                        carpeta
                        / f"{frame_count}__{generar_letras_aleatorias(10)}.jpg"
                    )
                    cv2.imwrite(str(frame_name), frame)

                success, frame = cap.read()
                frame_count += 1

            callbakcs[0](f"{video}", " Finalizado ")
            cap.release()

            if dele_vid:
                vid = (Path(self._path) / video).unlink()

        callbakcs[1](" Procesamiento Finalizado ")
