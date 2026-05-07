# youtube-timestamper

A lightweight CLI tool to fetch and manage YouTube video transcripts with accurate timestamps.

## Key Features

- Fetch transcripts from any YouTube video (URL or ID)
- Extracts accurate timestamped segments (start time and text)
- JSON output for easy integration with other tools/scripts
- Automatic language detection (English fallback)

## Tech Stack

- **Language**: Python 3.10+
- **Transcript API**: `youtube-transcript-api`

## Prerequisites

- Python 3.10 or higher
- `pip`

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-timestamper.git
cd youtube-timestamper
```

### 2. Install Dependencies

```bash
pip install youtube-transcript-api
```

### 3. Usage

The main entry point is `scripts/fetch_transcript.py`.

#### Fetch a Transcript

To fetch the transcript for a video (as a JSON array of segments):

```bash
python3 scripts/fetch_transcript.py <video_url_or_id>
```

Example output:
```json
{
  "segments": [
    {"start": 0.0, "text": "Hello world."},
    {"start": 2.5, "text": "This is a transcript."}
  ],
  "language": "en",
  "video_id": "dQw4w9WgXcQ"
}
```

#### Specify Language

To request a specific language (e.g., Spanish):

```bash
python3 scripts/fetch_transcript.py <video_url_or_id> --lang es
```

## Architecture

- **`scripts/fetch_transcript.py`**: The core utility script.
    - Handles input parsing for both full URLs and raw video IDs.
    - Uses `youtube-transcript-api` to interact with YouTube.
    - Formats output as JSON for stdout.
    - Gracefully handles common YouTube errors (disabled transcripts, unavailable videos).

## Troubleshooting

### Error: `youtube-transcript-api not installed`

**Solution:**
Ensure the dependency is installed in your current environment:
```bash
pip install youtube-transcript-api
```

### Error: Transcripts are disabled

**Solution:**
The video does not have transcript data enabled. You will need to transcribe this video manually or use a different source.

### Error: No transcript found

**Solution:**
The video does not have a transcript available in the requested language (or the default English). Try running without the `--lang` flag to grab the first available language.

## License

MIT
