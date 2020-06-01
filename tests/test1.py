import EasyTeleBot
from flask import Flask, send_file

file = open('json_file.json')
easy_bot = EasyTeleBot.CreateEasyTelegramBot(file)
app = easy_bot.flask_app


@app.route('/db')
def db():
    return send_file('../database/db.csv')


if __name__ == '__main__':
    print('main function started')
    app.run()
