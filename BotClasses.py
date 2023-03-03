from datetime import datetime
import config

class MeetUp:
    ''' MeetUp represents a meet up instance '''
    
    # Implicits
    def __init__(self, name: str = None, startdate: datetime = None, enddate: datetime = None, \
                description: str = None, location: int = None, status: str = None,payAmount: float = \
                None,payTo: str = None, payInfo: str = None, other: str = None, guildId: str = None) -> None:
        
        # Sets name value
        self.name = name
        self.startdate = startdate
        self.enddate = enddate  
        self.description = description
        self.location = location
        self.status = status
        self.payAmount = payAmount
        self.payTo = payTo
        self.payInfo = payInfo
        self.other = other
        self.guildId = guildId
        self.confirmed_going = None
 
    def __str__(self) -> str:
        pass
    
    # Modifiers    
    def set_name(self, name: str):
        """Changes the desired name of the meetup"""
        
        self.name = name
    
    def set_startdate(self, startdate: datetime = None):
        self.startdate = startdate

    def set_enddate(self, enddate: datetime = None):
        self.enddate = enddate

    def set_description(self, description: str  = None):
        self.description = description 
    
    def set_location(self, location: str  = None):
        self.location = location

    def set_status(self, status: str = None):
        self.status = status
    
    def set_payTo(self,payTo: str = None):
        self.payTo = payTo

    def set_payAmount(self,payAmount: float = None):
        self.payAmount = payAmount

    def set_payInfo(self,payInfo:str = None):
        self.payInfo = payInfo
    
    def set_other(self, other: str = None):
        self.other = other
    
    def get_name(self) -> str: 
        return self.name
    
    def get_startdate(self) -> datetime:
        if self.startdate != None:
            output = f'{self.startdate:%d %b %Y}'+ ' @ ' + f'{self.startdate:%H:%M:%S %p}'
        else:
            output = None
        return output

    def get_enddate(self) -> datetime:
        if self.enddate != None:
            output = f'{self.enddate:%d %b %Y}'+ ' @ '  + f'{self.enddate:%H:%M:%S %p}'
        else:
            output = None
        return output

    def get_description(self) -> str:
        return self.description
    
    def get_location(self) -> str:
        return self.location

    def get_status(self) -> str:
        return self.status 
    
    def get_payTo(self) -> str:
        return self.payTo

    def get_payAmount(self) -> float:
        return self.payAmount
    
    def get_payInfo(self) -> str:
        return self.payInfo

    def get_other(self) -> str:
        return self.other 

    def get_guild_id(self) -> str:
        return self.guildId
        

class MEETUP:
    MEETUPS = dict()

    def __init__(self):
        pass
    
    @staticmethod
    def retrieveFromDB():
        config.cursor.execute('SELECT * from meet_up;')
        
        for meetUp in config.cursor.fetchall():
            MEETUP.MEETUPS[meetUp['mu_name']] = \
                MeetUp(meetUp['mu_name'],meetUp['mu_startdate'],\
                    meetUp['mu_enddate'],meetUp['mu_description'],meetUp['mu_location'],\
                        meetUp['mu_status'],meetUp['mu_payamount'],meetUp['mu_payto'],\
                            meetUp['mu_payinfo'],meetUp['mu_other'])
        config.MEETUPS = MEETUP.MEETUPS


config.MeetUp = MeetUp
