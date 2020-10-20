import os
import sqlite3

from datetime import datetime

from bottle import get, post, request, template, redirect

import requests
import discord
from discord import Webhook, RequestsWebhookAdapter, File

file = open("TOKEN.txt",'r')
ID = int(file.readline().strip())
TOKEN = file.readline().strip()

ON_PYTHONANYWHERE = "PYTHONANYWHERE_DOMAIN" in os.environ.keys()

if ON_PYTHONANYWHERE:
    from bottle import default_app
else:
    from bottle import run, debug

@get('/')
def get_default():
    return template("default")

@get('/view_messages')
def get_messages():
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()
    cursor.execute("select * from sent_messages")
    result = cursor.fetchall()
    cursor.close()
    return template("view_messages",rows=result)

@get('/send_message')
def get_send_message():
    return template("send_message")

@post('/new_message')
def post_new_message():
    content = request.forms.get("content")
    author = request.forms.get("user_name")
    connection = sqlite3.connect("messages.db")
    cursor = connection.cursor()
    cursor.execute("insert into sent_messages(time,sender,content) values (?,?,?)", (str(datetime.now()), author, content))
    connection.commit()
    cursor.close()

    webhook = Webhook.partial(ID,TOKEN,adapter=RequestsWebhookAdapter())
    webhook.send("New message from: "+author+"\n"+content)

    redirect('/view_messages')




if ON_PYTHONANYWHERE:
    application = default_app()
else:
    debug(True)
    run(host="localhost", port=8080)