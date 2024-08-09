import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
import os

def video_to_audio(video_file, audio_file):
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile(audio_file)

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.RequestError:
            return "API unavailable"
        except sr.UnknownValueError:
            return "Unable to recognize speech"

st.title("Video to Text Converter")
st.write("Upload a video file and get the transcribed text.")

uploaded_video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

if uploaded_video is not None:
    video_path = os.path.join(uploaded_video.name)
    audio_path = os.path.splitext(video_path)[0] + ".wav"

    # Save the uploaded video file
    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    # Convert video to audio
    video_to_audio(video_path, audio_path)
    st.success("Audio extracted from video.")

    # Convert audio to text
    transcription = audio_to_text(audio_path)
    st.success("Audio transcribed to text.")

    # Display the transcribed text
    st.text_area("Transcribed Text", transcription, height=200)

    # Clean up temporary files
    os.remove(video_path)
    os.remove(audio_path)
