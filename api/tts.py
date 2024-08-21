from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import edge_tts
import io

app = FastAPI()

VOICES = ['en-US-GuyNeural', 'en-US-JennyNeural']

@app.post("/api/tts")
async def text_to_speech(text: str, voice: str = VOICES[0]):
    if voice not in VOICES:
        raise HTTPException(status_code=400, detail="Invalid voice")
    
    communicate = edge_tts.Communicate(text, voice)
    audio_stream = io.BytesIO()
    await communicate.stream(audio_stream)
    audio_stream.seek(0)
    
    return Response(content=audio_stream.getvalue(), media_type="audio/mpeg")

# Vercel requires a module-level app variable
from mangum import Mangum
handler = Mangum(app)