from discord import ui, ButtonStyle


class View(ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

def returnCreateButton(cursor,MEETUPS,object,cnx):
    class createButton(ui.Button):
        def __init__(self,label="Create", style=ButtonStyle.primary):
            super().__init__()
            self.label = label
            self.style = style

        async def callback(self,interaction):
            await interaction.response.send_modal(returnCreateModal(cursor,MEETUPS,object,cnx))
    return createButton()

def returnCreateModal(cursor,MEETUPS,object,cnx):
    class createModal(ui.Modal,title="Create Meet Up"):

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

            cursor.execute("select guild_id from guild")
            
            guilds = []
            for dictionary in cursor.fetchall():
                guilds.append(int(dictionary['guild_id']))

            if interaction.guild_id not in guilds:
                
                # Adding guild data to database
                cursor.execute(f"INSERT INTO guild values ({interaction.guild_id},{interaction.user.id})")

            MEETUPS[self.name.value] = object(self.name.value,description = description,startdate = startDate,enddate = endDate,location = location,guildId=interaction.guild_id)
            
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
            

            cursor.execute(f"INSERT INTO meet_up \
                (guild_id,mu_creator_id,mu_name,mu_startdate,mu_enddate,\
                    mu_description,mu_location) values ({interaction.guild_id},\
                        {interaction.user.id},'{self.name.value}',"\
                            + startDate + ","\
                                + endDate + ","\
                                    f"'{description}','{location}')")       
            cnx.commit()

            await interaction.response.send_message(f"{self.name.value} meet up has been created!")
    return createModal()

""" def editButtonCreator(MEETUPS):
    class editButton(ui.Button):
        def __init__(self,label="Edit", style=ButtonStyle.success):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self, interaction):
            view = View()
            if len(MEETUPS) == 0:                
                view.add_item(backButton())
                await interaction.response.edit_message(content="No meetups available.",view=view)
            else:
                view.add_item(editMeetUpSelect())
                view.add_item(backButton())
                await interaction.response.edit_message(content="Select meet up to be edited",view=view)
    
    return editButton() """

""" class historyButton(ui.Button):
    def __init__(self,label="History", style=ButtonStyle.secondary):
        super().__init__()
        self.label = label
        self.style = style
    async def callback(self,interaction):
        view = View()
        if len(MEETUPS) == 0:
            view.add_item(backButton())
            await interaction.response.edit_message(content="No history, as no meet ups created",view=view)
        else:
            view.add_item(historyMeetUpSelect())
            view.add_item(backButton())
            await interaction.response.edit_message(content="Meet up history. Select option(s) to view their details",view=view)


class settingsButton(ui.Button):
    def __init__(self,label="Settings", style=discord.ButtonStyle.danger):
        super().__init__()
        self.label = label
        self.style = style """