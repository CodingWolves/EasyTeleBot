from flask import send_file

from EasyTeleBot.TelegramBot import EasyTelegramBot

file = open('json_file.json')
file2 = open('json_file2.json')
easy_bot = EasyTelegramBot([file, file2], telegram_token="123", webhook_url="hook_url", bot_name="new_bot", default_action_id=3)
app = easy_bot.flask_app


@app.route('/db')
def db():
    return send_file('../database/db.csv')


if __name__ == '__main__':
    print('main function started')
    app.run()
