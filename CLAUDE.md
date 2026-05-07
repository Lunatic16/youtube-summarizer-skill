# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Timestamper — generates accurate chapter-style timestamps for YouTube videos by fetching real transcripts and grouping them into meaningful sections.

## Commands

```bash
# Fetch transcript (returns JSON with segments and language)
python scripts/fetch_transcript.py <video_id_or_url> [--lang en]

# Install dependency (if not using auto-install)
pip install youtube-transcript-api --break-system-packages
```

## Architecture

- **scripts/fetch_transcript.py** — Python script that extracts video IDs from URLs and fetches transcripts via `youtube-transcript-api`. Outputs JSON: `{"segments": [...], "language": "...", "video_id": "..."}` or `{"error": "..."}`.
- **youtube-timestamper.skill** — Skill definition file that describes the workflow for generating timestamps from transcripts.
- **SKILL.md** — Skill package archive (contains compressed skill files).

The script handles:
- URL parsing (standard, short, embed, shorts formats)
- Language fallback (requested → English → first available)
- Error cases (disabled transcripts, unavailable videos, no transcript found)
