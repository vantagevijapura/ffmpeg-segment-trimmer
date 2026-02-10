# FFmpeg Segment Trimmer (Lossless)

A small Python CLI utility that trims and recombines video segments using FFmpeg **without re-encoding**.

Designed for fast, deterministic video slicing when you know the timestamps and want zero quality loss.

---

## Why This Exists

FFmpeg is powerful but verbose for simple workflows like:
- Extracting multiple clips from a single source
- Quickly recombining them in order
- Avoiding re-encoding overhead

This script provides a lightweight interactive wrapper that:
- Prompts for timestamps
- Generates exact cuts
- Merges segments into a single output file
- Cleans up intermediate artifacts automatically

---

## Key Characteristics

- **Lossless**: uses `-c copy` throughout
- **Deterministic**: explicit `-ss` and `-to` timestamps
- **No dependencies** beyond FFmpeg
- **Interactive**: optimized for quick one-off workflows
- **Safe cleanup** of temp files

---

## How It Works

1. Accepts a path to a video file
2. Prompts for the number of segments
3. For each segment:
   - Requests start and end timestamps (MM:SS)
   - Normalizes input to HH:MM:SS
   - Uses FFmpeg to extract the segment
4. Concatenates all segments into a final output file
5. Deletes all temporary files

---

## Requirements

- Python 3.8+
- FFmpeg installed and available in `$PATH`

Verify FFmpeg:
```bash
ffmpeg -version
