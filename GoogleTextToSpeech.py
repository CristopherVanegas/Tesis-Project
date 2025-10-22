from gtts import gTTS
import pygame
import os

ruta = 'audios/audio.mp3'

def ConvertirTexto2Audio(mensaje):
    tts = gTTS(mensaje, lang='es')
    if not os.path.exists("audios"):
        os.makedirs("audios")
    tts.save(ruta)

def ReproducirMensaje(mensaje):
    ConvertirTexto2Audio(mensaje)

    if os.path.exists(ruta):
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()                   # Carga y reproduce el archivo de audio
    else:
        ConvertirTexto2Audio('Error gtts001: No se pudo traducir el mensaje de salida.')

    # Espera mientras se reproduce el audio
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


