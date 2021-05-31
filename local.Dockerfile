FROM python:3.9.2
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY . . 
CMD ["python", "src/bot.py"]