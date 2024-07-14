import assemblyai as aai
import os

def create_subtitles(audio_path, api_key):
    """Transcribe audio and generate subtitles using AssemblyAI."""
    aai.settings.api_key = api_key
    transcript = aai.Transcriber().transcribe(audio_path)
    subtitles = transcript.export_subtitles_srt()
    
    subtitles_path = os.path.join("Storage_layer", "subtitles", "subtitles.srt")
    with open(subtitles_path, "w") as f:
        f.write(subtitles)
    print(f'Subtitles created at {subtitles_path}')

# Directly specify the path to the audio file
audio_path = "Storage_layer/media/full_audio/full_script.mp3"
api_key = "3c9277c1c22e47b99ff159ed4e4405b8"
create_subtitles(audio_path, api_key)
