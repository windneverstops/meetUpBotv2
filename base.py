""" Base file for global variables and all imports/dependencies """
from datetime import datetime
from discord import ui,Embed,Intents
import mysql.connector as connector
from discord.ext import commands
import os
from dotenv import load_dotenv
import config

#Creating bot
#Dictionary for storing meet ups

config.MEETUPS = dict()
config.MEETUPS_TEMP = dict()
config.EDITKEY = ""
config.bot = commands.Bot(command_prefix=">", intents=Intents.all())
config.bot.remove_command("help")

load_dotenv(dotenv_path="config.env")
bot_token = os.getenv("DISCORD_BOT_TOKEN")
db_username = os.getenv("USERNAME")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")

configDict = {
    'user':db_username,
    'password':db_password,
    'database':'meetup',
    'host':db_host,
    'ssl_ca':'DigiCertGlobalRootCA.crt (2).pem',
    'autocommit':True
}

allowed_guilds = os.getenv("ALLOWED_GUILDS").split(',')
config.allowed_guilds  = [guild.strip() for guild in allowed_guilds]

""" config.cnx = dict()
for guild in config.allowed_guilds:
    config.cnx[guild] = connector.connect(**configDict) """

config.cnx = connector.connect(**configDict)
config.cursor = config.cnx.cursor(dictionary=True)

