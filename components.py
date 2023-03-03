from discord import ui, ButtonStyle,SelectOption,errors, TextStyle
from Functions import *
import config
from copy import deepcopy
import BotClasses

try:
    class View(ui.View):
            def __init__(self):
                super().__init__()
                self.value = None

    def homeView():
        view = View()
        
        create = CreateButton()
        edit = EditButton()
        history = HistoryButton()
        setting = SettingButton()

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
        

            if self.startDate.value.strip() == "":
                startDate = 'NULL'
            else:
                startDate = str_to_datetime(self.startDate.value.strip())
                startDateStr = self.startDate.value.strip()
                
            if self.endDate.value.strip() == "":
                endDate = 'NULL'
            else:
                endDate = str_to_datetime(self.endDate.value.strip())
                endDateStr = self.endDate.value.strip()

            description = self.description.value.strip()
            location = self.location.value.strip()

            config.cursor.execute("select guild_id from guild")
            issue = False
            
            guilds = []
            for dictionary in config.cursor.fetchall():
                guilds.append(int(dictionary['guild_id']))

            if interaction.guild_id not in guilds:
                
                # Adding guild data to database
                config.cursor.execute(f"INSERT INTO guild values ({interaction.guild_id},{interaction.user.id})")
            try: 
                config.MEETUPS[self.name.value] = config.MeetUp(self.name.value,description = description,startdate = startDate,enddate = endDate,location = location,guildId=interaction.guild_id)

                config.cursor.execute(f"INSERT INTO meet_up \
                    (guild_id,mu_creator_id,mu_name,mu_startdate,mu_enddate,\
                        mu_description,mu_location) values ({interaction.guild_id},\
                            {interaction.user.id},'{self.name.value}',"\
                                + f'STR_TO_DATE(\"{startDateStr}\",\"%d/%m/%Y %T\")' + ","\
                                    + f'STR_TO_DATE(\"{endDateStr}\",\"%d/%m/%Y %T\")' + ","\
                                        f"{python_to_sql_value(description)},{python_to_sql_value(location)})")     
                config.cnx.commit()
            except Exception as e:
                print(e)
                config.MEETUPS.pop(self.name.value)
                issue = True
            if issue == True:
                await interaction.response.send_message(f"Error! Please make sure the name is unique (case unsensitive)")
            else:
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
        async def callback(self,interaction):

            key = self.values[0]
            config.EDITKEY = key
            config.MEETUPS_TEMP[key] = deepcopy(config.MEETUPS[key])
            config.CHANGES.reset()

            view = View()
            view.add_item(NameEdit())
            view.add_item(DatesEdit())
            view.add_item(DescriptionEdit())
            view.add_item(StatusEdit())
            view.add_item(PaymentEdit())
            view.add_item(OtherEdit())
            view.add_item(DeleteEdit())
            view.add_item(confirmChanges())
            view.add_item(backToEditButton())
            
            await interaction.response.edit_message(content=f"{config.EDITKEY} edit options", view=view)

    class NameEdit(ui.Button):
            def __init__(self,label="Name", style=ButtonStyle.primary):
                super().__init__()
                self.label = label
                self.style = style
            async def callback(self,interaction):
                await interaction.response.send_modal(NameEditModal())

    class DatesEdit(ui.Button):
            def __init__(self,label="Dates" , style=ButtonStyle.primary):
                super().__init__()
                self.label = label
                self.style = style
            async def callback(self,interaction):
                await interaction.response.send_modal(DatesEditModal())   

    class DescriptionEdit(ui.Button):
        def __init__(self,label="Description" , style=ButtonStyle.primary):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self,interaction):
            await interaction.response.send_modal(DescriptionEditModal())

    class StatusEdit(ui.Button):
        def __init__(self,label="Status" , style=ButtonStyle.primary):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self,interaction):
            await interaction.response.send_modal(StatusEditModal())

    class PaymentEdit(ui.Button):
        def __init__(self,label="Payment" , style=ButtonStyle.primary):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self,interaction):
            await interaction.response.send_modal(PaymentEditModal())
        
    class OtherEdit(ui.Button):
        def __init__(self,label="Other" , style=ButtonStyle.primary):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self,interaction):
            await interaction.response.send_modal(OtherEditModal())

    class DeleteEdit(ui.Button):
        def __init__(self, label = "Delete Meet Up", style=ButtonStyle.danger):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self,interaction):
            config.CHANGES.delete = True
            config.CHANGES.deleteMessage = f'{config.EDITKEY}'
            await interaction.response.defer()

    class confirmChanges(ui.Button):
        def __init__(self,label="Save and Exit" , style=ButtonStyle.success):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self,interaction):
            output = ""
            if config.CHANGES.delete == True:
                config.MEETUPS.pop(config.EDITKEY)
                config.cursor.execute(f"delete from meet_up where mu_name = {config.EDITKEY}")
                output = f'{config.EDITKEY} has been deleted!'
            elif len(config.CHANGES.dbChange) != 0:
                config.MEETUPS[list(config.MEETUPS_TEMP.keys())[0]] = config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]]
                
                sqlOutput = "update meet_up set "
                for i,change in enumerate(config.CHANGES.dbChange):
                    if type(change['db_newval']) != str :
                        if type(change['db_newval']) == datetime:
                            sqlOutput += f"{change['db_key']} = STR_TO_DATE(\"{datetime_to_str_raw(change['db_newval'])}\",\"%d/%m/%Y %T\")"
                        else:
                            sqlOutput += f"{change['db_key']} = {change['db_newval']}"
                    else:
                        sqlOutput += f"{change['db_key']} = \'{change['db_newval']}\'"
                    if i != len(config.CHANGES.dbChange)-1:
                        sqlOutput += ','
                    else:
                        sqlOutput += f' where mu_name = \'{list(config.MEETUPS_TEMP.keys())[0]}\''

                    output += config.CHANGES.chatMessage[i]
                
            else:
                output = "No edits made"


            config.cursor.execute(sqlOutput)
            config.MEETUPS_TEMP.clear()

            viewConfirm = View()
            if len(config.MEETUPS) == 0:                
                viewConfirm.add_item(BackButton())
                await interaction.response.edit_message(content="No meetups available.",view=viewConfirm)
            else:
                viewConfirm.add_item(EditMeetUpSelect())
                viewConfirm.add_item(BackButton())
                await interaction.response.edit_message(content="Select meet up to be edited",view=viewConfirm)
            await interaction.response.defer()
            await interaction.guild.get_channel(interaction.channel_id).send(output)
            

    class backToEditButton(ui.Button):
        def __init__(self,label="Back", style=ButtonStyle.danger):
            super().__init__()
            self.label = label
            self.style = style
        async def callback(self, interaction):
            view = View()
            config.MEETUPS_TEMP.clear()
            if len(config.MEETUPS) == 0:                
                view.add_item(BackButton())
                await interaction.response.edit_message(content="No meetups available.",view=view)
            else:
                view.add_item(EditMeetUpSelect())
                view.add_item(BackButton())
                await interaction.response.edit_message(content="Select meet up to be edited",view=view)


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

    class NameEditModal(ui.Modal, title=""):
        name = ui.TextInput(label='New name', required=True)
        def __init__(self):
            super().__init__()
            self.title = "Change the name for " + config.EDITKEY
            self.name.placeholder = config.EDITKEY

        async def on_submit(self,interaction):
            config.MEETUPS_TEMP[config.EDITKEY].set_activity(self.name.value)
            config.MEETUPS_TEMP[self.name.value] = config.MEETUPS_TEMP.pop(config.EDITKEY)
            config.CHANGES.chatMessage.append(f"Name: {config.EDITKEY} --> {self.name.value}\n")
            config.CHANGES.dbChange.append({'db_key':'mu_name','db_newval':f'{self.name.value}'})
            await interaction.response.defer()

    class DatesEditModal(ui.Modal, title=""):
        startDate = ui.TextInput(label='Start date (dd/mm/yyyy hh24:mm:ss)', required=True)
        endDate = ui.TextInput(label='End date (dd/mm/yyyy hh24:mm:ss)', required=True)
        def __init__(self):
            super().__init__()
            self.title = "Change " + config.EDITKEY + " Dates"
            self.startDate.placeholder = config.MEETUPS[config.EDITKEY].get_startdate()
            self.endDate.placeholder = config.MEETUPS[config.EDITKEY].get_enddate()
        async def on_submit(self,interaction):
            oldStartdate = config.MEETUPS[config.EDITKEY].get_startdate()
            oldEnddate = config.MEETUPS[config.EDITKEY].get_enddate()
            config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_startdate(str_to_datetime(self.startDate.value))
            config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_enddate(str_to_datetime(self.endDate.value))
            config.CHANGES.chatMessage.append(f"Start date: {oldStartdate} --> {self.startDate.value}\n")
            config.CHANGES.dbChange.append({'db_key':'mu_startdate','db_newval':str_to_datetime(self.startDate.value)})
            config.CHANGES.chatMessage.append(f"End date: {oldEnddate} --> {self.endDate.value}\n")
            config.CHANGES.dbChange.append({'db_key':'mu_enddate','db_newval':str_to_datetime(self.endDate.value)})
            await interaction.response.defer()

    class DescriptionEditModal(ui.Modal, title=""):
        description = ui.TextInput(label='New description', required=True, style = TextStyle.paragraph)
        def __init__(self):
            super().__init__()
            self.title = config.EDITKEY + " Description"
            self.description.placeholder = config.MEETUPS[config.EDITKEY].get_description()
        async def on_submit(self,interaction):
            old = config.MEETUPS[config.EDITKEY].get_description()
            config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_description(self.description.value)
            config.CHANGES.chatMessage.append(f"Description: {old} --> {self.description.value}\n")
            config.CHANGES.dbChange.append({'db_key':'mu_description','db_newval':self.description.value})
            await interaction.response.defer()
        
    class StatusEditModal(ui.Modal, title=""):
        status = ui.TextInput(label='New status', required=True)
        def __init__(self):
            super().__init__()
            self.title = config.EDITKEY + " Status"
            self.status.placeholder = config.MEETUPS[config.EDITKEY].get_status()
        async def on_submit(self,interaction):
            old = config.MEETUPS[config.EDITKEY].get_status()
            config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_status(self.status.value)
            config.CHANGES.chatMessage.append(f'Status: {old} --> {self.status.value}\n')
            config.CHANGES.dbChange.append({'db_key':'mu_status','db_newval':self.status.value})
            await interaction.response.defer()

    class PaymentEditModal(ui.Modal, title=""):
        debtor = ui.TextInput(label='Debtor', required=True)
        paymentAmount = ui.TextInput(label='Payment Amount', required=False)
        payInfo = ui.TextInput(label='Payment Information', required=False)
        def __init__(self):
            super().__init__()
            self.title = config.EDITKEY + " Payment"
            self.debtor.placeholder = config.MEETUPS[config.EDITKEY].get_payTo()
            self.paymentAmount.placeholder = config.MEETUPS[config.EDITKEY].get_payAmount()
            self.payInfo.placeholder = config.MEETUPS[config.EDITKEY].get_payInfo()
        async def on_submit(self,interaction):
            oldDebtor = config.MEETUPS[config.EDITKEY].get_payTo()
            oldPayAmount = config.MEETUPS[config.EDITKEY].get_payAmount()
            oldPayInfo = config.MEETUPS[config.EDITKEY].get_payInfo()
            config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_payTo(self.debtor.value)
            try:
                config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_payAmount(float(self.paymentAmount.value.strip()))
            except:
                pass
            config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_payInfo(self.payInfo.value)
            config.CHANGES.chatMessage.append(f"Debtor: {oldDebtor} --> {self.debtor.value}\n")
            config.CHANGES.dbChange.append({'db_key':'mu_payto','db_newval':self.debtor.value})

            if self.paymentAmount.value.strip() != "":
                config.CHANGES.chatMessage.append(f"Amount each: {oldPayAmount} --> {self.paymentAmount.value}\n")
                config.CHANGES.dbChange.append({'db_key':'mu_payamount','db_newval':self.paymentAmount.value})
            else:
                config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_payAmount(None)

            if self.payInfo.value.strip() != "":
                config.CHANGES.chatMessage.append(f"Payment info: {oldPayInfo} --> {self.payInfo.value}\n")
                config.CHANGES.dbChange.append({'db_key':'mu_payinfo','db_newval':self.payInfo.value})
            else:
                config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_payInfo(None)
            await interaction.response.defer()

    class OtherEditModal(ui.Modal, title=""):
        other = ui.TextInput(label='Other information', required=True)
        def __init__(self):
            super().__init__()
            self.title = "Other information for " + config.EDITKEY
            self.other.placeholder = config.MEETUPS[config.EDITKEY].get_other()
        async def on_submit(self,interaction):
            old = config.MEETUPS[config.EDITKEY].get_other()
            config.MEETUPS_TEMP[list(config.MEETUPS_TEMP.keys())[0]].set_other(self.other.value)
            config.CHANGES.chatMessage.append(f'Other: {old} --> {self.other.value}')
            config.CHANGES.dbChange.append({'db_key':'mu_other','db_newval':self.other.value})
            await interaction.response.defer()

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
            
    class SettingButton(ui.Button):
        def __init__(self,label="Settings", style=ButtonStyle.danger):
            super().__init__()
            self.label = label
            self.style = style 
except KeyboardInterrupt:
    config.cnx.close()
    config.cursor.close()

    