#!/usr/bin/env python3
"""Extract slides from a YouTube video at fixed intervals and save them as a PDF."""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import cv2
import img2pdf
import yt_dlp

FORMAT = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b"


def download_video(url: str, out_dir: Path) -> Path:
    """Download the video and return the path to the resulting file."""
    opts = {
        "format": FORMAT,
        "outtmpl": str(out_dir / "video.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    files = list(out_dir.glob("video.*"))
    if not files:
        raise RuntimeError("Download failed: no video file found.")
    return files[0]


def extract_frames(video: Path, interval: int, quality: int, out_dir: Path) -> list[str]:
    """Save one JPEG every `interval` seconds and return their paths."""
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 0
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    duration = int(frames / fps) if fps else 0
    print(f"Duration: {duration // 60}:{duration % 60:02d}")

    images = []
    for t in range(0, max(duration, 1), interval):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, frame = cap.read()
        if not ok:
            continue
        path = out_dir / f"slide_{t // 60:02d}_{t % 60:02d}.jpg"
        cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        images.append(str(path))
        print(f"  extracted {t // 60:02d}:{t % 60:02d}")
    cap.release()
    return images


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("url", help="YouTube video URL")
    p.add_argument("-i", "--interval", type=int, default=30, help="seconds between frames (default: 30)")
    p.add_argument("-q", "--quality", type=int, default=95, help="JPEG quality 1-100 (default: 95)")
    p.add_argument("-o", "--output", default="slides.pdf", help="output PDF path (default: slides.pdf)")
    args = p.parse_args()

    if args.interval < 1:
        p.error("--interval must be >= 1")

    tmp = Path(tempfile.mkdtemp())
    try:
        print("Downloading video...")
        video = download_video(args.url, tmp)
        print(f"Extracting frames every {args.interval}s...")
        images = extract_frames(video, args.interval, args.quality, tmp)
        if not images:
            print("No slides extracted.", file=sys.stderr)
            return 1
        Path(args.output).write_bytes(img2pdf.convert(images))
        print(f"Done: {len(images)} slides -> {args.output}")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
