from views.MainMenu import MainMenu
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage
from tkinter import messagebox

class WelcomeScreen(CTkFrame): 
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self._build_ui()

    def _build_ui(self):
        self.configure(fg_color="#1c1c1c")  

        self.heading = CTkLabel(
            self,
            text="Welcome to FaceVision",
            font=("Microsoft YaHei UI Light", 55, "bold"),
            text_color="#ffffff"  
        )
        self.heading.place(relx=0.5, rely=0.22, anchor="center")

        self.subtitle = CTkLabel(
            self,
            text="Streamlined facial recognition for modern solutions",
            font=("Microsoft YaHei UI Light", 20),
            text_color="#cccccc"  
        )
        self.subtitle.place(relx=0.5, rely=0.35, anchor="center")

        
        self.start_button = CTkButton(
            self,
            text="Get Started",
            corner_radius=10,
            font=("Microsoft YaHei UI", 18),
            fg_color="#007bff",  
            hover_color="#0056b3",  
            width=200,
            height=50,
            text_color="white",  
            command=self.launch_app
        )
        self.start_button.place(relx=0.5, rely=0.55, anchor="center")

        self.show_info_button = CTkButton(
            self,
            text="Learn More",
            corner_radius=10,
            font=("Microsoft YaHei UI", 18),
            fg_color="#28a745",  
            hover_color="#1e7e34",  
            width=200,
            height=50,
            text_color="white",  
            command=self.show_info
        )
        self.show_info_button.place(relx=0.5, rely=0.70, anchor="center")

    def launch_app(self):
        if hasattr(self.master, "current_frame") and self.master.current_frame is not None:
            self.master.current_frame.destroy()  
        self.master.current_frame = MainMenu(self.master)  
        self.master.current_frame.grid(row=0, column=0, padx=10, pady=10)

    def show_info(self):
        messagebox.showinfo(
            "Learn More",
            "FaceVision is a cutting-edge facial recognition platform designed to deliver advanced solutions for securely storing personnel data and images. It's ideal for applications such as attendance management, secure door access, facial authentication, and payment systems."
        )
