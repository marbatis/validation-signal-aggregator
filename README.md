# validation-signal-aggregator

Dashboard for deterministic validation-readiness scoring across synthetic build signals.

## Overview
Analyzes build/test/field signals and reports confidence, blockers, and weak validation areas.

## Architecture
- Build loader: `app/services/build_loader.py`
- Signal aggregation: `app/services/signal_aggregator.py`
- Confidence scoring: `app/services/confidence_scoring.py`
- Blocker detection: `app/services/blocker_detection.py`
- Reporting: `app/services/analysis_service.py`

## Local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Routes
- `GET /` dashboard
- `GET /build/{build_id}` detail page
- `POST /api/analyze/sample/{build_id}` analyze sample build

## Heroku
`Procfile` and `runtime.txt` included.

## Mock mode
No OpenAI dependency is required.
