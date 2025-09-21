from datetime import date, datetime


class RouteCommand:
    def __init__(self,
                 user_id: str,
                 tenant_id: str,
                 description: str, 
                 date: date, 
                 type: str,
                 workplace: str,
                 persons: str,
                 activity: str,
                 diamond_count: int,
                 arrow_count: int,
                 sticker_count: int,
                 working_hours: float,
                 route_id: str = None,
                 ):
        self.description = description
        self.date = date
        self.type = type
        self.workplace = workplace
        self.persons = persons
        self.activity = activity
        self.diamond_count = diamond_count
        self.arrow_count = arrow_count
        self.sticker_count = sticker_count
        self.working_hours = working_hours
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.route_id = route_id

    
