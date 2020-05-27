from EasyBot.EasyRun import EasyBot

file = open('json_file.json')
bot = EasyBot(file)
bot.app.run()
