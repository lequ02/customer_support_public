import assemblyai as aai

def transcribe_audio(audio_file_path):
    aai.settings.api_key = "***********"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)
    return transcript.text