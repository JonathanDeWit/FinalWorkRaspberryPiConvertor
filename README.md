# Final Work Raspberry Pi Convertor
This project is part of my Final Work project for my Bachelor degree in Applied Computer Science at the Erasmus Brussel University of Applied Sciences and Arts.
My project mainly consisted of building a video surveillance system by using microcontrollers.
If you want to know more about the project, I invite you to consult the following links:


 ## Purpose
This GitHub repo contains an python project meant for an Raspberry Pi 4 B board.
This project primary goal is to receive a RTSP live video signal from an ESP32-Cam and convert it into SRT live video signal that will be send to a media server. 

You can find the code of the ESP32-Cam code [here](https://github.com/JonathanDeWit/FinalWorkESP32CamLiveCamera) and the code of the media server [here](https://github.com/JonathanDeWit/FinalWorkSrtServer).
Every API call you will find in this project was directed to the ASP.Net API which you can find [here](https://github.com/JonathanDeWit/FinalWorkApi)


 ## Prerequisite
To convert a RTSP signal to an SRT signal I used the open source command line tool [FFmpeg](https://ffmpeg.org/). It is important to install FFmpeg to be able to use this program. 

When I wrote this program, the default installation of FFmpeg was not enough to convert the RTSP signal into SRT since it lacked important components to be able to use the SRT protocol. This is why a customize installation is necessary. you can find documentation in Dutch for this custom installation right here.

Its also important to mention that you will need to install Python 3.9 or higher.


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
