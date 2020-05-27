from EasyBot.EasyRun import EasyBot

file = open('json_file.json')
easybot = EasyBot(file)
app = easybot.app

if __name__ == '__main__':
    print('main function started')
    easybot.app.run()
