import base64
import json
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):
    await websocket.accept()
    print("Client connected from Twilio Media Stream")

    while True:
        try:
            data = await websocket.receive_text()
            event = json.loads(data)

            event_type = event.get("event")

            # When audio starts
            if event_type == "start":
                print("Stream started")
            
            # Incoming raw audio chunk
            elif event_type == "media":
                audio_base64 = event["media"]["payload"]
                audio_bytes = base64.b64decode(audio_base64)

                # For now, just confirm receipt
                print(f"Received audio chunk, size = {len(audio_bytes)} bytes")

                # Whisper integration will go here in Step D

            # When Twilio stops streaming
            elif event_type == "stop":
                print("Stream stopped")
                break

        except Exception as e:
            print("Error:", e)
            break

    await websocket.close()
    print("Connection closed")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
