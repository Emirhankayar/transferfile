import os
import shutil
import cv2
import filetype
from os.path import expanduser

HOME = expanduser("~")
BASE = f"{HOME}/downloads"

def get_duration(results):
    cap = cv2.VideoCapture(results)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps)
    cap.release()
    return seconds

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:              
                results = os.path.join(root, file)
                kind = filetype.guess(results)
            
                if kind is None:
                    continue
                elif kind.mime.startswith('video'):
                    duration = get_duration(results)
                    if duration > 4800:
                        print(f"MOVED TO MOVIES ## \n {results} ##")
                        shutil.move(directory, f'{HOME}/Movies')
                        return
                    else:
                        print(f"MOVED TO SHOWS ## \n {results} ##")
                        shutil.move(directory, f'{HOME}/Shows')
                        return
                elif kind.mime.startswith('audio'):
                    print(f"MOVED TO MUSIC ## \n {results} ##")
                    shutil.move(directory, f'{HOME}/Music')
                    return

def main():
    directories = [os.path.join(BASE, dir) for dir in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, dir))]
    if not directories:
        print("THERE IS NOTHING TO MOVE! ##")
        return
    for directory in directories:
        process_directory(directory)

if __name__ == '__main__':
    main()
