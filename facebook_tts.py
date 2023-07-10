import facebook
from google.cloud import texttospeech
import os
import re

# Set up Facebook Graph API
graph = facebook.GraphAPI(access_token="YOUR_ACCESS_TOKEN", version="3.0")

# Set up Google Cloud Text-to-Speech API
client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Define regular expression to extract text from Facebook posts
regex = re.compile('<.*?>')

# Define function to convert text to speech and save as MP3 file
def convert_to_audio(text, filename):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'TTS MP3 file saved: {filename}')

# Get all text posts from the WhitehorseAnonymous Facebook page
posts = graph.get_connections("WhitehorseAnonymous", "posts", fields="message")

# Loop through each post and convert to TTS MP3 file
for post in posts["data"]:
    if "message" in post:
        # Remove HTML tags from post message
        text = regex.sub('', post["message"])
        # Set filename to post ID
        filename = f"{post['id']}.mp3"
        # Convert text to speech and save as MP3 file
        convert_to_audio(text, filename)
