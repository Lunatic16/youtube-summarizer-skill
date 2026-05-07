# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Timestamper — a Claude skill that generates accurate chapter-style timestamps for YouTube videos by fetching real transcripts and grouping them into meaningful sections.

## Commands

```bash
# Fetch transcript (returns JSON with segments and language)
python scripts/fetch_transcript.py <video_id_or_url> [--lang en]

# Install dependency (if not using auto-install)
pip install youtube-transcript-api --break-system-packages
```

## Architecture

- **scripts/fetch_transcript.py** — Python script that extracts video IDs from URLs and fetches transcripts via `youtube-transcript-api`. Outputs JSON: `{"segments": [...], "language": "...", "video_id": "..."}` or `{"error": "..."}`.
- **youtube-timestamper.skill** — Skill definition file that describes the 4-step workflow:
  1. Extract video ID and fetch transcript
  2. Handle errors gracefully (disabled transcripts, unavailable videos, etc.)
  3. Group segments into chapters based on topic boundaries and natural pauses
  4. Format output as YouTube-compatible timestamps (`0:00 Introduction`)
- **SKILL.md** — Skill package archive (contains compressed skill files).

## Key Behaviors

- **URL parsing**: Supports standard, short, embed, and shorts formats
- **Language fallback**: Requested → English → first available
- **Chapter scaling**: Targets 4–40 chapters based on video length
- **Error handling**: Returns structured JSON errors for graceful handling
