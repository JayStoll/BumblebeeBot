# Bumblebee Bot

## Dependencies
|      Name                 | Version  |
| --------------------- | -------- |
| [jdk-16.zip](https://jdk.java.net/archive/) | 16 |
| [lavaLink](https://ci.fredboat.com/viewLog.html?buildId=lastSuccessful&buildTypeId=Lavalink_Build&tab=artifacts&guest=1) | #1232 |
| [ffprobe](https://ffmpeg.org/) | 4.4 |
## To Run
1. install dependencies with `pip install -r requirements.txt`
2. install jdk and lavaLink dependencies from table above
    - extract the jdk into the root directory
    - place the lavalink.jar inside jdk-16/bin directory
3. install ffprobe from table above
4. from the config folder, copy the application.yml into the jdk-16/bin directory
5. switch into jdk-16/bin directory and run command `java -jar lavalink.jar`
6. change .env.dev to .env
7. while in root directory run command `python main.py` to run the bot
