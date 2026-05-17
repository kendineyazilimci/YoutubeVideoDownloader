import yt_dlp
import os
import platform

def get_default_desktop():
    """Sisteme göre Masaüstü yolunu bulur."""
    home = os.path.expanduser("~")
    paths = [
        os.path.join(home, 'Masaüstü'),
        os.path.join(home, 'Desktop'),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return home

def list_and_download(url):
    default_path = get_default_desktop()
    print(f"\nVarsayılan indirme konumu: {default_path}")
    path_input = input("Farklı bir yol girmek ister misiniz? (Varsayılan için boş bırakın): ").strip()
    
    download_dir = path_input if path_input else default_path

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    ydl_opts_base = {
        'cookiefile_from_browser': 'firefox',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_base) as ydl:
            print("Video bilgileri alınıyor... Lütfen bekleyin.")
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            print(f"\nVideo: {info.get('title')}\n")
            print(f"{'ID':<10} {'Çözünürlük':<15} {'Uzantı':<10} {'Not'}")
            print("-" * 50)

            for f in formats:
                if f.get('vcodec') != 'none':
                    res = f.get('resolution', 'N/A')
                    ext = f.get('ext', 'N/A')
                    f_id = f.get('format_id')
                    note = f.get('format_note', '')
                    print(f"{f_id:<10} {res:<15} {ext:<10} {note}")

            print("-" * 50)
            choice = input("\nİndirmek istediğiniz formatın ID'sini yazın. (En iyisi için boş bırakın.): ").strip()

            download_path = os.path.join(download_dir, '%(title)s.%(ext)s')
            selected_format = 'bestvideo+bestaudio/best' if choice == '' else f"{choice}+bestaudio/best"

            ydl_opts_download = {
                'cookiefile_from_browser': 'firefox',
                'format': selected_format,
                'outtmpl': download_path,
                'merge_output_format': 'mp4',
            }

            print(f"\nİndirme başlıyor... (Hedef: {download_dir})")
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_down:
                ydl_down.download([url])
            
            print("\nİndirme işlemi tamamlandı.")

    except Exception as e:
        print(f"\nBir hata oluştu: {e}")

if __name__ == "__main__":
    link = input("YouTube URL: ")
    list_and_download(link)