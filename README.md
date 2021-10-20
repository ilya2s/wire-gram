# WIRE-GRAM
A python script wich can automatically forward Telegram messages from a channel, group or chat to another channel, group or chat. This script can easily be deployed in the cloud through Heroku.

## Installation

Make sure to change the values of __ACCOUNT__, __PHONE_NUMBER__, __API_ID__, __API_HASH__, __SOURCE_CHAT__ and __TARGET_CHAT__ in ```wire-gram.py``` :
```python
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
```


#### Requirements
wire-gram requires [Pyrogram](https://docs.pyrogram.org/) framework. You can install it by running the following command in your terminal :

```bash
pip3 install -U pyrogram tgcrypto
```

#### Telegram API
You can get your __API_ID__ and __API_HASH__ from the [Telegram offical API](https://my.telegram.org/).

Visit https://core.telegram.org/ for more details.

## Deploy to Heroku
wire-gram can easily be deployed to Heroku by following their guide : [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python).

__runtime.txt__ declares wich version of python you're using && __requirements.txt__ declares the dependancies.

#### Dynos
Heroku runs your program on a web dyno(thread) by default. wire-gram is not at that stage yet, we have to run it on a backgroud __worker__ dyno.

 After creating the heroku app and deploying the script you need to run the following commands :

This command will kill the default web dyno :

```bash
heroku ps:scale web=0
```

This command will open a worker dyno :

```bash
heroku ps:sclae worker=1
```

## 





