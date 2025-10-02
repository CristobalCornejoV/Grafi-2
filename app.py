from tkinterdnd2 import TkinterDnD
from model import TTSModel
from view import TTSView
from controller import TTSController

if __name__ == "__main__":
    root = TkinterDnD.Tk()

    tts_model = TTSModel()

    tts_controller = TTSController(tts_model, None)
    tts_view = TTSView(root, tts_controller)
    
    tts_controller.view = tts_view

    root.mainloop()