import os
import requests
import random
from moviepy.editor import VideoFileClip
from pydub.utils import mediainfo

# Replace with your Pexels API key
PEXELS_API_KEY = "QPtwzcsThFYddfaJALK8gQBS0kKoEpU5gRMNb9fGtpGfFrKbXKfggWYU"
PEXELS_API_URL = "https://api.pexels.com/videos/search"

def pexels_search(query, per_page=15, orientation='landscape', sizes=['medium', 'large', 'small']):
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    for size in sizes:
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": orientation,
            "size": size
        }
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        if response.status_code == 200:
            videos = response.json().get('videos', [])
            if videos:
                return videos
        else:
            print(f"Error: {response.status_code} for size {size}")
    return []

def download_and_trim_video(video_url, save_path, filename, duration):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        video_file_path = os.path.join(save_path, f"temp_{filename}")
        with open(video_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        # Trim the video
        with VideoFileClip(video_file_path) as clip:
            if clip.duration < 3:  # Filter out videos shorter than 3 seconds
                os.remove(video_file_path)
                return None
            
            end_time = min(clip.duration, duration)
            trimmed_clip = clip.subclip(0, end_time)
            trimmed_video_path = os.path.join(save_path, filename)
            trimmed_clip.write_videofile(trimmed_video_path, codec='libx264')
        
        # Remove the original downloaded file
        os.remove(video_file_path)
        
        print(f"Trimmed and saved: {trimmed_video_path}")
        return trimmed_video_path
    else:
        print(f"Error downloading video: {response.status_code}")
        return None

def distribute_durations(total_duration, num_queries, min_duration=4, max_duration=6):
    total_duration = int(total_duration)  # Convert to integer
    base_duration = total_duration // num_queries
    remainder = total_duration % num_queries

    query_durations = [base_duration] * num_queries
    for i in range(remainder):
        query_durations[i] += 1

    all_durations = []
    for query_duration in query_durations:
        segment_durations = []
        while query_duration > 0:
            duration = min(random.uniform(min_duration, max_duration), query_duration)
            segment_durations.append(duration)
            query_duration -= duration
        all_durations.append(segment_durations)
    return all_durations

def calculate_audio_duration(audio_path):
    info = mediainfo(audio_path)
    return float(info['duration'])

def download_and_trim_videos_from_queries(queries, save_path, total_duration):
    os.makedirs(save_path, exist_ok=True)
    downloaded_video_ids = set()
    video_counter = 1

    num_queries = len(queries)
    all_durations = distribute_durations(total_duration, num_queries)
    
    for query, segment_durations in zip(queries, all_durations):
        print(f"Searching for: {query}")
        videos = pexels_search(query, per_page=30, orientation='landscape')  # Try different sizes
        
        if not videos:
            print(f"No relevant videos found for query: {query}. Retrying with less relevance.\n")
            videos = pexels_search(query, per_page=50, orientation='landscape', sizes=['small', 'medium', 'large'])
        
        if not videos:
            print(f"No relevant videos found for query: {query}. Skipping to the next query.\n")
            continue
        
        for duration in segment_durations:
            video_found = False
            for video in videos:
                video_id = video['id']
                if video_id in downloaded_video_ids:
                    continue
                
                video_url = video['video_files'][0]['link']
                filename = f"{video_counter}.mp4"
                trimmed_video_file = download_and_trim_video(video_url, save_path, filename, duration)
                
                if trimmed_video_file:
                    downloaded_video_ids.add(video_id)
                    print(f"Processed: {trimmed_video_file}\n")
                    video_counter += 1
                    video_found = True
                    break  # Move to the next duration segment
            
            if not video_found:
                print(f"No video processed for duration: {duration}. Trying less relevant options.\n")
                videos = pexels_search(query, per_page=50, orientation='landscape', sizes=['small', 'medium', 'large'])
                for video in videos:
                    video_id = video['id']
                    if video_id in downloaded_video_ids:
                        continue
                    video_url = video['video_files'][0]['link']
                    filename = f"{video_counter}.mp4"
                    trimmed_video_file = download_and_trim_video(video_url, save_path, filename, duration)
                    if trimmed_video_file:
                        downloaded_video_ids.add(video_id)
                        print(f"Processed: {trimmed_video_file}\n")
                        video_counter += 1
                        break  # Move to the next duration segment

    # Check if total duration is met, if not, redistribute remaining durations
    downloaded_videos = [os.path.join(save_path, f) for f in os.listdir(save_path) if f.endswith('.mp4')]
    current_duration = sum([VideoFileClip(video).duration for video in downloaded_videos])
    
    if current_duration < total_duration:
        remaining_duration = total_duration - current_duration
        additional_durations = distribute_durations(remaining_duration, len(downloaded_videos))
        
        for video_path, additional_duration in zip(downloaded_videos, additional_durations):
            with VideoFileClip(video_path) as clip:
                end_time = min(clip.duration + additional_duration, clip.duration)
                trimmed_clip = clip.subclip(0, end_time)
                trimmed_clip.write_videofile(video_path, codec='libx264')
                print(f"Extended and saved: {video_path}")

if __name__ == "__main__":
    queries = [
        "Artificial Intelligence Computer Science Machine Intelligence",
        "Advanced AI Functions Spoken Language, Data Analysis, Recommendations",
        "AI Optical Character Recognition Software",
        "SOCR AI Extract Text Data Image Documents",
        "AI Understanding Text Images Documents",
        "Neural Networks (CNN, RNN) in AI",
        "Applications of AI Agriculture Astronomy Governance",
        "AI Optimising Farming Practices Data Forecasting",
        "AI Astronomy Scientific Data Analysis  Discovery  Scientific  Insights  Discoveries",
        "Sinister AI Surveillance Spy Tech Threat Tracker",
        "Exploited AI Facial Recognition Control Citizens Surveillance",
        "AI Targeting Propaganda Enemies State",
        "AI Computer Advanced Functions Intelligent Behaviour",
        "AI Technology Examples Netflix Recommendations Google Assistant",
        "AI Advances Robotics Futuristic Technology"
    ]

    audio_path = "Storage_layer/media/full_audio/full_script.mp3"  
    total_duration = calculate_audio_duration(audio_path)
    
    save_path = "Storage_layer/media/video_chunks"
    download_and_trim_videos_from_queries(queries, save_path, total_duration)
