import http.client
import os
import json
from script_splitter import split_script_into_sentences  

API_KEY = 'sk_ad6eec1573af2f91fd3e7e0debe349887a6d557bbfdd0552'

voices = [
    {"voice_id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam", "attributes": ["pleasant"]},
    {"voice_id": "MF3mGyEYCl7XYWbV9V6O", "name": "Jessi", "attributes": ["confident", "casual", "pleasant"]},
    {"voice_id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "attributes": ["serious"]},
]

def select_voice(humour_level, creativity_level):
    if humour_level > 5:
        desired_attribute = "casual"
    elif creativity_level > 7:
        desired_attribute = "confident"
    else:
        desired_attribute = "serious"
    
    for voice in voices:
        if desired_attribute in voice['attributes']:
            return voice['voice_id']
    return voices[0]['voice_id']

def generate_speech(api_key, text, voice_id, output_filename):
    conn = http.client.HTTPSConnection("api.elevenlabs.io")
    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    payload = json.dumps({
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_id": voice_id
    })

    url = f"/v1/text-to-speech/{voice_id}?optimize_streaming_latency=0"
    conn.request("POST", url, headers=headers, body=payload)
    response = conn.getresponse()
    
    if response.status == 200:
        with open(f"{output_filename}.mp3", "wb") as file:
            file.write(response.read())
    else:
        print(f"Failed to generate speech: {response.reason} - {response.read().decode()}")

    conn.close()

def generate_full_speech(script, humour_level, creativity_level, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    voice_id = select_voice(humour_level, creativity_level)
    generate_speech(API_KEY, script, voice_id, os.path.join(output_folder, "full_script"))

def generate_speech_for_script(script_segments, humour_level, creativity_level, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    voice_id = select_voice(humour_level, creativity_level)

    for i, segment in enumerate(script_segments):
        output_path = os.path.join(output_folder, f"segment_{i}")
        generate_speech(API_KEY, segment, voice_id, output_path)

# Example usage
if __name__ == "__main__":
    script_text = """Artificial Intelligence (AI) is a broad branch of computer science that focuses on creating machines that can mimic human intelligence and perform complex tasks. AI enables computers to utilise advanced functions such as understanding spoken and written language, analysing data, making recommendations, and more.

One example of how AI is used is in optical character recognition (OCR). OCR uses AI to extract text and data from images and documents, turning unstructured content into structured data, and unlocking valuable insights. This is possible because AI can see and understand the text within images and documents, just like humans. This is accomplished with technologies like Convolutional Neural Networks (CNNs), and Recurrent Neural Networks (RNNs) which are modelled on the human brain and nervous system.

There are several applications of AI including agriculture, astronomy, governance, and many more. In agriculture, AI helps optimise various farming practices by analysing data and forecasting trends. In astronomy, AI enables scientists to analyse significant amounts of data, helping to discover new scientific insights.

AI can also be used for more sinister purposes. AI is exploited by authoritarian governments to control their citizens through facial and voice recognition techniques, enabling surveillance. This form of AI is also used to classify individuals as potential enemies of the state, targeting them with propaganda and misinformation.

Overall, AI is a set of technologies that allow computers to perform a variety of advanced functions, demonstrating intelligent behaviour to maximise the chances of achieving defined goals.

Remember, AI is all around us, from the personalised recommendations on Netflix to the interactive conversations with Google Assistant. Exciting advancements in AI are happening daily, and the future of this technology is limitless."""
    
    segments = split_script_into_sentences(script_text)
    
    # Generate full speech
    generate_full_speech(script_text, humour_level=4, creativity_level=6, output_folder="Storage_layer/media/full_audio")
    # Generate segmented speech
