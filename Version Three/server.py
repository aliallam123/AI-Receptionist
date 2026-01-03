import os
import json
from pathlib import Path
from typing import Any, Dict

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response

from intent_model import predict_intent

app = FastAPI()

# random config stuff, no keys here obvs
N8N_CHECK_AVAILABILITY_URL = os.getenv("N8N_CHECK_AVAILABILITY_URL", "")
N8N_BOOK_APPOINTMENT_URL = os.getenv("N8N_BOOK_APPOINTMENT_URL", "")
INTENT_CONFIDENCE_THRESHOLD = float(os.getenv("INTENT_CONFIDENCE_THRESHOLD", "0.60"))

# client config so it looks like multi tenant kinda, not rlly needed but looks pro
CLIENT_FILE = Path(__file__).parent / "Clients" / "client_config.json"
CLIENT_CONFIG: Dict[str, Any] = {}
if CLIENT_FILE.exists():
    CLIENT_CONFIG = json.loads(CLIENT_FILE.read_text(encoding="utf-8"))

# super basic memory, resets every call so dont deep it
conversation_state: Dict[str, Any] = {
    "service": None,
    "date": None,
    "time": None,
    "name": None,
    "contact": None,
    "availability_checked": False,
    "availability_confirmed": False,
    "call_stage": "greeting",
}


def twiml(xml_body: str) -> Response:
    # twilio wants xml so yeah
    xml = f'<?xml version="1.0" encoding="UTF-8"?><Response>{xml_body}</Response>'
    return Response(content=xml, media_type="text/xml")


def say_and_record(prompt: str, max_seconds: int = 8) -> Response:
    # say smth then record what they say back, sends it to /process_recording
    body = (
        f"<Say>{prompt}</Say>"
        f'<Record action="/process_recording" method="POST" maxLength="{max_seconds}" playBeep="true" />'
    )
    return twiml(body)


async def download_recording_bytes(recording_url: str) -> bytes:
    # grabs the audio file from twilio, hope it works lol
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(recording_url)
        r.raise_for_status()
        return r.content


def whisper_transcribe(audio_bytes: bytes) -> str:
    # whisper would go here, but im not putting api keys in github init
    # pretend this is what the caller said
    return "i want to book an appointment next tuesday at 3pm"


async def call_n8n(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # calls a webhook, if url missing just return a fake response
    if not url:
        return {"ok": False, "reason": "no_url_set", "payload": payload}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()

        # sometimes its json sometimes its not, whatever
        if r.headers.get("content-type", "").startswith("application/json"):
            return r.json()
        return {"ok": True}


def route_intent(intent: str, confidence: float) -> Dict[str, str]:
    # confidence thing so we dont do dumb stuff when its unsure
    if confidence < INTENT_CONFIDENCE_THRESHOLD:
        return {
            "action": "fallback",
            "reply": "sorry i didnt catch that, can you say it again",
        }

    # basic routing, probs not perfect but good enough for demo
    if intent in {"book_appointment", "book_restaurant", "book_hotel"}:
        conversation_state["call_stage"] = "collect_datetime"
        return {
            "action": "book",
            "reply": "ok cool, what date and time do you want",
        }

    if intent in {"check_availability", "find_train", "find_taxi"}:
        conversation_state["call_stage"] = "check_availability"
        return {
            "action": "availability",
            "reply": "sure, tell me the date and time and ill check",
        }

    return {
        "action": "fallback",
        "reply": "i can help with booking or checking availability, what do you need",
    }


@app.post("/voice")
async def voice(request: Request):
    # start of call, reset the state so it doesnt get messy
    conversation_state.update(
        {
            "service": None,
            "date": None,
            "time": None,
            "name": None,
            "contact": None,
            "availability_checked": False,
            "availability_confirmed": False,
            "call_stage": "greeting",
        }
    )

    business_name = CLIENT_CONFIG.get("business_name", "our clinic")
    prompt = f"hello, you have reached {business_name}. please say how i can help."
    return say_and_record(prompt, max_seconds=8)


@app.post("/process_recording")
async def process_recording(request: Request):
    # twilio posts form data like RecordingUrl
    form = await request.form()
    recording_url = form.get("RecordingUrl")

    if not recording_url:
        return say_and_record("i didnt get that recording, try again please", max_seconds=8)

    # download -> transcribe (whisper is stubbed)
    audio_bytes = await download_recording_bytes(str(recording_url))
    transcript = whisper_transcribe(audio_bytes).strip().lower()

    # intent model
    pred = predict_intent(transcript)
    intent = pred["intent"]
    confidence = pred["confidence"]

    decision = route_intent(intent=intent, confidence=confidence)

    # only 2 n8n flows for poc, rest is future work
    if decision["action"] == "availability":
        payload = {"transcript": transcript, "client": CLIENT_CONFIG.get("client_id", "demo")}
        await call_n8n(N8N_CHECK_AVAILABILITY_URL, payload)
        return say_and_record("ok i checked, what time works for you", max_seconds=8)

    if decision["action"] == "book":
        payload = {"transcript": transcript, "client": CLIENT_CONFIG.get("client_id", "demo")}
        await call_n8n(N8N_BOOK_APPOINTMENT_URL, payload)
        return twiml("<Say>thanks, your booking request is captured. goodbye.</Say><Hangup/>")

    # fallback loop
    return say_and_record(decision["reply"], max_seconds=8)


if __name__ == "__main__":
    import uvicorn

    # run local, for demo only
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
