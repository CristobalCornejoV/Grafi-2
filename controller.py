import os
import threading
from model import TTSModel, leer_pdf_por_paginas, leer_pptx_por_diapositivas, leer_txt, texto_a_fragmentos, texto_a_voz_edge_fragmentos, verificar_ffmpeg, instalar_ffmpeg

class TTSController:
    def __init__(self, model: TTSModel, view):
        self.model = model
        self.view = view
        self.hilo_proceso = None

    def log_a_vista(self, texto: str):
        self.view.root.after(0, self.view.log, texto)

    def actualizar_progreso_vista(self, actual: int, total: int):
        self.view.root.after(0, self.view.actualizar_progreso, actual, total)

    def mostrar_mensaje_error(self, titulo: str, mensaje: str):
        self.view.root.after(0, self.view.mostrar_error, titulo, mensaje)

    def mostrar_mensaje_info(self, titulo: str, mensaje: str):
        self.view.root.after(0, self.view.mostrar_info, titulo, mensaje)
        
    def solicitar_destino_audio(self) -> str:
        return self.view.solicitar_directorio("Selecciona carpeta para guardar audios")

    def establecer_voz(self, voz: str):
        self.model.set_voz(voz)

    def instalar_ffmpeg(self):
        if instalar_ffmpeg():
            self.mostrar_mensaje_info("Instalación", "Se intentó iniciar la instalación de ffmpeg con winget. Revisa tu consola o espera la ventana de winget.")
        else:
            self.mostrar_mensaje_error("Error", "No se pudo iniciar la instalación de ffmpeg con winget.")

    def iniciar_proceso_conversion(self, ruta_archivo: str):
        if self.model.proceso_activo:
            self.mostrar_mensaje_info("Proceso activo", "Hay un proceso en curso. Espera a que termine o cancélalo.")
            return

        self.view.limpiar_log_y_progreso()
        self.model.iniciar_proceso(ruta_archivo)
        self.log_a_vista(f"Iniciando proceso para: {ruta_archivo}")

        self.hilo_proceso = threading.Thread(target=self._proceso_principal_hilo, args=(ruta_archivo,))
        self.hilo_proceso.start()

    def cancelar_proceso(self):
        if self.model.proceso_activo:
            self.model.cancelar_proceso()
            self.mostrar_mensaje_info("Cancelar", "Solicitud de cancelación enviada.")
        else:
            self.mostrar_mensaje_info("Info", "No hay proceso en ejecución.")

    def _proceso_principal_hilo(self, ruta_archivo: str):
        try:
            if not verificar_ffmpeg():
                self.log_a_vista("[ADVERTENCIA] ffmpeg no está instalado o no se encuentra en PATH.")
            
            ext = os.path.splitext(ruta_archivo)[1].lower()
            
            if ext == ".txt":
                texto = leer_txt(ruta_archivo)
                fragmentos = texto_a_fragmentos(texto)
                self.log_a_vista(f"Archivo TXT leído, fragmentos creados: {len(fragmentos)}")
            elif ext == ".pdf":
                fragmentos = leer_pdf_por_paginas(ruta_archivo)
                self.log_a_vista(f"Archivo PDF leído, páginas encontradas: {len(fragmentos)}")
            elif ext == ".pptx":
                fragmentos = leer_pptx_por_diapositivas(ruta_archivo)
                self.log_a_vista(f"Archivo PPTX leído, diapositivas encontradas: {len(fragmentos)}")
            else:
                self.mostrar_mensaje_error("Error", "Tipo de archivo no soportado.")
                return

            if not fragmentos:
                self.mostrar_mensaje_error("Error", "El archivo está vacío o no se pudo extraer el texto.")
                return

            self.model.archivos_generados = texto_a_voz_edge_fragmentos(
                fragmentos, 
                self.model.carpeta_temporal, 
                voz=self.model.voz_seleccionada,
                log_func=self.log_a_vista, 
                actualizar_progreso_func=self.actualizar_progreso_vista
            )

            if not self.model.archivos_generados:
                if self.model.proceso_activo:
                    self.mostrar_mensaje_error("Error", "No se generaron archivos de audio.")
                self.log_a_vista("Proceso terminado por error o cancelación.")
                return
            
            carpeta_destino = self.solicitar_destino_audio()
            
            if not carpeta_destino:
                self.log_a_vista("Proceso cancelado por usuario al no seleccionar carpeta de destino.")
                return

            self.model.mover_archivos_a_destino(carpeta_destino)
            self.log_a_vista(f"Archivos movidos a: {carpeta_destino}")
            self.log_a_vista("\nProceso finalizado con éxito.")
            self.mostrar_mensaje_info("Éxito", f"Archivos guardados en:\n{carpeta_destino}")

        except Exception as e:
            self.log_a_vista(f"[ERROR] Ocurrió un error inesperado: {e}")
            self.mostrar_mensaje_error("Error Fatal", f"Ocurrió un error inesperado:\n{e}")
            
        finally:
            self.model.finalizar_proceso()