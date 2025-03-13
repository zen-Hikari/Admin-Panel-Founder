import requests
import threading
import random
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Daftar User-Agent untuk menghindari pemblokiran
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Kata kunci umum untuk mencari halaman login admin
admin_keywords = ["login", "admin", "dashboard", "username", "password"]

# Fungsi untuk mengecek apakah halaman memiliki form login
def check_login_page(url, domain):
    headers = {"User-Agent": random.choice(user_agents)}
    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all("form")
            input_fields = [input_tag.get("type", "").lower() for form in forms for input_tag in form.find_all("input")]
            
            if "password" in input_fields and any(keyword in response.text.lower() for keyword in admin_keywords):
                print(f"[+] Halaman login ditemukan: {url}")
    except requests.RequestException:
        pass

# Fungsi untuk menjelajahi URL dari halaman utama dan mencari halaman login
def crawl_site(target_url):
    headers = {"User-Agent": random.choice(user_agents)}
    domain = urlparse(target_url).netloc
    
    try:
        response = requests.get(target_url, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [urljoin(target_url, a.get("href")) for a in soup.find_all("a", href=True)]
            
            threads = []
            max_threads = 10
            
            for i, link in enumerate(links):
                if urlparse(link).netloc != domain:
                    continue  # Hindari mencari di luar domain target
                
                thread = threading.Thread(target=check_login_page, args=(link, domain))
                threads.append(thread)
                thread.start()
                
                if i % max_threads == 0:
                    for t in threads:
                        t.join()
                    threads = []
                time.sleep(0.1)  # Delay untuk menghindari deteksi firewall
            
            for thread in threads:
                thread.join()
        
    except requests.RequestException:
        pass

if __name__ == "__main__":
    target = input("Masukkan URL target (contoh: http://example.com): ").strip()
    print(f"[!] Menjelajahi {target} untuk mencari halaman login...")
    crawl_site(target)
    print("[!] Pencarian selesai.")