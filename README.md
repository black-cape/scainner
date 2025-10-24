# Scainner

Sc**ai**nner, pronounced scanner, is a project that applies automatic spreech recognition (ASR) technology to public service radio traffic. [Scanners](https://en.wikipedia.org/wiki/Radio_scanner) are communication receivers that continually scan across many frequencies automatically and emit any transmission they find from it's speaker.
They are often used to listen to police and fire department communications that occur on unencrypted frequencies. There is also a community of people across the world that have deployed [software defined radios](https://en.wikipedia.org/wiki/Software-defined_radio) (SDRs) to record these communications in their communities, and share those recordings on [OpenMHz](https://openmhz.com/). 

OpenMHz has [over a hundred systems](https://openmhz.com/systems) registered with it, including the police and fire departments of many major US cities. This is a of lot AI model training data being exposed for free which could prove useful for training your own models.

This library creates an object to poll OpenMHz's API for new calls at the specified endpoint and uses [fast-whisper](https://github.com/SYSTRAN/faster-whisper) to transcribe the audio to text. Fast-whisper is a fast and efficient reimplematnion of [OpenAI's Whisper model](https://github.com/openai/whisper). 

## Usage

```python
from scainner import Scainner

scainner = Scainner(
        endpoint="https://api.openmhz.com/ffxco/calls", model_size="distil-medium.en", compute_type="int8"
    )
for call in scainner.scan():
    print(call)

```
See `examples/` for additonal example usages.


## Installation

1. This project uses [uv](https://docs.astral.sh/uv/) to manage the environment and dependencies. Install it using it's installer via `curl -LsSf https://astral.sh/uv/install.sh | sh`
1. Run commands in the project environment with `uv run <command>`
    * To run the example, use `uv run python -m examples.fcpd-reston`
1. Add dependencies with `uv add <dependency>`
1. uv manages the virtual environment for you in the `.venv/` directory. If you want to explicitly (re)create it, use `uv venv`. To activate it run `source .venv/bin/activate` in your shell.
1. Install ffmpeg

## Contributing

To contrubute, please follow the guidance in the [governance](https://gitlab.blackcape.dev/black-mesa/governance) documentation. Please also join the `#mesa-scainner` Slack channel.
