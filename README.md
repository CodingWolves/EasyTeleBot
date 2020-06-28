# EasyTeleBot
EasyTeleBot is a package for creating an automated bot responder for telegram in python.

The program uses flask and webhook to get user messages from telegram.

## Installation
Install the package by entering in terminal
 
`pip install easytelebot`

Package Dependencies:
- flask
- python-telegram-bot

## Usage 
`from EasyTeleBot.TelegramBot import EasyTelegramBot`

After importing the EasyTeleBot get the config json file in one of two ways:

1. As string path `config_file = "config_file.json"`
1. As IO readable `config_file = open("config_file.json")`
1. As a **list** of the two above `config_files = [config_file1, config_file2]`

Use CreateEasyTelegramBot to create the bot it will create the whole bot automatically.

`bot = EasyTelegramBot(config_files)`

Inside this class lays a flask app which you can get by typing - `bot.flask_app`.
Run this flask app to start handling the messages telegram is sending to the bot (user message go through telegram servers).

Tested WSGI Usages:
- [x] gunicorn `gunicorn myapp:bot.flask_app`
- [ ] nginx
- [ ] Django

Telegram bot chats start with the word `"/start"` so you should enter this kind of action 


## Config File
Create a config file in json format according to these rules :
1. **"telegram_token"** - Is the telegram api token you get after creating a new bot through [BotFather](https://telegram.me/BotFather).
1. **"webhook_url"** - This is the url to tell telegram servers to forward the messages users send to bot chat,
 typically it will be the server url beginning and an identifier.
 example: `"https://example-server.herokuapp.com/example-identifier"`.
 The bot listens to this url. 
1. **"bot_name"** - Your bot name. Will make the flask server with this name.
1. [**"actions"**](https://github.com/idozahavy/EasyTeleBot#action) - A list of actions to configure the bot behavior.

Optional:

- **"default_action_id"** - If no action triggers this action id will perform.

You can also put those setting when constructing the class, but not actions.

`bot = EasyTelegramBot([file, file2], telegram_token="123", webhook_url="hook_url", bot_name="new_bot", default_action_id=3)`

#### Example config_file.json
```
{
    actions:[
        ...
    ]  
    "telegram_token": "example_token:KG5Gdv6AK05aeGctf25",
    "webhook_url": "https://example-server.herokuapp.com/example-identifier",
    "bot_name": "example_bot",

    "default_action_id": 50621
}
```

## Action
Each action has these attributes:
1. **"id"** - Action identifier.
1. **"triggers"** - List of user messages that initiate this action.
1. [**"type"**](https://github.com/idozahavy/EasyTeleBot#action-types) - The type of action. Each type of action does a different thing.
1. **"data"** - The data of the function (read [Action Types](https://github.com/idozahavy/EasyTeleBot#action-types) to better understand). 
If there is a format, it will try to extract saved information, example `"${name}"` will change to the value saved in `"name"`.
`"${last_text_received}"` will be the last text message the user sent to chat.

Optional attributes:
- **"next_action_id"** - Do this ids action right after the this action finishes.
- **"follow_up_action_id"** - The follow up action id, does this after the user sends back a message. This is for question actions.
- **"markup_type"** - When sending a markup, the users chat will have options to press, like `"/start"` and `"/help"`.
Every `','` will separate between words and every `':'` will separate between rows.
    - **"remove"** - Removes the previous markup the users chat has.
    - **"reply"** - Sends the markup to the user, when the user presses on one, it minimizes it.
    - **"static-reply"** - Sends the markup to the user, it will stay until you remove it.
- **"markup_data"** - If `"markup_type"` is `"reply"` or `"static-reply"`, uses this to make a list of reply keyboard options.

**Do not** use both `"next_action_id"` and `"follow_up_action_id"` in the same action. Use only one of them or none.

#### Example action
```
...
{
    "id": 1,
    "triggers": ["hi", "hello", "hey"],
    "type": "text",
    "data": "server says hello back",
    "next_action_id": 2
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
![Image of Example action and markup](https://github.com/idozahavy/EasyTeleBot/blob/master/.images/markup_example.jpg)

## Action Types
### text
Sends back a message containing the value in `"data"`.
```
...
    "triggers": ["hi", "hello", "hey"],
    "type": "text",
    "data": "server says hello back",
...
```

### animation
Sends back an animation where `"data"` value is the url of the animation. 
Converts all to gifs.
```
...
    "triggers": ["puppy"],
    "type": "animation",
    "data": "https://media.giphy.com/media/5awVf7q1nwkus/giphy.gif",
...
```

### save
Saves the value in `"data"` into `"save_to_data_name"` name space. To output this value, the `"data"` format is `"${data_name}"`.
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
    "follow_up_action_id": 2
},
{
    "id": 2,
    "triggers": [],
    "type": "save",
    "data": "${last_text_received}",
    "save_to_data_name": "name",
    "next_action_id": 3
},
{
    "id": 3,
    "triggers": [],
    "type": "text",
    "data": "your name is ${name}",
},
```

### calculate
Calculates the expression in `"data"` using math and saving it into `"calculate_result"`.
```
...
{
    "id": 1
    "triggers": ["calculate expression"],
    "type": "calculate",
    "data": "5^5",
    "next_action_id": 2
},
{
    "id": 2,
    "triggers": [],
    "type": "text",
    "data": "5^5 = ${calculate_result}"
}
...
```

### random
`"data"` is a list of possible values separated by `','`, randomly will chose one of them and save into `"${random_result}"`
```
{
  "id": 1,
  "triggers": [
    "random"
  ],
  "type": "random",
  "data": "1,2,3",
  "next_action_id": 2
},
{
  "id": 2,
  "triggers": [],
  "type": "text",
  "data": "${random_result}"
}
```

### redirect
`"data"` refers to the redirected action id, will works similarly to `"next_action_id"` but it is changeable by data saved. 
```
{
  "id": 1,
  "triggers": ["redirect to some_action_id"],
  "type": "redirect",
  "data": "${some_action_id}"
}
```
You can use it like the example below but it can be easily be the action it redirects to:
```
{
  "id": 2,
  "triggers": ["redirect to 3"],
  "type": "redirect",
  "data": "3"
},
{
  "id": 3,
  "triggers": [],
  "type": "text",
  "data": "Hello"
}
```
```
{
  "id": 3,
  "triggers": ["redirect to 3"],
  "type": "text",
  "data": "Hello"
}
```

### if
`"data"` is the evaluted text that checks for true or false, again it works with `${data}` strings.
`"true_action_id"` and `"false_action_id"` are the ids of the next actions if the result is true or false.
```
{
  "id": 1,
  "triggers": ["check"],
  "type": "if",
  "data": "${some_action_id}"
}
```
You can use it like the example below:
```
...
{
  "id": 2,
  "triggers": ["random the next action"],
  "type": "random",
  "data": "1,2",
  "next_action_id": 3
},
{
  "id": 3,
  "triggers": [],
  "type": "if",
  "data": "${random_result}>1",
  "true_action_id": 4,
  "false_action_id": 5
}
...
```
Or use it as a result to a message, but you need to account that it is a string so surround it with quotes.
This example will always go to 4 because its always true unless some other action will redirect to it:
```
...
{
  "id": 3,
  "triggers": ["something"],
  "type": "if",
  "data": "'${last_text_received}'=='something'",
  "true_action_id": 4,
  "false_action_id": 5
}
...
```