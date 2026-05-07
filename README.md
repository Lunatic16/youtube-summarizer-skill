# YouTube Timestamper

Generate accurate, chapter-style timestamps for YouTube videos by fetching real transcripts and grouping them into meaningful sections. Use this when you need timestamps for YouTube descriptions, table of contents, or to quickly understand what happens at specific points in a video.

## Key Features

- Fetches real YouTube transcripts with second-level precision
- Automatic language detection with fallback (requested → English → first available)
- Groups transcript segments into logical chapters based on topic boundaries
- Outputs timestamps in YouTube-compatible format (`M:SS` or `H:MM:SS`)
- Handles error cases gracefully (private videos, disabled transcripts, etc.)

## Tech Stack

- **Language**: Python 3.7+
- **Dependency**: `youtube-transcript-api`
- **Output Format**: JSON (segments with start times and text)

## Prerequisites

- Python 3.7 or higher
- `pip` or `pipx` for package installation
- Internet access (to fetch transcripts from YouTube)

## Getting Started

### 1. Clone or Navigate to the Project

```bash
cd /path/to/youtube-timestamper
```

### 2. Install the Dependency

The script auto-installs `youtube-transcript-api` if missing. For manual installation:

```bash
pip install youtube-transcript-api --break-system-packages
```

On some systems, you may need to use `--user` flag or a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install youtube-transcript-api
```

### 3. Run the Script

```bash
python scripts/fetch_transcript.py <video_id_or_url> [--lang en]
```

**Examples:**

```bash
# Using video ID
python scripts/fetch_transcript.py dQw4w9WgXcQ

# Using full URL
python scripts/fetch_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Using short URL
python scripts/fetch_transcript.py "https://youtu.be/dQw4w9WgXcQ"

# With language preference
python scripts/fetch_transcript.py "https://youtu.be/dQw4w9WgXcQ" --lang es
```

## Architecture

### Directory Structure

```
youtube-timestamper/
├── scripts/
│   └── fetch_transcript.py    # Main transcript fetching script
├── youtube-timestamper.skill  # Skill definition (workflow instructions)
├── SKILL.md                   # Skill package documentation
├── CLAUDE.md                  # Claude Code guidance
└── README.md                  # This file
```

### How It Works

1. **URL Parsing**: The script extracts the 11-character YouTube video ID from various URL formats (standard, short, embed, shorts).

2. **Transcript Fetching**: Uses `youtube-transcript-api` to fetch transcript data:
   - Checks for transcript availability
   - Prefers requested language, then English, then first available
   - Falls back to auto-generated captions if needed

3. **Output Format**: Returns JSON with one of two structures:

**Success:**
```json
{
  "segments": [
    {"start": 0.0, "text": "Welcome to the video"},
    {"start": 4.2, "text": "Today we're going to learn about..."},
    {"start": 8.5, "text": "Let's get started"}
  ],
  "language": "en",
  "video_id": "dQw4w9WgXcQ"
}
```

**Error:**
```json
{
  "error": "Transcripts are disabled for this video."
}
```

### Video ID Extraction Patterns

The script supports multiple input formats:

| Input Format | Example | Extracted ID |
|--------------|---------|--------------|
| Standard URL | `youtube.com/watch?v=ABC123` | `ABC123` |
| Short URL | `youtu.be/ABC123` | `ABC123` |
| Embed URL | `youtube.com/embed/ABC123` | `ABC123` |
| Shorts URL | `youtube.com/shorts/ABC123` | `ABC123` |
| Raw ID | `ABC123` | `ABC123` |

### Error Handling

| Error Type | Cause | User Action |
|------------|-------|-------------|
| `TranscriptsDisabled` | Video owner disabled captions | Ask user to paste transcript manually |
| `VideoUnavailable` | Video is private, deleted, or age-restricted | Cannot fetch; video is inaccessible |
| `NoTranscriptFound` | No transcript in requested language | Try without `--lang` flag |
| `ImportError` | `youtube-transcript-api` not installed | Script auto-installs; retry |

## Available Scripts

| Command | Description |
|---------|-------------|
| `python scripts/fetch_transcript.py <id>` | Fetch transcript as JSON |
| `python scripts/fetch_transcript.py <url> --lang en` | Fetch with language preference |

## Environment Variables

No environment variables required. The script runs with default Python installation.

Optional system configuration:

| Variable | Description |
|----------|-------------|
| `PYTHONPATH` | Add to path if running from external location |
| `HTTPS_PROXY` | Set proxy if required by network |

## Deployment

### Local Development

1. Install Python 3.7+
2. Install dependency: `pip install youtube-transcript-api`
3. Run: `python scripts/fetch_transcript.py <video_id>`

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY scripts/ scripts/
RUN pip install youtube-transcript-api

CMD ["python", "scripts/fetch_transcript.py", "VIDEO_ID"]
```

Build and run:

```bash
docker build -t youtube-timestamper .
docker run youtube-timestamper python scripts/fetch_transcript.py dQw4w9WgXcQ
```

### Serverless (AWS Lambda / Cloud Functions)

Package the script with dependencies:

```bash
# Create deployment package
pip install youtube-transcript-api -t ./package
cp scripts/fetch_transcript.py ./package/
cd package && zip -r ../timestamper.zip . && cd ..
```

Handler function:

```python
import json
from fetch_transcript import fetch_transcript, extract_video_id

def lambda_handler(event, context):
    video_id = extract_video_id(event.get('video_id'))
    result = fetch_transcript(video_id)
    return {'statusCode': 200, 'body': json.dumps(result)}
```

## Testing

### Manual Testing

Test with known video IDs:

```bash
# Should return segments
python scripts/fetch_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Should return error (private video)
python scripts/fetch_transcript.py "private_video_id"

# Should return error (invalid ID)
python scripts/fetch_transcript.py "not_a_real_id"
```

### Expected Output

**Valid video with transcript:**
```json
{"segments":[{"start":0.0,"text":"Intro"}],"language":"en","video_id":"ABC123"}
```

**Video without transcript:**
```json
{"error":"Transcripts are disabled for this video."}
```

Exit codes:
- `0`: Success
- `1`: Error (invalid URL, no transcript, network issue)

## Troubleshooting

### `youtube-transcript-api not installed`

The script should auto-install. If it fails:

```bash
pip install youtube-transcript-api --break-system-packages
```

Or use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install youtube-transcript-api
python scripts/fetch_transcript.py <video_id>
```

### `Could not extract a valid YouTube video ID`

Check input format:
- Ensure URL is complete (includes `https://`)
- Video ID must be exactly 11 characters
- Supported characters: `a-z`, `A-Z`, `0-9`, `_`, `-`

### `Transcripts are disabled for this video`

The video owner has disabled automatic captions and hasn't added manual captions. Workaround:
1. Open video in browser
2. Click `...` → "Open transcript"
3. Copy transcript text
4. Paste manually for timestamp generation

### `No transcript found for this video in the requested language`

Remove the `--lang` flag to fetch any available language:

```bash
python scripts/fetch_transcript.py <video_id>
```

### Network/Timeout Errors

The script may fail in restricted environments. Solutions:
1. Check firewall/proxy settings
2. Verify internet connectivity
3. Try from a different network

### JSON Output Parsing

If integrating programmatically:

```python
import subprocess
import json

result = subprocess.run(
    ['python', 'scripts/fetch_transcript.py', video_id],
    capture_output=True, text=True
)
data = json.loads(result.stdout)

if 'error' in data:
    print(f"Error: {data['error']}")
else:
    print(f"Found {len(data['segments'])} segments")
```

## Integration with YouTube Timestamper Skill

This repository includes a skill definition (`youtube-timestamper.skill`) that integrates with Claude Code. The skill:

1. Runs `fetch_transcript.py` to get raw transcript data
2. Groups segments into logical chapters based on topic boundaries
3. Formats output as YouTube-compatible timestamps (`0:00 Introduction`, etc.)

See `youtube-timestamper.skill` for the full workflow.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test with various video types (long-form, shorts, different languages)
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api) - The underlying library for fetching transcripts
