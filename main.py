import json
from bot import Bot


token = ""
email = ""
password = ""

ChannelID  = "" 
messageID  = ""

toId = ""
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36"

proxy = ""

with open("./message.json") as json_data:
        message = json.load(json_data)
json_data.close()


bot = Bot(token = token, email = email, password = password, proxy = proxy,  captcha = '', user_agent='') 
# bot.readMessage(ChannelID, messageID)
# bot.sendDM(toId, message["text"]+message["hider"]+message["embedLinks"])



