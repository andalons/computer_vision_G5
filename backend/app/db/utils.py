"""
Utility functions for extracting video metadata
"""

import yt_dlp

def extract_video_metadata(url: str) -> dict:
    """
    Extract metadata from a video URL (YouTube, TikTok).
    Auto-detects platform and returns core metadata.
    """

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        raise ValueError(f"Failed to extract metadata: {str(e)}")

    platform = info.get("extractor_key", "").lower()

    if platform not in ["youtube", "tiktok"]:
        raise ValueError(f"Unsupported platform: {platform}")

    return {
        "url": url,
        "platform": platform,
        "title": info.get("title"),
        "influencer": info.get("uploader"),
        "duration_seconds": info.get("duration"),
        "likes": info.get("like_count"),
        "comments": info.get("comment_count"),
        "views": info.get("view_count"),
        "description": info.get("description"),
    }
