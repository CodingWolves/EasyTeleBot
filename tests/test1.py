from flask import send_file

from EasyTeleBot.TelegramBot import EasyTelegramBot

file = open('json_file.json')
file2 = open('json_file2.json')
easy_bot = EasyTelegramBot([file, file2])
app = easy_bot.flask_app


@app.route('/db')
def db():
    return send_file('../database/db.csv')


if __name__ == '__main__':
    print('main function started')
    app.run()
