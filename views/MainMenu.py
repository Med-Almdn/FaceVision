from customtkinter import CTkFrame, CTkLabel, CTkButton ,CTkImage
from views.ImageManagementModule import ImageManagementModule
from PIL import Image

class MainMenu(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self._build_ui()
 
    def _build_ui(self):
        self.heading = CTkLabel(self, text="Main Menu", font=("Microsoft YaHei UI Light", 32, "bold"), text_color="white")
        self.heading.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))

        button_width = 400
        button_height = 100

        self.streaming_desktop_icon = CTkImage(Image.open("assets/icon-desktop.png").resize((45, 45)))
        self.image_management_icon = CTkImage(Image.open("assets/icon-img-man.png").resize((45, 45)))

        self.btn_streaming_desktop = CTkButton(
            master=self, text="Streaming Desktop", image=self.streaming_desktop_icon, compound="left", width=button_width, height=button_height,
            font=('Torus Notched SemiBold', 22), corner_radius=13, command=lambda: self.initiate_desktop_streaming()
        )
        
        self.btn_gestion_images = CTkButton(
            master=self, text="Image Manager", image=self.image_management_icon, compound="left", width=button_width, height=button_height,
            font=('Torus Notched SemiBold', 22), corner_radius=13, command=lambda: self.navigate_to_image_manager()
        )
        
        self.btn_streaming_desktop.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")
        self.btn_gestion_images.grid(row=3, column=0, padx=20, pady=20, sticky="w")

    def initiate_desktop_streaming(self):
        from views.LiveStreamModule import LiveStreamModule  
        if hasattr(self.master, "current_frame") and self.master.current_frame is not None:
            self.master.current_frame.destroy()        
        self.master.current_frame = LiveStreamModule(self.master)
        self.master.current_frame.grid(row=0, column=0)

    def navigate_to_image_manager(self):

        if hasattr(self.master, "current_frame") and self.master.current_frame is not None:
            self.master.current_frame.destroy()   
        self.master.current_frame = ImageManagementModule(self.master)
        self.master.current_frame.grid(row=0, column=0)

