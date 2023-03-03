from datetime import datetime
from discord import Embed
import config


def str_to_datetime(input:str) -> datetime:
    """ Converts string to datetime.
    Converts from a specific format: dd/mm/yyyy 24hr:mm:ss """
    year = []
    time = []
    timeEdit = input.split()
    for numberYear in timeEdit[0].split('/'):
        year.append(int(numberYear))
    for numberTime in timeEdit[1].split(':'):
        time.append(int(numberTime))       
    return datetime(year[2],year[1],year[0], time[0],time[1],time[2]) 

def datetime_to_str_rep(input:datetime) -> str:
    return f'{input:%d %b %Y}'+ ' @ ' + f'{input:%H:%M:%S %p}'

def datetime_to_str_raw(input:datetime) -> str:
    return f'{input:%d/%m/%Y}'+ ' ' + f'{input:%H:%M:%S}'

def python_to_sql_value(input) -> str:
    if input == None or input == '':
        return 'NULL'
    else:
        return f"\'{input}\'"

def money_to_str(input: float | int) -> str:
    return '$' + str(input)
    
def create_meetUp_embed(name) -> Embed:
    """ Generates a meet up embed object based off the name/key. Returns an embed object """
    embed = Embed(title = name, description = config.MEETUPS[name].get_description())
    if config.MEETUPS[name].get_startdate() != None:
        datetimeInfo = config.MEETUPS[name].get_startdate()
        embed.add_field(name="Start date and time",value = datetimeInfo)

    if config.MEETUPS[name].get_enddate() != None:
        datetimeInfo = config.MEETUPS[name].get_enddate()
        embed.add_field(name="End date and time",value = datetimeInfo)
    
    if config.MEETUPS[name].get_location() != None:
        embed.add_field(name="Location",value = config.MEETUPS[name].get_location())
    
    if config.MEETUPS[name].get_status() != None:
        embed.add_field(name="Status",value = config.MEETUPS[name].get_status())

    if config.MEETUPS[name].get_payTo() != None:
        embed.add_field(name="Person to pay back",value = config.MEETUPS[name].get_payTo())
    
    if config.MEETUPS[name].get_payAmount() != None:
        embed.add_field(name="Amount per person to be paid back",value = str(config.MEETUPS[name].get_payAmount()))
    
    if config.MEETUPS[name].get_payInfo() != None:
        embed.add_field(name="Pay information",value =config.MEETUPS[name].get_payInfo())
    
    if config.MEETUPS[name].get_other() != None:
        embed.add_field(name="Other information",value = config.MEETUPS[name].get_other())
    
    return embed
