import pyttsx3
import speech_recognition as sr
import mysql.connector
from difflib import SequenceMatcher as SM
import random
import time
from io import open
import time, sys

recognizer=sr.Recognizer()
microphone = sr.Microphone(device_index=0)
eng = pyttsx3.init()
eng.setProperty("rate", 140)
eng.setProperty("volume", 1.0)
listVoices=eng.getProperty("voices")
eng.setProperty("voice", listVoices[1].id)
eng.say("Welcome again")
eng.runAndWait()

def recognizeMicAudio():
    word = ""
    print("Listen...")
    with microphone as source:
        audio=recognizer.listen(source)
        word=recognizer.recognize_google(audio)
    return word

conexion=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="diccionario")
cursor=conexion.cursor(buffered = True)

word=""
contador=0
while word != "silence":
    word = recognizeMicAudio()
    #print(word)
    cursor.execute("SELECT * FROM oracion")
    nDatos=cursor.rowcount
    #print("Se han encontrado", nDatos)

    for fila in cursor:
        ide = fila[0]
        entrada=fila[1]
        salida=fila[2]
        #print(ide)
        #print(entrada)
        #print(salida)
        similitud = SM(None, entrada, word).ratio()
        if similitud>0.8:
            eng.say(salida)
            eng.runAndWait()
        """if similitud<0.8:
            print("Has entado en el else")
            cursor.execute("INSERT INTO oracion VALUES(NULL,'Pregunta','Respuesta')")
            conexion.commit()"""
