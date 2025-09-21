import boto3
import io
from datetime import datetime

from routes.domain.entities.TemplateValueObject import TemplateValueObject
from routes.domain.repositories.TemplateRepository import TemplateRepository

class TemplateS3Repository(TemplateRepository):
    def __init__(self, bucket_name="wwtemplate", 
                 object_key="wege_2025.xlsx", 
                 aws_region="eu-central-1"):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.aws_region = aws_region

    def get_latest_template(self):
        s3 = boto3.client("s3", region_name=self.aws_region)
        response = s3.get_object(Bucket=self.bucket_name, Key=self.object_key)
        file_data = io.BytesIO(response["Body"].read())
        return TemplateValueObject(
            file_data=file_data,
            date=datetime.now()
        )