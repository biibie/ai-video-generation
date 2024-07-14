# AI Video Creation Toolkit

## Overview
This toolkit contains various scripts for creating educational videos using AI-generated scripts, speech synthesis, video downloading and trimming, audio-video merging, and subtitle generation. The process follows a structured workflow to ensure seamless integration between each component.

## Features
1. **Script Generation: Generates educational content scripts using Cohere's language model.**
2. **Script Splitting: Splits scripts into manageable sentences for easier processing.**
3. **Text-to-Speech Conversion: Converts scripts into high-quality speech using ElevenLabs API.**
4. **Search Query Creation: Creates search queries from script segments to retrieve relevant videos.**
5. **Video Downloading: Downloads and trims videos from Pexels.**
6. **Video Assembly: Concatenates and standardizes video clips.**
7. **Final Video Assembly: Merges audio with video and adds subtitles.**
8. **Subtitle Generation: Generates subtitles using AssemblyAI.**


Each step builds upon the previous one, ensuring a smooth and cohesive process for creating the final educational video.

## Prerequisites
1. Python 3.x
2. FFmpeg (for video processing)
3. Required Python packages (detailed in each section)

## Setup
1. Install FFmpeg:
   - Download and install FFmpeg from (https://www.wikihow.com/Install-FFmpeg-on-Windows).
   - Ensure FFmpeg is accessible from your command line.

2. Install required Python packages:
   ```sh
   pip install nltk langchain langchain-cohere langchain-community langchain-core sentence-transformers assemblyai moviepy pillow numpy requests pydub

3. Obtain API keys for the following services: (you should login first, then get api keys for free)

    -Cohere (https://cohere.com/) 
    -AssemblyAI (https://www.assemblyai.com/)
    -ElevenLabs (https://elevenlabs.io/)
    -Pexels (https://www.pexels.com/)




## How It Works
It all starts with the creation of a script using the Script_generator.py script. This script takes various parameters such as topic, level of explanation, target audience age, creativity, and humor. With these parameters in mind, the script is carefully crafted to explain the chosen topic. To accomplish this, we leverage the power of the Cohere API and Langchain.

Once the script is ready, we move on to the script_splitter.py script. This script splits the generated script into smaller sentences, which are then used to generate audio dialogues using the text_to_speech.py script and ElevenLabs Text-to-Speech (TTS) service. In parallel, we generate a search query for each sentence using the search_query.py script with Cohere and Langchain. These search queries help us retrieve relevant videos from pexels

With the audio files, we proceed to download the videos using the videos_downloader.py script. This script downloads relevant video clips from Pexels and trims them to match the audio durations. Then, we transform these video clips into a standardized format using the video_assembler.py script. 

Finally, we save the completed video by combining the video clips and audio using the final_video_assembler.py script. The resulting video is now ready to be shared!  To enhance the video with subtitles, we use the subtitles.py script to generate subtitle files from the audio, ensuring accessibility and clarity. 

## Scripts and Usage
1. Script Generation (Script_generator.py)
    Description :
-Generates an educational script using the Cohere AI model based on a given topic, explanation level, target age, creativity, humor, and duration.

    Usage:
-Ensure you have your Cohere API key in keys.json.


2. Script Splitting (script_splitter.py)
    Description:
-Splits a given script into sentences using NLTK's sentence tokenizer for easier processing.

    Usage:
-Ensure you have NLTK installed.


3. Text-to-Speech Conversion (text_to_speech.py)
    Description:
-Converts the generated script into speech using the ElevenLabs API and splits the script into manageable segments. the audio will be found in Storage_layer/media in full_audio and audio_chinks (for the character later on)

    Usage:
-Ensure you have your ElevenLabs API key in keys.json.


4. Search Query Creation (search_query.py)
    Description:
-Generates search queries from script segments to retrieve relevant stock videos.

    Usage:
-Ensure you have your Cohere API key in keys.json.


5. Video Downloading (videos_downloader.py)
    Description:
-Downloads and trims videos from Pexels based on search queries and distributes the durations to match the total audio length. and store them in Storage_layer/media/video_chunks

    Usage:
-Ensure you have your Pexels API key in keys.json.


6. Video Assembly (video_assembler.py)
    Description:
-Concatenates video clips, adjusts their length to match the audio, and saves the final output in Storage_layer/media/video_assembler

    Usage:
-Place your video files in a directory named video_assembler


7. Final Video Assembly (final_video_assembler.py)
    Description:
-Merges an audio file with a video file using FFmpeg, and adds subtitles to the video. stored in final_video

    Usage:
-Ensure FFmpeg is installed and accessible from your command line.

8. Subtitle Generation (subtitles.py)
    Description:
-Transcribes audio and generates subtitles using AssemblyAI.

    Usage:
-Ensure you have your AssemblyAI API key in keys.json.
