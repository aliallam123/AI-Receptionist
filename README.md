# AI Receptionist (Strategic Digital Leadership Final Project)

This repository contains my Strategic Digital Leadership final project: a proof-of-concept (PoC) AI receptionist for UK SMEs (demo vertical: dental clinic). The PoC focuses on confidence-calibrated intent handling and two downstream workflows (availability check + booking) triggered via n8n.

## What this project demonstrates
- inbound call handling (Twilio-style webhook flow in the PoC scaffolding)
- speech-to-text (Whisper in the working PoC, stubbed in the public repo where needed)
- intent classification with confidence scoring
- confidence-aware routing (proceed vs fallback for low-confidence inputs)
- workflow orchestration via n8n webhooks:
  - check availability
  - book appointment
- clear V1 → V2 → V3 design evolution (version control evidence)

## Repository structure
- `Version One/`  
  early rapid prototype (media stream scaffold, minimal logic)  
- `Version Two/`  
  GCP exploration / alternative build attempt (experiments and tests)  
- `Version Three/`  
  final PoC snapshot aligned to the report (intent classifier + confidence routing + n8n stubs + requirements)  
- `Report/`  
  final written report submission artefact  
- `Presentation/`  
  presentation and demo materials  
- `Machine Learning Workflow/`  
  training and evaluation artefacts for the intent classifier  
- `results (iterations)/`, `data/`, `multi_woz_v22/`  
  datasets, runs, and outputs used during development  

## Quick start (Version Three)

## 1) create a virtual environment
```bash
python -m venv .venv
```
Windows:
`.venv\Scripts\activate`

Mac/Linux:

`source .venv/bin/activate`

## 2) install dependencies
`pip install -r "Version Three/requirements.txt"`

## 3) set environment variables (no secrets committed)

Required:
`N8N_CHECK_AVAILABILITY_URL`
`N8N_BOOK_APPOINTMENT_URL`

Optional:
`INTENT_CONFIDENCE_THRESHOLD (default: 0.60)`

Windows PowerShell example:
`$env:N8N_CHECK_AVAILABILITY_URL="https://example.com/webhook/check"`
`$env:N8N_BOOK_APPOINTMENT_URL="https://example.com/webhook/book"`
`$env:INTENT_CONFIDENCE_THRESHOLD="0.60"`

Mac/Linux example:
`export N8N_CHECK_AVAILABILITY_URL="https://example.com/webhook/check"`
`export N8N_BOOK_APPOINTMENT_URL="https://example.com/webhook/book"`
`export INTENT_CONFIDENCE_THRESHOLD="0.60"`

## 4) run the api
From the Version Three/ folder:
`uvicorn server:app --host 0.0.0.0 --port 8000 --reload`

## Notes about the public repo
credentials and API keys are never committed
some integrations are intentionally stubbed in the public version (e.g., whisper/TTS calls) to keep the repo safe to share
this repo’s main purpose is to evidence design iteration, architecture decisions, and version control aligned to the report

## High-level call flow
inbound call hits /voice
caller speech is captured and transcribed (whisper in working PoC)
transcript is passed into the intent classifier to return intent + confidence
confidence routing decides: proceed vs fallback prompt
if applicable, one of two n8n workflows is triggered: availability check or booking request

## License
Educational use only (university module submission). No production warranty.

