from datetime import date
import uuid

class TemplateValueObject:
    
    def __init__(self, 
                 id: str=None,
                 file_data: bytes=None,
                 date: date = None):
        if (id is None):
            self._id = str(uuid.uuid4())
        else:
            self._id = id
        self._date = date
        self._file_data = file_data

    @property
    def file_data(self) -> str:
        return self._file_data

    @file_data.setter
    def file_data(self, value: str):
        self._file_data = value

    @property
    def date(self) -> date:
        return self._date

    @date.setter
    def date(self, value: date):
        self._date = value