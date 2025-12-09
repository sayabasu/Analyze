# Analyzer Service

This repository exposes a Flask-based Presidio analyzer API. The service supports entity filtering via environment flags and can now be containerized.

## Docker

1. Build the image (from the repo root):
   ```sh
   docker build -t analyzer-service .
   ```

2. Run the image with your `.env` file and required port mappings:
   ```sh
   docker run --env-file .env -p 9090:9090 analyzer-service
   ```

   The container honors `ANALYZER_API_KEY`, entity flags (e.g., `IN_PAN=TRUE`), and listens on the port set in `.env`.

3. Test against the running container:
   ```sh
   curl -X POST http://127.0.0.1:9090/analyze \
     -H "Content-Type: application/json" \
     -H "X-API-Key: changeme123" \
     -d '{"text":"My PAN is ABCDE1234F.","language":"en"}'
   ```

   Adjust `X-API-Key` to match the value specified in your `.env`.

## Docker Compose

Alternatively, build and run the service with Docker Compose:

1. Build and start everything:
   ```sh
   docker compose up --build
   ```

2. Stop services:
   ```sh
   docker compose down
   ```

The Compose file uses the same `.env` variables and exposes port `9090`, so the same curl/PAN tests work once the service is healthy.

## Notes

- The Dockerfile installs `en_core_web_lg` during build; no additional runtime steps are required.
- Keep `.env` outside the image (it's excluded via `.dockerignore`) and pass sensitive flags at runtime via `--env-file`, `docker compose` automatically takes `.env` in repo root unless overridden.
