from datetime import datetime

from discord import ui


# Storage class
class MeetUp:
    ''' MeetUp represents a meet up instance '''
    
    # Implicits
    def __init__(self, name: str = None, startdate: datetime = None, enddate: datetime = None, \
                description: str = None, location: int = None, status: str = None,payAmount: float = \
                None,payTo: str = None, payInfo: str = None, other: str = None, guild_id: str = None) -> None:
        
        # Sets activity value
        self.name = name    
        
        # create new date object for start date
        if startdate != None:
            self.startdate = startdate
        else:
            pass

        # create new date object for end date
        if enddate != None:
            self.enddate = enddate
        else:
            pass
        
        self.description = description
        self.location = location
        self.status = status
        self.guild_id = guild_id

        self.payAmount = payAmount
        self.payTo = payTo
        self.payInfo = payInfo
        self.other = other
        #self.confirmed_going = None
 
    def __str__(self) -> str:
        pass
    
    # Modifiers    
    def change_activity(self, activity: str):
        """Changes the desired activity of the meetup"""
        self.name = activity
    
    def change_startdate(self, startdate: list):
        self.startdate = datetime.datetime(startdate[0],startdate[1],startdate[2],startdate[3],startdate[4],startdate[5])

    def change_enddate(self, enddate: list):
        self.enddate = datetime.datetime(enddate[0],enddate[1],enddate[2],enddate[3],enddate[4],enddate[5])

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
        return self.name
    
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

    def get_guild_id(self):
        return self.guild_id
        
# General view class
class BotView(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

