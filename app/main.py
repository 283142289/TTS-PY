from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
import io
import edge_tts

app = FastAPI()

VOICES = ['en-US-GuyNeural', 'en-US-JennyNeural']

@app.post("/tts")
async def text_to_speech(
    text: str = Query(..., description="Text to convert to speech"),
    voice: str = Query(VOICES[0], description="Voice to use for speech synthesis")):
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
