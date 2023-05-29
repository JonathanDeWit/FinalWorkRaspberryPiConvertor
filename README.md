# Final Work Raspberry Pi Convertor
This project is part of my Final Work project for my Bachelor degree in Applied Computer Science at the Erasmus Brussel University of Applied Sciences and Arts.
My project mainly consisted of building a video surveillance system by using microcontrollers.
If you want to know more about the project, I invite you to consult the following links:

[Final Work Paper](https://github.com/JonathanDeWit/FinalWorkRaspberryPiConvertor/blob/master/FinalWorkPaper.pdf) (NL)

Other related repositories:
* [ESP32-CAM microcontroller surveillance camera](https://github.com/JonathanDeWit/FinalWorkESP32CamLiveCamera)
* [ASP.NET API](https://github.com/JonathanDeWit/FinalWorkApi)
* [SRT Media server automation](https://github.com/JonathanDeWit/FinalWorkSrtServer)
* [Android App](https://github.com/JonathanDeWit/FinalWorkAndroidApp)

 ## Purpose
This GitHub repo contains an python project meant for an Raspberry Pi 4 B board.
This project primary goal is to receive a RTSP live video signal from an ESP32-Cam and convert it into SRT live video signal that will be send to a media server.


 ## Prerequisite
To convert a RTSP signal to an SRT signal I used the open source command line tool [FFmpeg](https://ffmpeg.org/). It is important to install FFmpeg to be able to use this program. 

When I wrote this program, the default installation of FFmpeg was not enough to convert the RTSP signal into SRT since it lacked important components to be able to use the SRT protocol. This is why a customize installation is necessary. you can find documentation in Dutch for this custom installation right [here](https://github.com/JonathanDeWit/FinalWorkRaspberryPiConvertor/blob/master/FFmpegCustomInstallGuid.pdf) (NL).

Its also important to mention that you will need to install Python 3.9 or higher.

The domain name and path of the API request are stored in ‘conf.csv’ if you want to change it feel free to edit this file.
The username and password of the SrtServer user are stored in ‘profile.csv’ if you want to change it feel free to edit this file. 


 ## Primary features
 - Convert a RTSP live video signal into a SRT live video signal
   - Every conversion is executed on a individual thread.
 - Make API calls.
   - authenticate and store the JWT token.
     - Replace the JWT token when it is about to expire.
   - Retreave the system status.
   - Updating the microcontroller status.
     - Updating the Raspberry Pi conversion status.


 ## RTSP to SRT conversion
The Raspberry Pi will check almost every second using the API to see if the system should be activated or not and if the ESP32-Cam already started to transmit the RTSP live stream. If so it will start the convert every RTSP sigil individually in a new tread. 
When the API returns that the system needs to turn off the Raspberry Pi will stop every thread and process running for every conversion until the system state change again.

To convert the RTSP signal into a SRT signal the program use the following FFmpeg command:

ffmpeg -i rtsp://< incoming RTSP address > -pix_fmt yuv420p -c:v libx264 -r 30 -b:v 1000k -f mpegts srt://< Media Server Ip > : < port >
