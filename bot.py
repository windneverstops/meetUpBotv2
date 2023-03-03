import base
import Functions
import components
import BotClasses

@base.bot.command()
async def MeetUp(ctx):

    
    view = components.ui.View()
    
    create = components.returnCreateButton(base.cursor,base.MEETUPS,BotClasses.MeetUp,base.cnx)


    view.add_item(create)



    await ctx.send(view=view)



    
    

base.bot.run(base.bot_token)