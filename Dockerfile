FROM ubuntu

RUN apt-get update -y
RUN apt-get install -y curl
RUN apt-get install -y python
RUN apt-get install -y openjdk-16-jdk
RUN apt-get install -y pip
RUN apt-get install -y tar

COPY . /opt/source
WORKDIR /opt/source

RUN pip install -r requirements.txt

RUN ["curl", "https://download.java.net/java/GA/jdk16/7863447f0ab643c585b9bdebf67c69db/36/GPL/openjdk-16_linux-x64_bin.tar.gz", "--output", "openjdk-16.tar.gz"]
RUN ["tar", "zxvf", "openjdk-16.tar.gz"]

RUN ["cp", "config/application.yml", "jdk-16/bin"]
RUN ["cp", "Lavalink.jar", "jdk-16/bin"]

RUN ["cp", ".env.dev", ".env"]

EXPOSE 2333/tcp

ENTRYPOINT ["python", "main.py"]

CMD ["nohup", "java", "-jar", "jdk-16/bin/Lavalink.jar", ".", "&"]