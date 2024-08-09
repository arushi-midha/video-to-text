import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
import os

def video_to_audio(video_file, audio_file):
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile(audio_file)

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    transcription = ""
    
    with sr.AudioFile(audio_file) as source:
        total_duration = int(source.DURATION)
        offset = 0
        while offset < total_duration:
            chunk_duration = min(60, total_duration - offset)
            chunk = recognizer.record(source, duration=chunk_duration)
            try:
                text = recognizer.recognize_google(chunk)
                transcription += text + " "
            except sr.UnknownValueError:
                transcription += "[Unrecognized Speech] "
            except sr.RequestError:
                transcription += "[API Error] "
            offset += chunk_duration
    
    return transcription

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

    # Display loading message while transcribing
    with st.spinner("Transcribing audio..."):
        transcription = audio_to_text(audio_path)

    st.success("Audio transcribed to text.")

    # Display the transcribed text
    st.text_area("Transcribed Text", transcription, height=200)

    # Provide an option to download the transcription
    st.download_button(
        label="Download Transcription as Text File",
        data=transcription,
        file_name="transcription.txt",
        mime="text/plain"
    )

# Footer section
footer = """<style>
a:link , a:visited{
color: white;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: lavender;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: grey;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p> </p>
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://github.com/arushi-midha" target="_blank">Arushi Midha</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
