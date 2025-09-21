#from app.domain.users.entities.UserId import UserId

from datetime import date
from .RouteId import RouteId

class RouteEntity:
    
    def __init__(self, 
                 route_id: RouteId=None, 
                 user_id: str=None, 
                 tenant_id:str=None, 
                 description: str = "", 
                 type: str = "",
                 workplace: str = "",
                 persons: str = "",
                 activity: str = "",
                 diamond_count: int = 0,
                 arrow_count: int = 0,
                 sticker_count: int = 0,
                 working_hours: float = 0.0,
                 date: date = None):
        if (route_id is None):
            self.route_id = RouteId.generate()
        else:
            self.route_id = route_id
        self._description = description
        self._date = date
        self._user_id = user_id
        self._tenant_id = tenant_id
        self._type = type
        self._workplace = workplace
        self._persons = persons
        self._activity = activity
        self._diamond_count = diamond_count
        self._arrow_count = arrow_count
        self._sticker_count = sticker_count
        self._working_hours = working_hours        

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def date(self) -> date:
        return self._date

    @date.setter
    def date(self, value: date):
        self._date = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def tenant_id(self):
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, value):
        self._tenant_id = value

    @property
    def workplace(self):
        return self._workplace

    @workplace.setter
    def workplace(self, value):
        self._workplace = value

    @property
    def persons(self):
        return self._persons

    @persons.setter
    def persons(self, value):
        self._persons = value

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, value):
        self._activity = value

    @property
    def diamond_count(self):
        return self._diamond_count

    @diamond_count.setter
    def diamond_count(self, value):
        self._diamond_count = value

    @property
    def arrow_count(self):
        return self._arrow_count

    @arrow_count.setter
    def arrow_count(self, value):
        self._arrow_count = value

    @property
    def sticker_count(self):
        return self._sticker_count

    @sticker_count.setter
    def sticker_count(self, value):
        self._sticker_count = value

    @property
    def working_hours(self):
        return self._working_hours

    @working_hours.setter
    def working_hours(self, value):
        self._working_hours = value

    def __repr__(self):
        return (f"RouteEntity(route_id={self.route_id}, description={self.description}, date={self.date}, "
                f"user_id={self.user_id}, tenant_id={self.tenant_id}, type={self.type}, workplace={self.workplace}, "
                f"persons={self.persons}, activity={self.activity}, diamond_count={self.diamond_count}, "
                f"arrow_count={self.arrow_count}, sticker_count={self.sticker_count}, working_hours={self.working_hours})")