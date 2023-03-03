from discord import ui, ButtonStyle,SelectOption,errors
from Functions import *
import config

class View(ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

def homeView():
    view = View()
    
    create = CreateButton()
    edit = EditButton()
    history = HistoryButton()

    view.add_item(create)
    view.add_item(edit)
    view.add_item(history)
    return view

class CreateButton(ui.Button):
    def __init__(self,label="Create", style=ButtonStyle.primary):
        super().__init__()
        self.label = label
        self.style = style

    async def callback(self,interaction):
        await interaction.response.send_modal(CreateModal())

class CreateModal(ui.Modal,title="Create Meet Up"):

    def __init__(self):
        super().__init__()
    name = ui.TextInput(label='Title',placeholder="Name of the meet up", required=True)
    description = ui.TextInput(label='Description', required = False, placeholder="Information about the meet up")
    startDate = ui.TextInput(label='Start date and time',placeholder="dd/mm/yyyy hh24:mm:ss", required = False)
    endDate = ui.TextInput(label='End date and time',placeholder="dd/mm/yyyy hh24:mm:ss", required = False)
    location = ui.TextInput(label='Location', required = False, placeholder="Where")

    async def on_submit(self,interaction):
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

        config.cursor.execute("select guild_id from guild")
        
        guilds = []
        for dictionary in config.cursor.fetchall():
            guilds.append(int(dictionary['guild_id']))

        if interaction.guild_id not in guilds:
            
            # Adding guild data to database
            config.cursor.execute(f"INSERT INTO guild values ({interaction.guild_id},{interaction.user.id})")

        config.MEETUPS[self.name.value] = config.MeetUp(self.name.value,description = description,startdate = startDate,enddate = endDate,location = location,guildId=interaction.guild_id)
        
        if description == None:
            description = 'null'
        
        if startDate == None:
            startDate = 'null'
        else:
            startDate = f'STR_TO_DATE(\"{startDate}\",\"%d/%m/%Y %T\")'
    
        if endDate == None:
            endDate = 'null'
        else:
            endDate = f'STR_TO_DATE(\"{endDate}\",\"%d/%m/%Y %T\")'

        if location == None:
            location = 'null'
        

        config.cursor.execute(f"INSERT INTO meet_up \
            (guild_id,mu_creator_id,mu_name,mu_startdate,mu_enddate,\
                mu_description,mu_location) values ({interaction.guild_id},\
                    {interaction.user.id},'{self.name.value}',"\
                        + startDate + ","\
                            + endDate + ","\
                                f"'{python_to_sql_value(description)}','{python_to_sql_value(location)}')")       
        config.cnx.commit()

        await interaction.response.send_message(f"{self.name.value} meet up has been created!")
   


class EditButton(ui.Button):
    def __init__(self,label="Edit", style=ButtonStyle.success):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self, interaction):
        view = View()
        if len(config.MEETUPS) == 0:                
            view.add_item(BackButton)
            await interaction.response.edit_message(content="No meetups available.",view=view)
        else:
            view.add_item(EditMeetUpSelect())
            view.add_item(BackButton())
            await interaction.response.edit_message(content="Select meet up to be edited",view=view)
    
class EditMeetUpSelect(ui.Select):
        def __init__(self):
            options = []
            for key in config.MEETUPS.keys():
                options.append(SelectOption(label = key))
            super().__init__(min_values = 1, max_values = 1,options = options)

class BackButton(ui.Button):
    def __init__(self,label="Back", style=ButtonStyle.danger):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        config.MEETUPS_TEMP.clear()
        await interaction.response.edit_message(content = "",view=homeView())

class HistoryButton(ui.Button):
    def __init__(self,label="History", style=ButtonStyle.secondary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        view = View()
        if len(config.MEETUPS) == 0:
            view.add_item(BackButton())
            await interaction.response.edit_message(content="No history, as no meet ups created",view=view)
        else:
            view.add_item(HistoryMeetUpSelect())
            view.add_item(BackButton())
            await interaction.response.edit_message(content="Meet up history. Select option(s) to view their details",view=view)

class HistoryMeetUpSelect(ui.Select):
    def __init__(self):
        options = [SelectOption(label="All")]
        super().__init__(min_values = 1, max_values = len(config.MEETUPS)+1,options = options)

        if len(config.MEETUPS) != 0:
            for key in config.MEETUPS.keys():
                self.append_option(SelectOption(label = key))
    
    async def callback(self,interaction):
    
        if self.values[0] == "All":
     
            try:
                await interaction.response.send_message("All history:")
                for name in config.MEETUPS.keys():
                    #await interaction.guild.get_channel(interaction.channel_id).send(embed=create_meetUp_embed(name))
                    #await interaction.response.defer()  
                    channel = config.bot.get_channel(interaction.channel_id)
                    await channel.send(embed=create_meetUp_embed(name))
                    #if i == 0:
                    #    await interaction.response.send_message(embed=create_meetUp_embed(name))
                    #else:
                    #    await interaction.followup.send(embed=create_meetUp_embed(name))
                    #i+=1
            except errors.InteractionResponded:
                pass
            
                
        else:
            try:
                await interaction.response.send_message("Selected history:")
                for name in self.values:  
                    channel = config.bot.get_channel(interaction.channel_id)
                    print(name)
                    await channel.send(embed=create_meetUp_embed(name))
            except errors.InteractionResponded:
                pass
           

""" class settingsButton(ui.Button):
    def __init__(self,label="Settings", style=discord.ButtonStyle.danger):
        super().__init__()
        self.label = label
        self.style = style  """