import numpy as np
import os
import shutil
import json
from tkinter import filedialog
from PIL import Image 
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkTextbox, CTkToplevel, CTkCheckBox, CTkImage
import face_recognition
from DatabaseHandler import *

IMAGES_FOLDER = "image_folder"

class ImageManagementModule(CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.face_data_file = "face_data.db"
        DatabaseHandler.create_table()  
        self._build_ui()

    def _build_ui(self):
        self.grid(padx=0, pady=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.frame1 = CTkFrame(self)
        self.frame1.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        self.frame1.grid_columnconfigure(0, weight=1)

        self.heading = CTkLabel(
            master=self.frame1,
            text="List Person Manager",
            font=("Microsoft YaHei UI Light", 26, "bold"),
            text_color="white"
        )
        self.heading.grid(row=0, column=0, padx=20, pady=(80, 20), sticky="ew")

        self.add_btn = CTkButton(
            master=self.frame1,
            text="Add",
            corner_radius=10,
            fg_color="#007bff",
            height=30,
            font=('Torus Notched SemiBold', 18, "bold"),
            command=self.show_add_person_dialog
        )
        self.add_btn.grid(row=1, column=0, padx=15, pady=(0, 20), sticky="ew")

        self.delete_btn = CTkButton(
            master=self.frame1,
            text="Delete",
            corner_radius=10,
            font=('Torus Notched SemiBold', 18, "bold"),
            fg_color="#007bff",
            height=30,
            command=self.show_delete_person_by_id_dialog
        )
        self.delete_btn.grid(row=2, column=0, padx=15, pady=(0, 20), sticky="ew")

        self.search_btn = CTkButton(
            master=self.frame1,
            text="Search",
            corner_radius=10,
            font=('Torus Notched SemiBold', 18, "bold"),
            fg_color="#007bff",
            height=30,
            command=self.show_search_dialog
        )
        self.search_btn.grid(row=3, column=0, padx=15, pady=(0, 20), sticky="ew")

        self.refrech_btn = CTkButton(
            master=self.frame1,
            text="Refrech",
            corner_radius=10,
            font=('Torus Notched SemiBold', 18, "bold"),
            fg_color="#007bff",
            height=30,
            command=self.refrech_person_list
        )
        self.refrech_btn.grid(row=5, column=0, padx=15, pady=(0, 20), sticky="ew")

        self.menu_button = CTkButton(
            master=self.frame1,
            text="Go to Menu",
            corner_radius=10,
            font=('Torus Notched SemiBold', 18, "bold"),
            fg_color="#007bff",
            height=30,
            command=self.navigate_to_main_menu
        )
        self.menu_button.grid(row=6, column=0, padx=15, pady=(0, 40), sticky="ew")

        self.frame2 = CTkFrame(self)
        self.frame2.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)

        self.show_all_persons(self.frame2)

    def refrech_person_list(self):
        self.show_all_persons(self.frame2)

    def show_all_persons(self, frame):

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        for widget in frame.winfo_children():
            widget.destroy()

        persons = DatabaseHandler.get_all_persons_id_and_name()
        header_frame = CTkFrame(frame)
        header_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        header_frame.grid_columnconfigure(0, weight=1)  
        header_frame.grid_columnconfigure(1, weight=1)  
        header_frame.grid_columnconfigure(2, weight=1)  

        checkbox_header = CTkLabel(header_frame, text="Select", font=("Microsoft YaHei UI Light", 16, "bold"), text_color="white")
        checkbox_header.grid(row=0, column=0, padx=0, pady=10)

        id_header = CTkLabel(header_frame, text="ID", font=("Microsoft YaHei UI Light", 16, "bold"), text_color="white")
        id_header.grid(row=0, column=1, padx=0, pady=10)

        name_header = CTkLabel(header_frame, text="Name", font=("Microsoft YaHei UI Light", 16, "bold"), text_color="white")
        name_header.grid(row=0, column=2, padx=0, pady=10)

        row = 1

        for person in persons:
            person_id, name = person

            # Checkbox for selection
            check_box = CTkCheckBox(header_frame, text=row, font=("Microsoft YaHei UI Light", 15), command=lambda person_id=person_id: self.handle_checkbox_toggle(person_id,check_box),checkmark_color="#f0f0f0")           
            check_box.grid(row=row, column=0, padx=0)

            # ID label
            person_id_label = CTkLabel(header_frame, text=f"{person_id}", font=("Microsoft YaHei UI Light", 15), text_color="white")
            person_id_label.grid(row=row, column=1, padx=0)

            # Name label
            person_name = CTkLabel(header_frame, text=f"{name}", font=("Microsoft YaHei UI Light", 15), text_color="white")
            person_name.grid(row=row, column=2, padx=0)

            row += 1

    def show_add_person_dialog(self):

        add_person_window = CTkToplevel(self)
        add_person_window.title("Add Person")
        add_person_window.geometry("500x300+600+300") 

        add_person_window.frame1 = CTkFrame(add_person_window)
        add_person_window.frame1.grid(row=0, column=0, padx=15, pady=15)

        heading = CTkLabel(add_person_window.frame1, text="Add Person", font=("Microsoft YaHei UI Light", 20,"bold"), text_color="white")
        heading.grid(row=0, column=0, columnspan=2, padx=0, pady=(30,15), sticky="ew")
        
        # Name input
        name_label = CTkLabel(add_person_window.frame1, text="Name", font=("Microsoft YaHei UI Light", 16))
        name_label.grid(row=1, column=0, padx=(30,10), pady=(25,0), sticky="w")
        name_entry = CTkTextbox(add_person_window.frame1, height=1, width=200)
        name_entry.grid(row=1, column=1, padx= (0,30), pady=(25,0), sticky="w")

        # Id input
        id_label = CTkLabel(add_person_window.frame1, text="Id", font=("Microsoft YaHei UI Light", 16))
        id_label.grid(row=2, column=0, padx=(30,10), pady=(10,0), sticky="w")
        id_entry = CTkTextbox(add_person_window.frame1, height=1, width=200)
        id_entry.grid(row=2, column=1, padx=(0,30), pady=(10,0), sticky="w")

        # Select image button
        image_button = CTkButton(add_person_window.frame1, text="Select Image", width=200, command=lambda: self.choose_image_file(image_status_label))
        image_button.grid(row=3, column=0, padx=(30,10), pady=(10,0), sticky="w")

        # Image status label
        image_status_label = CTkLabel(add_person_window.frame1, text="No image selected", font=("Microsoft YaHei UI Light", 12), text_color="red")
        image_status_label.grid(row=3, column=1, padx= (0,30), pady=(10,0), sticky="w")

        # Add person button
        add_person_btn = CTkButton(add_person_window.frame1, text="Add Person", width=200, command=lambda: self.add_new_person(id_entry,name_entry, add_person_window, image_status_label))
        add_person_btn.grid(row=4, column=0, padx=(30,10), pady=(10,25), sticky="w")

        # Close button
        close_btn = CTkButton(add_person_window.frame1, text="Cancel", width=200, command=add_person_window.destroy)
        close_btn.grid(row=4, column=1, padx= (0,30), pady=(10,25), sticky="w")

        add_person_window.resizable(False, False)  
        add_person_window.transient(self)  
        add_person_window.grab_set()  

    def choose_image_file(self, image_status_label):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            self.selected_image_path = image_path
            image_status_label.configure(text=f" {os.path.basename(image_path)}", text_color="green")

    def add_new_person(self, id_entry, name_entry, add_person_window, image_status_label):
        name = name_entry.get("0.0", "end-1c").strip()
        id = id_entry.get("0.0", "end-1c").strip()

        if name and id and hasattr(self, "selected_image_path"):
            image_path = self.selected_image_path

            destination_folder = IMAGES_FOLDER
            os.makedirs(destination_folder, exist_ok=True)  
            destination_path = os.path.join(destination_folder, f"{id}_{name}.jpg")
            try:
                image = Image.open(image_path)
                img_rgb = image.convert("RGB")
                img_array = np.array(img_rgb)
                encode = face_recognition.face_encodings(img_array)

                if encode:
                    serialized_encode = json.dumps(encode[0].tolist())
                    shutil.copy(image_path, destination_path)

                    DatabaseHandler.insert_person(id, name, serialized_encode, destination_path)
                    add_person_window.destroy()

                    self.show_all_persons(self.frame2)
                else:
                    print("No face found in the image.")
                    image_status_label.configure(text="No face found in the image.", text_color="red")

            except Exception as e:
                print(f"Error saving the image or processing: {e}")
        else:
            print("All fields must be filled, and an image must be selected.")

    def show_delete_person_by_id_dialog(self):
        delete_person_window = CTkToplevel(self)
        delete_person_window.title("Delete Person")
        delete_person_window.geometry("500x300+600+300") 

        delete_person_window.frame1 = CTkFrame(delete_person_window)
        delete_person_window.frame1.grid(row=0, column=0, padx=14, pady=50)

        heading = CTkLabel(delete_person_window.frame1, text="Delete Person by Id", font=("Microsoft YaHei UI Light", 20,"bold"), text_color="white")
        heading.grid(row=0, column=0, columnspan=2, padx=0, pady=(30,15), sticky="ew")
        
        # Id input
        id_label = CTkLabel(delete_person_window.frame1, text="Id", font=("Microsoft YaHei UI Light", 16, "bold"))
        id_label.grid(row=1, column=0, padx=(30,10), pady=(10,0), sticky="ew")
        id_entry = CTkTextbox(delete_person_window.frame1, height=1, width=200)
        id_entry.grid(row=1, column=1, padx=(0,30), pady=(10,0), sticky="w")

        # Delete person button
        delete_person_btn = CTkButton(delete_person_window.frame1, text="Delete Person", width=200, command=lambda: self.remove_selected_person(id_entry,delete_person_window,id_status_label))
        delete_person_btn.grid(row=2, column=0, padx=(30,10), pady=(10,0), sticky="w")

        # Close button
        close_btn = CTkButton(delete_person_window.frame1, text="Cancel", width=200, command=delete_person_window.destroy)
        close_btn.grid(row=2, column=1, padx= (0,30), pady=(10,0), sticky="w")

        # Id status label
        id_status_label = CTkLabel(delete_person_window.frame1, text="", font=("Microsoft YaHei UI Light", 14), text_color="red")
        id_status_label.grid(row=3, column=0, columnspan=2, padx= 30, pady=(5,15), sticky="w")

        delete_person_window.resizable(False, False)  
        delete_person_window.transient(self)  
        delete_person_window.grab_set()  

    def remove_selected_person(self, id_entry, delete_person_window, id_status_label):
        id = id_entry.get("0.0", "end-1c").strip() 
        if id:
            person = DatabaseHandler.get_person_by_id(id)
            if person:
                _, _, _, image_path = person  
                result = DatabaseHandler.delete_person_by_id(id)
                if result:
                    try:
                        if os.path.exists(image_path):
                            os.remove(image_path)
                            print(f"Image deleted: {image_path}")
                    except Exception as e:
                        print(f"Error deleting image: {e}")

                    # Close the delete window and refresh the person list
                    delete_person_window.destroy()
                    self.show_all_persons(self.frame2)
                else:
                    id_status_label.configure(text="Failed to delete person.", text_color="red")
            else:
                id_status_label.configure(text="No person found with this ID.", text_color="red")
        else:
            id_status_label.configure(text="Please enter a valid ID.", text_color="red")

    def navigate_to_main_menu(self):
        from views.MainMenu import MainMenu
        if hasattr(self.master, "current_frame") and self.master.current_frame is not None:
            self.master.current_frame.destroy()  
        self.master.current_frame = MainMenu(self.master)  
        self.master.current_frame.grid(row=0, column=0, padx=10, pady=10)

    def show_search_dialog(self):
        search_window = CTkToplevel(self)
        search_window.title("Search Person")
        search_window.geometry("500x300+600+300") 

        search_window.frame1 = CTkFrame(search_window)
        search_window.frame1.grid(row=0, column=0, padx=14, pady=50)

        heading = CTkLabel(search_window.frame1, text="Search Person", font=("Microsoft YaHei UI Light", 20,"bold"), text_color="white")
        heading.grid(row=0, column=0, columnspan=2, padx=0, pady=(30,15), sticky="ew")
        
        # Id / name input
        label = CTkLabel(search_window.frame1, text="Id / Name", font=("Microsoft YaHei UI Light", 16, "bold"))
        label.grid(row=1, column=0, padx=(30,10), pady=(10,0), sticky="ew")
        entry = CTkTextbox(search_window.frame1, height=1, width=200)
        entry.grid(row=1, column=1, padx=(0,30), pady=(10,0), sticky="w")

        search_btn = CTkButton(search_window.frame1, text="Search Person", width=200, command=lambda: self.select_person(entry, search_window, entry_status_label))
        search_btn.grid(row=2, column=0, padx=(30,10), pady=(10,0), sticky="w")

        # Close button
        close_btn = CTkButton(search_window.frame1, text="Cancel", width=200, command=search_window.destroy)
        close_btn.grid(row=2, column=1, padx= (0,30), pady=(10,0), sticky="w")

        # Id status label
        entry_status_label = CTkLabel(search_window.frame1, text="", font=("Microsoft YaHei UI Light", 14), text_color="red")
        entry_status_label.grid(row=3, column=0, columnspan=2, padx= 30, pady=(5,15), sticky="w")

        search_window.resizable(False, False)  
        search_window.transient(self)  
        search_window.grab_set()  

    def select_person(self, entry, window, entry_status_label):
        value = entry.get("0.0", "end-1c").strip() 

        if value.isdigit():  
            result = DatabaseHandler.get_person_by_id(int(value))
        elif isinstance(value, str) and value: 
            result = DatabaseHandler.get_person_by_name(value)
        else:  
            entry_status_label.configure(text="Invalid input, please enter a valid ID or name", text_color="red")
            return  

        if result:
            window.destroy() 
            self.refresh_person_list(self.frame2,result)  
        else:
            entry_status_label.configure(text="No person found ", text_color="red")

    def refresh_person_list(self, frame, persons):
        for widget in frame.winfo_children():
            widget.destroy()

        header_frame = CTkFrame(frame)
        header_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        header_frame.grid_columnconfigure(0, weight=1)  
        header_frame.grid_columnconfigure(1, weight=1)  
        header_frame.grid_columnconfigure(2, weight=1)  

        checkbox_header = CTkLabel(header_frame, text="Select", font=("Microsoft YaHei UI Light", 16, "bold"), text_color="white")
        checkbox_header.grid(row=0, column=0, padx=0, pady=10)

        id_header = CTkLabel(header_frame, text="ID", font=("Microsoft YaHei UI Light", 16, "bold"), text_color="white")
        id_header.grid(row=0, column=1, padx=0, pady=10)

        name_header = CTkLabel(header_frame, text="Name", font=("Microsoft YaHei UI Light", 16, "bold"), text_color="white")
        name_header.grid(row=0, column=2, padx=0, pady=10)

        row = 1

        # Add person rows with checkboxes
        for person in persons:
            person_id, name = person

            # Checkbox for selection
            check_box = CTkCheckBox(header_frame, text=row, font=("Microsoft YaHei UI Light", 15), command=lambda person_id=person_id: self.handle_checkbox_toggle(person_id))
            check_box.grid(row=row, column=0, padx=0)

            # ID label
            person_id_label = CTkLabel(header_frame, text=f"{person_id}", font=("Microsoft YaHei UI Light", 15), text_color="white")
            person_id_label.grid(row=row, column=1, padx=0)

            # Name label
            person_name = CTkLabel(header_frame, text=f"{name}", font=("Microsoft YaHei UI Light", 15), text_color="white")
            person_name.grid(row=row, column=2, padx=0)

            row += 1

    def handle_checkbox_toggle(self, person_id,check_box):
        person = DatabaseHandler.get_person_by_id(person_id)
        if not person:
            print(f"No person found with ID {person_id}")
            return

        person_id, name, encoded_face, image_path = person

        person_details_window = CTkToplevel(self)
        person_details_window.title(f"Details of {name}")
        person_details_window.geometry("450x270+600+300")

        # Configure the window layout
        person_details_window.grid_rowconfigure(0, weight=1)
        person_details_window.grid_columnconfigure(0, weight=1)
        person_details_window.grid_columnconfigure(1, weight=1)

        # Left frame for ID and Name
        left_frame = CTkFrame(person_details_window)
        left_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")

        # Title
        title_label = CTkLabel(
            left_frame,
            text="Person Details",
            font=("Microsoft YaHei UI Light", 22, "bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=35, pady=(35, 10), sticky="ew")

        # ID
        id_label = CTkLabel(
            left_frame,
            text=f"ID: {person_id}",
            font=("Microsoft YaHei UI Light", 16),
            text_color="white"
        )
        id_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        # Name
        name_label = CTkLabel(
            left_frame,
            text=f"Name: {name}",
            font=("Microsoft YaHei UI Light", 16),
            text_color="white"
        )
        name_label.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="w")

        # Right frame for Image
        right_frame = CTkFrame(person_details_window)
        right_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        try:
            image = Image.open(image_path)
            img_ctk = CTkImage(light_image=image, size=(150, 180))  
            img_label = CTkLabel(right_frame, image=img_ctk, text="")  
            img_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        except Exception as e:
            print(f"Error loading image: {e}")
            img_label = CTkLabel(
                right_frame,
                text="Image not available",
                font=("Microsoft YaHei UI Light", 14),
                text_color="red"
            )
            img_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        close_btn = CTkButton(
            person_details_window,
            text="Close",
            command=person_details_window.destroy,
            fg_color="#007bff",
            font=('Torus Notched SemiBold', 16, "bold")
        )
        close_btn.grid(row=1, column=0, 
                       columnspan=2,  padx=10, 
                       pady=(15, 10), 
                       sticky="ew")

        person_details_window.transient(self)
        person_details_window.grab_set()
        check_box.deselect()
        