from EasyTeleBot import TelegramBot
from flask import send_file

file = open('json_file.json')
file2 = open('json_file2.json')
easy_bot = TelegramBot.CreateEasyTelegramBot([file, file2])
app = easy_bot.flask_app


@app.route('/db')
def db():
    return send_file('../database/db.csv')


if __name__ == '__main__':
    print('main function started')
    app.run()
