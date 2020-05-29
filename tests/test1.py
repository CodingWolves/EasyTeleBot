import EasyTeleBot

file = open('json_file.json')
easy_bot = EasyTeleBot.CreateEasyTelegramBot(file)
app = easy_bot.flask_app

if __name__ == '__main__':
    print('main function started')
    app.run()
