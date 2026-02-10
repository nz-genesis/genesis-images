from fastapi import FastAPI, HTTPException

app = FastAPI(title="Intent Adapter", version="0.1.0")

@app.post("/intent")
async def ingest_intent(payload: dict):
    # Phase 3.3 stub:
    # Validate shape minimally; do not decide, do not execute.
    # Return a placeholder canonical INTENT or a clear rejection.
    if not payload:
        raise HTTPException(status_code=400, detail="Empty payload")

    return {
        "status": "accepted",
        "intent": {
            "schema": "INTENT",
            "note": "Phase 3.3 stub — normalization only"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
