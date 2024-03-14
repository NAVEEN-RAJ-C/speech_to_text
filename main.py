# Import necessary libraries
import streamlit as st
import vosk
import sys
import os
import pyaudio


# Define function to transcribe speech to text using Vosk
def transcribe_audio(audio):
    # Initialize Vosk recognizer
    model = vosk.Model("D:/CNR/GUVI_ZEN_DS/Projects/speech_to_text/vosk-model-en-us-0.22-lgraph")  # "model_folder_path"
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Process audio in chunks
    while True:
        data = audio.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            st.write(result)


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

            # Call function to transcribe audio
            transcribe_audio(stream)

            # Close audio stream
            stream.stop_stream()
            stream.close()

    # Close PyAudio instance
    p.terminate()


# Run main function
if __name__ == "__main__":
    main()
