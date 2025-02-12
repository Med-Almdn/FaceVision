from customtkinter import CTk
from views.WelcomeScreen import WelcomeScreen

class FaceVisionMainApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("FaceVision")
        self.geometry("945x505+300+200")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=1)  

        self.current_frame = None  
        self.show_welcome_frame()

    def show_welcome_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()  
        self.current_frame = WelcomeScreen(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

if __name__ == "__main__":
    app = FaceVisionMainApp()
    app.mainloop()
 