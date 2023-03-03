import base
import Functions
import components
import BotClasses
import config

@config.bot.command()
async def MeetUp(ctx):

    await ctx.send(view=components.homeView())

@config.bot.event
async def on_ready():
    BotClasses.MEETUP.retrieveFromDB()
    

config.bot.run(base.bot_token)