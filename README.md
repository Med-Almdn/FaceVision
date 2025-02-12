# FaceVision: Real-Time Facial Recognition System

## Description

FaceVision is a modular and scalable facial recognition system designed for real-time face detection and personnel management. The system integrates advanced facial recognition technologies with an intuitive graphical user interface, making it suitable for applications such as attendance tracking, access control, and identity verification.

## Features

- **Real-Time Face Detection**: Utilizes the `face_recognition` library and OpenCV for live video feed processing with minimal latency.
- **CRUD Operations**: Full support for Create, Read, Update, and Delete operations on personnel records.
- **Image-Based Encoding**: Converts facial images into 128-dimensional numerical vectors for accurate identification.
- **Modern GUI**: Built using CustomTkinter, providing a responsive and visually appealing user interface.
- **Database Management**: Uses SQLite for secure and efficient storage of facial encodings, metadata, and images.
- **Icons**: Various icons integrated in the interface for better user experience, such as:
  - **Person Icon** for adding or managing personnel
  - **Camera Icon** for accessing live streaming
  - **Database Icon** for managing the database
  - **Search Icon** for personnel search functionality

## Architecture

FaceVision is structured into three primary layers:

1. **Database Layer**: Manages data storage and retrieval using SQLite.
2. **Utilities Layer**: Handles backend operations like image preprocessing and face matching.
3. **Application GUI**: Provides a user-friendly interface for interacting with the system.

## Technology Stack

- **Programming Language**: Python
- **Facial Recognition**: `face_recognition` library, OpenCV
- **Database**: SQLite
- **GUI Framework**: CustomTkinter
- **Image Processing**: Pillow (PIL)
- **Data Handling**: Numpy
- **Concurrency**: Threading

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Med-Almdn/FaceVision.git
   ```
2. Navigate to the project directory:
   ```bash
   cd FaceVision
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Welcome Screen**: Start by navigating through the welcome screen to the main menu.
2. **Main Menu**: Access different modules such as real-time streaming and image management.
3. **Image Manager**: Add, delete, or search for personnel records using intuitive icons like the **Person Icon** and **Search Icon**.
4. **Streaming Module**: View live video feed with real-time face detection and recognition.

## What I Learned

- **Facial Recognition Technology**: I gained hands-on experience with the `face_recognition` library and OpenCV, deepening my understanding of facial recognition, face detection, and encoding techniques.
- **SQLite Database Integration**: Learned how to integrate SQLite into a Python application for efficient and secure data management.
- **Real-Time Video Processing**: Improved my skills in handling real-time video streams, utilizing OpenCV to process frames and match faces on the fly.
- **Graphical User Interface (GUI) Design**: Mastered the use of CustomTkinter to design an intuitive and responsive user interface that supports modern features like icons and modularity.
- **Image Encoding**: I learned how to convert images into a numerical format that can be used for efficient comparison and matching in real-time applications.

## Code Structure

- **main.py**: Entry point of the application.
- **views/**: Contains GUI modules (WelcomeScreen.py, MainMenu.py, ImageManagementModule.py, LiveStreamModule.py).
- **models/**: Core data model definitions (DatabaseHandler.py).
- **assets/**: Static resources like images and icons.
- **image_folder/**: Stores user-uploaded images.
- **face_data.db**: SQLite database file.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgments

- Thanks to the developers of the `face_recognition` library and OpenCV for their robust tools.
- Special thanks to the CustomTkinter community for providing a modern GUI framework.
