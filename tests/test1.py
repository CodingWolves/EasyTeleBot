from EasyBot.EasyRun import EasyBot

file = open('json_file.json')
app = EasyBot(file)

if __name__ == '__main__':
    print('main function started')
    bot.app.run(threaded=True)
