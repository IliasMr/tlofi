import subprocess
import json
import sys
import re
from urllib.parse import urlparse
import os

# TODO: more error checking


ascii_opening = """

  __  .__          _____.__ 
_/  |_|  |   _____/ ____\__|
\   __\  |  /  _ \   __\|  |
 |  | |  |_(  <_> )  |  |  |
 |__| |____/\____/|__|  |__|

 🎶 Lofi Radio 🎶
"""


# terminal colors
GREEN = '\033[92m'  
CYAN = '\033[36m'   
RESET = '\033[0m'  # default

# create temp folder if does not exist
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)  

PID_FILE = os.path.join(TEMP_DIR, "pid.txt")  
STREAMS_FILE = os.path.join(os.path.dirname(__file__), "media", "streams.txt") 
CURRENT_FILE = os.path.join(TEMP_DIR, "current.txt")


def read_streams():
    if not os.path.exists(STREAMS_FILE):
        print ("No streams file found")
        return []
    with open(STREAMS_FILE, "r") as file:
        return [line.strip() for line in file if line.strip()]

def list():

    if os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, "r") as current:
            id = current.read(1)
    else:
        print("No active playback found")
        return
    
    currentID = int(id)

    streams = read_streams()
    if not streams:
        print(f"{CYAN}> No streams available. Add one with 'tlofi add <url>'{RESET}")
        return
    
    print(f"{CYAN}> Queue{RESET}")
    for i, url in enumerate(streams):
        title = subprocess.check_output(["yt-dlp", "-O", "title", url], text=True).strip()
        title = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", title).strip()
        if (i == currentID):
            print(f"{GREEN}{i+1}. {title} || {url}{RESET}")    
        else:
            print(f"{i+1}. {title} || {url}")


def play():
    streams = read_streams()
    if not streams:
        print("No streams available! Add one with 'tlofi add <url>'")
        return

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
        print("falied to get URL")
        return None

    # use --intf dummy for playing in the background
    vlc_p = subprocess.Popen(["vlc", audio_url, "--intf", "dummy", "--play-and-exit"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f">{GREEN}♫ Now playing:{RESET}{title} ♫")

    with open(PID_FILE, "w") as pid_file:
        pid_file.write(str(vlc_p.pid))



def help():
    print(f"{CYAN}>Commands{RESET}")
    print("skip      -> skip to the next stream in queue")
    print("stop      -> stop playing and exit")
    print("list      -> print the stream queue")
    print("add <url> -> add new stream url to queue")       #TODO: to implement


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
    stream_id = (stream_id + 1) % len(read_streams())

    with open(CURRENT_FILE, "w") as current:
        current.write(str(stream_id))

    print(f"{CYAN}>Skipped to next stream.{RESET}")
    play()

if __name__ == "__main__":


    if len(sys.argv) == 1:
        if os.path.exists(PID_FILE):
            print("tlofi is already running")   
            quit()
        print(ascii_opening)
        
        # start from the 1st stream in the list
        with open(CURRENT_FILE, "w") as current:
            current.write("0")

        play()
    elif sys.argv[1] == "stop":
        stop()
    elif sys.argv[1] == "help":
        help()
    elif sys.argv[1] == "list":
        list()
    elif sys.argv[1] == "skip":
        skip()
