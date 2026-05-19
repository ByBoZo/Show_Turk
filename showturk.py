#!/usr/bin/env python3

import json
import re
import requests
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

CONFIG_FILE = "config.json"
CHROME_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def get_showturk_token() -> Optional[str]:
    """Show Türk'ten güncel token alır"""
    url = "https://www.showturk.com.tr/canli-yayin"
    
    headers = {
        "User-Agent": CHROME_UA,
        "Referer": "https://www.showturk.com.tr/",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        # Token'ı bul
        pattern = r'playlist\.m3u8\?e=(\d+)&st=([a-zA-Z0-9_-]+)'
        match = re.search(pattern, html)
        
        if match:
            e, st = match.groups()
            stream_url = f"https://ciner-live.ercdn.net/showturk/playlist.m3u8?e={e}&st={st}&tv=1"
            return stream_url
        else:
            print("❌ Token bulunamadı")
            return None
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def create_single_m3u(stream_url: str, output_folder: Path) -> Path:
    """Tek kanal için M3U dosyası oluşturur"""
    output_folder.mkdir(parents=True, exist_ok=True)
    
    path = output_folder / "Show_Turk.m3u"
    content = f"""#EXTM3U
#EXTVLCOPT:http-referrer=https://www.showturk.com.tr/
#EXTINF:-1 tvg-id="Show Türk" tvg-logo="https://i.postimg.cc/tR2dkHH3/Show-Turk-logo.png" group-title="TR: ULUSAL",SHOW TÜRK
{stream_url}
"""
    path.write_text(content, encoding="utf-8")
    return path

def create_playerlist_m3u(output_folder: Path) -> Path:
    """Ana playlist oluşturur (GitHub raw linkiyle)"""
    github_base = "https://raw.githubusercontent.com/ByBoZo/Show_Turk/main/playlist"
    
    content = f"""#EXTM3U
#EXTINF:-1 tvg-id="Show Türk" tvg-logo="https://i.postimg.cc/tR2dkHH3/Show-Turk-logo.png" group-title="TR: ULUSAL",SHOW TÜRK
{github_base}/Show_Turk.m3u
"""
    path = output_folder / "playerlist.m3u"
    path.write_text(content, encoding="utf-8")
    return path

def main():
    print("=" * 60)
    print("🎬 Show Türk M3U Güncelleyici")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    output_folder = Path("playlist")
    
    # Token al
    stream_url = get_showturk_token()
    if not stream_url:
        print("❌ Stream URL alınamadı")
        return 1
    
    # M3U dosyalarını oluştur
    single_file = create_single_m3u(stream_url, output_folder)
    print(f"✅ {single_file} oluşturuldu")
    
    playerlist_file = create_playerlist_m3u(output_folder)
    print(f"✅ {playerlist_file} oluşturuldu")
    
    print(f"\n📄 Kullanım linkleri:")
    print(f"   https://raw.githubusercontent.com/ByBoZo/Show_Turk/main/playlist/playerlist.m3u")
    print(f"   https://raw.githubusercontent.com/ByBoZo/Show_Turk/main/playlist/Show_Turk.m3u")
    
    return 0

if __name__ == "__main__":
    exit(main())