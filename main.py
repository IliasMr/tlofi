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

# def read_streams():
#     with open("streams.txt") as file:
#         streams = file.readlines()
#     return streams

# terminal colors
GREEN = '\033[92m'  
CYAN = '\033[36m'   
RESET = '\033[0m'  # default



class StreamManager:
    def __init__(self):
        self.streams = [
            "https://www.youtube.com/watch?v=jfKfPfyJRdk",
            "https://www.youtube.com/watch?v=5yx6BWlEVcY",
            "https://www.youtube.com/watch?v=Dx5qFachd3A"
        ]
    def list_streams(self, streamID):
        print(f"{CYAN}>Queue{RESET}")

        i=0
        for url in self.streams:
            title = subprocess.check_output(["yt-dlp", "-O", "title", url], text=True).strip()
            title = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", title).strip()
            if(streamID == i):
                print(f"{GREEN}{title} || {url}{RESET}")
            else:
                print(f"{title} || {url}")
            print(" ")
            i+=1

    def add_stream(self,url):

        parsedUrl = urlparse(url)
        if parsedUrl.scheme in ['http', 'https'] and parsedUrl.netloc in ['youtube.com', 'www.youtube.com', 'youtu.be']:
            if url not in self.streams:
                self.streams.append(url)
                print(f"{CYAN}>{len(self.streams)} in queue{RESET}")
                # TODO: also get and save title
        else:
            print(f"{CYAN}>Invalid URL. Please provide a valid youtube link.{RESET}")


def refresh_screen(current):
    os.system("clear" if os.name == "posix" else "cls")  
    print(ascii_opening)
    print(f">{GREEN}♫ Now playing:{RESET} random ♫\n")




def play(urlsManager, stream_id):
    if urlsManager.streams[stream_id] is not None:
        stream_url = urlsManager.streams[stream_id]
    else:
        print("No stream in queue! Play a stream with play")
        return None

    # Get stream info 
    metadata = subprocess.check_output(["yt-dlp", "-j", "-f", "bestaudio", stream_url], text=True)
    stream_info = json.loads(metadata)
    
    title = stream_info.get("title", "Unknown Title")
    title = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", title).strip()

    audio_url = stream_info.get("url", None)
    if not audio_url:
        print("falied to get URL")
        return None

    # FFMPEG
    # subprocess.Popen(["ffplay", "-re", "-i", audio_url, "-vn", "-f", "pulse", "default"], 
    #                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # VLC 
    # use --intf dummy for playing in the background
    vlc_p = subprocess.Popen(["vlc", audio_url, "--intf", "dummy", "--play-and-exit"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f">{GREEN}♫ Now playing:{RESET}{title} ♫")

    return vlc_p


def help():
    print(f"{CYAN}>Commands{RESET}")
    print("skip      -> skip to the next stream url in the txt file")
    print("stop      -> stop playing and exit the program")
    print("list      -> print the stream queue")
    print("add <url> -> add new stream url to queue")



if __name__ == "__main__":

    print(ascii_opening)

    urlsManager = StreamManager()

    stream_id = 0
    vlc = play(urlsManager, stream_id)

    try:
        while(True):

            key = input()
            args = key.split(maxsplit=1)

            if not args:
                continue    # empty

            command = args[0]
            if command.strip() == "stop":
                vlc.terminate()
                break
            elif command.strip() == "skip":

                vlc.terminate()
                stream_id= (stream_id+1) % len(urlsManager.streams) 
                vlc = play(urlsManager, stream_id)
            elif command.strip() == "help":
                help()
            elif command.strip() == "list":
                urlsManager.list_streams(stream_id)
            elif command == "add" and len(args) > 1:
                url = args[1]
                urlsManager.add_stream(url)
            else:
                print(">No such command..type <help> for available commands")
                
    except KeyboardInterrupt:
        vlc.terminate()
        sys.exit(0)