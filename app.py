import tkinter as tk
from telas.TelaLogin import TelaLogin
from services.conexao import Database

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Desk-Help")
        self.configurar_tela()

        self.frames = {}
        self.exibir_frame("login")

    def configurar_tela(self):
        self.config(bg="#D8EAF7")

    def exibir_frame(self, frame_name):
        for frame in self.frames.values():
            frame.place_forget()

        if frame_name not in self.frames:
            if frame_name == "login":
                frame = TelaLogin(self)
            else:
                raise ValueError(f"Frame '{frame_name}' não encontrado.")
        
            self.frames[frame_name] = frame
            frame.pack(expand=True, fill=tk.BOTH) 
        else:
            self.frames[frame_name].pack(expand=True, fill=tk.BOTH)

    def deletar_frames(self, exclude=[]):
        for key, frame in list(self.frames.items()):
            if key not in exclude:
                frame.destroy()
                del self.frames[key] 

    def trocar_para_menu(self):
        self.deletar_frames(exclude=['menu'])
        self.exibir_frame("menu")
        
    def switch_to_login(self):
        self.exibir_frame("login")

def iniciar_app():
    app = App()
    app.mainloop()
    
def iniciar_conexao():
    db_instance = Database()
    db_instance.criar_tabelas()

if __name__ == "__main__":
    # connection_thread = threading.Thread(target=iniciar_conexao, daemon=True)
    # connection_thread.start()
    # connection_thread.join()
    iniciar_conexao()
    iniciar_app()