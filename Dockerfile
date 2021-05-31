FROM python:3.8-slim-buster AS build

# Install required base tools for psutil and start.sh
RUN apt-get update && \
    apt-get install gcc python3-dev netcat -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* 

# Only rebuild if package requirements are updated
WORKDIR /usr/src/app
COPY ./requirements.txt .
# Install python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

FROM build
COPY . .
CMD ["python", "src/bot.py"]