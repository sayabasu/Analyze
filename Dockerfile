FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=9090

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Download the spaCy model referenced by analyzer_service.
RUN python -m spacy download en_core_web_lg

EXPOSE 9090

CMD ["python", "analyzer_service.py"]
