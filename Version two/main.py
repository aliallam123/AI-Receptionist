from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/voice")
async def voice(request: Request):
    twiml = """
    <Response>
        <Say voice="alice">Hello, thanks for calling. This is your AI receptionist.</Say>
    </Response>
    """
    return PlainTextResponse(twiml, media_type="application/xml")
