import base
import Functions
import components
import BotClasses
import config
from time import sleep

try:
    @config.bot.command()
    async def MeetUp(ctx):
        await ctx.send(view=components.homeView())

    @config.bot.event
    async def on_ready():
        BotClasses.MEETUP.retrieveFromDB()

except KeyboardInterrupt:
    config.cnx.close()
    config.cursor.close()
except:
    config.cnx.close()
    config.cursor.close()
        

config.bot.run(base.bot_token)