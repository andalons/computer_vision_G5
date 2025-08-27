import sys
import yt_dlp

def descargar_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,
        'quiet': True,
        'format': 'mp4/bestaudio/best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Descargado: {output_path}")
        return True
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python descargar_video.py <url> <output_path>")
        sys.exit(1)
    url = sys.argv[1]
    output_path = sys.argv[2]
    descargar_video(url, output_path)
