""" Base file for global variables and all imports/dependencies """
from datetime import datetime
from discord import ui,Embed,Intents
import mysql.connector as connector
from discord.ext import commands
import os
from dotenv import load_dotenv

#Creating bot
#Dictionary for storing meet ups

MEETUPS = dict()
MEETUPS_TEMP = dict()
EDITKEY = ""
bot = commands.Bot(command_prefix=">", intents=Intents.all())
bot.remove_command("help")

load_dotenv(dotenv_path="config.env")
bot_token = os.getenv("DISCORD_BOT_TOKEN")
db_username = os.getenv("USERNAME")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")
config = {
    'user':db_username,
    'password':db_password,
    'database':'meetup',
    'host':db_host,
    'ssl_ca':'DigiCertGlobalRootCA.crt (2).pem'
}
cnx = connector.connect(**config)
cursor = cnx.cursor(dictionary=True)

class MeetUp:
    ''' MeetUp represents a meet up instance '''
    
    # Implicits
    def __init__(self, name: str = None, startdate: datetime = None, enddate: datetime = None, \
                description: str = None, location: int = None, status: str = None,payAmount: float = \
                None,payTo: str = None, payInfo: str = None, other: str = None, guildId: str = None) -> None:
        
        # Sets name value
        self.name = name
        self.startdate = startdate
        self.enddate = enddate  
        self.description = description
        self.location = location
        self.status = status
        self.payAmount = payAmount
        self.payTo = payTo
        self.payInfo = payInfo
        self.other = other
        self.guildId = guildId
        self.confirmed_going = None
 
    def __str__(self) -> str:
        pass
    
    # Modifiers    
    def set_name(self, name: str):
        """Changes the desired name of the meetup"""
        
        self.name = name
    
    def set_startdate(self, startdate: datetime = None):
        self.startdate = startdate

    def set_enddate(self, enddate: datetime = None):
        self.enddate = enddate

    def set_description(self, description: str  = None):
        self.description = description 
    
    def set_location(self, location: str  = None):
        self.location = location

    def set_status(self, status: str = None):
        self.status = status
    
    def set_payTo(self,payTo: str = None):
        self.payTo = payTo

    def set_payAmount(self,payAmount: float = None):
        self.payAmount = payAmount

    def set_payInfo(self,payInfo:str = None):
        self.payInfo = payInfo
    
    def set_other(self, other: str = None):
        self.other = other
    
    def get_name(self) -> str: 
        return self.name
    
    def get_startdate(self) -> datetime:
        if self.startdate != None:
            output = f'{self.startdate:%d %b %Y}'+ ' @ ' + f'{self.startdate:%H:%M:%S %p}'
        else:
            output = None
        return output

    def get_enddate(self) -> datetime:
        if self.enddate != None:
            output = f'{self.enddate:%d %b %Y}'+ ' @ '  + f'{self.enddate:%H:%M:%S %p}'
        else:
            output = None
        return output

    def get_description(self) -> str:
        return self.description
    
    def get_location(self) -> str:
        return self.location

    def get_status(self) -> str:
        return self.status 
    
    def get_payTo(self) -> str:
        return self.payTo

    def get_payAmount(self) -> float:
        return self.payAmount
    
    def get_payInfo(self) -> str:
        return self.payInfo

    def get_other(self) -> str:
        return self.other 

    def get_guild_id(self) -> str:
        return self.guildId
        
