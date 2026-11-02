# YouTube Slide Extractor

Turn a YouTube lecture or presentation into a PDF of slides. The tool downloads the video, grabs a frame every *N* seconds, and stitches the frames into a single PDF.

Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp), [OpenCV](https://opencv.org/) and [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf).

## Option 1: Google Colab (no install)

Open `youtube_slide_extractor.ipynb` in Colab, run the cells, enter the URL and interval, and the PDF downloads automatically.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/youtube-slide-extractor/blob/main/youtube_slide_extractor.ipynb)

(Replace `YOUR_USERNAME` after pushing.)

## Option 2: Command line

Requires Python 3.9+ and [ffmpeg](https://ffmpeg.org/download.html) on your PATH (yt-dlp uses it to merge audio and video).

```bash
git clone https://github.com/YOUR_USERNAME/youtube-slide-extractor.git
cd youtube-slide-extractor
pip install -r requirements.txt

python slide_extractor.py "https://youtu.be/VIDEO_ID" --interval 30 --output slides.pdf
```

| Option | Default | Description |
|---|---|---|
| `url` | required | YouTube video URL |
| `-i, --interval` | 30 | Seconds between extracted frames |
| `-q, --quality` | 95 | JPEG quality (1-100) |
| `-o, --output` | slides.pdf | Output PDF path |

## Notes

- Fixed-interval extraction can produce duplicate slides or miss quick transitions. Pick an interval that matches the pace of the talk.
- Only download videos you have the right to use. Respect YouTube's Terms of Service and the creator's copyright.
- If downloads fail, update yt-dlp: `pip install -U yt-dlp`.

## License

MIT
