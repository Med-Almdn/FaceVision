import sqlite3
import json
import numpy as np

class DatabaseHandler:
    DATABASE_PATH = 'face_data.db'

    @staticmethod
    def create_connection():
        return sqlite3.connect(DatabaseHandler.DATABASE_PATH)

    @staticmethod
    def create_table():
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                encoding BLOB NOT NULL,
                image_path TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    @staticmethod
    def insert_person(person_id, name, encoding, image_path):
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()

        cursor.execute(''' 
            INSERT INTO persons (id, name, encoding, image_path)
            VALUES (?, ?, ?, ?)
        ''', (person_id, name, encoding, image_path))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_persons_id_and_name():
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id, name FROM persons')
        persons = cursor.fetchall()

        conn.close()
        return persons

    @staticmethod
    def get_person_by_name(name):
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM persons WHERE name = ?
        ''', (name,))
        person = cursor.fetchone()

        conn.close()
        return person

    @staticmethod
    def get_person_by_id(person_id):
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM persons WHERE id = ?
        ''', (person_id,))
        person = cursor.fetchone()

        conn.close()
        return person

    @staticmethod
    def get_all_persons():
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM persons')
            rows = cursor.fetchall()

            ids_list = []
            names_list = []
            encode_list = []
            image_paths = []

            for row in rows:
                ids_list.append(row[0])    
                names_list.append(row[1])
                encode_list.append(np.array(json.loads(row[2]), dtype=np.float64))  # Deserialize encoding       
                image_paths.append(row[3])
            
            return ids_list, names_list, encode_list, image_paths
        
        except Exception as e:
            print(f"Error fetching persons: {e}")
            return [], [], [], []
        finally:
            conn.close()

    @staticmethod
    def delete_person_by_id(person_id):
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM persons WHERE id = ?
        ''', (person_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    @staticmethod
    def get_all_person_names_and_ids():
        conn = DatabaseHandler.create_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id, name FROM persons')
        persons = cursor.fetchall()

        conn.close()
        return persons


