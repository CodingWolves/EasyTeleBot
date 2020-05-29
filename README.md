# EasyTeleBot
EasyTeleBot is a package for creating an automated bot responder for telegram in python.

The program uses flask and webhook to get user messages from telegram.

##Installation
Install the package by entering in terminal
 
```pip install easytelebot```

Package Dependencies:
- flask
- python-telegram-bot

##Usage 
After importing the EasyTeleBot get the config json file in one of two ways:
1. As string path ```config_file = "config_file.json"```
1. As IO readable ```config_file = open("config_file.json")```

Use CreateEasyTelegramBot to create the bot it will create the whole bot automatically.

```bot = EasyTeleBot.CreateEasyTelegramBot(config_file)```

Inside this class lays a flask app which you can get by typing - ```bot.flask_app```.
Run this flask app to start handling the messages users sent to the bot.

Tested WSGI Usages:
-[x] gunicorn ```gunicorn myapp:bot.flask_app```
-[ ] nginx
-[ ] Django



##Config File
Create a config file in json format according to the next rules :
1. **"telegram_token"** - Is the telegram api token you get after creating a new bot through [BotFather](https://telegram.me/BotFather).
1. **"webhook_url"** - This is the url to tell telegram servers to forward the messages users send to bots chat,
 typically it will be the server url beginning and an identifier.
 example: ```"https://example-server.herokuapp.com/example-identifier"```.
 The bot listens to this url extension. 
1. **"bot_name"** - Your bot name. Will make the flask server this name.
1. **"actions"** - A list of actions to configure the bot behavior.

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
1. **"type"** - The type of action. Each type of action does a different thing.
1. **"data"** - The data of the function (read "Action Types" to better understand). 
If there is a format, it will try to extract saved information, example "{data.name}" will change to the value saved in "name".

Optional attributes:
- **"next_act_id"** - Do this ids action right after the this action finishes.
- **"follow_up_act_id"** - The follow up action id, does this after the user sends back a message. This is for question actions.
- **"markup_type"** - When sending a markup, the users chat will have options to press, like "/start" and "/help".
Every ',' will separate between words and every ':' will separate between rows.
    - **"remove"** - Removes the previous markup the users chat has.
    - **"reply"** - Sends the markup to the user, when the user presses on one, it minimizes it.
    - **"static-reply"** - Sends the markup to the user, it will stay until you remove it.
- **"markup_data"** - If "markup_type" is "reply" or "static-reply", uses this to make a list of reply keyboard options.

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

##Action Types
### text
Sends back a message containing "data".
```
...
"type": "text",
...
```

### animation
Sends back an animation where "data" is the url of the animation. 
```
...
"type": "animation",
...
```

### save
Saves the value that is in "data" into "save_to_data_name".
```
...
"type": "save",
"save_to_data_name": "data_name"
...
```




