from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import re
from PIL import Image
import numpy as np

# Specify the directory containing your videos
video_dir = 'Storage_layer/media/video_chunks'
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
concatenated_video_path = os.path.join(VIDEO_ASSEMBLER_DIR, "concat_video.mp4")
concatenated_clip.write_videofile(concatenated_video_path, codec='libx264')

# Print the results
print(f"The concatenated video has been saved as {concatenated_video_path}")
