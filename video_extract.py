from moviepy.editor import VideoFileClip
from transformers import pipeline
import torch


# Function to extract audio from video
def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    if audio : 
        video.audio.write_audiofile(audio_path)
        video.close()
        return 1
    return 0

# Function to transcribe audio
def transcribe_audio(audio_path):
    # Load the automatic speech recognition pipeline
    asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")
    # Process the audio file
    transcription = asr(audio_path)
    return transcription['text']

# Function to summarize text
def summarize_text(text):
    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    # Process the text
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Main function to process a video and get a summarized transcript
def video_transcript(video_path):
    audio_path = 'temp_audio.wav'

    # Extract audio from the video
    audio = extract_audio(video_path, audio_path)
    summary = ''
    if audio : 
        # Transcribe the audio to text
        transcript = transcribe_audio(audio_path)

        # Summarize the text
        summary = summarize_text(transcript)

    return summary

