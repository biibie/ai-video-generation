from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
import re
from PIL import Image
import numpy as np

# Specify the directories containing your videos and audio
video_dir = 'Storage_layer/media/video_chunks'
AUDIO_PATH = 'Storage_layer/media/full_audio/full_script.mp3'
VIDEO_ASSEMBLER_DIR = 'Storage_layer/media/video_assembler'

# Function to extract the numeric part of the filename
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# Function to resize frames using PIL
def resize_frame(frame, size):
    image = Image.fromarray(frame)
    resized_image = image.resize(size, Image.Resampling.LANCZOS)
    return np.array(resized_image)

# Function to adjust the length of audio and video to match each other
def adjust_length(video_clip, audio_clip):
    """Adjust the length of audio and video to match each other."""
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration
    duration_difference = abs(video_duration - audio_duration)
    
    if audio_duration > video_duration:
        audio_clip = audio_clip.subclip(0, video_duration)
        adjusted_audio_path = "adjusted_audio.mp3"
        audio_clip.write_audiofile(adjusted_audio_path)
        print(f"Audio was longer by {duration_difference:.2f} seconds. It has been adjusted to match the video length and saved as {adjusted_audio_path}.")
        return adjusted_audio_path, None
    else:
        video_clip = video_clip.subclip(0, audio_duration)
        adjusted_video_path = "adjusted_video.mp4"
        video_clip.write_videofile(adjusted_video_path, codec='libx264')
        print(f"Video was longer by {duration_difference:.2f} seconds. It has been adjusted to match the audio length and saved as {adjusted_video_path}.")
        return None, adjusted_video_path

# Get a list of all video files in the directory
video_files = [f for f in os.listdir(video_dir) if f.endswith(('mp4', 'avi', 'mov', 'mkv'))]

# Sort the files based on the numeric value in their filenames
video_files.sort(key=extract_number)

# Standardize the resolution of the clips
standard_resolution = (1920, 1080)  # Example resolution (width, height)

# Create a list of standardized VideoFileClip objects
clips = []
for video_file in video_files:
    clip = VideoFileClip(os.path.join(video_dir, video_file))
    # Resize each frame of the clip
    clip_resized = clip.fl_image(lambda frame: resize_frame(frame, standard_resolution))
    clips.append(clip_resized)

# Concatenate all video clips
concatenated_clip = concatenate_videoclips(clips)
concatenated_video_path = "concatenated_video.mp4"
concatenated_clip.write_videofile(concatenated_video_path, codec='libx264')

# Load the audio clip
audio_clip = AudioFileClip(AUDIO_PATH)

# Adjust the length of the concatenated video clip and the audio clip
adjusted_audio_path, adjusted_video_path = adjust_length(concatenated_clip, audio_clip)

# Save the path of the audio file to a text file for the subtitle script
audio_path_to_use = adjusted_audio_path if adjusted_audio_path else AUDIO_PATH
with open("audio_path.txt", "w") as f:
    f.write(audio_path_to_use)

# Print the results
print(f"The concatenated video has been saved as {concatenated_video_path}")
if adjusted_audio_path:
    print(f"The adjusted audio has been saved as {adjusted_audio_path}")
if adjusted_video_path:
    print(f"The adjusted video has been saved as {adjusted_video_path}")
