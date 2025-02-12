import cv2
import os
import face_recognition

def find_encodings(images):
    encodeList = []
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img_rgb)
        if encodings:
            encodeList.append(encodings[0])
    return encodeList

def load_images_from_folder(folder_path):
    images = []
    class_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(folder_path, filename)
            img = cv2.imread(path)
            images.append(img)
            class_names.append(os.path.splitext(filename)[0])
    return images, class_names
