import threading
import cv2
import numpy as np
from customtkinter import CTkImage, CTkFrame, CTkLabel, CTkButton, CTkTextbox
from PIL import Image
import face_recognition

from DatabaseHandler import *

class LiveStreamModule(CTkFrame): 
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.running = False
        self.thread = None
        imgBg = "assets\\bgvidio.png"
        self.image_video = CTkImage(light_image=Image.open(imgBg), dark_image=Image.open(imgBg), size=(550, 430))
        self.last_detected_name = ""
        self._build_ui()

    def _build_ui(self):
        self.frame1 = CTkFrame(self)
        self.frame1.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="nsew")

        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        self.heading = CTkLabel(
            master=self.frame1,
            text="FaceVision",
            font=("Microsoft YaHei UI Light", 40, "bold"),
            text_color="white"
        )
        self.heading.grid(row=0, column=0, padx=0, pady=(80, 10), sticky="ew")

        self.textbox = CTkTextbox(
            master=self.frame1,
            font=("Arial", 16),
            width=270,
            height=80,
            corner_radius=10
        )
        self.textbox.grid(row=1, column=0, padx=15, pady=(12.5, 0), sticky="w")
        self.textbox.insert("0.0", "Name\t:\nId\t:")

        self.start_button = CTkButton(
            master=self.frame1,
            text="Start Streaming",
            corner_radius=10,
            font=('Torus Notched SemiBold', 18, "bold"),
            fg_color="#007cff",
            width=270,
            command=self.start_streaming
        )
        self.start_button.grid(row=2, column=0, padx=15, pady=(12.5, 0), sticky="w")

        self.stop_button = CTkButton(
            master=self.frame1,
            text="Stop Streaming",
            corner_radius=10,
            font=('Torus Notched SemiBold', 18, "bold"),
            fg_color="#007cff",
            width=270,
            command=self.stop_streaming
        )
        self.stop_button.grid(row=3, column=0, padx=15, pady=(12.5, 0), sticky="w")

        self.menu_button = CTkButton(
            master=self.frame1,
            text="Go to Menu",
            corner_radius=10,
            font=('Torus Notched SemiBold', 18, "bold"),
            fg_color="#007cff",
            width=270,
            command=self.navigate_to_main_menu
        )
        self.menu_button.grid(row=4, column=0, padx=15, pady=(12.5, 105), sticky="w")

        self.frame2 = CTkFrame(self)
        self.frame2.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="nsew")

        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)

        self.video_label = CTkLabel(
            master=self.frame2,
            image=self.image_video,
            text=""
        )
        self.video_label.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

    def start_streaming(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.face_detection_streaming, daemon=True)
            self.thread.start()

    def stop_streaming(self):
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join(timeout=1)
                self.thread = None
            self.after(0, self.update_ui, "", "")
            self.after(0, self.update_video_label, self.image_video)

    def update_ui(self, name, person_id):
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", f"Name\t: {name}\nId\t: {person_id}")

    def update_video_label(self, img_ctk):
        self.video_label.configure(image=img_ctk)
        self.video_label.image = img_ctk

    def draw_rounded_rectangle(self, img, rect, color, thickness=2):
        left, top, right, bottom = rect
        cv2.rectangle(img, (left, top), (right, bottom), color, thickness, lineType=cv2.LINE_AA)

    def face_detection_streaming(self):
        """Stream video and perform face detection."""
        ids_list, names_list, encode_list, _ = DatabaseHandler.get_all_persons()
        encode_list = np.array(encode_list, dtype=np.float64)

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame, model='hog')
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for encoding, location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(encode_list, encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(encode_list, encoding)
                name = "Unknown"
                person_id = "N/A"

                if matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = names_list[best_match_index]
                        person_id = ids_list[best_match_index]

                top, right, bottom, left = [coord * 4 for coord in location]
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                self.draw_rounded_rectangle(frame, (left, top, right, bottom), color)

                if name != self.last_detected_name:
                    self.after(0, self.update_ui, name, person_id)
                    self.last_detected_name = name

            img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img_ctk = CTkImage(light_image=img_pil, dark_image=img_pil, size=(550, 430))
            self.after(0, self.update_video_label, img_ctk)

        cap.release()
        self.after(0, self.update_video_label, self.image_video)

    def navigate_to_main_menu(self):
        from views.MainMenu import MainMenu
        if hasattr(self.master, "current_frame") and self.master.current_frame is not None:
            self.master.current_frame.destroy() 
        self.master.current_frame = MainMenu(self.master)  
        self.master.current_frame.grid(row=0, column=0, padx=10, pady=10)


