from SpeechRecognitionScript import ReconocerComandos
from GoogleTextToSpeech import ReproducirMensaje
from InicializarProcesos import InicializarProcesos

if __name__ == "__main__":
    InicializarProcesos()
    ReproducirMensaje("Hola Usuario")
    ReconocerComandos()