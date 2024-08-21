import asyncio
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

VOICES = ['en-US-GuyNeural', 'en-US-JennyNeural']

@app.post("/tts")
async def text_to_speech(text: str, voice: str = VOICES[0]):
    if voice not in VOICES:
        raise HTTPException(status_code=400, detail="Invalid voice")
    
    communicate = edge_tts.Communicate(text, voice)
    audio_stream = io.BytesIO()
    await communicate.stream(audio_stream)
    audio_stream.seek(0)
    
    return StreamingResponse(audio_stream, media_type="audio/mpeg")

@app.get("/")
def read_root():
    return {"message": "TTS API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)