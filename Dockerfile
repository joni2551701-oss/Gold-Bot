# GoldBot v0.3 — Docker foundation (Phase 56).
#
# Not required for the current deployment (GitHub Actions runs
# main.py on a schedule; telegram/polling.py runs directly on a VPS
# per docs/DEPLOYMENT.md). This exists as a ready foundation for a
# future containerized deployment -- no trading/strategy/AI/risk logic
# is touched by this file, it only packages the existing, unmodified
# application.
#
# Build:  docker build -t goldbot .
# Run (trading pipeline, one-shot):
#   docker run --env-file .env goldbot python main.py
# Run (Telegram polling, long-running):
#   docker run --env-file .env goldbot python -m telegram.polling

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# database/goldbot.db is written at runtime -- mount a volume over
# /app/database if persistence across container restarts is required;
# see docs/DEPLOYMENT.md's Backup section.

CMD ["python", "main.py"]
