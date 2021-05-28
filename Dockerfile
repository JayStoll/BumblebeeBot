FROM openjdk:11
COPY . /usr/src/app
WORKDIR /usr/src/app
ENTRYPOINT ["java", "-jar", "lavalink.jar"]