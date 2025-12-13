from fastapi import FastAPI
from pydantic import BaseModel
import requests
import vertexai
from vertexai.preview.generative_models import GenerativeModel

#region as london for gdpr compliance
vertexai.init(project="ai-receptionist-480219", location="europe-west2")
model = GenerativeModel("gemini-1.5-flash-001")

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    message: str

# X'd out my cloud run apps
CHECK_AVAILABILITY_URL = "https://check-availability-XXXXXX.europe-west2.run.app"
BOOK_APPOINTMENT_URL = "https://book-appointment-XXXXX.europe-west2.run.app"
SEND_MESSAGE_URL = "https://send-message-XXXXX.europe-west2.run.app"


# In memory session store (temp)
sessions = {}


def classify_intent(text: str) -> str:
    prompt = f"""
Classify the user's intent into ONE label.
Return only the label. No explanation.

Labels:
booking_request
availability_question
faq_question
message_request
unclear

Rules:
- booking_request only if user wants to proceed now
- if user asks questions before booking, use faq_question
- if unsure, use unclear

User message:
{text}
"""
    response = model.generate_content(prompt)
    return response.text.strip().lower()


@app.post("/chat")
def chat(req: ChatRequest):
    # Initialise session
    if req.session_id not in sessions:
        sessions[req.session_id] = {
            "state": "initial",
            "context": {}
        }

    session = sessions[req.session_id]

    try:
        intent = classify_intent(req.message)

        valid_intents = {
            "booking_request",
            "availability_question",
            "faq_question",
            "message_request",
            "unclear",
        }

        if intent not in valid_intents:
            intent = "unclear"

        # Intent handling
        if intent == "faq_question":
            session["state"] = "answering_faq"
            return {"reply": "Sure. What would you like to know?"}

        if intent == "availability_question":
            session["state"] = "checking_availability"
            return {"reply": "I can help with availability. What day are you looking for?"}

        if intent == "booking_request":
            session["state"] = "booking_in_progress"
            return {"reply": "Great. What day and time would you like to book?"}

        if intent == "message_request":
            requests.post(
                SEND_MESSAGE_URL,
                json={"target": "business", "message": req.message},
                timeout=5
            )
            session["state"] = "message_sent"
            return {"reply": "Your message has been sent."}

        return {"reply": "I can help with bookings, availability, or questions."}

    except requests.RequestException:
        return {"reply": "I can't reach the booking system right now. Please try again shortly."}

    except Exception as e:
        print(f"Session {req.session_id} error: {e}")
        return {"reply": "Something went wrong. Please start again."}
