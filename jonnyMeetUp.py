import discord
import datetime
from discord.ext import commands
from discord import ui
from copy import deepcopy

# Global Variables
MEETUPS = dict()
MEETUPS_TEMP = dict()
CHANGES = []
EDITKEY = ""

# Create the bot
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
bot.remove_command("help")

'''
BOT EVENTS AND COMMANDS
'''
# Start up bot
@bot.event
async def on_ready():
    print("Bot is online")

# Main bot command
'''
Starting embed to help user
'''
@bot.command()
async def MeetUp(ctx):
    view = generate_view(False)
    embed = discord.Embed(title="Welcome to the MeetUp Bot!",
                          colour=discord.Colour.from_rgb(183, 133, 239),
                          description="Type \"help\" for a guide on how to use this bot, or type \"help <Button Name>\" for more information on a specific button.")
    await ctx.send(embed=embed,view=view)

# Custom help function
@bot.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title="HELP", 
                       colour= discord.Colour.from_rgb(183, 133, 239), 
                       description="Type \">MeetUp\" to get started! Use >help <command> to see what each button will do. The commands are listed below vvv")
    em.add_field(name="MeetUp", value="Brings up main menu for creating meetup. Type \">help MeetUp\" for a guide on how to use this bot",inline=False)
    em.add_field(name="Create", value="Input details to create a meetup", inline= False)
    em.add_field(name="Edit", value="Edit details of an existing meetup.", inline= False)
    em.add_field(name="History", value="View details of created meetups.", inline= False)
    em.add_field(name="Settings", value="Not implemented yet :D", inline= False)
    await ctx.send(embed = em)

@help.command()
async def MeetUp(ctx):
    em = discord.Embed(title="Step by step guide to making a meetup", 
                       colour=discord.Colour.brand_green(),
                       description="Type \">MeetUp\" when you are ready to get started!")
    em.add_field(name="Step 1:", value="Click the \"Create\" button to get started and make a meetup", inline=False)
    em.add_field(name="Step 2:", value="The square above the button menu will keep track of the last change you made!", inline=False)
    em.add_field(name="Step 3:", value="Using the existing message from the bot, click the \"Edit\" button if you wish to make any changes to your recently created meetup.", inline=False)
    em.add_field(name="Step 4:", value="Click the \"History\" button if you simply wish to view the details of an existing meetup.", inline=False)
    em.add_field(name="Step 5:", value="Create as many meetups as you wish! The bot will keep track of them all.", inline=False)
    await ctx.send(embed=em)

@help.command()
async def Create(ctx):
    em = discord.Embed(title="Create Popup Fields", 
    colour= discord.Colour.og_blurple(),
    description="Clicking this button will display a popup where you can input the details of a new meetup.")
    em.add_field(name="Title", value="This field is the title of the meetup", inline=False)
    em.add_field(name="Description", value="This field holds information about the meetup", inline=False)
    em.add_field(name="Start Date", value="Determines the start date and time of the meetup. Please use the YYYY-MM-DD hh24:mm:ss date time format", inline=False)
    em.add_field(name="End Date", value="Determines the end date and time of the meetup. Please use the YYYY-MM-DD hh24:mm:ss date time format", inline=False)
    em.add_field(name="Location", value="Determines location of the meetup", inline=False)

    await ctx.send(embed=em)

@help.command()
async def Edit(ctx):
    em = discord.Embed(title="Edit Menu buttons", colour= discord.Colour.green())
    em.add_field(name="Name", value="Change the title of the meetup.",inline=False)
    em.add_field(name="Dates", value="Change the date and time of the meetup.",inline=False)
    em.add_field(name="Description", value="Change the description of the meetup.",inline=False)
    em.add_field(name="Status", value="Change the status of the meetup.",inline=False)
    em.add_field(name="Payment", value="Change the debtor, and value amount that people will pay.",inline=False)
    em.add_field(name="Other", value="Add any other notes to the meetup.",inline=False)
    em.add_field(name="Delete Meetup", value="Deletes the existing meetup permanently",inline=False)
    em.add_field(name="Save and Exit", value="Saves all changes the user has made so far",inline=False)
    em.add_field(name="Back", value="Returns to the Edit Selection page without saving the changes",inline=False)
    await ctx.send(embed=em)

@help.command()
async def History(ctx):
    em = discord.Embed(title="History Select Menu",colour=discord.Colour.greyple())
    em.add_field(name="All Select Option", value="Select \"All\" to view all, or select the specific meetups you want to see.")
    em.add_field(name="Selecting multiple options", value="Select any option(s) to view the details of the selected meetup")
    await ctx.send(embed=em)

@help.command()
async def Settings(ctx):
    em = discord.Embed(title="History Select Menu",
        colour=discord.Colour.greyple(),
        description="Soz bro not available yet \U0001F605")
    await ctx.send(embed=em)

'''
MISCELLANEOUS COMMANDS
'''
# NOT IN USE
def convert_string_to_datetime(input):
    year = []
    time = []
    timeEdit = input.split()
    for numberYear in timeEdit[0].split('/'):
        year.append(int(numberYear))
    for numberTime in timeEdit[1].split(':'):
        time.append(int(numberTime))
    return [year[2],year[1],year[0],time[0],time[1],time[2]]

# Generates information embed that informs user that meetup has been created
def create_meetUp_embed(name) -> discord.Embed:
    """ Generates a meet up embed object based off the name/key. Returns an embed object """
    embed = discord.Embed(title = name, description = MEETUPS[name].get_description(),colour=discord.Colour.from_rgb(183, 133, 239))
    if MEETUPS[name].get_startdate() != None:
        datetimeInfo = MEETUPS[name].get_startdate()
        embed.add_field(name="Start date and time",value = datetimeInfo, inline=False)

    if MEETUPS[name].get_enddate() != None:
        datetimeInfo = MEETUPS[name].get_enddate()
        embed.add_field(name="End date and time",value = datetimeInfo, inline=False)
    
    if MEETUPS[name].get_location() != None:
        embed.add_field(name="Location",value = MEETUPS[name].get_location(), inline=False)
    
    if MEETUPS[name].get_status() != None:
        embed.add_field(name="Status",value = MEETUPS[name].get_status(), inline=False)

    if MEETUPS[name].get_payTo() != None:
        embed.add_field(name="Person to pay back",value = MEETUPS[name].get_payTo(), inline=False)
    
    if MEETUPS[name].get_payAmount() != None:
        embed.add_field(name="Amount per person to be paid back",value = str(MEETUPS[name].get_payAmount()), inline=False)
    
    if MEETUPS[name].get_payInfo() != None:
        embed.add_field(name="Pay information",value = MEETUPS[name].get_payInfo(), inline=False)
    
    if MEETUPS[name].get_other() != None:
        embed.add_field(name="Other information",value = MEETUPS[name].get_other(), inline=False)
    
    return embed

# Generates generic edit view class, takes True or False and generates different button view
def generate_view(edit:bool) -> ui.View: 
    """Use False to generate MeetUp menu, and True to generate edit meetup menu

    Args:
        edit (bool): Tells user whether menu is edit menu or main menu

    Returns:
        ui.View: generic view class
    """
    view = BotView()
    if edit == False:
        view.add_item(CreateButton())
        view.add_item(EditButton())
        view.add_item(HistoryButton())
        view.add_item(SettingsButton())

    if edit == True:
        view.add_item(NameEdit())
        view.add_item(DatesEdit())
        view.add_item(DescriptionEdit())
        view.add_item(StatusEdit())
        view.add_item(PaymentEdit())
        view.add_item(OtherEdit())
        view.add_item(DeleteEdit())
        view.add_item(SaveAndExit())
        view.add_item(BackToEditButton())
    
    return view

# Generates generic embed to document changes
def edit_changes_embed() -> discord.Embed:
    embed = discord.Embed(title=f"\"{EDITKEY}\" edit options",
                    colour=discord.Colour.from_rgb(183, 133, 239),
                    description="Changes will be documented below:")
    for i in range(len(CHANGES)):
        embed.add_field(name=f"{i+1}:",value=f"{CHANGES[i]}",inline=False)
    return embed    
   
'''
VIEW AND STORAGE CLASSES
'''
# Storage class
class MeetingUp:
    ''' MeetUp represents a meet up instance '''
    
    # Implicits
    def __init__(self, activity: str = None, startdate: datetime.datetime = None, enddate: datetime.datetime = None, description: str = None, location: str = None, status: str = None,payAmount: float = None,payTo: str = None, payInfo: str = None, other: str = None) -> None:
        
        # Sets activity value
        self.activity = activity    
        
        # create new date object for start date
        if startdate != None: 
            self.startdate = datetime.datetime.fromisoformat(startdate)
        else: self.startdate = startdate

        # create new date object for end date
        if enddate != None: 
            self.enddate = datetime.datetime.fromisoformat(enddate)
            
        else: self.enddate = enddate
        
        self.description = description
        self.location = location
        self.status = status


        self.payAmount = payAmount
        self.payTo = payTo
        self.payInfo = payInfo
        self.other = other
 
    def __str__(self) -> str:
        pass
    
    # Modifiers    
    def change_activity(self, activity: str):
        """Changes the desired activity of the meetup"""
        self.activity = activity
    
    def change_startdate(self, startdate: str):
        self.startdate = datetime.datetime.fromisoformat(startdate)

    def change_enddate(self, enddate: str):
        self.enddate = datetime.datetime.fromisoformat(enddate)

    def change_description(self, description: str):
        self.description = description 
    
    def change_location(self, location: str):
        self.location = location

    def change_status(self, status: str):
        self.status = status
    
    def change_payTo(self,payTo: str):
        self.payTo = payTo

    def change_payAmount(self,payAmount: float):
        self.payAmount = payAmount

    def change_payInfo(self,payInfo:str):
        self.payInfo = payInfo
    
    def change_other(self, other: str):
        self.other = other
    
    def get_activity(self): 
        return self.activity
    
    def get_startdate(self):
        if self.startdate != None:
            output = f'{self.startdate:%d %b %Y}'+ ' @ ' + f'{self.startdate:%H:%M:%S %p}'
        else:
            output = None
        return output

    def get_enddate(self):
        if self.enddate != None:
            output = f'{self.enddate:%d %b %Y}'+ ' @ '  + f'{self.enddate:%H:%M:%S %p}'
        else:
            output = None
        return output

    def get_description(self):
        return self.description
    
    def get_location(self):
        return self.location

    def get_status(self):
        return self.status 
    
    def get_payTo(self):
        return self.payTo

    def get_payAmount(self):
        if self.payAmount != None:
            return '$' + str(self.payAmount) 
        else:
            return None
    
    def get_payInfo(self):
        return self.payInfo

    def get_other(self):
        return self.other 

# General view class
class BotView(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = None

'''
MODAL CLASSES
'''
# Modal that runs when "Create" is clicked
class CreateModal(ui.Modal,title="Create Meet Up"):

    def __init__(self):
        super().__init__()
    name = ui.TextInput(label='Title',placeholder="Name of the meet up", required=True)
    description = ui.TextInput(label='Description', required = False, placeholder="Information about the meet up")
    startDate = ui.TextInput(label='Start date and time (YYYY-MM-DD hh24:mm:ss)',placeholder="yyyy-mm-dd hh24:mm:ss", required = False)
    endDate = ui.TextInput(label='End date and time (YYYY-MM-DD hh24:mm:ss)',placeholder="yyyy-mm-dd hh24:mm:ss", required = False)
    location = ui.TextInput(label='Location', required = False, placeholder="Where")
    
    async def on_submit(self,interaction: discord.Interaction):
        if self.description.value.split() == "":
            description = None
        else:
            description = self.description.value.strip()

        if self.startDate.value.strip() == "":
            startDate = None
        else:
            startDate = self.startDate.value.strip() 
            
        if self.endDate.value.strip() == "":
            endDate = None
        else:
            endDate = self.endDate.value.strip() 
            
        if self.location.value.strip() == "":
            location = None
        else:
            location = self.location.value.strip()
            

        MEETUPS[self.name.value] = MeetingUp(self.name.value, description = description, startdate = startDate, enddate = endDate, location = location, status = "Idea")
        view = generate_view(False)
        await interaction.response.edit_message(content=f"Meet up \"{self.name.value}\" has been created!", embed=create_meetUp_embed(self.name.value),view=view)

# Modal that is displayed to edit the name of the meetup 
class NameEditModal(ui.Modal, title=""):
    global EDITKEY
    global EDITKEY_TEMP
    name = ui.TextInput(label='New name', required=True)
    def __init__(self):
        super().__init__()
        self.title = "Change the name for " + EDITKEY
        self.name.placeholder = EDITKEY

    async def on_submit(self,interaction:discord.Interaction):
        MEETUPS_TEMP[EDITKEY].change_activity(self.name.value)
        MEETUPS_TEMP[self.name.value] = MEETUPS_TEMP.pop(EDITKEY)
        CHANGES.append(f"Name: {EDITKEY} --> {self.name.value}\n")

        view = generate_view(True)
        embed = edit_changes_embed()
        
            
        await interaction.response.edit_message(embed=embed,view=view)
        "await interaction.response.defer()"

# Modal displayed to edit start/end date of meetup
class DatesEditModal(ui.Modal, title=""):
    global EDITKEY
    startDate = ui.TextInput(label='Start date and time (YYYY-MM-DD hh24:mm:ss)', required=False)
    endDate = ui.TextInput(label='End date and time (YYYY-MM-DD hh24:mm:ss)', required=False)
    def __init__(self):
        super().__init__()
        self.title = "Change " + EDITKEY + " Dates"
        if MEETUPS[EDITKEY].get_startdate() == None:
            self.startDate.placeholder = "YYYY-MM-DD hh24:mm:ss"
        else:
            self.startDate.placeholder = MEETUPS[EDITKEY].get_startdate()
            
        if MEETUPS[EDITKEY].get_enddate() == None:    
            self.endDate.placeholder = "YYYY-MM-DD hh24:mm:ss"
        else:
            self.endDate.placeholder = MEETUPS[EDITKEY].get_enddate()
            
                
    async def on_submit(self,interaction:discord.Interaction):
        # Generate view class and retrieve previous date values
        oldStartdate = MEETUPS[EDITKEY].get_startdate()
        oldEnddate = MEETUPS[EDITKEY].get_enddate()
        view = generate_view(True)
        
        # If both fields blank, then no changes to be made
        if self.startDate.value == '' and self.endDate.value == '':
            await interaction.response.send_message(content="No changes made!")
            await interaction.response.defer()
            
        # Change start date if input in field is valid    
        if self.startDate.value != '' and self.endDate.value == '':
            MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_startdate(self.startDate.value)
            CHANGES.append(f"Start date: {oldStartdate} --> {self.startDate.value}\n")
            embed = edit_changes_embed()
            
        # Change end date if input in field is valid            
        elif self.startDate.value == '' and self.endDate.value != '':
            MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_enddate(self.endDate.value)
            CHANGES.append(f"End date: {oldEnddate} --> {self.endDate.value}\n")
            embed = edit_changes_embed()

        # Change both        
        else:
            MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_startdate(self.startDate.value)
            MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_enddate(self.endDate.value)
            CHANGES.append(f"Start date: {oldStartdate} --> {self.startDate.value}\n")
            CHANGES.append(f"End date: {oldEnddate} --> {self.endDate.value}\n")            
            embed = edit_changes_embed()
            
        await interaction.response.edit_message(embed=embed,view=view)
        "await interaction.response.defer()"

# Modal displayed to edit the description
class DescriptionEditModal(ui.Modal, title=""):
    global EDITKEY
    description = ui.TextInput(label='New description', required=True, style = discord.TextStyle.paragraph)
    def __init__(self):
        super().__init__()
        self.title = EDITKEY + " Description"
        if MEETUPS[EDITKEY].get_description() == None:
            self.description.placeholder = "No description yet!"
        else:
            self.description.placeholder = MEETUPS[EDITKEY].get_description()
    
    async def on_submit(self,interaction: discord.Interaction):
        old = MEETUPS[EDITKEY].get_description()
        MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_description(self.description.value)
        CHANGES.append(f"Description: {old} --> {self.description.value}\n")
        
        # regenerate embed and edit menu view
        view = generate_view(True)
        embed = edit_changes_embed()
        
        await interaction.response.edit_message(embed=embed, view=view)
        
# Modal to input payment tracking   
class PaymentEditModal(ui.Modal, title=""):
    global EDITKEY
    debtor = ui.TextInput(label='Debtor', required=True)
    paymentAmount = ui.TextInput(label='Payment Amount', required=False)
    payInfo = ui.TextInput(label='Payment Information', required=False)
    def __init__(self):
        super().__init__()
        self.title = EDITKEY + " Payment"
        if MEETUPS[EDITKEY].get_payTo() == None:
            self.debtor.placeholder = "Name of person to receive payment"
        else:
            self.debtor.placeholder = MEETUPS[EDITKEY].get_payTo()
            
        if MEETUPS[EDITKEY].get_payAmount() == None:
            self.paymentAmount.placeholder = "Payment in AUD (no need for $)"
        else:    
            self.paymentAmount.placeholder = MEETUPS[EDITKEY].get_payAmount()
            
        if MEETUPS[EDITKEY].get_payInfo() == None:
            self.payInfo.placeholder = "Additional details regarding payment"
        else:
            self.payInfo.placeholder = MEETUPS[EDITKEY].get_payInfo()
    
    async def on_submit(self,interaction: discord.Interaction):
        oldDebtor = MEETUPS[EDITKEY].get_payTo()
        oldPayAmount = MEETUPS[EDITKEY].get_payAmount()
        oldPayInfo = MEETUPS[EDITKEY].get_payInfo()
        MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_payTo(self.debtor.value)
        try:
            MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_payAmount(float(self.paymentAmount.value.strip()))
        except:
            pass
        MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_payInfo(self.payInfo.value)
        
        CHANGES.append(f"Debtor: {oldDebtor} --> {self.debtor.value}\n")
        
        if self.paymentAmount.value.strip() != "":
            CHANGES.append(f"Amount each: {oldPayAmount} --> {self.paymentAmount.value}\n")
        else:
            MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_payAmount(None)

        if self.payInfo.value.strip() != "":
            CHANGES.append(f"Payment info: {oldPayInfo} --> {self.payInfo.value}\n")
        else:
            MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_payInfo(None)
            
        view = generate_view(True)
        embed =  edit_changes_embed()
        
        await interaction.response.edit_message(embed=embed,view=view)
        "await interaction.response.defer()"

# Modal to edit other meetup details
class OtherEditModal(ui.Modal, title=""):
    global EDITKEY
    other = ui.TextInput(label='Other information', required=True)
    def __init__(self):
        super().__init__()
        self.title = "Other information for " + EDITKEY
        
        if MEETUPS[EDITKEY].get_other() == None:
            self.other.placeholder = "Additional details about the meetup"
        else:
            self.other.placeholder = MEETUPS[EDITKEY].get_other()
    
    async def on_submit(self,interaction: discord.Interaction):
        old = MEETUPS[EDITKEY].get_other()
        MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_other(self.other.value)
        CHANGES.append(f'Other: {old} --> {self.other.value}')
        view = generate_view(True)
        embed = edit_changes_embed()
        await interaction.response.edit_message(embed=embed, view=view)
          


'''
SELECT MENU CLASSES
'''
# Shows which 
class HistoryMeetUpSelect(ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="All")]
        super().__init__(min_values = 1, max_values = len(MEETUPS)+1,options = options)

        if len(MEETUPS) != 0:
            for key in MEETUPS.keys():
                self.append_option(discord.SelectOption(label = key))
    
    async def callback(self,interaction):
      
        # make sure to re-edit this message back
        if self.values[0] == "All":
            i = 0
            try:
                await interaction.response.send_message("All history:")
                for name in MEETUPS.keys():
                    #await interaction.guild.get_channel(interaction.channel_id).send(embed=create_meetUp_embed(name))
                    #await interaction.response.defer()  
                    channel = bot.get_channel(interaction.channel_id)
                    await channel.send(embed=create_meetUp_embed(name))
                    #if i == 0:
                    #    await interaction.response.send_message(embed=create_meetUp_embed(name))
                    #else:
                    #    await interaction.followup.send(embed=create_meetUp_embed(name))
                    #i+=1
            except discord.errors.InteractionResponded:
                pass
            except Exception as e:
                print(e)
                
        else:
            try:
                await interaction.response.send_message("Selected history:")
                for name in self.values:  
                    channel = bot.get_channel(interaction.channel_id)
                    await channel.send(embed=create_meetUp_embed(name))
            except discord.errors.InteractionResponded:
                pass
            except Exception as e:
                print(e)

# Select menu to choose which meetup to edit
class editMeetUpSelect(ui.Select):
    def __init__(self):
        options = []
        for key in MEETUPS.keys():
            options.append(discord.SelectOption(label = key))
        super().__init__(min_values = 1, max_values = 1,options = options)
        
    
    async def callback(self,interaction):
        global EDITKEY
        global CHANGES
        key = self.values[0]
        EDITKEY = key
        MEETUPS_TEMP[EDITKEY] = deepcopy(MEETUPS[EDITKEY])
        CHANGES = []
        view = generate_view(True)
        
        # Creating embed
        embed = edit_changes_embed()
        
        await interaction.response.edit_message(content="", embed=embed, view=view)

# Menu to edit status
class StatusEditMenu(ui.Select):
    global EDITKEY
    def __init__(self):
        options = [discord.SelectOption(label="Idea"),
                discord.SelectOption(label="Planning"),
                discord.SelectOption(label="Planned"),
                discord.SelectOption(label="Occurring"),
                discord.SelectOption(label="Finished"),
                discord.SelectOption(label="Awaiting Payment")]
        
        super().__init__(max_values=1,options=options)
        self.placeholder = MEETUPS[EDITKEY].get_status()
     
    async def callback(self,interaction:discord.Interaction):
        old = MEETUPS[EDITKEY].get_status()
        MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]].change_status(self.values[0])
        CHANGES.append(f'Status: {old} --> {self.values[0]}\n')
        
        # Get back edit menu
        view = generate_view(True)
        
        # Edit embed
        embed=edit_changes_embed()
        
        await interaction.response.edit_message(content="", embed=embed, view=view)
        



'''
BUTTON CLASSES
'''
# Button to pull up creation modal
class CreateButton(ui.Button):
    def __init__(self,label="Create", style=discord.ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style

    async def callback(self,interaction):
        await interaction.response.send_modal(CreateModal())

# Button to bring user to edit selection page
class EditButton(ui.Button):
    def __init__(self,label="Edit", style=discord.ButtonStyle.success):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self, interaction):
        view = BotView()
        if len(MEETUPS) == 0:                
            view.add_item(BackToMenuButton())
            embed = discord.Embed(title="No meetups available.",colour=discord.Colour.green())
            await interaction.response.edit_message(content="",embed=embed,view=view)
        else:
            view.add_item(editMeetUpSelect())
            view.add_item(BackToMenuButton())
            embed = discord.Embed(title = "Select meet up to be edited",colour=discord.Colour.green())
            for index, key in enumerate(MEETUPS):
                embed.add_field(name=f"{index+1}:",value=f"{key}",inline=False)
            await interaction.response.edit_message(content="",embed=embed,view=view)

# Button to bring user to history page
class HistoryButton(ui.Button):
    def __init__(self,label="History", style=discord.ButtonStyle.secondary):
        super().__init__()
        self.label = label
        self.style = style
    
    async def callback(self,interaction):
        view = BotView()
        if len(MEETUPS) == 0:
            view.add_item(BackToMenuButton())
            embed = discord.Embed(title="No meetups currently created",colour=discord.Colour.light_grey())
            await interaction.response.edit_message(content="",embed=embed,view=view)
        else:
            view.add_item(HistoryMeetUpSelect())
            view.add_item(BackToMenuButton())
            embed = discord.Embed(title = "Meet up history. Select option(s) to view their details",colour=discord.Colour.light_grey())
            for index, key in enumerate(MEETUPS):
                embed.add_field(name=f"{index+1}:",value=f"{key}",inline=False)

            await interaction.response.edit_message(content="",embed=embed,view=view)

# Button to bring user to settings page
'''
use embed for instructions/information
'''
class SettingsButton(ui.Button):
    def __init__(self,label="Settings", style=discord.ButtonStyle.danger):
        super().__init__()
        self.label = label
        self.style = style
    
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Nothing to see here :D",colour=discord.Colour.red())
        view = BotView()
        view.add_item(BackToMenuButton())
        await interaction.response.edit_message(content="",embed=embed,view=view)

# Brings up modal to edit Meetup name
class NameEdit(ui.Button):
    def __init__(self,label="Name", style=discord.ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        await interaction.response.send_modal(NameEditModal())

# Brings up modal to edit date
class DatesEdit(ui.Button):
    def __init__(self,label="Dates" , style=discord.ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        
        await interaction.response.send_modal(DatesEditModal())   

class DescriptionEdit(ui.Button):
    def __init__(self,label="Description" , style=discord.ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        await interaction.response.send_modal(DescriptionEditModal())

class StatusEdit(ui.Button):
    def __init__(self,label="Status" , style=discord.ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        view = BotView()
        view.add_item(StatusEditMenu())
        view.add_item(BackToEditMenu())
        await interaction.response.edit_message(content="Please edit the status!", view=view)

class PaymentEdit(ui.Button):
    def __init__(self,label="Payment" , style=discord.ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        await interaction.response.send_modal(PaymentEditModal())
     
class OtherEdit(ui.Button):
    def __init__(self,label="Other" , style=discord.ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        await interaction.response.send_modal(OtherEditModal())

# Brings up first prompt to delete meetup
class DeleteEdit(ui.Button):
    def __init__(self, label = "Delete Meet Up", style=discord.ButtonStyle.danger):
        super().__init__()
        self.label = label
        self.style = style
    
    async def callback(self,interaction: discord.Interaction):
        view = BotView()
        view.add_item(DeleteMeetupPermanently())
        view.add_item(BackToEditMenu())
        embed = discord.Embed(title=f"Are you sure you want do delete meetup \"{EDITKEY}\"?", 
                              colour=discord.Colour.from_rgb(183, 133, 239))
        
        await interaction.response.edit_message(content="",embed=embed,view=view)

# Button to actually delete meetup
class DeleteMeetupPermanently(ui.Button):
    def __init__(self, style: discord.ButtonStyle = discord.ButtonStyle.danger, label: str = "Delete"):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: discord.Interaction):
        del MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]]
        CHANGES.clear
        MEETUPS.pop(EDITKEY)
        
        embed = discord.Embed(title=f"Meet up \"{EDITKEY}\" has been deleted", colour=discord.Colour.from_rgb(183, 133, 239))

        view = generate_view(False)
        print(MEETUPS)
        await interaction.response.edit_message(content="",embed=embed,view=view)

# Button to go back to edit page
class BackToEditMenu(ui.Button):
    def __init__(self, label = "Cancel", style=discord.ButtonStyle.secondary) -> None:
        super().__init__(label=label,style=style)
        
    async def callback(self, interaction: discord.Interaction):
        view = generate_view(True)
        embed = edit_changes_embed()
        await interaction.response.edit_message(embed = embed, view=view)
        
# Button to confirm changes made in editing session
class SaveAndExit(ui.Button):
    def __init__(self,label="Save and Exit" , style=discord.ButtonStyle.success):
        super().__init__()
        self.label = label
        self.style = style
    
    async def callback(self,interaction):
        view = BotView()
        view.add_item(ConfirmEditChanges())
        view.add_item(BackToEditMenu())
        
        if len(CHANGES) == 0:
            embed = discord.Embed(title=f"\"{EDITKEY}\"", 
                                    description="No changes made to this meetup,",
                                    colour=discord.Colour.from_rgb(183, 133, 239))
        else:
            embed: discord.Embed = edit_changes_embed()
            embed.description = f"Are you sure you wish to make the following changes to meetup \"{EDITKEY}\"?"
            embed.title = "Changes made during this edit session:"
        
        await interaction.response.edit_message(embed=embed, view=view)

# Confirms changes made during edit session  
class ConfirmEditChanges(ui.Button):
    def __init__(self, style: discord.ButtonStyle = discord.ButtonStyle.success, label: str = "Confirm Changes"):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: discord.Interaction):
        embed = edit_changes_embed()
        if len(CHANGES) == 0:
            embed.title = f"\"{EDITKEY}\""
            embed.description = "No changes made!"
        
        else:
            MEETUPS[list(MEETUPS_TEMP.keys())[0]] = MEETUPS_TEMP[list(MEETUPS_TEMP.keys())[0]]
            if list(MEETUPS_TEMP.keys())[0] != EDITKEY:
                MEETUPS.pop(EDITKEY)

            MEETUPS_TEMP.clear()
            embed.title = f"All changes to \"{EDITKEY}\" made successfully!"
            embed.description = "Changes are as follows below:"
    

        
        MEETUPS_TEMP.clear()
        view = generate_view(False)
        await interaction.response.edit_message(content="",embed=embed,view=view)

# Button that takes you back to menu from edit selection page
class BackToMenuButton(ui.Button):
    def __init__(self,label="Back", style=discord.ButtonStyle.danger):
        super().__init__()
        self.label = label
        self.style = style
    
    async def callback(self,interaction):
        view = BotView()
        embed = discord.Embed(title="Welcome to the MeetUp Bot!",
                          colour=discord.Colour.from_rgb(183, 133, 239),
                          description="Type \"help\" for a guide on how to use this bot, or type \"help <Button Name>\" for more information on a specific button.")

        create = CreateButton()
        edit = EditButton()
        history = HistoryButton()
        settings = SettingsButton()

        view.add_item(create)
        view.add_item(edit)
        view.add_item(history)
        view.add_item(settings)
        MEETUPS_TEMP.clear()
        await interaction.response.edit_message(content = "",embed=embed,view=view)

# Button that takes you back to edit selection page from edit menu
'''
add more user information and a confirmation button (If people complain)
'''
class BackToEditButton(ui.Button):
    def __init__(self,label="Back", style=discord.ButtonStyle.secondary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self, interaction):
        view = BotView()
        MEETUPS_TEMP.clear()
        if len(MEETUPS) == 0:                
            view.add_item(BackToMenuButton())
            await interaction.response.edit_message(content="No meetups available.",view=view)
        else:
            view.add_item(editMeetUpSelect())
            view.add_item(BackToMenuButton())
            await interaction.response.edit_message(content="Select meet up to be edited",view=view)


# Bot run token
bot.run('MTA2NjYzNjc1NTUwOTQ1NjkxNg.GxxTMI.8NlNNpIedAedropo8C8CndG3JXhRyh6O4CAC1o')