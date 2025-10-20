FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    awscli \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py deploy.sh .
COPY ecowitt/ ecowitt/
COPY templates/ templates/
COPY static/ static/

RUN mkdir -p output && \
    chmod -v +x snap.py weathercam.py deploy.sh

ENV PYTHONPATH=/app

CMD ["./deploy.sh"]
