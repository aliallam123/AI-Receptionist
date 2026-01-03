import os
from typing import Dict, Any, List

import numpy as np
import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer

# sentence transformer used for embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# label list (kept explicit so it is easy to audit in the report)
INTENT_LABELS: List[str] = [
    "book_hotel",
    "book_restaurant",
    "find_attraction",
    "find_hotel",
    "find_restaurant",
    "find_taxi",
    "find_train",
]

# optional confidence threshold used by server routing
DEFAULT_THRESHOLD = float(os.getenv("INTENT_CONFIDENCE_THRESHOLD", "0.60"))


class IntentClassifier(nn.Module):
    # small feed-forward classifier on top of embeddings
    def __init__(self, num_labels: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(384, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_labels),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def _load_model(weights_path: str) -> IntentClassifier:
    # load weights if present, otherwise return an untrained model so the code is runnable
    model = IntentClassifier(num_labels=len(INTENT_LABELS))
    if os.path.exists(weights_path):
        state = torch.load(weights_path, map_location="cpu")
        model.load_state_dict(state)
    model.eval()
    return model


# global model instance (simple poc pattern)
model = _load_model("intent_classifier_filtered_best.pth")


def is_confident(confidence: float, threshold: float = DEFAULT_THRESHOLD) -> bool:
    # helper used by server to decide if automation is safe
    return confidence >= threshold


def predict_intent(text: str) -> Dict[str, Any]:
    # embed the text
    emb = embedder.encode([text], convert_to_numpy=True)
    x = torch.tensor(emb, dtype=torch.float32)

    # forward pass
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1).numpy()[0]

    # best prediction
    intent_id = int(np.argmax(probs))
    confidence = float(probs[intent_id])
    intent = INTENT_LABELS[intent_id]

    return {
        "intent": intent,
        "confidence": confidence,
        "intent_id": intent_id,
        "probabilities": probs.tolist(),
        "confident": is_confident(confidence),
    }
