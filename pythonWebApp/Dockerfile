FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app 
RUN pip3 install flask requests jinja2 gunicorn boto3 datetime
COPY . .
ENV BG_COLOR=beige
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]

