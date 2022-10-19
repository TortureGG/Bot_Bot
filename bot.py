# from re import S
import discum
from   colorama import Fore, Back
import datetime
import json




class Bot(object):

    def __init__(self, token, email, password, proxy, captcha, user_agent): 

        self.token      = token
        self.email      = email
        self.password   = password
        #============================
        self.proxy      = proxy
        self.captcha    = captcha
        self.user_agent = user_agent
        #============================
        self.connected  = False
        self.valid      = False 
        self.name       = 'Name Unknown'
        self.phone      = 'Phone Unknown'
        self.id         = 'ID Unknown'
        self.guilds     = []
        #============================

        log = {"console":False, "file":False, "encoding":"utf-8"}
        self.client = discum.Client(token = self.token, proxy = self.proxy, log = log)  
        # self.client = discum.Client(token = self.token, log = log)  
        # self.client = discum.Client(email = self.email, password = self.password, log = log)  
        # self.client = discum.Client(token = self.token, email = self.email, password = self.password, log = log)  
        # self.client = discum.Client(log = log)  

        # self.client.switchProxy(self.proxy)
        self.getID()
        self.getToken()
        self.checkToken()

        # self.getGuilds()
        # self.login()

        if (self.valid == False): return

        # return
        self.client.gateway.command({"function":onInitialize, "params":{"bot": self}})  
        self.client.gateway.run(False) #auto_reconnect (bool) - auto reconnect (resume when possible) for all cases except bot.gateway.close() and ctrl-c. Defaults to True

    def login(self):
        resp = self.client.login(self.email, self.password)[0]
        # print(json.dumps(resp.json(), sort_keys=True, indent=4))

        if 'captcha_key' in resp.json():
            print(Back.YELLOW + f"LOGIN Invalid: Captcha-Required for {self.email}" + Back.BLACK)
            self.valid = False
            return

        self.token  = resp.json()["token"]
        self.id     = resp.json()["user_id"]
    
    def getToken(self):
        self.token = self.client._Client__user_token
        print(Back.BLUE + f"Get Token: {self.token}" + Back.BLACK)
    
    def checkToken(self): 
        self.valid = False
        resp = self.client.checkToken(token=self.token)
        if (resp[0] and resp[1]):
            self.valid = True
            print(Back.GREEN + "Valid token: " + self.token + Back.BLACK)
            return True
        
        print(Back.RED +  f"Invalid token: {self.token}" + Back.BLACK)  
        return False

    def getID(self):
        self.id  = self.client._Client__user_id
        print(Back.BLUE + f"Get ID: {self.id}" + Back.BLACK)

    def getGuilds(self): 
        resp = self.client.getGuilds()
        self.responseStatus(resp, False)
        for guild in resp.json():
            self.guilds.append(guild["id"])

    def sendDM(self, id, message):

        # message = message["content"].replace("<user>", f"<@{id}>")
        message = message.replace("<user>", f"<@{id}>")
        
        newDM = self.client.createDM([id]).json()["id"]
        resp = self.client.sendMessage(newDM, message=message)

        self.responseStatus(resp, False)
        return

    def readMessage(self, ChannelID , messageID):
        # resp = self.client.getMessages(aroundMessage = messageID)
        resp = self.client.getMessage(ChannelID,messageID)
        self.responseStatus(resp)
        print(json.dumps(resp.json(), sort_keys=True, indent=4))

    def changeAvatar(self, avatar):
        resp = self.client.setAvatar(avatar)
        self.responseStatus(resp, False)

    def changeName(self, name):
        resp = self.client.setUsername(name)
        self.responseStatus(resp, False)

    def joinGuild(self, link):
        # обрежем ссылку если присутсвует 
        cutBegin = link.find("https://discord.gg/")
        if(cutBegin != -1):
            link = link[cutBegin+19:]

        resp = self.client.joinGuild(link)
        self.responseStatus(resp, False)

    def leaveAllGuilds(self):
        self.getGuilds()
        for i in range(len(self.guilds)):
            resp = self.client.leaveGuild(self.guilds[i])
            self.responseStatus(resp, False)
        return
    
    def responseStatus(self, resp, printResponse):
        date = datetime.datetime.today()
        if 200 <= resp.status_code < 300: print(Back.GREEN + date.strftime('%H:%M:%S') +  f" SUCCESS {resp.status_code} by {self.email}" + Back.BLACK)
        else:                             print(Back.RED   + date.strftime('%H:%M:%S') +  f" ERROR {resp.status_code} by {self.email} response:{resp.json()}" + Back.BLACK)
        
        if (printResponse): print(json.dumps(resp.json(), sort_keys=True, indent=4))
        return resp.status_code

# @bot.gateway.command
def onInitialize(resp, bot):

    if resp.event.ready_supplemental:
        bot.client.gateway.log = {"console":False, "file":False}  # True False

        date = datetime.datetime.today()

        bot.connected = bot.client.gateway.connected

        if (bot.connected):     print(Back.GREEN + f"Gateway Connected: {bot.connected} by {bot.email}" + Back.BLACK)
        if (not bot.connected): print(Back.RED   + f"Gateway Connected: {bot.connected} by {bot.email}" + Back.BLACK)

        if (bot.connected):
            print(Back.BLUE + f"Proxy {bot.client.gateway.proxy_host}:{bot.client.gateway.proxy_port} type={bot.client.gateway.proxy_type} auth={bot.client.gateway.proxy_auth} session_id = {bot.client.gateway.session_id}" + Back.BLACK)

            bot.client.gateway.session.saveMemory()

            sessionRead = bot.client.gateway.session.read()

            # print(json.dumps(sessionRead,    sort_keys=True, indent=4))
            # print(json.dumps(sessionRead.get('friends'), sort_keys=True, indent=4))
            # print(json.dumps(sessionRead.get('guilds'),  sort_keys=True, indent=4))

            # bot.name    = bot.client.gateway.session.user['username']
            # bot.phone   = bot.client.gateway.session.user['phone']
            # bot.id      = bot.client.gateway.session.user['id']
            # bot.guilds  = bot.client.gateway.session.guildIDs

            print(bot.name)
            # print(bot.phone)
            # print(bot.guilds)


        bot.client.gateway.log = {"console":False, "file":False}
        bot.client.gateway.close() 


