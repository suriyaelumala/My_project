from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import azure.cognitiveservices.speech as speechsdk
import PyPDF2  # Corrected: Capitalized 'P' and 'PDF'
import io
import os
import uuid
from typing import Optional

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Speech Config (replace with your keys)
speech_key = "YOUR_AZURE_SPEECH_KEY"
service_region = "YOUR_AZURE_REGION"

# Temporary storage
audio_files = {}

@app.post("/api/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed.")
    content = await file.read()
    pdf = PyPDF2.PdfReader(io.BytesIO(content))  # Corrected: Capitalized reference
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return {"text": text.strip()}

@app.post("/api/synthesize")
async def synthesize(data: dict):
    text = data.get("text", "")
    accent = data.get("accent", "en-US")
    format_ = data.get("format", "mp3")
    
    # Configure speech synthesis
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_output_format = speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3 if format_ == "mp3" else speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    
    # Accent handling
    if accent == "en-US":
        speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
    elif accent == "en-GB":
        speech_config.speech_synthesis_voice_name = "en-GB-SoniaNeural"
    elif accent == "tamil":
        text = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US"><voice name="en-US-AriaNeural"><prosody rate="medium">{text.replace("a", "<phoneme alphabet=\"ipa\" ph=\"ɑ\">a</phoneme>")}</prosody></voice></speak>'
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    elif accent == "slang":
        speech_config.speech_synthesis_voice_name = "en-US-ZiraNeural"
        text = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US"><voice name="en-US-ZiraNeural"><prosody pitch="low" rate="fast">{text}</prosody></voice></speak>'
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_id = str(uuid.uuid4())
        audio_files[audio_id] = result.audio_data
        return {"audioUrl": f"/api/download/{audio_id}"}
    else:
        raise HTTPException(status_code=500, detail="TTS failed.")

@app.get("/api/download/{audio_id}")
async def download_audio(audio_id: str):
    if audio_id not in audio_files:
        raise HTTPException(status_code=404, detail="Audio not found.")
    audio_data = audio_files.pop(audio_id)
    return FileResponse(io.BytesIO(audio_data), media_type="audio/mpeg", filename="speech.mp3")
