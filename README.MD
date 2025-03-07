# T-lofi
A simple python script for playing **LoFi Girl** livestreams in the terminal.

## Features
- ```tlofi``` for playing a random stream 
- ```tlofi <title>``` for playing a specific stream
- ```tlofi list``` for available streams 
- ```tlofi skip``` for playing the next stream
- ```tlofi help``` for available commands 
- ```tlofi info``` for info on the currently playing stream
- ```tlofi stop``` for exiting

## Streams 
- https://www.youtube.com/watch?v=HuFYqnbVbzY  - chill
- https://www.youtube.com/watch?v=P6Segk8cr-c  - sad
- https://www.youtube.com/watch?v=1oDrJba2PSsA - study
- https://www.youtube.com/watch?v=28KRPhVzCus  - sleep
- https://www.youtube.com/watch?v=TtkFsfOP9QI - piano
- https://www.youtube.com/watch?v=Na0w3Mz46GA - asian
- https://www.youtube.com/watch?v=S_MOd40zlYU - ambient
- https://www.youtube.com/watch?v=4xDzrJKXOOY - synth
- https://www.youtube.com/watch?v=jfKfPfyJRdk - relax

All streams are from [LoFi](https://www.youtube.com/@LofiGirl) Girl channel.<br>


### Streams Management 
Streams can be added/replaced from the JSON file in media dir.<br>
For every stream a respective "type" keyword must be added.<br>
Then it can be played with ```tlofi <title>``` 


## How to run 
```
git clone https://github.com/IliasMr/tlofi.git
cd tlofi
chmod +x setup.sh
sudo ./setup.sh
```
- setup.sh: installs vlc, yt-dlp and creates an alias for tlofi to start the script easily (for debian)