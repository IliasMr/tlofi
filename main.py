import subprocess
import json
import sys
import re

# TODO: add error checking

ascii_opening = """
  _        __ _       _      
 | |      / _(_)     | |     
 | |     | |_ _  __ _| |__  
 | |     |  _| |/ _` | '_ \ 
 | |____ | | | | (_| | | | |
 |______||_| |_|\__, |_| |_|
                 __/ |      
                |___/       
   🎶 Lofi Radio 🎶
"""



def read_streams():
    with open("streams.txt") as file:
        streams = file.readlines()
    return streams

def play(stream_id):
    stream_url = streams[stream_id]

    # Get stream info 
    metadata = subprocess.check_output(["yt-dlp", "-j", stream_url], text=True)
    stream_info = json.loads(metadata)
    title = stream_info.get("title", "Unknown Title")
    title = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", title).strip()

    # Get the audio URL
    audio_url = subprocess.check_output(["yt-dlp", "-f", "bestaudio", "-g", stream_url], text=True).strip()

    # subprocess.Popen(["ffplay", "-re", "-i", audio_url, "-vn", "-f", "pulse", "default"], 
    #                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # use --intf dummy for playing in the background
    vlc_p = subprocess.Popen(["vlc", audio_url, "--intf", "dummy", "--play-and-exit"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"♫ Now playing: {title} ♫")

    return vlc_p


if __name__ == "__main__":

    print(ascii_opening)
    streams = read_streams()

    # start from the 1st one 
    stream_id = 0
    vlc = play(stream_id)

    try:
        while(True):
            key = input()
            if key.strip() == "stop":
                print("exiting..")
                vlc.terminate()
                break
            elif key.strip() == "skip":
                #print("skipping stream..")
                vlc.terminate()
                stream_id= (stream_id+1) % len(streams) 
                vlc = play(stream_id)
            elif key.strip() == "help":
                print("--Commands--")
                print("skip -> skip to the next stream url in the txt file")
                print("stop -> stop playing and exit the program")
            else:
                print("No such command..type <help> for available commands")
                
    except KeyboardInterrupt:
        print("exiting..")
        vlc.terminate()
        sys.exit(0)