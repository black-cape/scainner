# ScAInner

Sc**AI**nner, pronounced scanner, is a project that applies automatic spreech recognition (ASR) technology to public service radio traffic. [Scanners](https://en.wikipedia.org/wiki/Radio_scanner) are communication receivers that continually scan across many frequencies automatically and emit any transmission they find from it's speaker.
They are often used to listen to police and fire department communications that occur on unencrypted frequencies. There is also a community of people across the world that have deployed [software defined radios](https://en.wikipedia.org/wiki/Software-defined_radio) (SDRs) to record these communications in their communities, and share those recordings on [OpenMHz](https://openmhz.com/). 

OpenMHz has [over a hundred systems](https://openmhz.com/systems) registered with it, including the police and fire departments of many major US cities. 

This project polls OpenMHz's API for new calls at the specified endpoint and uses [fast-whisper](https://github.com/SYSTRAN/faster-whisper) to transcribe the audio to text. Fast-whisper is a fast and efficient reimplematnion of [OpenAI's Whisper model](https://github.com/openai/whisper). 

## Usage

You can configure `ScAInner` with several environment variables to control its behavior:

- `ENDPOINT`: The OpenMHz API endpoint to poll for calls.
- `SLACK_WEBHOOK_URL`: If provided, allows the app to send call notifications to a Slack channel via webhook. Optional.
- `FETCH_INTERVAL`: How many seconds to wait between each poll for new calls. Defaults to 60 seconds.
- `WHISPER_MODEL_SIZE`: The Whisper model to use for transcription (e.g., `distil-small.en`, `distil-large-v3`). Controls speed and accuracy.
- `WHISPER_COMPUTE_TYPE`: Set the computation type for fast-whisper (e.g., `int8`, `float16`, or `default`).
- `MONGO_DB_HOSTNAME`, `MONGO_DB_PORT`, `MONGO_DB_NAME`: If you are using database logging, these define the connection to MongoDB.
    - To not database calls, do not set `MONGO_DB_HOSTNAME` in your `.env`.
- `NOTIFICATION_PATTERNS`: Python regex patterns that specify which calls should trigger notifications. These should be delimiated by `&&&`
  - If `SLACK_WEBHOOK_URL` is set and this is not, all calls will trigger notifications.

Copy `example.env` and adjust variables as desired.

Once your `.env` is configured, you can bring up ScAInner and MongoDB with `docker compose up`.

## Installation

1. This project uses [uv](https://docs.astral.sh/uv/) to manage the environment and dependencies. Install it using it's installer via `curl -LsSf https://astral.sh/uv/install.sh | sh`
1. Run commands in the project environment with `uv run <command>`
    * To run the example, use `uv run python -m examples.fcpd-reston`
1. Add dependencies with `uv add <dependency>`
1. uv manages the virtual environment for you in the `.venv/` directory. If you want to explicitly (re)create it, use `uv venv`. To activate it run `source .venv/bin/activate` in your shell.
  1. Use `uv sync` to install dependencies in a fresh venv.
1. Install ffmpeg
