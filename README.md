# YouTube Timestamper (Claude Skill)

A Claude Code skill that generates accurate, chapter-style timestamps for YouTube videos by fetching real transcripts and grouping them into meaningful sections.

## What It Does

When you share a YouTube URL and ask for timestamps, chapters, or a table of contents, this skill:

1. Fetches the actual transcript from YouTube (with second-level precision)
2. Groups segments into logical chapters based on topic boundaries
3. Outputs timestamps in YouTube-compatible format for descriptions

**Example usage:**
- "Add timestamps to this video: https://youtube.com/watch?v=..."
- "What happens at 10:30 in this video?"
- "Make chapters for this video"
- "Generate a table of contents with timestamps"

## Installation

The skill installs its dependency (`youtube-transcript-api`) automatically when triggered. No manual setup required.

If running manually:

```bash
pip install youtube-transcript-api --break-system-packages
```

## How It Works

### Step 1: Extract Video ID and Fetch Transcript

The skill runs the bundled script:

```bash
python scripts/fetch_transcript.py "<url_or_video_id>" [--lang en]
```

The script:
- Parses YouTube URLs (standard, short, embed, shorts formats)
- Extracts the 11-character video ID
- Fetches transcript via `youtube-transcript-api`
- Returns JSON: `{"segments": [...], "language": "...", "video_id": "..."}` or `{"error": "..."}`

### Step 2: Handle Errors

| Error | User Message |
|-------|--------------|
| Transcripts disabled | "This video has transcripts turned off. Paste the transcript manually." |
| Video unavailable | "This video appears to be private, age-restricted, or deleted." |
| No transcript found | "No transcript available in the requested language." |
| Network error | "Couldn't reach YouTube. Paste the transcript text manually." |

### Step 3: Group Into Chapters

The raw transcript has hundreds of short segments. The skill identifies **topic boundaries** by looking for:

- Topic shifts (new concepts, speaker transitions)
- Natural pauses (gaps > 3–5 seconds)
- Transitional phrases ("Now let's talk about...", "Moving on...")

**Target chapter count by video length:**

| Duration | Chapters |
|----------|----------|
| < 10 min | 4–7 |
| 10–30 min | 7–12 |
| 30–60 min | 12–20 |
| 60–90 min | 18–28 |
| 90+ min | 25–40 |

### Step 4: Format Output

Timestamps are formatted for YouTube descriptions:

```
0:00 Introduction
1:45 What Is Machine Learning
4:22 Types of Neural Networks
9:10 Training a Model
14:33 Common Pitfalls
19:08 Real World Applications
24:55 Conclusion
```

**Format rules:**
- First chapter must be `0:00` (YouTube requirement)
- Use `M:SS` for videos under 1 hour, `H:MM:SS` for longer
- Titles are 2–6 words, title case, no ending punctuation

## Project Structure

```
youtube-timestamper/
├── scripts/
│   └── fetch_transcript.py    # Transcript fetching script
├── youtube-timestamper.skill  # Skill definition (workflow)
├── SKILL.md                   # Skill package archive
├── CLAUDE.md                  # Claude Code guidance
└── README.md                  # This file
```

## Files

### `scripts/fetch_transcript.py`

Python script that:
- Extracts video IDs from various URL formats
- Fetches transcripts via `youtube-transcript-api`
- Handles language fallback (requested → English → first available)
- Outputs JSON to stdout

### `youtube-timestamper.skill`

Skill definition file that describes:
- When to trigger (YouTube URL + timestamp request)
- How to fetch and process transcripts
- Error handling strategies
- Output formatting rules

### `SKILL.md`

Compressed skill package for distribution.

## Supported URL Formats

| Format | Example |
|--------|---------|
| Standard | `youtube.com/watch?v=ABC123` |
| Short | `youtu.be/ABC123` |
| Embed | `youtube.com/embed/ABC123` |
| Shorts | `youtube.com/shorts/ABC123` |
| Raw ID | `ABC123` |

## Requirements

- Python 3.7+
- `youtube-transcript-api` (auto-installed)
- Internet connection

## Limitations

- Only works with public YouTube videos
- Requires captions/transcript to be enabled
- Auto-generated captions may have accuracy issues
- Videos under 3 minutes may not benefit from chapters

## Troubleshooting

### "Transcripts are disabled"
Video owner has disabled captions. Ask user to paste transcript manually.

### "No transcript found"
Try without specifying a language, or check if video has auto-captions.

### Script doesn't run
Ensure Python 3.7+ is installed and `youtube-transcript-api` is available:

```bash
pip install youtube-transcript-api
```

## License

MIT License
