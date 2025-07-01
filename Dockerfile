FROM public.ecr.aws/docker/library/python:3.12.1-slim
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task
COPY wwapp/ ./
RUN python -m pip install -r requirements.txt
RUN python -mpip install gunicorn
#CMD ["ls","/var/task", "--all"]
#CMD ["python3","app.py"]
CMD ["gunicorn", "-b=:8080", "-w=1", "app:webapp"]