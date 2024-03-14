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


# Define main function
def main():
    # Set up Streamlit UI
    st.title("Speech-to-Text Web Application")

    # Initialize PyAudio for audio capture
    p = pyaudio.PyAudio()

    # Capture audio from microphone
    st.write("Click below to start recording:")
    if st.button("Start Recording"):
        with st.spinner("Recording..."):
            # Set up audio stream
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            frames = []

            # Capture audio data in chunks
            for i in range(0, int(16000 / 8000 * 5)):  # Capture audio for 5 seconds
                data = stream.read(8000)
                frames.append(data)

            # Save captured audio to WAV file
            audio_file_path = "audio.wav"
            with wave.open(audio_file_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                wf.setframerate(16000)
                wf.writeframes(b"".join(frames))

            # Close audio stream
            stream.stop_stream()
            stream.close()

            # Call function to transcribe audio
            transcribed_text = transcribe_audio(audio_file_path)

            # Display transcribed text
            st.write("Transcribed Text:")
            st.write(transcribed_text)

    # Close PyAudio instance
    p.terminate()


# Run main function
if __name__ == "__main__":
    main()
