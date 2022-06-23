#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from conexionDB import DataBase

import pyrebase


#Creo el enlace con Google Firebase Firestore Para obtener las descripciones.
cred = credentials.Certificate('lsmKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

firebaseConfig = {
    'apiKey': "AIzaSyCJac1VR0O03uWSCKx6K98ggr6e9o5OdeI",
    'authDomain': "aprendiendo-lsm.firebaseapp.com",
    'databaseURL': "https://aprendiendo-lsm.firebaseio.com",
    'projectId': "aprendiendo-lsm",
    'storageBucket': "aprendiendo-lsm.appspot.com",
    'messagingSenderId': "399242686008",
    'appId': "1:399242686008:web:2167ebeccb8fb6c61000cd",
    'measurementId': "G-RYY680CFF5"
}

firebase = pyrebase.initialize_app(firebaseConfig)




# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

database = DataBase()

#Contadores de uso
contUsoAcc = 1
contUsoAve = 1
contUsoAni = 1
contUsoCom = 1
contUsoCri = 1
contUsoDoc = 1
contUsoDra = 1
contUsoFam = 1
contUsoFan = 1
contUsoHis = 1
contUsoHor = 1
contUsoMus = 1
contUsoMys = 1
contUsoRom = 1
contUsoCie = 1
contUsoTvm = 1
contUsoThr = 1
contUsoGue = 1
contUsoWes = 1



# Manejador cuando una persona no escribe un comando
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Por favor, seleccione un comando de la lista desplegada por /Inicio o /Información ")

# Manejadores de comandos del ChatBot.
def start(update, context):
    users_dic = {
        'id': update.message.from_user.id,
        'primer_nombre': update.message.from_user.first_name
    }
    
    inicio = f"""¡Hola {users_dic["primer_nombre"]} ! Bienvenido a LSM ChatBot, aquí encontrarás un diccionario electrónico de fácil acceso para el Lenguaje de Señas Mexicano (LSM). :) \nElige entre los siguientes géneros.\n/Abecedario\n/Animales\n/Calendario\n/Color\n/FrutasYVerduras\n/Lugares\n/Numeros\n/RepublicaMexicana\nPara volver a este panel de selección recuerda escribir /Inicio"""
    update.message.reply_text(inicio)

    database.agregarUsuarios(users_dic)
   
def buscar(update, seccion):
    buscarsec = db.collection(str(seccion))
    docs = buscarsec.stream()
    storage = firebase.storage()
    for doc in docs:
        biblio = doc.to_dict()
        update.message.reply_text("IMAGEN: "+storage.child(doc.id+".png").get_url(None)+"\n ** PALABRA: {} **\nDescripción: {}".format(doc.id, biblio["desc"]))
        #print(u'{} => {}'.format(doc.id, doc.to_dict()))

    

def info(update, context):
    informacion = "Gracias por utilizar este chat.\nEspero que este diccionario electrónico te haya servido. :)\nDesarrollado por: Erick Oswaldo Gallegos Pérez\nCorreo: erozgp@gmail.com\nInstagram: @gallegos.lml\nUNISTMO Campus Tehunatepec."
    update.message.reply_text(informacion)

def abecedario(update, context):
    global contUsoAve
    update.message.reply_text("Buscando para Abecedario...")
    buscar(update, 'abecedario')
    contUsoAve+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

def animales(update, context):
    global contUsoAcc
    update.message.reply_text("Buscando para Animales...")
    buscar(update, 'ANIMALES')
    contUsoAcc+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

def calendario(update, context):
    global contUsoAni 
    update.message.reply_text("Buscando para Calendario...")
    buscar(update, 'CALEN')
    contUsoAni+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

def color(update, context):
    global contUsoCom
    update.message.reply_text("Buscando para Color...")
    buscar(update, 'COLOR')
    contUsoCom+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

def fv(update, context):
    global contUsoCri
    update.message.reply_text("Buscando para Frutas y verduras...")
    buscar(update, 'FV')
    contUsoCri+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

def lugares(update, context):
    global contUsoDoc
    update.message.reply_text("Buscando para Lugares...")
    buscar(update, 'LG')
    contUsoDoc+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

def numeros(update, context):
    global contUsoDra
    update.message.reply_text("Buscando para Números...")
    buscar(update, 'NUMEROS')
    contUsoDra+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

def mexico(update, context):
    global contUsoFam
    update.message.reply_text("Buscando para República Mexicana...")
    buscar(update, 'MX')
    contUsoFam+=1
    update.message.reply_text("¿Desea volver al panel de selección? \nToca aquí /Inicio")

    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1494828937:AAFEg563d9Zkr51mR0Y8Ohx3xi4MnTKKA2I", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("Inicio", start))
    #dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("Abecedario", abecedario))
    dp.add_handler(CommandHandler("Animales", animales))
    dp.add_handler(CommandHandler("Calendario", calendario))
    dp.add_handler(CommandHandler("Color", color))
    dp.add_handler(CommandHandler("FrutasYVerduras", fv))
    dp.add_handler(CommandHandler("Lugares", lugares))
    dp.add_handler(CommandHandler("Numeros", numeros))
    dp.add_handler(CommandHandler("RepublicaMexicana", mexico))
    dp.add_handler(CommandHandler("Informacion", info))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()