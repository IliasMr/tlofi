import subprocess
import json
import sys
import re
import os
from random import randrange

"""List with the available streams.""" 

streams = [
"https://www.youtube.com/watch?v=HuFYqnbVbzY",      # chill 
"https://www.youtube.com/watch?v=P6Segk8cr-c",      # sad
"https://www.youtube.com/watch?v=1oDrJba2PSs",      # study
"https://www.youtube.com/watch?v=28KRPhVzCus",      # sleep
"https://www.youtube.com/watch?v=TtkFsfOP9QI",      # piano 
"https://www.youtube.com/watch?v=Na0w3Mz46GA",      # asian 
"https://www.youtube.com/watch?v=S_MOd40zlYU",      # ambient 
"https://www.youtube.com/watch?v=4xDzrJKXOOY",      # synth
"https://www.youtube.com/watch?v=jfKfPfyJRdk"       # relax
]


"""Each type corresponds to the respective stream by index."""
streamTypes = ["chill", "sad", "study", "sleep", "piano", "asian", "ambient", "synth", "relax"]


# terminal colors
GREEN = '\033[92m'  
CYAN = '\033[36m'   
RESET = '\033[0m'  # default

# create temp folder if does not exist
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)  

PID_FILE = os.path.join(TEMP_DIR, "pid.txt")  
CURRENT_FILE = os.path.join(TEMP_DIR, "current.txt")
#STREAMS_FILE = os.path.join(os.path.dirname(__file__), "media", "streams.txt") 


# def read_streams():
#     if not os.path.exists(STREAMS_FILE):
#         print ("No streams file found")
#         return []
#     with open(STREAMS_FILE, "r") as file:
#         return [line.strip() for line in file if line.strip()]

ascii_opening = """

  __  .__          _____.__ 
_/  |_|  |   _____/ ____\__|
\   __\  |  /  _ \   __\|  |
 |  | |  |_(  <_> )  |  |  |
 |__| |____/\____/|__|  |__|


"""

## 🎶 Lofi Radio 🎶


# list available streams
def list_q():

    running = False
    if os.path.exists(CURRENT_FILE):
        running = True
        with open(CURRENT_FILE, "r") as current:
            id = current.read(1)
        currentID = int(id)
        
    
    for i, (url,title) in enumerate(zip(streams,streamTypes)):
        #title = subprocess.check_output(["yt-dlp", "-O", "title", url], text=True).strip()
        #title = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", title).strip()
        if running == True:
            if (i == currentID):
                print(f"{GREEN}{i+1}. {title.ljust(7)} || {url.ljust(7)}{RESET}")    

            else:
                print(f"{i+1}. {title.ljust(7)} || {url.ljust(7)}")
        else:
            print(f"{i+1}. {title.ljust(7)} || {url.ljust(7)}")


# start playing lofi
def play():

    with open(CURRENT_FILE, "r") as current:
        id = current.read(1)

    stream_url = streams[int(id)]

    # Get stream info 
    metadata = subprocess.check_output(["yt-dlp", "-j", "-f", "bestaudio", stream_url], text=True)
    stream_info = json.loads(metadata)
    
    title = stream_info.get("title", "Unknown Title")
    title = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", title).strip()

    audio_url = stream_info.get("url", None)
    if not audio_url:
        print("Failed to get URL. Please select a different stream")
        return None

    # use --intf dummy for playing in the background
    vlc_p = subprocess.Popen(["vlc", audio_url, "--intf", "dummy", "--play-and-exit"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f">{GREEN}♫ Now playing:{RESET}{title} ♫")

    with open(PID_FILE, "w") as pid_file:
        pid_file.write(str(vlc_p.pid))


# help section
def helpp():
    #print(f"{CYAN}>Commands{RESET}")
    print("tlofi            -> play a random stream from the list")
    print("tlofi <stream>   -> play a specific stream from the list.")
    print("tlofi skip       -> skip to the next stream in the list")
    print("tlofi stop       -> stop playing and exit")
    print("tlofi list       -> list the available streams")
    print("tlofi info       -> get info for the current stream")


# stop session and exit
def stop():
    if not os.path.exists(PID_FILE):
        print("No active playback found")
        return
    
    with open(PID_FILE, "r") as pid_file:
        pid = pid_file.read().strip()

    try:
        os.kill(int(pid), 9) 
        os.remove(PID_FILE)
        os.remove(CURRENT_FILE)
        print(f"{CYAN}> Stopped playback{RESET}")
    
    except ProcessLookupError:
        print("No active VLC process found.")

# skip to the next stream
def skip():
    if not os.path.exists(PID_FILE):
        print("No active playback found")
        return
    
    # terminate previous session
    with open(PID_FILE, "r") as pid_file:
        pid = pid_file.read().strip()
    try:
        os.kill(int(pid), 9) 
    except ProcessLookupError:
        print("No active VLC process found.")

    if os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, "r") as current:
            try:
                stream_id = int(current.read().strip())
            except ValueError:
                stream_id = 0           # default to 0 if corrupted
    else:
        stream_id = 0  
    stream_id = (stream_id + 1) % len(streams)

    with open(CURRENT_FILE, "w") as current:
        current.write(str(stream_id))

    print(f"{CYAN}>Skipped to next stream.{RESET}")
    play()

# helper to stop the previous session 
def stop_previous_session():
   
    with open(PID_FILE, "r") as pid_file:
        pid = pid_file.read().strip()
    try:
        os.kill(int(pid), 9) 
    except ProcessLookupError:
        print("Error: Could not kill vlc session")

# displays info for current playing stream
def info():
    if not os.path.exists(CURRENT_FILE):
        print("No stream is currently playing.")
        return

    with open(CURRENT_FILE, "r") as current:
        id = current.read().strip()
    
    if not id.isdigit() or int(id) >= len(streams):
        print("Invalid stream ID.")
        return

    stream_url = streams[int(id)]
    
    try:
        metadata = subprocess.check_output(["yt-dlp", "-j", "-f", "bestaudio", stream_url], text=True)
        stream_info = json.loads(metadata)
    except Exception as e:
        print(f"Error fetching stream info: {e}")
        return

    title = stream_info.get("title", "Unknown Title")
    uploader = stream_info.get("uploader", "Unknown Uploader")
    upload_date = stream_info.get("upload_date", "Unknown Date")
    thumbnail = stream_info.get("thumbnail", "No Thumbnail")
    direct_audio_url = stream_info.get("url", "Unavailable")

    if upload_date != "Unknown Date" and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

    print(f"{CYAN}Currently Playing:{RESET}{title}🎵")
    print(f"{CYAN}Uploader: {RESET}{uploader}")
    print(f"{CYAN}Uploaded on: {RESET}{upload_date}")
    print(f"{CYAN}Video URL: {RESET}{streams[int(id)]}")
    print(f"{CYAN}Direct Audio URL: {RESET}{direct_audio_url}")
    print(f"{CYAN}Thumbnail: {RESET}{thumbnail}")

            

if __name__ == "__main__":

    streams_map = {
        "chill": 0,
        "sad": 1,
        "study": 2,
        "sleep": 3,
        "piano": 4,
        "asian": 5,
        "ambient": 6,
        "synth": 7,
        "relax": 8
    }
    if len(sys.argv) > 2:
        print("No such command. Run 'tlofi help' for usage")
        exit()

    if len(sys.argv) == 1:
        
        # kill the previous session first
        if os.path.exists(PID_FILE):
            stop_previous_session()

        print(ascii_opening)
        randomID = randrange(9)
        with open(CURRENT_FILE, "w") as current:
            current.write(str(randomID))
        play()
    elif sys.argv[1] in streams_map:
        if os.path.exists(PID_FILE):
            stop_previous_session()

        with open(CURRENT_FILE, "w") as current:
            current.write(str(streams_map[sys.argv[1]]))
        print(ascii_opening)
        play()
    elif sys.argv[1] == "stop":
        stop()
    elif sys.argv[1] == "list":
        list_q()
    elif sys.argv[1] == "skip":
        skip()
    elif sys.argv[1] == "help":
        helpp()
    elif sys.argv[1] == "info":
        info()
    else: 
        print(f"{CYAN}No such command. Type 'tlofi help' for available commands.{RESET}")