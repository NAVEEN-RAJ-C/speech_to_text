# Import necessary libraries
import streamlit as st
from google.cloud import speech_v1p1beta1 as speech
import io
import os
import pyaudio
import wave


# Define function to transcribe audio using Google Cloud Speech-to-Text API
def transcribe_audio(audio_file):
    # Set up Google Cloud Speech-to-Text client
    client = speech.SpeechClient()

    # Read audio file
    with io.open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    # Set up audio configuration
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Perform transcription
    response = client.recognize(request={"config": config, "audio": audio})

    # Extract and return transcribed text
    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript.strip() + " "
    return transcribed_text
