import subprocess
import os

def get_duration_ffmpeg(file_path):
    """Get the duration of a media file using ffmpeg."""
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    return float(result.stdout.strip())

def synchronize_audio_video_ffmpeg(video_path, audio_path, output_path):
    """Synchronize audio with video using ffmpeg."""
    video_duration = get_duration_ffmpeg(video_path)
    audio_duration = get_duration_ffmpeg(audio_path)
    offset = abs(video_duration - audio_duration)

    if video_duration > audio_duration:
        cmd = f'ffmpeg -y -v verbose -i "{video_path}" -itsoffset {offset} -i "{audio_path}" -c:v copy -c:a aac -strict experimental -b:a 192k -shortest -map 0:v:0 -map 1:a:0 "{output_path}"'
    else:
        cmd = f'ffmpeg -y -v verbose -itsoffset {offset} -i "{audio_path}" -i "{video_path}" -c:v copy -c:a aac -strict experimental -b:a 192k -shortest -map 1:v:0 -map 0:a:0 "{output_path}"'

    subprocess.call(cmd, shell=True)
    print('Synchronization Done')

def add_subtitles_ffmpeg(video_path, subtitles_path, output_path):
    """Add subtitles to a video using ffmpeg."""
    cmd = f'ffmpeg -y -i "{video_path}" -vf subtitles="{subtitles_path}" "{output_path}"'
    subprocess.call(cmd, shell=True)
    print('Subtitles added')

# usage
if __name__ == "__main__":
    concatenated_video_path = "Storage_layer/media/video_assembler/concat_video.mp4"
    audio_path = "Storage_layer/media/full_audio/full_script.mp3"
    subtitles_path = "Storage_layer/subtitles/subtitles.srt"
    temp_output_path = "temp_video_with_audio.mp4"
    final_output_path = "finaaaaaal.mp4"

    # Merge audio with video
    synchronize_audio_video_ffmpeg(concatenated_video_path, audio_path, temp_output_path)

    # Add subtitles to the video
    add_subtitles_ffmpeg(temp_output_path, subtitles_path, final_output_path)

    # Clean up the temporary file
    os.remove(temp_output_path)

    print(f'Final video with audio and subtitles created at {final_output_path}')