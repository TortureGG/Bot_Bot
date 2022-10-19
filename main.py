import json
from bot import Bot


token = "MzU2NDM2OTM0ODExMzIwMzIz.GM3_H3.BOyRYPqnVpd0bgksFNg39EInvV5b9xS9vt8OlQ"
email = "torturegg@gmail.com"
password = "M23mav46r9ik106"

ChannelID  = "1022142035345543238" 
messageID  = "1022142263595388989"

toId = "944274436364828722"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36"

proxy = ""
# proxy = "http://147.28.155.79:3128"
# proxy = "http://185.61.78.196:8088"
# proxy = "http:/:"

# proxy = "https://88.214.237.136:8181"
# proxy = "socks4://85.172.60.202:1181"

with open("./message.json") as json_data:
        message = json.load(json_data)
json_data.close()


bot = Bot(token = token, email = email, password = password, proxy = proxy,  captcha = '', user_agent='') 
# bot.readMessage(ChannelID, messageID)
# bot.sendDM(toId, message["text"]+message["hider"]+message["embedLinks"])



