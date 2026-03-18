# Changelog - youtube-summarizer

All notable changes to the youtube-summarizer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] - 2026-03-18

### 🐛 Fixed

- **youtube-transcript-api compatibility issue**
  - **Issue:** Script used outdated API methods (`get_transcript()`, `list_transcripts()`) that don't exist in current library versions (0.6+)
  - **Error:** `AttributeError: type object 'YouTubeTranscriptApi' has no attribute 'get_transcript'`
  - **Root Cause:** The youtube-transcript-api library changed its API from static methods to instance-based methods
  - **Solution:** Updated to use the new API pattern:
    - Create instance: `api = YouTubeTranscriptApi()`
    - List transcripts: `api.list(video_id)`
    - Fetch transcript: `transcript.fetch()`
    - Extract text: `[snippet.text for snippet in fetched.snippets]`
  - **Impact:** Skill now works with youtube-transcript-api v0.6+ and future versions

### 🔧 Changed

- **`extract-transcript.py`** - Complete rewrite of transcript extraction logic
  - Old API (broken): `YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])`
  - New API (working): Iterate `api.list(video_id)` → `transcript.fetch()` → extract from `snippets`
  - Added proper fallback logic for auto-generated transcripts
  - Improved error messages for missing transcripts

- **`SKILL.md`** - Updated all code examples to reflect new API usage
  - Fixed Step 2: Added `api = YouTubeTranscriptApi()` initialization
  - Fixed Step 3: Updated transcript extraction to use `snippets` attribute
  - Removed references to deprecated `get_transcript()` and `list_transcripts()` methods

### 🧪 Tested

- ✅ Tested with auto-generated transcripts (English)
- ✅ Tested `--list` option for available transcripts
- ✅ Tested fallback from preferred language to English
- ✅ Verified transcript extraction for video IDs: `QFKIyPNBhtw`, `RYrtfLiNMu8`

### 📝 Notes

- **Breaking Change:** None for end users - only internal API usage changed
- **Backward Compatibility:** Requires youtube-transcript-api v0.6+ (current PyPI version)
- **Migration:** No user action needed; skill handles API internally

---

## [1.2.1] - 2026-02-04

### 🐛 Fixed

- **Exit code propagation in `--list` mode**
  - **Issue:** Script always exited with status 0 even when `list_available_transcripts()` failed
  - **Risk:** Broke automation pipelines that rely on exit codes to detect failures
  - **Root Cause:** Return value from `list_available_transcripts()` was ignored
  - **Solution:** Now properly checks return value and exits with code 1 on failure
  - **Impact:** Scripts in automation can now correctly detect when transcript listing fails (invalid video ID, network errors, etc.)

### 🔧 Changed

- `extract-transcript.py` (lines 58-60)
  - Before: `list_available_transcripts(video_id); sys.exit(0)`
  - After: `success = list_available_transcripts(video_id); sys.exit(0 if success else 1)`

### 📝 Notes

- **Breaking Change:** None - only affects error handling behavior
- **Backward Compatibility:** Scripts that check exit codes will now work correctly
- **Migration:** No changes needed for existing users

### 🔗 Related

- Identified by Codex automated review in antigravity-awesome-skills PR #62
- Also fixed in antigravity-awesome-skills fork

---

## [1.2.0] - 2026-02-04

### ✨ Added

- Intelligent prompt workflow integration
- LLM processing with Claude CLI or GitHub Copilot CLI
- Progress indicators with rich terminal UI
- Multiple output formats
- Enhanced error handling

### 🔧 Changed

- Major refactor of transcript extraction logic
- Improved documentation in SKILL.md
- Updated installation requirements

---

## [1.0.0] - 2025-02-01

### ✨ Initial Release

- YouTube transcript extraction
- Language detection and selection
- Basic summarization
- Markdown output format
- Support for multiple languages
