# coding=utf-8
import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)

#este bot está listo para desplegarse en HEROKU
#las variables como el token de verificación y el secret de facebook lo tienen que guardar como variables de entorno en HEROKU.

#este metodo es para verificar el TOKEN de facebook y enlazar el bot
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]: # se guarda en heroku
            return "Error de Token", 403
        return request.args["hub.challenge"], 200

    return "Prueba app via get", 200


@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]

                    #conversación para que puedan probar el bot en forma simple

                    if (message_text == "Hola"):
                        send_message(sender_id, "Hola, quieres empezar")
                    if (message_text == "Si"):
                        send_message(sender_id, "Esta es una prueba de Chat con el API de facebook, escribe Card")
                    if (message_text == "No"):
                        send_message(sender_id, "¿Para que me hablas?, dime que Si")
                    if (message_text == "Card"):
                        send_cards(sender_id,"texto en las cards","http://imagizer.imageshack.us/600x504f/923/MFVbGo.jpg","http://imagizer.imageshack.us/600x399f/923/Wh4tUe.jpg","http://imagizer.imageshack.us/600x400f/922/GCA2N3.jpg")


                if messaging_event.get("delivery"):
                       pass
                if messaging_event.get("optin"):
                       pass
                if messaging_event.get("postback"):
                       pass


    return "ok", 200

#definicion del envío con plantillas genericas de mensajes esta la muestra con un mensaje común y con una card.
#en https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template
#encuentran todos los tipos de plantillas nosotros dejamos con esto dos de muestra.

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"] # y este también se guarda en heroku
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_cards(recipient_id, message_text, img_card_uno, img_card_dos, img_card_tres):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "$1.000.000",
                            "image_url": img_card_uno,
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Me interesa",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }, {
                                    "type": "postback",
                                    "title": "Volver",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }
                            ]
                        }, {
                            "title": "$3.000.000",
                            "image_url": img_card_dos,
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Me interesa",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }, {
                                    "type": "postback",
                                    "title": "Volver",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }
                            ]
                        }, {
                            "title": "$3.000.000",
                            "image_url": img_card_tres,
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Me interesa",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }, {
                                    "type": "postback",
                                    "title": "Volver",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)