import threading
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Desk-Help")
        self.configurar_tela()

        self.frames = {}
        self.exibir_frame("login")

    def configurar_tela(self):
        self['bg'] = "#D8EAF7"

    def exibir_frame(self, frame_name):
        for frame in self.frames.values():
            frame.place_forget()

        if frame_name not in self.frames:
            if frame_name == "login":
                frame = TelaLogin(self)
            else:
                raise ValueError(f"Frame '{frame_name}' não encontrado.")

            self.frames[frame_name] = frame
            frame.place(x=0, y=0)
        else:
            self.frames[frame_name].place(x=0, y=0)


    def deletar_frames(self, exclude=[]):
        for key, frame in list(self.frames.items()):
            if key not in exclude:
                frame.destroy()
                del self.frames[key] 

    def trocar_para_menu(self):
        self.deletar_frames(exclude=['menu'])
        self.exibir_frame("menu")

def iniciar_app():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    connection_thread = threading.Thread()
    connection_thread.start()
    connection_thread.join()
    iniciar_app()