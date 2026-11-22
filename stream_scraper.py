import json
import requests  # Yedek kontrol için
from curl_cffi import requests as cffi_requests

class TaraftariumBypassScraper:
    def __init__(self, base_url="https://g1b.d72577a9dd0ec74.cfd/"):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36",
            "Referer": "https://taraftarium1089.xyz/",
            "Origin": "https://taraftarium1089.xyz/",
            "Accept": "*/*",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site"
        }

    def fetch_and_validate_streams(self, channel_ids, output_filename="active_streams.json"):
        active_streams = []
        print(f"[*] curl_cffi ile Cloudflare koruması taranıyor: {self.base_url}")

        for ch_id in channel_ids:
            stream_url = f"{self.base_url}/{ch_id}/mono.m3u8"
            
            try:
                # Chrome tarayıcı parmak izini taklit ederek istek atıyoruz
                response = cffi_requests.get(
                    stream_url,
                    headers=self.headers,
                    impersonate="chrome110",
                    timeout=10
                )
                
                print(f"[*] {ch_id} - Durum Kodu: {response.status_code}")
                
                if response.status_code == 200 and ("#EXTM3U" in response.text or "m3u8" in response.headers.get("Content-Type", "")):
                    print(f"[+] Aktif Yayın Bulundu: {stream_url}")
                    active_streams.append({
                        "channel_id": ch_id,
                        "stream_url": stream_url,
                        "status": "active"
                    })
                else:
                    print(f"[-] Pasif veya Engellendi: {stream_url} (Kod: {response.status_code})")
            except Exception as e:
                print(f"[!] Bağlantı Hatası ({ch_id}): {str(e)}")

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(active_streams, f, indent=4, ensure_ascii=False)
        
        print(f"[*] İşlem tamamlandı. Toplam {len(active_streams)} aktif yayın {output_filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    scraper = TaraftariumBypassScraper("https://g1b.d72577a9dd0ec74.cfd/")
    
    # Test edilecek kanal ID listesi
    channels_to_test = ["ss", "bein1", "bein2", "bein3", "bein4", "ssport", "tivibu", "trtsport"]
    
    scraper.fetch_and_validate_streams(channels_to_test)
