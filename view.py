import os 
from tkinter import Tk, Button, Text, Scrollbar, END, StringVar, ttk, Menu, Toplevel, Label
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox, filedialog
from typing import Callable

class TTSView:
    def __init__(self, root: TkinterDnD.Tk, controller):
        self.root = root
        self.controller = controller
        
        root.title("Texto a Audio MP3 (Edge TTS) - MVC")
        root.geometry("500x520")
        root.resizable(False, False)
        root.configure(bg="#f0f0f0")

        if os.path.exists("icon.ico"):
            root.iconbitmap("icon.ico")

        self.voz_var = StringVar()
        self.voz_var.set("es-CL-CatalinaNeural")
        self.progress_var = StringVar()
        self.progress_var.set("")

        self.crear_menu()
        self.crear_widgets()

        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.on_archivo_arrastrado)
        
        self.combo_voz.bind("<<ComboboxSelected>>", self.on_voz_seleccionada)

    def crear_menu(self):
        menubar = Menu(self.root)
        
        archivo_menu = Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Seleccionar archivo", command=self.on_seleccionar_archivo_click)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Cerrar programa", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        acerca_menu = Menu(menubar, tearoff=0)
        acerca_menu.add_command(label="Acerca de", command=self.on_acerca_de_click)
        acerca_menu.add_command(label="Instalar ffmpeg", command=self.on_instalar_ffmpeg_click)
        menubar.add_cascade(label="Ayuda", menu=acerca_menu)

        self.root.config(menu=menubar)

    def crear_widgets(self):
        self.btn_seleccionar = Button(self.root, text="Selecciona archivo PDF, PPTX o TXT (o arrástralo aquí)", 
                                      command=self.on_seleccionar_archivo_click)
        self.btn_seleccionar.pack(pady=10)
        
        self.btn_cancelar = Button(self.root, text="Cancelar Proceso", command=self.on_cancelar_proceso_click, bg="white")
        self.btn_cancelar.pack(pady=5)
        
        lista_voces = ["es-CL-CatalinaNeural", "es-CL-LorenzoNeural"]
        label_voz = ttk.Label(self.root, text="Selecciona voz:")
        label_voz.pack(pady=(10,0))
        self.combo_voz = ttk.Combobox(self.root, textvariable=self.voz_var, values=lista_voces, state="readonly")
        self.combo_voz.pack()

        self.progress_label = ttk.Label(self.root, textvariable=self.progress_var, font=("Arial", 12))
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=460, mode='determinate')
        self.progress_bar.pack(pady=5)

        self.log_text = Text(self.root, wrap='word', height=25, font=("Consolas", 11))
        self.log_text.pack(expand=True, fill='both')
        self.scrollbar = Scrollbar(self.log_text)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.log_text.yview)

    def log(self, texto: str):
        self.log_text.insert(END, texto + "\n")
        self.log_text.see(END)
        self.root.update_idletasks()

    def limpiar_log_y_progreso(self):
        self.log_text.delete(1.0, END)
        self.progress_var.set("")
        self.progress_bar["value"] = 0

    def actualizar_progreso(self, actual: int, total: int):
        self.progress_var.set(f"Procesando fragmento {actual} de {total}")
        self.progress_bar["maximum"] = total
        self.progress_bar["value"] = actual
        self.root.update_idletasks()

    def mostrar_info(self, titulo: str, mensaje: str):
        messagebox.showinfo(titulo, mensaje)

    def mostrar_error(self, titulo: str, mensaje: str):
        messagebox.showerror(titulo, mensaje)
        
    def solicitar_directorio(self, titulo: str) -> str:
        return filedialog.askdirectory(title=titulo)

    def mostrar_ventana_instalacion_ffmpeg(self, instalar_func: Callable[[], None]):
        ventana = Toplevel(self.root)
        ventana.title("Instalación de ffmpeg")
        ventana.geometry("400x250")
        ventana.resizable(False, False)
        ventana.grab_set()

        texto = (
            "Esta aplicación requiere ffmpeg para funcionar correctamente.\n"
            "Puedes instalarlo automáticamente usando winget en Windows 11.\n\n"
            "Si no tienes winget, instala ffmpeg manualmente desde:\n"
            "https://ffmpeg.org/download.html"
        )
        Label(ventana, text=texto, justify="left", padx=10, pady=10, wraplength=380).pack()

        Button(ventana, text="Instalar ffmpeg con winget", command=instalar_func).pack(pady=10)
        Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

    def on_seleccionar_archivo_click(self):
        rutas = filedialog.askopenfilenames(title="Selecciona archivo(s)",
                                             filetypes=[("Archivos de texto", "*.txt"),
                                                        ("PDF", "*.pdf"),
                                                        ("PowerPoint", "*.pptx"),
                                                        ("Todos los archivos", "*.*")])
        if rutas:
            for ruta in rutas:
                self.controller.iniciar_proceso_conversion(ruta)

    def on_archivo_arrastrado(self, event):
        archivos = self.root.tk.splitlist(event.data)
        for archivo in archivos:
            self.controller.iniciar_proceso_conversion(archivo)

    def on_cancelar_proceso_click(self):
        self.controller.cancelar_proceso()
        
    def on_voz_seleccionada(self, event):
        self.controller.establecer_voz(self.voz_var.get())

    def on_acerca_de_click(self):
        mensaje = ("App creada por Cristobal Cornejo\nDesarrollada con Vibe Coding\n\n"
                   "Esta aplicación convierte archivos de texto (.txt, .pdf, .pptx) a audio MP3 usando Edge TTS.\n\n"
                   "Requisito: ffmpeg instalado.")
        self.mostrar_info("Acerca de", mensaje)

    def on_instalar_ffmpeg_click(self):
        self.mostrar_ventana_instalacion_ffmpeg(self.controller.instalar_ffmpeg)