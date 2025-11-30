FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get upgrade -y && apt-get -y install ffmpeg
COPY ./scainner/ pyproject.toml /code/
WORKDIR /code/

# Bake model into image so you don't redownload every start
ARG WHISPER_MODEL_SIZE=distil-small.en
RUN uv run python -c "from faster_whisper import WhisperModel; WhisperModel('${WHISPER_MODEL_SIZE}')"

CMD [ "uv", "run", "python", "main.py" ]
