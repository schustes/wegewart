from datetime import datetime

from routes.domain.entities.RouteEntity import RouteEntity
from routes.domain.entities.TemplateValueObject import TemplateValueObject
from routes.domain.repositories.TemplateRepository import TemplateRepository

import io

class TemplateFileRepository(TemplateRepository):
    def get_latest_template(self):
        in_file = open("/home/stephan/personal/swv/wege_2025.xlsx", "rb")
        bytes_in = io.BytesIO(in_file.read())
        #data = in_file.read()
        in_file.close()
        return TemplateValueObject(
            file_data=bytes_in,
            date=datetime.now()
        )
