import sys
import yt_dlp

def download_video(url, output_path):
    ydl_options = {
        'outtmpl': output_path,
        'quiet': True,
        'format': 'mp4/bestaudio/best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])
        print(f"Downloaded: {output_path}")
        return True
    except Exception as error:
        print(f"Error downloading {url}: {error}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_video.py <url> <output_path>")
        sys.exit(1)
    url = sys.argv[1]
    output_path = sys.argv[2]
    download_video(url, output_path)
