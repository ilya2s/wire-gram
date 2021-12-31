from ast import parse
from inspect import cleandoc
import re
from pyrogram import Client
from pyrogram import filters
import pyrogram
from pyrogram.methods.messages import send_message
from pyrogram.types.messages_and_media.message import Message
from pyrogram.types import Photo
import os
import argparse


# ----------- CONFIG ---------- #
# ACCOUNT & PHONE_NUMBER have to be a STRING
ACCOUNT = "YOUR TELEGRAM USERNAME"
PHONE_NUMBER = "YOUR TELEGRAM PHONE NUMBER"


# API ID
API_ID = 111111                                                 # YOUR TELEGRAM API ID
API_HASH = "fj232jfj20rj0932ir203jf9j320ur22"                   # YOUR TELEGRAM API HASH


# CHAT IDs
SOURCE_CHAT = 0                                                 # The ID of the chat where you want to listen for messages (can be a table of int for multiple source chats)
TARGET_CHAT = 0                                                 # The ID of the chat where you wanna forward messages to (can be a table of int for multiple target chats)
# ----------------------------- #


app = Client(
    ACCOUNT,
    phone_number=PHONE_NUMBER,
    api_id=API_ID,
    api_hash=API_HASH
)


# Cool print if you run wire-gram on your terminal
wire_gram = """
=====================================================================

██╗    ██╗██╗██████╗ ███████╗     ██████╗ ██████╗  █████╗ ███╗   ███╗
██║    ██║██║██╔══██╗██╔════╝    ██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
██║ █╗ ██║██║██████╔╝█████╗█████╗██║  ███╗██████╔╝███████║██╔████╔██║
██║███╗██║██║██╔══██╗██╔══╝╚════╝██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
╚███╔███╔╝██║██║  ██║███████╗    ╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝

=====================================================================
"""
print(wire_gram)


# Prints all chat IDs
async def getAllChatIDs():
    async with app:
        for x in  await app.get_dialogs():
            print(x.chat.type, x.chat.title, x.chat.id)


# Verify if a message is a reply
def isMessageReply(message):
    isReply = isinstance(message.reply_to_message, Message)
    return isReply


# Parse Message : 
# if message is a reply : return a list of [Original message, reply]
# if is not a reply : return the message
def parseMessage(message):
    if(isMessageReply(message)):
        parsedMessage = [message.reply_to_message, message]
        return parsedMessage
    else :
        parsedMessage = message
        return parsedMessage 


# Verify if a parsed Message is a reply
def isParsedMessageReply(parsedMessage):
    isReply = isinstance(parsedMessage, list)
    return isReply


# Fetch the original message of a reply
def fetchOriginalMessage(parsedMessage):
    if (isParsedMessageReply(parsedMessage)) :
        return parsedMessage[0]


def fetchReplyMessage(parsedMessage):
    if (isParsedMessageReply(parsedMessage)) :
        return parsedMessage[1]


# Get Target chat history : return a list of {Message}
def targetHistory(client, targetChatID):
    return client.get_history(targetChatID)


# Compare the text of two Messages
def compareText(firstMessage, secondMessage):
    return firstMessage.text == secondMessage.text


# Find a similarity between one of the messages in the history and the original message
# return id of the similar message in history
def compareMessages(history, originalMessage):
    similarity = False
    for m in history :
        similarity = compareText(m, originalMessage)
        if similarity :
            return m.message_id
        

# Verify if Message is a Photo
def isMessagePhoto(message) :
    return isinstance(message.photo, Photo)


# Keep track of the progress while downloading
def progress(current, total) :
    print(f"{current * 100 / total:.1f}%")


# Download the Photo from Message
def downloadPhoto(client, message) :
    if(isMessagePhoto(message)) :
        return client.download_media(message, progress=progress)


def sendMessage(client, parsedMessage):
    if (isParsedMessageReply(parsedMessage)):
        original = fetchOriginalMessage(parsedMessage)
        reply = fetchReplyMessage(parsedMessage)
        history = targetHistory(client, TARGET_CHAT)
        isSimilarID = compareMessages(history, original)

        if (isMessagePhoto(reply)):
            photoPath = downloadPhoto(client, reply)

            client.send_photo(
                chat_id = TARGET_CHAT,
                photo = photoPath,
                reply_to_message_id = isSimilarID
            )

            os.remove(photoPath)
        else :
            client.send_message(
                chat_id = TARGET_CHAT,
                text = reply.text,
                reply_to_message_id = isSimilarID
            )

    else :
        if (isMessagePhoto(parsedMessage)):
            photoPath = downloadPhoto(client, parsedMessage)

            client.send_photo(
                chat_id = TARGET_CHAT,
                photo = photoPath
            )

            os.remove(photoPath)
        else :
            client.send_message(
            chat_id = TARGET_CHAT,
            text = parsedMessage.text
        )        


# Creates "--id" parameter for command line
parser = argparse.ArgumentParser(description='Print IDs or Forward messages')
parser.add_argument('-i', '--id',action='store_true',  help='Print the id of all current chats')
args = parser.parse_args()

if args.id:
    app.run(getAllChatIDs())
else:
    @app.on_message((filters.chat(SOURCE_CHAT)) & (~filters.regex("IGNORE ANY MESSAGE THAT CONTAINS THIS STRING")))


    def my_handler(client, message):
        parsedMessage = parseMessage(message)
        sendMessage(client, parsedMessage)
        print("MESSAGE SENT")


    app.run()