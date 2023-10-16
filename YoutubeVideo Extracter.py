import os
from pytube import YouTube
import cv2

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def DownloadAndProcessFile(file_location, frames_folder, frame_interval):
    ensure_folder_exists(frames_folder)
    cap = cv2.VideoCapture(file_location)
    
    print("Video found")
    
    # Process the video frames and save them as individual images
    frame_count = 0  # Initialize a variable to count the frames
    time_per_frame = 1.0 / cap.get(cv2.CAP_PROP_FPS)  # Time per frame in seconds
    
    while True:
        ret, frame = cap.read()
        
        if not ret:  # If no more frames to read
            break

        # Capture frame at specified interval
        if frame_count % (frame_interval // time_per_frame) == 0:
            frame_filename = f"{frames_folder}/frame_{frame_count:04d}.jpg"  # File name for current frame with leading zeroes
            cv2.imwrite(frame_filename, frame)  # Save current frame as image file in JPEG

        frame_count += 1

    cap.release()
    print(f"Processed {frame_count} frames and saved selected frames in '{frames_folder}'.")

def DownloadAndProcessYTVideo(link, frames_folder, frame_interval):
    try:
        youtubeObject = YouTube(link)
        youtubeStream = youtubeObject.streams.get_highest_resolution()

        temp_video_path = youtubeStream.download()

        print("Video has downloaded successfully")

        cap = cv2.VideoCapture(temp_video_path)

        frame_count = 0  # Initialize a variable to count the frames
        time_per_frame = 1.0 / cap.get(cv2.CAP_PROP_FPS)  # Time per frame in seconds

        while True:
            ret, frame = cap.read()

            if not ret:  # If no more frames to read
                break

            # Capture frame at specified interval
            if frame_count % (frame_interval // time_per_frame) == 0:
                frame_filename = f"{frames_folder}/frame_{frame_count:04d}.jpg"  # File name for current frame with leading zeroes
                cv2.imwrite(frame_filename, frame)  # Save current frame as image file in JPEG

            frame_count += 1

        cap.release()
        print(f"Processed {frame_count} frames and saved selected frames in '{frames_folder}'.")

    except:
        print("An error has occurred:")

if __name__ == "__main__":
    videoOrLink = input("To retrieve frames from an MP4 video file, type 'file'. For a YouTube video, type 'link': ")

    frames_folder_name = input("Enter a name for the folder to save frame images: ")
    target_path = input("Enter the path where you want to place the folder: ")
    frames_folder = os.path.join(target_path, frames_folder_name)

    frame_interval = int(input("Enter the frame capture interval in seconds: "))

    if videoOrLink == "file":
        file_location = input("Input path to video file: ")
        DownloadAndProcessFile(file_location, frames_folder, frame_interval)
    elif videoOrLink == "link":
        link = input("Enter the YouTube video URL: ")
        DownloadAndProcessYTVideo(link, frames_folder, frame_interval)
    else:
        print("You must type 'file' or 'link'")
        quit()
