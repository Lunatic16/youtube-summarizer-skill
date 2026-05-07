#!/usr/bin/env python3
"""
fetch_transcript.py — Fetch a YouTube transcript with timestamps.

Usage:
    python fetch_transcript.py <video_id_or_url> [--lang en]

Output:
    JSON array of {"start": <seconds>, "text": "<text>"} to stdout.
    On error, prints {"error": "<message>"} to stdout and exits with code 1.
"""

import sys
import json
import re


def extract_video_id(input_str: str) -> str:
    """Extract video ID from a URL or return as-is if already an ID."""
    patterns = [
        r'(?:v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'(?:shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, input_str)
        if match:
            return match.group(1)
    # If it looks like a raw video ID (11 chars, alphanumeric + _ -)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', input_str.strip()):
        return input_str.strip()
    return None


def fetch_transcript(video_id: str, lang: str = None):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
        )
    except ImportError:
        return {"error": "youtube-transcript-api not installed. Run: pip install youtube-transcript-api --break-system-packages"}

    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)

        # Prefer requested language, then English, then first available
        transcript = None
        if lang:
            try:
                transcript = transcript_list.find_transcript([lang])
            except Exception:
                pass

        if transcript is None:
            try:
                transcript = transcript_list.find_transcript(['en'])
            except Exception:
                pass

        if transcript is None:
            # Fall back to first available (auto-translated if needed)
            transcript = next(iter(transcript_list))

        fetched = transcript.fetch()
        segments = [{"start": s.start, "text": s.text} for s in fetched]
        return {"segments": segments, "language": transcript.language_code, "video_id": video_id}

    except TranscriptsDisabled:
        return {"error": "Transcripts are disabled for this video. Ask the user to paste the transcript manually."}
    except VideoUnavailable:
        return {"error": "Video is unavailable (private, age-restricted, or deleted)."}
    except NoTranscriptFound:
        return {"error": "No transcript found for this video in the requested language."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="YouTube URL or video ID")
    parser.add_argument("--lang", default=None, help="Preferred language code (e.g. en, es)")
    args = parser.parse_args()

    video_id = extract_video_id(args.video)
    if not video_id:
        result = {"error": f"Could not extract a valid YouTube video ID from: {args.video}"}
        print(json.dumps(result))
        sys.exit(1)

    result = fetch_transcript(video_id, lang=args.lang)

    if "error" in result:
        print(json.dumps(result))
        sys.exit(1)
    else:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
