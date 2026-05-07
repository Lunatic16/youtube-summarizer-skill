---
name: youtube-timestamper
description: >
  Generate accurate, chapter-style timestamps for YouTube videos. Use this skill
  whenever a user shares a YouTube URL and wants timestamps, chapters, a table of
  contents, a summary with timecodes, or asks "what happens at X minute" in a video.
  Also trigger for requests like "break this video into sections", "make chapters for
  this", "timestamped summary", or "add timestamps to my YouTube description". This
  skill fetches the real transcript from YouTube to avoid hallucinated timestamps —
  use it even for casual or quick requests, since accuracy depends on having real data.
---

# YouTube Timestamper

Generates accurate, human-readable chapter timestamps for YouTube videos by fetching
the real transcript (with second-level offsets) and grouping it into meaningful sections.

**Never invent or guess timestamps.** Always use real transcript data or explicitly
tell the user that the transcript is unavailable.

---

## Step 1 — Extract the video ID and fetch the transcript

Run the bundled script using `bash_tool`. The script handles URL parsing and language
fallback automatically:

```bash
pip install youtube-transcript-api --break-system-packages -q 2>/dev/null
python /path/to/skill/scripts/fetch_transcript.py "<url_or_video_id>"
```

The script path is relative to wherever the skill is installed. Use the path shown
in your `available_skills` list, or find it with:
```bash
find /mnt/skills -name "fetch_transcript.py" 2>/dev/null | head -1
```

The script outputs one of:
- **Success**: `{"segments": [...], "language": "en", "video_id": "..."}`
  - Each segment: `{"start": 42.3, "text": "some spoken text"}`
- **Error**: `{"error": "..."}`

---

## Step 2 — Handle errors gracefully

If the script returns an error:

| Error type | What to tell the user |
|---|---|
| Transcripts disabled | "This video has transcripts turned off. You can paste the transcript manually — YouTube's auto-captions are available under the `...` menu → 'Open transcript'." |
| Video unavailable | "This video appears to be private, age-restricted, or deleted." |
| No transcript found | "No transcript is available in the requested language. Try without specifying a language, or paste it manually." |
| Network / install error | "I couldn't reach YouTube from this environment. Paste the transcript text and I'll generate timestamps from that." |

If the user pastes a transcript manually, parse it by looking for timestamp patterns
like `[0:00]`, `(1:23)`, or just raw text blocks — then proceed to Step 3.

---

## Step 3 — Group segments into chapters

The raw transcript has hundreds of short segments. Your job is to identify **topic
boundaries** and group them into meaningful chapters.

**Scale chapter count to video length:**
| Video duration | Target chapters |
|---|---|
| Under 10 min | 4–7 |
| 10–30 min | 7–12 |
| 30–60 min | 12–20 |
| 60–90 min | 18–28 |
| 90+ min | 25–40 |

Never stop early — cover the entire video from start to finish.

**How to find good boundaries:**
- Look for topic shifts: new concepts introduced, speaker transitions, scene changes
- Look for natural pauses (gaps > 3–5 seconds between segments)
- Look for transitional phrases: "Now let's talk about...", "Moving on...", "The next
  thing is...", "So in summary..."
- Aim for chapters of roughly similar length, but let content drive the cuts

**For long transcripts (30+ min):** Process the transcript in thirds or halves mentally,
ensuring you identify chapter boundaries throughout the *entire* video — not just the
first portion. Always verify your last timestamp is within a few minutes of the video end.

**Use the `start` value of the first segment in each group as the chapter timestamp.**

---

## Step 4 — Format the output

Always format timestamps so they work as YouTube chapter markers:
- The **first chapter must start at `0:00`** (YouTube requires this)
- Format: `M:SS Title` for videos under 1 hour, `H:MM:SS Title` for longer
- Title: 2–6 words, title case, no punctuation at the end
- Keep it scannable — this output is meant to be pasted into a YouTube description

**Example output:**
```
0:00 Introduction
1:45 What Is Machine Learning
4:22 Types of Neural Networks
9:10 Training a Model
14:33 Common Pitfalls
19:08 Real World Applications
24:55 Conclusion and Resources
```

After the timestamps, offer a one-sentence summary of each chapter if the user might
want it (e.g. for a video description). Don't pad with unnecessary commentary.

---

## Tips for quality

- If the transcript has filler words or garbled auto-captions, use the surrounding
  context to infer the topic rather than quoting bad text in chapter titles
- For tutorial videos, chapters often follow the step sequence — respect that structure
- For interviews, chapters often follow question topics — use the question as the title
- For lectures, chapters follow conceptual units — name the concept, not the time slot
- If a video is under 3 minutes, timestamps may not be useful — tell the user that
  YouTube only shows chapters for videos with 3+ chapters and the first at 0:00
- **For long videos (30+ min):** Always scan all the way to the end of the transcript
  before writing timestamps. A common failure mode is stopping at chapter 12 partway
  through. Check that your final timestamp is near the video's end.

---

## Compatibility

Requires `youtube-transcript-api`. The script installs it automatically if missing.
Works with any public YouTube video that has auto-generated or manual captions.
