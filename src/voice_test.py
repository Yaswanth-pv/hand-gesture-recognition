import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)    # speaking speed (words per minute)
engine.setProperty('volume', 1.0)  # volume (0.0 to 1.0)

engine.say("Hand gesture recognition system is ready")
engine.runAndWait()