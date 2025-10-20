import cv2
import tkinter as tk
from tkinter import Label
import os
import numpy as np

# Cargar los clasificadores Haar para rostros y ojos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Inicializar el capturador de video (0 por defecto es la cámara principal)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

# Crear la ventana de la interfaz con Tkinter
root = tk.Tk()
root.title("Detección de Rostros con Lentes")

# Instrucción en la interfaz gráfica
instruction_label = Label(root, text="Presiona 'o' para tomar foto\nPresiona 'q' para salir", font=('Arial', 14))
instruction_label.pack()

# Variable para almacenar la imagen capturada
captured_frame = None

# Inicializar el reconocedor de rostros LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Ruta para almacenar el archivo de entrenamiento
training_data_path = "trainer"
if not os.path.exists(training_data_path):
    os.makedirs(training_data_path)

trainer_file = f"{training_data_path}/trainer.yml"

# Si el archivo de modelo ya existe, cargarlo
if os.path.exists(trainer_file):
    recognizer.read(trainer_file)
    print("Modelo de entrenamiento cargado correctamente.")
else:
    print("No se encontró un modelo entrenado. Se entrenará uno nuevo.")

# Función para actualizar la imagen de la cámara en la interfaz gráfica
def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convertir la imagen a RGB para mostrarla en Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Crear una imagen de Tkinter a partir de la imagen de OpenCV
        img = tk.PhotoImage(image=frame)
        label.img = img
        label.config(image=img)
    root.after(10, update_frame)

# Crear un widget Label para mostrar la cámara en vivo
label = Label(root)
label.pack()

# Variable global para contar los ID de los rostros
id_counter = 0

# Diccionario para almacenar los nombres con sus IDs
id_to_name = {}

# Función para registrar un rostro y su nombre
def register_face(face, name):
    global id_counter  # Usamos la variable global
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = face[y:y+h, x:x+w]
        # Añadir el rostro al dataset para entrenamiento
        face_samples.append(roi_gray)
        ids.append(id_counter)  # Asignar un ID único entero
        id_to_name[id_counter] = name  # Guardar el nombre asociado al ID
        id_counter += 1  # Incrementar el contador de ID
        cv2.putText(face, f"Registrando: {name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Lista para almacenar los rostros registrados y sus ids
face_samples = []
ids = []

# Función principal de la cámara en vivo
while True:
    # Captura el frame en vivo
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo obtener el frame de la cámara")
        break

    # Mostrar las instrucciones de las teclas en el frame
    cv2.putText(frame, "Presiona 'o' para tomar foto", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Presiona 'q' para salir", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Si ya se han registrado rostros, hacer reconocimiento en vivo
    if len(face_samples) > 0:  # Verifica si ya se registraron rostros
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en la imagen
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Dibujar un rectángulo azul alrededor de los rostros detectados
        for (x, y, w, h) in faces:
            # Dibujar un rectángulo azul alrededor del rostro
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Región de los ojos dentro del rostro detectado
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Si se detectan al menos 2 ojos, considera que la persona usa lentes
            if len(eyes) >= 2:  # Si se detectan dos ojos, probablemente esté usando lentes
                # Añadir texto sobre el rectángulo del rostro
                cv2.putText(frame, "Utiliza lentes", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Reconocer al rostro registrado
            id_, confidence = recognizer.predict(roi_gray)
            if confidence < 100:  # Si la confianza es baja, significa que se reconoce bien
                name = id_to_name.get(id_, "Desconocido")  # Obtener el nombre desde el diccionario
                cv2.putText(frame, f"Nombre: {name}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Cuadro verde para la persona reconocida

    # Mostrar el video en vivo con el cuadro y el nombre
    cv2.imshow('Camera Live', frame)

    # Esperar por una tecla
    key = cv2.waitKey(1) & 0xFF

    # Si se presiona "o", tomar la foto y registrar el rostro
    if key == ord('o'):
        captured_frame = frame
        print("Foto tomada")

        # Registrar rostro y nombre
        name = input("Ingresa el nombre de la persona: ")
        register_face(captured_frame, name)

        # Entrenar el modelo con los rostros registrados solo una vez
        if len(face_samples) > 0:  # Asegúrate de que haya rostros registrados
            recognizer.train(face_samples, np.array(ids))
            recognizer.save(f"{trainer_file}")  # Guardar el modelo entrenado
            print(f"Modelo de entrenamiento guardado en {trainer_file}")

    # Si se presiona "q", salir
    elif key == ord('q'):
        print("Saliendo...")
        break

# Liberar la cámara en vivo
cap.release()

# Cerrar todas las ventanas de OpenCV
cv2.destroyAllWindows()
