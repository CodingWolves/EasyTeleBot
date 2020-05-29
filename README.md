# EasyTeleBot
EasyTeleBot is a package for creating an automated bot responder for telegram in python.

The program uses flask and webhook to get user messages from telegram.

## Installation
Install the package by entering in terminal
 
```pip install easytelebot```

Package Dependencies:
- flask
- python-telegram-bot

## Usage 
```import EasyTeleBot```

After importing the EasyTeleBot get the config json file in one of two ways:

1. As string path ```config_file = "config_file.json"```
1. As IO readable ```config_file = open("config_file.json")```

Use CreateEasyTelegramBot to create the bot it will create the whole bot automatically.

```bot = EasyTeleBot.CreateEasyTelegramBot(config_file)```

Inside this class lays a flask app which you can get by typing - ```bot.flask_app```.
Run this flask app to start handling the messages telegram is sending to the bot (user message go through telegram servers).

Tested WSGI Usages:
- [x] gunicorn ```gunicorn myapp:bot.flask_app```
- [ ] nginx
- [ ] Django



## Config File
Create a config file in json format according to these rules :
1. **"telegram_token"** - Is the telegram api token you get after creating a new bot through [BotFather](https://telegram.me/BotFather).
1. **"webhook_url"** - This is the url to tell telegram servers to forward the messages users send to bot chat,
 typically it will be the server url beginning and an identifier.
 example: ```"https://example-server.herokuapp.com/example-identifier"```.
 The bot listens to this url. 
1. **"bot_name"** - Your bot name. Will make the flask server with this name.
1. [**"actions"**](https://github.com/idozahavy/EasyTeleBot#Action) - A list of actions to configure the bot behavior.

#### Example config_file.json
```
{
    actions:[
        ...
    ]  
    "telegram_token": "example_token:KG5Gdv6AK05aeGctf25",
    "webhook_url": "https://example-server.herokuapp.com/example-identifier",
    "bot_name": "example_bot"
}
```

## Action
Each action has these attributes:
1. **"id"** - Action identifier.
1. **"triggers"** - List of user messages that initiate this action.
1. [**"type"**](https://github.com/idozahavy/EasyTeleBot#ActionTypes) - The type of action. Each type of action does a different thing.
1. **"data"** - The data of the function (read _"Action Types"_ to better understand). 
If there is a format, it will try to extract saved information, example _"{data.name}"_ will change to the value saved in _"name"_.
_"{data.last_text_received}"_ will change into the last text message the user sent to the bots chat.

Optional attributes:
- **"next_act_id"** - Do this ids action right after the this action finishes.
- **"follow_up_act_id"** - The follow up action id, does this after the user sends back a message. This is for question actions.
- **"markup_type"** - When sending a markup, the users chat will have options to press, like _"/start"_ and _"/help"_.
Every _','_ will separate between words and every _':'_ will separate between rows.
    - **"remove"** - Removes the previous markup the users chat has.
    - **"reply"** - Sends the markup to the user, when the user presses on one, it minimizes it.
    - **"static-reply"** - Sends the markup to the user, it will stay until you remove it.
- **"markup_data"** - If _"markup_type"_ is _"reply"_ or _"static-reply"_, uses this to make a list of reply keyboard options.

**Do not** use both _"next_act_id"_ and _"follow_up_act_id"_ in the same action. Use only one of them or none.

#### Example action
```
...
{
    "id": 1,
    "triggers": ["hi", "hello", "hey"],
    "type": "text",
    "data": "server says hello back",
    "next_act_id": 2
},
{
    "id": 2,
    "triggers": [],
    "type": "text",
    "data": "server got to this action right after action id 1, now you got markup options",
    "markup_type": "reply",
    "markup_data": "left top,right top:left bottom,right bottom"
},
...
```

## Action Types
### text
Sends back a message containing _"data"_.
```
...
    "triggers": ["hi", "hello", "hey"],
    "type": "text",
    "data": "server says hello back",
...
```

### animation
Sends back an animation where _"data"_ is the url of the animation. 
Converts all to gifs.
```
...
    "triggers": ["puppy"],
    "type": "animation",
    "data": "https://media.giphy.com/media/5awVf7q1nwkus/giphy.gif",
...
```

### save
Saves the value that is in _"data"_ into _"save_to_data_name"_.
```
...
    "triggers": ["save 'ok' into 'blop' data name"],
    "type": "save",
    "data": "ok",
    "save_to_data_name": "blop"
...
```
Usually **you should** use it to save user input like this example:
```
...
{
    "id": 1,
    "triggers": ["save my name"],
    "type": "text",
    "data": "please enter your name",
    "follow_up_act_id": 2
},
{
    "id": 2,
    "triggers": [],
    "type": "save",
    "data": "{data.last_text_received}",
    "save_to_data_name": "name",
    "next_act_id": 3
},
{
    "id": 3,
    "triggers": [],
    "type": "text",
    "data": "your name is {data.name}",
},
```




