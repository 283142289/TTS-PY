import uvicorn
import edge_tts
import asyncio
import os
from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

@app.post("/api/tts")
async def post_data(text: str = Body('', title='文本', embed=True),
                    voice: str = Body('', title='语言参数', embed=True),
                    name: str = Body('', title='文件名', embed=True),
                    rate: str = Body('', title='速度', embed=True),
                    volume: str = Body('', title='音量', embed=True)):
    # Use the current directory to save the file
    output = os.path.join(os.getcwd(), f"{name}.mp3")
    tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
    await tts.save(output)
    return {"message": output}

@app.get("/")
async def root():
    return {"message": "Welcome to the TTS API"}

@app.get("/play/{filename}")
async def play_audio(filename: str):
    file_path = os.path.join(os.getcwd(), f"{filename}.mp3")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return an HTML page with an audio player
    html_content = f"""
    <html>
        <head>
            <title>Play {filename}</title>
        </head>
        <body>
            <h1>Playing {filename}.mp3</h1>
            <audio controls autoplay>
                <source src="https://arena.lmsys.orgfiles/{filename}.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/files/{filename}")
async def get_audio_file(filename: str):
    file_path = os.path.join(os.getcwd(), filename)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
