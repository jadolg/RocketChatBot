# REST API based bot for [Rocket.Chat](http://rocket.chat)

## Install

`pip install RocketChatAPIBot`

## Usage

### Create new bot

```python
import os
from RocketChatBot import RocketChatBot

botname = os.environ['BOTNAME']
botpassword = os.environ['BOTPASSWORD']
server_url = os.environ['BOT_URL']

bot = RocketChatBot(botname, botpassword, server_url)
```

### Send message to channel

`bot.send_message('starting bot...', channel_id='GENERAL')`

### Direct message handler

Gets triggered when sentence starts with the botname like '@botname echo hello'

```python
def greet(msg, user, channel_id):
    bot.send_message('hello @' + user, channel_id)
    
bot.add_dm_handler(['hey', 'hello', ], greet)
```

Receives a list of keywords to trigger the command and the method to execute. The method should receive as parameters always msg as the message, user and channel_id

### Auto answer handler

Gets triggered with the mention of keywords. Only made to respond with simple text, no functions.
```python
bot.add_auto_answer(['good news', 'i have good news', ], ['hell yeah!', 'tell me, tell me!', 'you are already good news ;)', ])

```

### Direct answer handler

Gets triggered when sentence starts with the name of the bot and keywords are in the sentence like '@botname who are you?'
```python
bot.add_direct_answer(['who are you?', 'what is your name?', ], ['I am botname', ])
```

### Handle unknow commands

```python
bot.unknow_command = ['I do not know what you want me to do...', 'I\'m almost sure I\'m not programmed to do that', 'I have no idea how to do that so here is a hug :hugging:']
```
