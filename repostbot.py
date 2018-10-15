import telegram,logging,hashlib,random
from telegram.ext import Updater, CommandHandler, Dispatcher, MessageHandler, Filters
TOKEN = "TokenGoesHere"
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
picfile = "pichashes.txt"
insultsfile = "insults.txt"
insults = []
with open(insultsfile, 'r') as f:
    for line in f:
        line = line.strip()
        insults.append(line)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="It works")

def repostcheck(bot,update):
    #print(update.message)
    file_id = update.message.photo[-1].file_id
    newFile = bot.get_file(file_id)
    newFile.download('image.jpg')
    photohash = getHash('image.jpg')
    checkForMatch(photohash,update)

def checkForMatch(newhash,update):
    chatId = update.message.chat_id
    hashfilename = str(chatId)[1:] + picfile
    open(hashfilename, "a+")
    if open(hashfilename, 'r').read().find(newhash) != -1:
        print("This string was found")
        ##TODO More insults
        update.message.reply_text(random.choice(insults))
    else:
        print("wow new maymay")
        with open(hashfilename, 'a+') as file:
            file.write(newhash + '\n')

def getHash(picture):
    h = hashlib.sha256()
    with open(picture, 'rb', buffering=0) as pic:
        for b in iter(lambda : pic.read(128*1024), b''):
            h.update(b)
    print("hashed")
    return h.hexdigest()

print(bot.get_me())

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

newImageHandler = MessageHandler(Filters.photo, repostcheck)
dispatcher.add_handler(newImageHandler)
updater.start_polling()
