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

### 1) create a virtual environment
```bash
python -m venv .venv
```
Windows:
.venv\Scripts\activate

Mac/Linux:

source .venv/bin/activate
