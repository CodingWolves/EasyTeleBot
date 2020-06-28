import os

from flask import send_file

from EasyTeleBot.TelegramBot import EasyTelegramBot

file = open('json_file.json')
file2 = open('json_file2.json')
easy_bot = EasyTelegramBot([file, file2], telegram_token=os.environ['TELEGRAM_TOKEN'])
app = easy_bot.flask_app


@app.route('/db')
def db():
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 3000)
    sock.connect(server_address)

    message = 'I am here'
    sock.sendall(message.encode('utf-8'))
    sock.close()

    return send_file('../database/db.csv')


if __name__ == '__main__':
    print('main function started')
    app.run()
