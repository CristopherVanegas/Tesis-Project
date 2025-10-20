import cv2
import tkinter as tk
from tkinter import Label

# Cargar los clasificadores Haar para rostros y ojos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Iniciar la captura de video desde la cámara web (0 por defecto es la cámara principal)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Crear la ventana de la interfaz con Tkinter
root = tk.Tk()
root.title("Detección de Rostros con Lentes")

# Instrucción en la interfaz gráfica
instruction_label = Label(root, text="Presiona 'o' para tomar foto\nPresiona 'q' para salir", font=('Arial', 14))
instruction_label.pack()

# Variable para almacenar la imagen capturada
captured_frame = None


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

# Función principal de la cámara en vivo
while True:
    # Captura el frame en vivo
    ret, frame = cap.read()

    # Mostrar las instrucciones de las teclas en el frame
    cv2.putText(frame, "Presiona 'o' para tomar foto", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Presiona 'q' para salir", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar el video en vivo
    cv2.imshow('Camera Live', frame)

    # Esperar por una tecla
    key = cv2.waitKey(1) & 0xFF

    # Si se presiona "o", tomar la foto
    if key == ord('o'):
        captured_frame = frame
        print("Foto tomada")

        # Detener la cámara en vivo
        break

    # Si se presiona "q", salir
    elif key == ord('q'):
        print("Saliendo...")
        break

# Liberar la cámara en vivo
cap.release()

# Si se capturó una foto, procesarla y mostrarla con los rostros detectados
if captured_frame is not None:
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Dibujar un rectángulo azul alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        # Dibujar un rectángulo azul alrededor del rostro
        cv2.rectangle(captured_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Región de los ojos dentro del rostro detectado
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Verificar si se detectan ojos
        if len(eyes) >= 2:  # Si detecta al menos 2 ojos, asumimos que la persona usa lentes
            # Mejorando la precisión al usar un umbral más riguroso
            cv2.putText(captured_frame, "Utiliza lentes", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            cv2.putText(captured_frame, "No utiliza lentes", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar la foto con los rostros y la anotación de lentes
    cv2.imshow('Captured Photo with Faces and Lentes', captured_frame)
    cv2.waitKey(0)  # Espera hasta que presiones cualquier tecla para cerrar

# Cerrar todas las ventanas de OpenCV
cv2.destroyAllWindows()
